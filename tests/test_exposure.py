"""Tests for S1 exposure reporting and the Proposal A machinery
(native-path exposure scoring + trace-level logistic model)."""

import math

import pytest

from harness.exposure import (
    exposure_stats,
    fit_logistic,
    native_eligible_counts,
)
from harness.scoring import EligibilityScorer
from tests.stub_lm import ScriptedLM


class TestNativeEligibleCounts:
    def test_counts_eligible_sites_on_native_trace(self):
        # Native record whose trace contains one rule-01 site with two
        # eligible candidates under the stub's branch distribution.
        text = "Go on. Thus, x is 2 now here. END"
        lm = ScriptedLM([("", text)], branch={
            "Go on. ": {"T": 0.46, "S": 0.44, "H": 0.001},
            "Go on. S": {"o": 0.9},
            "Go on. Th": {"u": 0.9, "e": 0.0001},
        })
        record = {"id": "p1", "family": "reachability", "depth": 4,
                  "mode": "native", "text": text, "prompt_chars": 0}
        [out] = list(native_eligible_counts(
            [record], EligibilityScorer(lm)))
        assert out["id"] == "p1"
        assert out["native_eligible_total"] >= 1
        assert out["native_eligible_by_rule"]["tier_a_01_connectives"] == 1

    def test_prompt_region_excluded(self):
        text = "Thus, x is 2 now here. Go END"
        lm = ScriptedLM([("", text)])
        record = {"id": "p1", "family": "reachability", "depth": 4,
                  "mode": "native", "text": text,
                  "prompt_chars": len(text)}  # everything is prompt
        [out] = list(native_eligible_counts([record], EligibilityScorer(lm)))
        assert out["native_eligible_total"] == 0


class TestExposureStats:
    def test_mean_median_distribution(self):
        recs = []
        for i, k in enumerate([0, 1, 1, 2, 6]):
            sites = [{"rule_id": "r", "intervened": True}] * k
            recs.append({"id": f"p{i}", "family": "reachability", "depth": 4,
                         "mode": "randomized", "sites": sites})
        stats = exposure_stats(recs)
        cell = stats[("reachability", 4)]
        assert cell["mean"] == pytest.approx(2.0)
        assert cell["median"] == 1
        assert cell["distribution"] == {0: 1, 1: 2, 2: 1, 6: 1}
        assert cell["n"] == 5


class TestLogistic:
    def test_recovers_known_coefficients(self):
        import random
        rng = random.Random(7)
        beta_true = [-0.5, 1.2, -0.8]
        rows = []
        for _ in range(4000):
            x = [1.0, rng.uniform(-2, 2), rng.uniform(-2, 2)]
            z = sum(b * v for b, v in zip(beta_true, x))
            p = 1 / (1 + math.exp(-z))
            rows.append((x, 1 if rng.random() < p else 0))
        beta = fit_logistic([x for x, _ in rows], [y for _, y in rows])
        for b_hat, b in zip(beta, beta_true):
            assert b_hat == pytest.approx(b, abs=0.15)

    def test_separable_data_does_not_blow_up(self):
        xs = [[1.0, float(i)] for i in range(20)]
        ys = [0] * 10 + [1] * 10
        beta = fit_logistic(xs, ys)
        assert all(math.isfinite(b) for b in beta)
