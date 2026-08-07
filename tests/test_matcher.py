"""Tests for the Tier A site matcher.

Every test encodes a behavior required by rules/tier_a/*.json (frozen) plus the
conservative-skip principle from CLAUDE.md: when a rule's contextual matcher is
ambiguous, the location is NOT a site.

Matcher API under test:
    match_sites(text) -> list[Site]
    Site: rule_id, set_id, start, end, matched, candidates
    - char-offset spans; text[start:end] == matched
    - matched is always one of candidates
    - overlapping sites resolved: lowest rule_id wins, other rule skips
"""

import pytest

from harness.matcher import match_sites


def sites_for(text, rule=None, set_id=None):
    out = match_sites(text)
    if rule is not None:
        out = [s for s in out if s.rule_id == rule]
    if set_id is not None:
        out = [s for s in out if s.set_id == set_id]
    return out


def assert_span_integrity(text):
    for s in match_sites(text):
        assert text[s.start:s.end] == s.matched
        assert s.matched in s.candidates
        assert len(s.candidates) >= 2


R1 = "tier_a_01_connectives"
R2 = "tier_a_02_punctuation"
R3 = "tier_a_03_discourse_markers"
R4 = "tier_a_04_contractions"
R5 = "tier_a_05_whitespace"
R6 = "tier_a_06_operator_spacing"
R7 = "tier_a_07_list_markers"


# ---------------------------------------------------------------------------
# Rule 1 — connectives
# ---------------------------------------------------------------------------

class TestConnectives:
    def test_sentence_initial_thus_with_comma(self):
        text = "x = 5. Thus, y = 6."
        [s] = sites_for(text, R1)
        assert s.matched == "Thus"
        assert set(s.candidates) == {"Thus", "Therefore", "Hence", "So"}

    def test_text_initial_therefore_followed_by_clause(self):
        text = "Therefore the result is 12."
        [s] = sites_for(text, R1)
        assert s.matched == "Therefore"

    def test_sentence_initial_so_with_symbolic_clause(self):
        text = "We substitute. So x = 17."
        [s] = sites_for(text, R1)
        assert s.matched == "So"

    def test_mid_sentence_so_after_clause_comma(self):
        text = "We rearrange the terms, so the result follows."
        [s] = sites_for(text, R1)
        assert s.matched == "so"
        assert set(s.candidates) == {"thus", "therefore", "hence", "so"}

    def test_so_that_purpose_clause_excluded(self):
        text = "We simplify the fraction, so that the terms cancel."
        assert sites_for(text, R1) == []

    def test_sentence_initial_so_that_excluded(self):
        text = "Group the terms. So that the sum telescopes, pair them."
        assert sites_for(text, R1) == []

    def test_comparative_so_much_excluded(self):
        text = "The second term grows, so much faster than the first."
        assert sites_for(text, R1) == []

    def test_degree_so_adjective_that_excluded(self):
        text = "The bound is, so loose that it tells us nothing."
        assert sites_for(text, R1) == []

    def test_so_what_question_skipped_no_clause(self):
        text = "The lemma fails. So what?"
        assert sites_for(text, R1) == []

    def test_inside_double_quotes_excluded(self):
        text = 'The hint said "Thus, use induction on n."'
        assert sites_for(text, R1) == []

    def test_inside_fenced_code_excluded(self):
        text = "Run this:\n```\nso = compute(x)\nthus = so + 1\n```\nDone."
        assert sites_for(text, R1) == []

    def test_hence_no_following_clause_skipped(self):
        # "Hence proved." — no detectable subject-verb clause, no comma: skip.
        text = "The base case holds. Hence proved."
        assert sites_for(text, R1) == []


# ---------------------------------------------------------------------------
# Rule 2 — punctuation
# ---------------------------------------------------------------------------

class TestPunctuation:
    def test_now_comma_variant_site(self):
        text = "Now we compute the product."
        [s] = sites_for(text, R2, "comma_after_initial_connective")
        assert s.matched == "Now "
        assert set(s.candidates) == {"Now, ", "Now "}

    def test_then_with_comma_site(self):
        text = "Add 3 to both sides. Then, divide by 2."
        [s] = sites_for(text, R2, "comma_after_initial_connective")
        assert s.matched == "Then, "
        assert set(s.candidates) == {"Then, ", "Then "}

    def test_rule1_wins_overlap_on_thus(self):
        # "Thus, ..." matches rule 1 (the word) and rule 2 (word + comma).
        # Spans overlap; lowest rule_id wins, so ONLY the rule 1 site survives.
        text = "x = 5. Thus, y = 6."
        assert len(sites_for(text, R1)) == 1
        assert sites_for(text, R2) == []

    def test_display_line_final_period_site(self):
        text = "We evaluate step by step.\nx = 42.\nNext we substitute."
        [s] = sites_for(text, R2, "final_period_on_display_line")
        assert s.matched == "x = 42."
        assert set(s.candidates) == {"x = 42.", "x = 42"}

    def test_display_line_without_period_site(self):
        text = "Step one gives this line:\nf3(x) = (5*x + 2) mod 97\nNow apply f4."
        sites = sites_for(text, R2, "final_period_on_display_line")
        assert len(sites) == 1
        assert sites[0].matched == "f3(x) = (5*x + 2) mod 97"

    def test_prose_sentence_period_not_a_display_line(self):
        text = "We conclude the following.\nThe answer is 42.\nDone."
        assert sites_for(text, R2, "final_period_on_display_line") == []

    def test_decimal_point_never_matched(self):
        text = "Multiply by 0.5 to halve it."
        assert sites_for(text, R2) == []

    def test_quoted_connective_excluded(self):
        text = 'The prompt says "Now, show your work."'
        assert sites_for(text, R2) == []


# ---------------------------------------------------------------------------
# Rule 3 — discourse markers
# ---------------------------------------------------------------------------

class TestDiscourseMarkers:
    def test_note_that_site(self):
        text = "Note that x is even."
        [s] = sites_for(text, R3)
        assert s.matched == "Note that"
        assert set(s.candidates) == {"Note that", "Observe that", "Notice that"}

    def test_in_other_words_site(self):
        text = "The map is injective and surjective. In other words, it is a bijection."
        recap = sites_for(text, R3, "recap")
        assert len(recap) == 1
        assert recap[0].matched == "In other words,"

    def test_sequencing_set_lost_to_rule2_overlap(self):
        # "Next," / "Then," are also rule 2 connectives; rule 2's span
        # (connective + optional comma) overlaps, and 02 < 03 wins.
        # Mechanical consequence of the frozen tables — documented for review.
        text = "Compute f1 of x. Next, compute f2."
        assert sites_for(text, R3, "sequencing") == []
        assert len(sites_for(text, R2)) == 1

    def test_first_site_when_no_enumeration(self):
        text = "First, we factor the modulus."
        init = sites_for(text, R3, "initiation")
        assert len(init) == 1
        assert init[0].matched == "First,"

    def test_first_excluded_when_trace_has_ordinal_enumeration(self):
        text = "First, factor n. Second, test each factor."
        assert sites_for(text, R3, "initiation") == []

    def test_quoted_marker_excluded(self):
        text = 'The card reads "Note that all inputs are positive."'
        assert sites_for(text, R3) == []

    def test_mid_sentence_marker_not_matched(self):
        text = "We should note that x is even."
        assert sites_for(text, R3) == []


# ---------------------------------------------------------------------------
# Rule 4 — contractions
# ---------------------------------------------------------------------------

class TestContractions:
    def test_its_contraction_site(self):
        text = "It's even, since 4 divides it."
        [s] = sites_for(text, R4)
        assert s.matched == "It's"
        assert s.candidates == ["It's", "It is"]

    def test_it_is_expansion_site(self):
        text = "Because it is even, we halve it."
        [s] = sites_for(text, R4)
        assert s.matched == "it is"
        assert s.candidates == ["it is", "it's"]

    def test_possessive_its_no_site(self):
        text = "The graph keeps its edges."
        assert sites_for(text, R4) == []

    def test_quoted_contraction_excluded(self):
        text = 'She wrote "it\'s trivially true" in the margin.'
        assert sites_for(text, R4) == []

    def test_code_contraction_excluded(self):
        text = "Set the flag: `dont_retry = True` before running."
        assert sites_for(text, R4) == []

    def test_cannot_site(self):
        text = "We cannot divide by zero."
        [s] = sites_for(text, R4)
        assert s.matched == "cannot"
        assert s.candidates == ["cannot", "can't"]

    def test_dont_casing_preserved(self):
        text = "Don't divide by zero."
        [s] = sites_for(text, R4)
        assert s.matched == "Don't"
        assert s.candidates == ["Don't", "Do not"]

    def test_lets_clause_initial_hortative_site(self):
        text = "Let's compute the residue."
        [s] = sites_for(text, R4)
        assert s.matched == "Let's"

    def test_lets_not_clause_initial_skipped(self):
        text = "The lemma lets us cancel the factor."
        assert sites_for(text, R4) == []

    def test_wont_site(self):
        text = "The term won't vanish."
        [s] = sites_for(text, R4)
        assert s.matched == "won't"
        assert s.candidates == ["won't", "will not"]


# ---------------------------------------------------------------------------
# Rule 5 — whitespace
# ---------------------------------------------------------------------------

class TestWhitespace:
    def test_double_newline_between_paragraphs_site(self):
        text = "We factor the modulus into primes.\n\nNext we apply the CRT."
        [s] = sites_for(text, R5)
        assert s.matched == "\n\n"
        assert set(s.candidates) == {"\n", "\n\n"}

    def test_single_newline_between_paragraphs_site(self):
        text = "We factor the modulus into primes.\nNext we apply the CRT."
        [s] = sites_for(text, R5)
        assert s.matched == "\n"

    def test_boundary_adjacent_to_code_fence_excluded(self):
        text = "Run the check.\n\n```\nassert x == 5\n```\n\nIt passes."
        assert sites_for(text, R5) == []

    def test_list_item_boundaries_excluded(self):
        text = "- factor the modulus\n- test each residue\n- combine"
        assert sites_for(text, R5) == []

    def test_blank_line_before_list_excluded(self):
        # Blank-line presence before a markdown list changes rendering semantics.
        text = "We need three steps.\n\n- factor\n- test\n- combine"
        assert sites_for(text, R5) == []


# ---------------------------------------------------------------------------
# Rule 6 — operator spacing
# ---------------------------------------------------------------------------

class TestOperatorSpacing:
    def test_equals_spaced_site(self):
        text = "So we get x = 17 as the residue."
        eq = sites_for(text, R6, "equals")
        assert len(eq) == 1
        assert eq[0].matched == " = "
        assert set(eq[0].candidates) == {"=", " = "}

    def test_equals_unspaced_site(self):
        text = "Substituting gives y=41 here."
        eq = sites_for(text, R6, "equals")
        assert len(eq) == 1
        assert eq[0].matched == "="

    def test_plus_site(self):
        text = "Compute 3 + 4 to get 7."
        plus = sites_for(text, R6, "plus")
        assert len(plus) == 1

    def test_times_site(self):
        text = "The product 6*7 appears twice."
        times = sites_for(text, R6, "times")
        assert len(times) == 1

    def test_numeric_minus_ambiguous_range_skipped(self):
        # "5-10" could be a range; matcher cannot prove binary reading: skip.
        text = "Pick any value in 5-10 for the seed."
        assert sites_for(text, R6, "binary_minus") == []

    def test_identifier_minus_binary_site(self):
        text = "Then x - 3 is divisible by 7."
        minus = sites_for(text, R6, "binary_minus")
        assert len(minus) == 1

    def test_unary_minus_skipped(self):
        text = "The root is -5 in this branch."
        assert sites_for(text, R6, "binary_minus") == []

    def test_double_star_exponent_skipped(self):
        text = "Evaluate 2**8 first."
        assert sites_for(text, R6) == []

    def test_arrow_skipped(self):
        text = "The edge a->b closes the cycle."
        assert sites_for(text, R6) == []

    def test_comparison_operators_skipped(self):
        text = "Loop while i <= n and j >= 0 and x != y and a == b."
        assert sites_for(text, R6) == []

    def test_code_block_operators_skipped(self):
        text = "```\nx=17\ny = x+1\n```"
        assert sites_for(text, R6) == []

    def test_scientific_notation_minus_skipped(self):
        text = "The tolerance is 1e-5 at most."
        assert sites_for(text, R6) == []


# ---------------------------------------------------------------------------
# Rule 7 — list markers
# ---------------------------------------------------------------------------

class TestListMarkers:
    def test_dash_bullet_site_per_line(self):
        text = "- factor the modulus\n- test each residue"
        sites = sites_for(text, R7)
        assert len(sites) == 2
        assert all(s.matched == "- " for s in sites)
        assert all(set(s.candidates) == {"- ", "* "} for s in sites)

    def test_star_bullet_site(self):
        text = "* first item\n* second item"
        sites = sites_for(text, R7)
        assert len(sites) == 2
        assert all(s.matched == "* " for s in sites)

    def test_numbered_list_no_site(self):
        text = "1. factor\n2. test"
        assert sites_for(text, R7) == []

    def test_indented_bullet_site_glyph_only(self):
        text = "- outer step\n  - inner step"
        sites = sites_for(text, R7)
        assert len(sites) == 2
        inner = [s for s in sites if s.start > 0][-1]
        assert inner.matched == "- "

    def test_code_block_bullet_excluded(self):
        text = "```\n- not a list, a diff line\n```"
        assert sites_for(text, R7) == []

    def test_mid_line_dash_not_a_bullet(self):
        text = "The interval - open at both ends - is short."
        assert sites_for(text, R7) == []


# ---------------------------------------------------------------------------
# Cross-cutting properties
# ---------------------------------------------------------------------------

class TestCrossCutting:
    def test_span_integrity_on_mixed_trace(self):
        text = (
            "First, note the setup. It's an affine map.\n\n"
            "x = 17. Thus, f1(x) = (3*x + 2) mod 97.\n"
            "- reduce the constant\n- verify the residue\n"
            "Then, we cannot skip the check, so the proof stands."
        )
        assert_span_integrity(text)

    def test_no_overlapping_sites_ever_returned(self):
        text = "x = 5. Thus, y = 6. Then, note that it's done.\n- item one\n- item two"
        sites = match_sites(text)
        ordered = sorted(sites, key=lambda s: s.start)
        for a, b in zip(ordered, ordered[1:]):
            assert a.end <= b.start, f"overlap: {a} vs {b}"

    def test_sites_sorted_by_position(self):
        text = "So x = 3 holds. Note that y = 4."
        sites = match_sites(text)
        starts = [s.start for s in sites]
        assert starts == sorted(starts)

    def test_empty_text_no_sites(self):
        assert match_sites("") == []
