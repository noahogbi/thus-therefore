"""Intervention decoder (SPEC section 2, HANDOFF item 3).

Decoding is greedy everywhere. As text is generated, the site matcher runs
over the realized trace; a site is *confirmed* once generation has advanced
`lookahead_chars` past its end (or generation has ended), so that all local
contextual exclusions in the tables have the context they inspect. Confirmed
sites are processed strictly left to right:

- The site is force-scored by the EligibilityScorer against the realized
  prefix at that moment — which includes all prior randomized interventions,
  before applying randomization at the current site (frozen prefix wording).
- If >= 2 candidates are eligible, one is sampled UNIFORMLY among the
  eligible set. If the sampled candidate differs from the native span, the
  candidate is spliced in and everything after the edit span is discarded and
  regenerated from the realized sequence (the discarded text was lookahead
  conditioned on the native span). If the native span is sampled, the
  already-generated continuation is bit-identical to a regeneration, so it is
  kept.
- A frontier records how far decisions have been made; a decided site is
  never re-decided, and sites inside the prompt are never decided.

Outcome neutrality: with intervene=False (native arm) the decoder is pure
greedy with no site machinery, byte-identical to greedy decoding.

Conservative causal-knowledge rule (REVIEW_LOG, implementation note): the
rule 03 initiation set's exclusion is trace-global (drop the set whenever the
trace contains ordinal enumeration), which cannot be evaluated mid-generation
— text produced later could flip it. Per CLAUDE.md rule 2 the decoder never
randomizes that set; its sites are logged with a skip reason and reported as
structurally unavailable during generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from harness.matcher import Site, match_sites
from harness.scoring import EligibilityScorer, SequenceLM

# (rule_id, set_id) pairs whose table exclusions are trace-global and hence
# undecidable mid-generation. Conservative-skip during decoding.
GLOBALLY_EXCLUDED_MID_GENERATION = {
    ("tier_a_03_discourse_markers", "initiation"),
}


@dataclass
class SiteRecord:
    rule_id: str
    set_id: str
    start: int
    end: int
    matched: str
    candidates: list[str]
    logps: dict[str, float]
    eligible: list[str]
    chosen: str | None = None
    intervened: bool = False
    skip_reason: str | None = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id, "set_id": self.set_id,
            "start": self.start, "end": self.end, "matched": self.matched,
            "candidates": self.candidates, "logps": self.logps,
            "eligible": self.eligible, "chosen": self.chosen,
            "intervened": self.intervened, "skip_reason": self.skip_reason,
        }


@dataclass
class DecodeResult:
    text: str
    prompt_chars: int
    generated_tokens: int
    ended: str  # "eos" | "max_tokens"
    sites: list[SiteRecord] = field(default_factory=list)

    @property
    def density(self) -> dict[str, float]:
        """Intervenable (>= 2 eligible) sites per 1,000 generated tokens,
        per rule (SPEC section 9)."""
        out: dict[str, float] = {}
        if self.generated_tokens == 0:
            return out
        for rec in self.sites:
            if len(rec.eligible) >= 2 and rec.skip_reason != "global_exclusion_undecidable_mid_generation":
                out[rec.rule_id] = out.get(rec.rule_id, 0.0) + 1.0
        return {r: n * 1000.0 / self.generated_tokens for r, n in out.items()}


class InterventionDecoder:
    def __init__(self, lm: SequenceLM, scorer: EligibilityScorer, rng,
                 matcher: Callable[[str], list[Site]] = match_sites,
                 lookahead_chars: int = 100, intervene: bool = True):
        self.lm = lm
        self.scorer = scorer
        self.rng = rng
        self.matcher = matcher
        self.lookahead_chars = lookahead_chars
        self.intervene = intervene

    def generate(self, prompt: str, max_new_tokens: int) -> DecodeResult:
        ids = self.lm.encode(prompt)
        prompt_id_len = len(ids)
        realized = prompt
        frontier = len(prompt)
        records: list[SiteRecord] = []
        ended: str | None = None

        while True:
            if self.intervene:
                site = self._next_confirmed_site(realized, frontier, terminal=ended is not None)
                if site is not None:
                    realized, ids, frontier = self._decide_site(
                        realized, ids, site, records)
                    continue
            if ended is not None:
                break
            if len(ids) - prompt_id_len >= max_new_tokens:
                ended = "max_tokens"
                continue
            nxt = self.lm.greedy_next(ids)
            if self.lm.eos_id is not None and nxt == self.lm.eos_id:
                ended = "eos"
                continue
            ids = ids + [nxt]
            realized = self.lm.decode(ids)

        return DecodeResult(
            text=realized, prompt_chars=len(prompt),
            generated_tokens=len(ids) - prompt_id_len,
            ended=ended, sites=records)

    # -- internals ---------------------------------------------------------

    def _next_confirmed_site(self, realized: str, frontier: int,
                             terminal: bool) -> Site | None:
        for site in self.matcher(realized):
            if site.start < frontier:
                continue
            if terminal or site.end + self.lookahead_chars <= len(realized):
                return site
            # Sites are position-sorted; nothing later can be confirmed if
            # this one is not.
            return None
        return None

    def _decide_site(self, realized: str, ids: list[int], site: Site,
                     records: list[SiteRecord]) -> tuple[str, list[int], int]:
        scored = self.scorer.score_site(realized, site)
        rec = SiteRecord(
            rule_id=site.rule_id, set_id=site.set_id,
            start=site.start, end=site.end, matched=site.matched,
            candidates=list(site.candidates),
            logps={c.text: c.logp for c in scored.candidates},
            eligible=scored.eligible_texts(),
        )
        records.append(rec)

        if (site.rule_id, site.set_id) in GLOBALLY_EXCLUDED_MID_GENERATION:
            rec.skip_reason = "global_exclusion_undecidable_mid_generation"
            return realized, ids, site.end
        if not scored.intervenable:
            rec.skip_reason = "fewer_than_two_eligible"
            return realized, ids, site.end

        chosen = self.rng.choice(rec.eligible)
        rec.chosen = chosen
        if chosen == site.matched:
            # Regenerating from here would be bit-identical: keep the tail.
            return realized, ids, site.end

        rec.intervened = True
        realized = realized[:site.start] + chosen
        ids = self.lm.encode(realized)
        return realized, ids, site.start + len(chosen)
