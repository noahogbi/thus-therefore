"""Tests for the run harness and depth calibrator (HANDOFF items 4-5)."""

import json

import pytest

from harness.calibrate import calibrate
from harness.runner import extract_answer, extract_answer_extended, run_problems
from harness.scoring import EligibilityScorer
from tests.stub_lm import ScriptedLM


class TestExtractAnswer:
    def test_extracts_last_answer_line(self):
        assert extract_answer("ANSWER: 12\nmore\nANSWER: 42") == "42"

    def test_normalizes_numeric(self):
        assert extract_answer("ANSWER: 042") == "42"
        assert extract_answer("ANSWER: -56") == "-56"

    def test_none_answer(self):
        assert extract_answer("thinking...\nANSWER: none") == "none"

    def test_missing_answer(self):
        assert extract_answer("no answer emitted") is None


class TestExtractAnswerExtended:
    """Eighth-relay 8.1(b) rule, frozen as exact mechanics (REVIEW_LOG):
    ANSWER-line regex takes precedence; else the LAST \\boxed{<integer>} in
    the trace; nothing else accepted."""

    def test_answer_line_takes_precedence_over_boxed(self):
        assert extract_answer_extended("\\boxed{99}\nANSWER: 7") == "7"
        assert extract_answer_extended("ANSWER: 7\nthen \\boxed{99}") == "7"

    def test_last_boxed_integer_when_no_answer_line(self):
        assert extract_answer_extended("\\boxed{12} then \\boxed{042}") == "42"

    def test_boxed_negative_and_display_math(self):
        assert extract_answer_extended("\\[\n\\boxed{-56}\n\\]") == "-56"

    def test_non_integer_boxed_is_not_a_match(self):
        assert extract_answer_extended("\\boxed{x+2} and \\boxed{3.5}") is None
        # ...and does not shadow an earlier integer boxed: LAST *integer* box.
        assert extract_answer_extended("\\boxed{5} and \\boxed{x}") == "5"

    def test_nothing_else_accepted(self):
        assert extract_answer_extended("the answer is 12") is None

    def test_matches_frozen_extractor_when_answer_line_present(self):
        text = "steps...\nANSWER: 042"
        assert extract_answer_extended(text) == extract_answer(text) == "42"


def make_problem(pid, prompt, answer, family="composition", depth=3):
    return {"id": pid, "family": family, "depth": depth,
            "prompt": prompt, "answer": answer}


class TestRunProblems:
    def test_native_run_records_correctness(self):
        p1 = make_problem("p1", "Q1: ", "7")
        p2 = make_problem("p2", "Q2: ", "9")
        lm = ScriptedLM([
            ("Q1: ", "Q1: x is 7 here. ANSWER: 7"),
            ("Q2: ", "Q2: y is 8 here. ANSWER: 8"),
        ])
        records = list(run_problems(
            lm, [p1, p2], mode="native", seed=1, max_new_tokens=200))

        by_id = {r["id"]: r for r in records}
        assert by_id["p1"]["correct"] is True
        assert by_id["p1"]["answer_extracted"] == "7"
        assert by_id["p2"]["correct"] is False
        assert by_id["p2"]["answer_extracted"] == "8"
        assert by_id["p1"]["mode"] == "native"
        assert by_id["p1"]["sites"] == []

    def test_randomized_run_logs_sites_and_is_seed_deterministic(self):
        prompt = "Go on. "
        script = prompt + "Thus, x is 2 now here. ANSWER: 2"
        p = make_problem("p1", prompt, "2")
        branch = {
            prompt: {"T": 0.46, "S": 0.44, "H": 0.001},
            prompt + "S": {"o": 0.9},
            prompt + "Th": {"u": 0.9, "e": 0.0001},
        }
        scripts = [("", script),
                   (prompt + "So", prompt + "So, x is 2 now here. ANSWER: 2")]

        runs = []
        for _ in range(2):
            lm = ScriptedLM(scripts, branch=branch)
            [r] = list(run_problems(lm, [p], mode="randomized", seed=99,
                                    max_new_tokens=200))
            runs.append(r)

        assert runs[0]["text"] == runs[1]["text"]  # same seed -> same run
        assert runs[0]["sites"] == runs[1]["sites"]
        [site] = [s for s in runs[0]["sites"]
                  if s["rule_id"] == "tier_a_01_connectives"]
        assert set(site["eligible"]) == {"Thus", "So"}
        assert runs[0]["correct"] is True

    def test_extended_extraction_mode(self):
        p = make_problem("p1", "Q: ", "7")
        lm = ScriptedLM([("Q: ", "Q: compute. \\boxed{7}")])
        [r] = list(run_problems(lm, [p], mode="native", seed=1,
                                max_new_tokens=200, extended_extraction=True))
        assert r["answer_extracted"] == "7"
        assert r["correct"] is True
        assert r["extraction_rule"] == "extended"

    def test_frozen_extraction_is_the_default_and_labeled(self):
        p = make_problem("p1", "Q: ", "7")
        lm = ScriptedLM([("Q: ", "Q: compute. \\boxed{7}")])
        [r] = list(run_problems(lm, [p], mode="native", seed=1,
                                max_new_tokens=200))
        assert r["answer_extracted"] is None
        assert r["correct"] is False
        assert r["extraction_rule"] == "frozen"

    def test_rules_arm_passthrough(self):
        prompt = "Go on. "
        script = prompt + "Thus, x is 2 now here. ANSWER: 2"
        p = make_problem("p1", prompt, "2")
        lm = ScriptedLM([("", script)])
        [r] = list(run_problems(lm, [p], mode="randomized", seed=1,
                                rules={"tier_a_06_operator_spacing"},
                                max_new_tokens=200))
        assert all(s["rule_id"] == "tier_a_06_operator_spacing"
                   for s in r["sites"])


class TestCalibrate:
    def test_with_and_without_trace_accuracy_gap(self):
        # The stub answers correctly when allowed to "reason" (script) and
        # incorrectly when the no-trace suffix is appended.
        p = make_problem("p1", "Q: ", "7", family="composition", depth=4)
        from harness.calibrate import NO_TRACE_SUFFIX
        lm = ScriptedLM([
            ("Q: ", "Q: step step. ANSWER: 7"),
            ("Q: " + NO_TRACE_SUFFIX, "Q: " + NO_TRACE_SUFFIX + "ANSWER: 3"),
        ])
        grid = calibrate(lm, [p], max_new_tokens=200)
        cell = grid[("composition", 4)]
        assert cell["with_trace_acc"] == 1.0
        assert cell["without_trace_acc"] == 0.0
        assert cell["gap"] == 1.0
        assert cell["n"] == 1
