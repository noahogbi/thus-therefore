"""Integration test: HFCausalLM adapter against a real (tiny) HF model.

Validates the transformers API surface we rely on (pinned 5.14.1 in
environment.json) so version drift surfaces here, on CPU, rather than on the
rented GPU. Uses sshleifer/tiny-gpt2 (~2 MB, random weights — behavior is
meaningless, determinism and interface are what's under test).

Skips cleanly if the model can't be downloaded (offline).
"""

import math

import pytest

try:
    from harness.scoring import EligibilityScorer, HFCausalLM
    LM = HFCausalLM("sshleifer/tiny-gpt2")
except Exception as e:  # pragma: no cover - offline/dependency skip
    LM = None
    SKIP_REASON = f"tiny model unavailable: {e}"

pytestmark = pytest.mark.skipif(LM is None, reason="tiny HF model unavailable")


def test_encode_decode_roundtrip():
    text = "So we get x = 17 as the residue."
    assert LM.decode(LM.encode(text)) == text


def test_greedy_next_deterministic():
    ids = LM.encode("The value is")
    assert LM.greedy_next(ids) == LM.greedy_next(list(ids))


def test_sequence_logprob_finite_and_additive():
    ids = LM.encode("x = 17 and y = 41")
    lp_all = LM.sequence_logprob(ids, 1)
    lp_head = LM.sequence_logprob(ids[:4], 1)
    assert math.isfinite(lp_all)
    assert lp_all < 0
    # Scoring the first 4 tokens then tokens 4.. must sum to the whole.
    lp_tail = LM.sequence_logprob(ids, 4)
    assert lp_all == pytest.approx(lp_head + lp_tail, abs=1e-4)


def test_extra_terminal_tokens_resolved_to_ids():
    # Eighth-relay 8.1(b): terminal set = {configured EOS, <|endoftext|>}.
    # tiny-gpt2's EOS *is* <|endoftext|>, so the set collapses; a second
    # ordinary vocab token proves distinct ids are added.
    lm = HFCausalLM("sshleifer/tiny-gpt2",
                    extra_terminal_tokens=["<|endoftext|>"])
    assert lm.terminal_ids == {lm.eos_id}
    lm2 = HFCausalLM("sshleifer/tiny-gpt2",
                     extra_terminal_tokens=["<|endoftext|>", "the"])
    tid = lm2.tok.convert_tokens_to_ids("the")
    assert tid is not None and tid >= 0
    assert lm2.terminal_ids == {lm2.eos_id, tid}


def test_default_has_no_terminal_ids_attribute():
    # Absent the opt-in, the adapter must not grow a terminal_ids attribute:
    # the decoder's frozen single-EOS path (rung 1) keys off its absence.
    assert not hasattr(LM, "terminal_ids")


def test_kv_cache_greedy_matches_uncached():
    # The cached path must be behaviorally identical to the naive full
    # forward (the bit-identity sanity reference).
    uncached = HFCausalLM("sshleifer/tiny-gpt2", use_cache=False)
    ids_c = LM.encode("We compute the value of x now.")
    ids_u = list(ids_c)
    for _ in range(25):
        ids_c.append(LM.greedy_next(ids_c))
        ids_u.append(uncached.greedy_next(ids_u))
    assert ids_c == ids_u


def test_kv_cache_seqlogprob_matches_uncached():
    uncached = HFCausalLM("sshleifer/tiny-gpt2", use_cache=False)
    ids = LM.encode("x = 17 and y = 41 so z = 58")
    # Prime the cache with a longer sequence, then score a shorter prefix
    # variant to exercise the crop path.
    LM.greedy_next(ids)
    branch = ids[:6] + LM.encode(" instead")
    got = LM.sequence_logprob(branch, 3)
    want = uncached.sequence_logprob(branch, 3)
    assert got == pytest.approx(want, abs=1e-3)


def test_kv_cache_divergent_branches_score_equal():
    # Scoring candidate A then candidate B then A again (as the scorer does
    # across sites) must not drift.
    prefix = LM.encode("The sum is ")
    a = prefix + LM.encode("42 exactly")
    b = prefix + LM.encode("41 roughly")
    first = LM.sequence_logprob(a, len(prefix))
    LM.sequence_logprob(b, len(prefix))
    again = LM.sequence_logprob(a, len(prefix))
    assert first == pytest.approx(again, abs=1e-5)


def test_scorer_end_to_end_on_real_tokenizer():
    from harness.matcher import match_sites

    text = "We substitute the value. So x = 17 holds for the residue now."
    [site] = [s for s in match_sites(text) if s.rule_id == "tier_a_01_connectives"]
    scored = EligibilityScorer(LM).score_site(text, site)

    assert len(scored.candidates) == 4
    assert all(math.isfinite(c.logp) for c in scored.candidates)
    matched = [c for c in scored.candidates if c.text == site.matched]
    assert len(matched) == 1
    # Best candidate is always eligible by construction.
    best = max(scored.candidates, key=lambda c: c.logp)
    assert best.eligible
