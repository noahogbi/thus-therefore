"""Tests for the O1/O2 analysis (SPEC sections 6 and 9, HANDOFF item 7)."""

import pytest

from harness.analysis import analyze_arm, slope


def recs(mode, cells):
    """cells: {(family, depth): [bool, ...]} -> run records."""
    out = []
    for (family, depth), corrects in cells.items():
        for i, c in enumerate(corrects):
            out.append({"id": f"{family}-{depth}-{i}", "family": family,
                        "depth": depth, "mode": mode, "correct": c})
    return out


class TestSlope:
    def test_positive_slope(self):
        assert slope([(2, 0.0), (4, 0.1), (6, 0.2)]) == pytest.approx(0.05)

    def test_flat(self):
        assert slope([(2, 0.1), (4, 0.1), (6, 0.1)]) == pytest.approx(0.0)

    def test_underdetermined_is_none(self):
        assert slope([(2, 0.1)]) is None


class TestAnalyzeArm:
    def test_o1_and_o2_per_family(self):
        native = recs("native", {
            ("composition", 2): [True] * 10,
            ("composition", 4): [True] * 10,
            ("composition", 6): [True] * 10,
        })
        randomized = recs("randomized", {
            ("composition", 2): [True] * 10,                    # penalty 0.0
            ("composition", 4): [True] * 9 + [False],           # penalty 0.1
            ("composition", 6): [True] * 8 + [False] * 2,       # penalty 0.2
        })
        result = analyze_arm(native, randomized)

        comp = result["families"]["composition"]
        assert comp["cells"]["2"]["penalty"] == pytest.approx(0.0)
        assert comp["cells"]["6"]["penalty"] == pytest.approx(0.2)
        assert comp["o2_slope"] == pytest.approx(0.05)
        assert result["o1_mean_penalty"] == pytest.approx(0.1)

    def test_mismatched_cells_ignored_with_note(self):
        native = recs("native", {("composition", 2): [True] * 4})
        randomized = recs("randomized", {("composition", 2): [True, False],
                                         ("multiplication", 3): [True]})
        result = analyze_arm(native, randomized)
        assert "multiplication" not in result["families"]
        assert result["unmatched_cells"] == ["multiplication:3"]
