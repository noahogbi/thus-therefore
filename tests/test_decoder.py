"""Tests for the intervention decoder (SPEC section 2, HANDOFF item 3).

Greedy everywhere; at confirmed intervenable sites, uniform sample among
eligible candidates, splice, and regenerate the continuation from the
realized sequence. The decoder must be outcome-neutral: native mode is pure
greedy with no site machinery.
"""

import pytest

from harness.decoder import InterventionDecoder
from harness.scoring import EligibilityScorer
from tests.stub_lm import ScriptedLM

PROMPT = "P: "
# Rule 1 site: sentence-initial "Thus" followed by a detectable clause.
SCRIPT = PROMPT + "Go on. Thus, x is 2 now here. END"


class PickRng:
    """Deterministic rng: always picks `want` if present, else first."""

    def __init__(self, want):
        self.want = want
        self.calls = []

    def choice(self, options):
        self.calls.append(list(options))
        return self.want if self.want in options else options[0]


def make_decoder(lm, rng=None, intervene=True, **kw):
    return InterventionDecoder(
        lm=lm, scorer=EligibilityScorer(lm), rng=rng or PickRng(None),
        intervene=intervene, lookahead_chars=20, **kw)


def branch_two_eligible():
    # At the site prefix, make exactly {Thus, So} eligible: T and S nearly
    # tied (T slightly ahead so greedy still emits the script), 'o' after 'S'
    # kept on-path for scoring; Hence killed at 'H'; Therefore killed at the
    # 'u'/'e' split.
    return {
        PROMPT + "Go on. ": {"T": 0.46, "S": 0.44, "H": 0.001},
        PROMPT + "Go on. S": {"o": 0.9},
        PROMPT + "Go on. Th": {"u": 0.9, "e": 0.0001},
    }


class TestNativeMode:
    def test_native_greedy_reproduces_script(self):
        lm = ScriptedLM([("", SCRIPT)])
        result = make_decoder(lm, intervene=False).generate(PROMPT, max_new_tokens=100)
        assert result.text == SCRIPT
        assert result.ended == "eos"
        assert result.sites == []


class TestIntervention:
    def test_uniform_sample_among_eligible_and_splice(self):
        lm = ScriptedLM(
            [("", SCRIPT), (PROMPT + "Go on. So", PROMPT + "Go on. So, x is 2 now here. END")],
            branch=branch_two_eligible(),
        )
        rng = PickRng("So")
        result = make_decoder(lm, rng=rng).generate(PROMPT, max_new_tokens=100)

        [rec] = [r for r in result.sites if r.rule_id == "tier_a_01_connectives"]
        assert set(rec.eligible) == {"Thus", "So"}
        assert rng.calls == [["Thus", "So"]]
        assert rec.chosen == "So"
        assert rec.intervened
        assert result.text.startswith(PROMPT + "Go on. So,")
        assert "Thus" not in result.text

    def test_choosing_the_native_candidate_keeps_the_tail(self):
        lm = ScriptedLM([("", SCRIPT)], branch=branch_two_eligible())
        rng = PickRng("Thus")
        result = make_decoder(lm, rng=rng).generate(PROMPT, max_new_tokens=100)

        [rec] = [r for r in result.sites if r.rule_id == "tier_a_01_connectives"]
        assert rec.chosen == "Thus"
        assert not rec.intervened
        assert result.text == SCRIPT

    def test_site_decided_exactly_once(self):
        # After splicing "So", the new text contains an equally valid site at
        # the same position; the frontier must prevent re-deciding it.
        lm = ScriptedLM(
            [("", SCRIPT), (PROMPT + "Go on. So", PROMPT + "Go on. So, x is 2 now here. END")],
            branch=branch_two_eligible(),
        )
        result = make_decoder(lm, rng=PickRng("So")).generate(PROMPT, max_new_tokens=100)
        r1 = [r for r in result.sites if r.rule_id == "tier_a_01_connectives"]
        assert len(r1) == 1

    def test_fewer_than_two_eligible_skips(self):
        # Kill every alternative: only the native "Thus" is eligible.
        lm = ScriptedLM([("", SCRIPT)], branch={
            PROMPT + "Go on. ": {"T": 0.9, "S": 0.0001, "H": 0.0001},
        })
        rng = PickRng(None)
        result = make_decoder(lm, rng=rng).generate(PROMPT, max_new_tokens=100)
        [rec] = [r for r in result.sites if r.rule_id == "tier_a_01_connectives"]
        assert rec.skip_reason == "fewer_than_two_eligible"
        assert rec.chosen is None
        assert rng.calls == []
        assert result.text == SCRIPT


class TestBoundaries:
    def test_prompt_sites_never_decided(self):
        prompt = "Go on. Thus, x is 2 now here. "
        script = prompt + "y is 3 today. END"
        lm = ScriptedLM([("", script)])
        result = make_decoder(lm).generate(prompt, max_new_tokens=100)
        assert all(r.start >= len(prompt) for r in result.sites)

    def test_initiation_set_deferred_by_decoder(self):
        # REVIEW_LOG implementation note: the initiation set's exclusion is
        # trace-global (ordinal enumeration anywhere), which is unknowable
        # mid-generation. Conservative-skip: never randomize it while decoding.
        script = PROMPT + "Go. First, x is 2 now here. END"
        lm = ScriptedLM([("", script)])
        result = make_decoder(lm).generate(PROMPT, max_new_tokens=100)
        [rec] = [r for r in result.sites if r.set_id == "initiation"]
        assert rec.skip_reason == "global_exclusion_undecidable_mid_generation"
        assert not rec.intervened
        assert result.text == script


class TestDensity:
    def test_density_counts_intervenable_sites_per_1000_tokens(self):
        lm = ScriptedLM(
            [("", SCRIPT), (PROMPT + "Go on. So", PROMPT + "Go on. So, x is 2 now here. END")],
            branch=branch_two_eligible(),
        )
        result = make_decoder(lm, rng=PickRng("So")).generate(PROMPT, max_new_tokens=100)
        gen_tokens = result.generated_tokens
        assert gen_tokens > 0
        expected = 1000.0 / gen_tokens
        assert result.density["tier_a_01_connectives"] == pytest.approx(expected)

    def test_max_tokens_budget_respected(self):
        lm = ScriptedLM([("", SCRIPT)])
        result = make_decoder(lm, intervene=False).generate(PROMPT, max_new_tokens=5)
        assert result.generated_tokens == 5
        assert result.ended == "max_tokens"
