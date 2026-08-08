"""Eligibility scorer (SPEC section 2, frozen; REVIEW_LOG F5 span semantics).

At each matched site, every candidate is force-scored as the raw
log-probability of the full candidate span given the realized prefix:

    log P(candidate span | prefix) >= log P(best candidate span | prefix) - 1.5

Natural-log units, no length normalization (frozen — deliberately
conservative). The span scored is the F5 *score span*: the site's invariant
left/right context inside `score_start:score_end` with the edit-region
candidate spliced in. A site is intervenable iff >= 2 candidates are eligible.

Token-boundary rule: tokenizers may merge tokens across the prefix/span
boundary (e.g. "x" + "=" -> "x="), so the prefix-alone tokenization and the
full tokenization can diverge before the span starts. We score from the end
of the common token prefix, charging any re-tokenized boundary tokens to the
candidate. The same rule applies to every candidate at a site, so the frozen
delta comparison is well-defined.

The LM interface is deliberately tiny so the core logic is testable without
any model download; `HFCausalLM` adapts a Hugging Face causal LM to it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from harness.matcher import Site

DELTA_NATS = 1.5  # frozen (SPEC section 2); changing this triggers FREEZE.md


class SequenceLM(Protocol):
    eos_id: int | None

    def encode(self, text: str) -> list[int]: ...
    def decode(self, ids: list[int]) -> str: ...
    def greedy_next(self, ids: list[int]) -> int: ...
    def sequence_logprob(self, ids: list[int], from_index: int) -> float: ...


@dataclass
class ScoredCandidate:
    text: str        # the edit-region candidate
    span_text: str   # candidate spliced into the score span
    logp: float
    eligible: bool


@dataclass
class ScoredSite:
    site: Site
    candidates: list[ScoredCandidate]
    best_logp: float

    @property
    def intervenable(self) -> bool:
        return sum(c.eligible for c in self.candidates) >= 2

    def eligible_texts(self) -> list[str]:
        return [c.text for c in self.candidates if c.eligible]


def _common_prefix_len(a: list[int], b: list[int]) -> int:
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


class EligibilityScorer:
    def __init__(self, lm: SequenceLM, delta: float = DELTA_NATS):
        self.lm = lm
        self.delta = delta

    def score_site(self, text: str, site: Site) -> ScoredSite:
        prefix = text[:site.score_start]
        left = text[site.score_start:site.start]
        right = text[site.end:site.score_end]
        prefix_ids = self.lm.encode(prefix)

        scored: list[tuple[str, str, float]] = []
        for cand in site.candidates:
            span_text = left + cand + right
            full_ids = self.lm.encode(prefix + span_text)
            start = _common_prefix_len(prefix_ids, full_ids)
            logp = self.lm.sequence_logprob(full_ids, start)
            scored.append((cand, span_text, logp))

        best = max(lp for _, _, lp in scored)
        candidates = [
            ScoredCandidate(c, s, lp, lp >= best - self.delta)
            for c, s, lp in scored
        ]
        return ScoredSite(site=site, candidates=candidates, best_logp=best)


class HFCausalLM:
    """Hugging Face adapter for SequenceLM. GPU-box workhorse; import-lazy so
    the rest of the harness has no torch dependency.

    Transparent KV caching: consecutive calls reuse the attention cache for
    the longest common token prefix with the previous call, so incremental
    greedy decoding is O(1) forwards per token and candidate scoring reuses
    the shared prefix. The interface is unchanged and results must match the
    uncached path (verified in tests/test_hf_integration.py); `use_cache=
    False` forces the naive full-forward path, which doubles as the
    bit-identity sanity reference the working rules call for.
    """

    def __init__(self, model_id: str, revision: str | None = None,
                 device: str = "cpu", dtype: str | None = None,
                 use_cache: bool = True):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._torch = torch
        self.tok = AutoTokenizer.from_pretrained(model_id, revision=revision)
        kwargs = {}
        if dtype:
            kwargs["dtype"] = getattr(torch, dtype)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, revision=revision, **kwargs).to(device).eval()
        self.device = device
        self.eos_id = self.tok.eos_token_id
        self.use_cache = use_cache
        self._cache_ids: list[int] = []
        self._cache = None

    def encode(self, text: str) -> list[int]:
        # No special tokens: the trace is scored/generated as raw text and
        # any BOS handling must be identical across candidates and arms.
        return self.tok.encode(text, add_special_tokens=False)

    def decode(self, ids: list[int]) -> str:
        return self.tok.decode(ids, skip_special_tokens=False,
                               clean_up_tokenization_spaces=False)

    def _logprob_rows(self, ids: list[int], first_needed_pos: int):
        """Log-softmax rows for positions first_needed_pos..len(ids)-1.

        With caching enabled, reuses the KV cache for the common prefix of
        `ids` and the previous call's ids, cropped so that every needed
        position is actually forwarded.
        """
        torch = self._torch
        if not self.use_cache:
            with torch.no_grad():
                logits = self.model(
                    torch.tensor([ids], device=self.device)).logits[0]
            return torch.log_softmax(
                logits[first_needed_pos:].float(), dim=-1)

        common = 0
        for a, b in zip(self._cache_ids, ids):
            if a != b:
                break
            common += 1
        # Must forward at least the positions whose logits we need, and at
        # least one token overall.
        start = min(common, first_needed_pos, len(ids) - 1)
        if start == 0 or self._cache is None:
            start = 0
            past = None
        else:
            self._cache.crop(start)
            past = self._cache
        with torch.no_grad():
            out = self.model(
                torch.tensor([ids[start:]], device=self.device),
                past_key_values=past, use_cache=True)
        self._cache = out.past_key_values
        self._cache_ids = list(ids)
        rows = torch.log_softmax(out.logits[0].float(), dim=-1)
        return rows[first_needed_pos - start:]

    def greedy_next(self, ids: list[int]) -> int:
        rows = self._logprob_rows(ids, len(ids) - 1)
        return int(rows[-1].argmax().item())

    def sequence_logprob(self, ids: list[int], from_index: int) -> float:
        if from_index <= 0:
            raise ValueError("cannot score the first token unconditionally")
        rows = self._logprob_rows(ids, from_index - 1)
        total = 0.0
        for i in range(from_index, len(ids)):
            total += float(rows[i - from_index, ids[i]].item())
        return total
