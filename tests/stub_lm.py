"""Deterministic character-level stub LM for scorer/decoder unit tests.

Char-level tokenization (one codepoint = one token id) gives tests exact
control over spans and probabilities without any model download. The LM's
distribution at each step:

- If the current prefix string is a key in `branch`, use that explicit
  char -> probability mapping (remaining mass spread over the rest of the
  vocab uniformly).
- Otherwise the "scripted" continuation char gets SCRIPT_P and the rest of
  the vocab shares the remainder. The scripted char at a position comes from
  the longest-anchor script whose anchor is a prefix of the realized text,
  indexed by position (see ScriptedLM.scripts).
- Past the end of the selected script, EOS is preferred.
"""

from __future__ import annotations

import math

EOS_ID = 0
SCRIPT_P = 0.9
VOCAB = [chr(c) for c in range(32, 127)] + ["\n"]


class CharTokenizer:
    def encode(self, text: str) -> list[int]:
        return [ord(c) for c in text]

    def decode(self, ids: list[int]) -> str:
        return "".join(chr(i) for i in ids)


class ScriptedLM:
    eos_id = EOS_ID

    def __init__(self, scripts: list[tuple[str, str]], branch: dict[str, dict[str, float]] | None = None):
        # scripts: list of (anchor, full_text). The active script for a prefix
        # is the one with the longest anchor that the prefix starts with;
        # full_text must itself start with the anchor.
        self.scripts = sorted(scripts, key=lambda s: -len(s[0]))
        self.branch = branch or {}
        self._tok = CharTokenizer()

    # -- tokenizer surface -------------------------------------------------
    def encode(self, text: str) -> list[int]:
        return self._tok.encode(text)

    def decode(self, ids: list[int]) -> str:
        return self._tok.decode(ids)

    # -- distribution ------------------------------------------------------
    def _dist(self, prefix: str) -> dict[str | int, float]:
        if prefix in self.branch:
            explicit = self.branch[prefix]
            rest = max(0.0, 1.0 - sum(explicit.values()))
            others = [c for c in VOCAB if c not in explicit]
            base = rest / (len(others) + 1)  # +1 for EOS
            dist: dict[str | int, float] = {c: base for c in others}
            dist[EOS_ID] = base
            dist.update(explicit)
            return dist
        for anchor, text in self.scripts:
            if prefix.startswith(anchor):
                if len(prefix) < len(text):
                    preferred: str | int = text[len(prefix)]
                else:
                    preferred = EOS_ID
                break
        else:
            preferred = EOS_ID
        others = [c for c in VOCAB if c != preferred]
        base = (1.0 - SCRIPT_P) / (len(others) + 1)
        dist = {c: base for c in others}
        dist[EOS_ID] = base
        dist[preferred] = SCRIPT_P
        return dist

    def _logp(self, prefix: str, char_or_eos: str | int) -> float:
        return math.log(self._dist(prefix)[char_or_eos])

    # -- LM protocol -------------------------------------------------------
    def greedy_next(self, ids: list[int]) -> int:
        prefix = self.decode(ids)
        dist = self._dist(prefix)
        best = max(dist.items(), key=lambda kv: (kv[1], -(kv[0] if isinstance(kv[0], int) else ord(kv[0]))))
        key = best[0]
        return key if isinstance(key, int) else ord(key)

    def sequence_logprob(self, ids: list[int], from_index: int) -> float:
        total = 0.0
        for i in range(from_index, len(ids)):
            prefix = self.decode(ids[:i])
            total += self._logp(prefix, chr(ids[i]))
        return total
