"""Tests for the eligibility scorer (SPEC section 2, REVIEW_LOG F5).

The scorer must:
- score each candidate as the raw log-probability of the full forced span
  (left context + candidate + right context of the F5 score span) given the
  realized prefix, with NO length normalization;
- mark a candidate eligible iff logp >= best - 1.5 nats;
- mark the site intervenable iff >= 2 candidates are eligible;
- handle tokenizers that merge tokens across the prefix/span boundary by
  scoring from the end of the common token prefix.
"""

import math

import pytest

from harness.matcher import Site
from harness.scoring import DELTA_NATS, EligibilityScorer
from tests.stub_lm import ScriptedLM


def make_site(text, matched, candidates, score_start=None, score_end=None):
    start = text.index(matched)
    end = start + len(matched)
    return Site(
        rule_id="test_rule", set_id="test", start=start, end=end,
        matched=matched, candidates=candidates,
        score_start=start if score_start is None else score_start,
        score_end=end if score_end is None else score_end,
    )


class TestEligibility:
    def test_delta_rule_splits_candidates(self):
        # Explicit branch at the site: A=0.5, B=0.3 (gap 0.51 < 1.5, both
        # eligible), C=0.01 (gap 3.9 > 1.5, ineligible).
        text = "xxA"
        lm = ScriptedLM([("", text)], branch={"xx": {"A": 0.5, "B": 0.3, "C": 0.01}})
        site = make_site(text, "A", ["A", "B", "C"])
        scored = EligibilityScorer(lm).score_site(text, site)

        by_text = {c.text: c for c in scored.candidates}
        assert by_text["A"].eligible
        assert by_text["B"].eligible
        assert not by_text["C"].eligible
        assert scored.intervenable

    def test_raw_logp_no_length_normalization(self):
        text = "xxA"
        lm = ScriptedLM([("", text)], branch={"xx": {"A": 0.5, "B": 0.3, "C": 0.01}})
        site = make_site(text, "A", ["A", "B", "C"])
        scored = EligibilityScorer(lm).score_site(text, site)
        by_text = {c.text: c for c in scored.candidates}
        assert by_text["A"].logp == pytest.approx(math.log(0.5))
        assert by_text["B"].logp == pytest.approx(math.log(0.3))
        assert by_text["C"].logp == pytest.approx(math.log(0.01))

    def test_single_eligible_not_intervenable(self):
        text = "xxA"
        lm = ScriptedLM([("", text)], branch={"xx": {"A": 0.9, "B": 0.001}})
        site = make_site(text, "A", ["A", "B"])
        scored = EligibilityScorer(lm).score_site(text, site)
        assert not scored.intervenable
        assert sum(c.eligible for c in scored.candidates) == 1

    def test_delta_is_frozen_value(self):
        assert DELTA_NATS == 1.5


class TestScoreSpanSplicing:
    def test_candidates_spliced_into_score_span(self):
        # Site edits '=' inside score span "x=1" (REVIEW_LOG F5): the scorer
        # must score "x" + candidate + "1", not the bare candidate.
        text = "q x=1 r"
        lm = ScriptedLM([("", text)])
        site = make_site(text, "=", ["=", " = "], score_start=2, score_end=5)
        scored = EligibilityScorer(lm).score_site(text, site)

        by_text = {c.text: c for c in scored.candidates}
        assert by_text["="].span_text == "x=1"
        assert by_text[" = "].span_text == "x = 1"
        # On-script candidate scores three SCRIPT_P chars; the spaced variant
        # goes off-script and must score strictly lower.
        assert by_text["="].logp == pytest.approx(3 * math.log(0.9))
        assert by_text["="].logp > by_text[" = "].logp

    def test_identical_candidate_scores_equal(self):
        text = "q x=1 r"
        lm = ScriptedLM([("", text)])
        site = make_site(text, "=", ["=", "="], score_start=2, score_end=5)
        scored = EligibilityScorer(lm).score_site(text, site)
        assert scored.candidates[0].logp == pytest.approx(scored.candidates[1].logp)


class TestTokenBoundary:
    def test_scoring_starts_at_common_token_prefix(self):
        # A tokenizer that merges "x=" into one id: the prefix "q x" tokenizes
        # to [q, ' ', x] but the full text retokenizes the boundary, so the
        # scorer must charge the merged token to the candidate (score from the
        # common prefix, not from len(prefix_ids)).
        class MergingLM(ScriptedLM):
            def encode(self, text):
                ids, i = [], 0
                while i < len(text):
                    if text[i:i + 2] == "x=":
                        ids.append(1000)
                        i += 2
                    else:
                        ids.append(ord(text[i]))
                        i += 1
                return ids

            def decode(self, ids):
                return "".join("x=" if i == 1000 else chr(i) for i in ids)

            def sequence_logprob(self, ids, from_index):
                self.seen_from_index = from_index
                return -1.0

        text = "q x=1 r"
        lm = MergingLM([("", text)])
        site = make_site(text, "=", ["="], score_start=2, score_end=5)
        EligibilityScorer(lm).score_site(text, site)
        # prefix "q x" -> [q, ' ', x] (3 ids); full "q x=1" -> [q, ' ', 1000, 1]
        # common prefix is 2 ids, so scoring must start at index 2.
        assert lm.seen_from_index == 2
