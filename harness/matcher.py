"""Tier A site matcher.

Applies the frozen candidate tables in rules/tier_a/*.json to a text trace and
returns intervention sites as character-offset spans. Tokenizer-deterministic in
the sense required by SPEC section 2: pure string rules, no model calls; the
mapping from char spans to token spans happens later in the eligibility scorer
against the pinned tokenizer.

Conservative-skip principle (CLAUDE.md rule 2): wherever a contextual judgment
is required and the heuristic cannot prove the site qualifies, the location is
not a site. Heuristics here may only under-match relative to the tables, never
over-match.

Overlap resolution (rules/tier_a/01 exclusion list): lowest rule_id wins; the
other rule's site is dropped entirely.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

RULES_DIR = Path(__file__).resolve().parent.parent / "rules" / "tier_a"

R1 = "tier_a_01_connectives"
R2 = "tier_a_02_punctuation"
R3 = "tier_a_03_discourse_markers"
R4 = "tier_a_04_contractions"
R5 = "tier_a_05_whitespace"
R6 = "tier_a_06_operator_spacing"
R7 = "tier_a_07_list_markers"


@dataclass
class Site:
    rule_id: str
    set_id: str
    start: int
    end: int
    matched: str
    candidates: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "set_id": self.set_id,
            "start": self.start,
            "end": self.end,
            "matched": self.matched,
            "candidates": self.candidates,
        }


def _load_rule(name: str) -> dict:
    with open(RULES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


_R1_TABLE = _load_rule("01_connectives.json")["candidate_sets"][0]
R1_MEMBERS = _R1_TABLE["members"]                      # capitalized
R1_MEMBERS_MID = _R1_TABLE["members_mid_sentence"]     # lowercase

# rules/tier_a/02 set comma_after_initial_connective pattern list
R2_CONNECTIVES = ["Thus", "Therefore", "Hence", "So", "Then", "Next", "Now"]

R3_SETS = {s["set_id"]: s["members"] for s in _load_rule("03_discourse_markers.json")["candidate_sets"]}
R4_SETS = {s["set_id"]: s["members"] for s in _load_rule("04_contractions.json")["candidate_sets"]}
R7_GLYPHS = _load_rule("07_list_markers.json")["candidate_sets"][0]["members"]  # ["- ", "* "]


# ---------------------------------------------------------------------------
# Shared context detection
# ---------------------------------------------------------------------------

def _mask_spans(text: str, spans: list[tuple[int, int]]) -> list[bool]:
    mask = [False] * len(text)
    for s, e in spans:
        for i in range(s, min(e, len(text))):
            mask[i] = True
    return mask


def _code_mask(text: str) -> list[bool]:
    spans = []
    # Fenced blocks; an unclosed fence masks to end of text (conservative).
    pos = 0
    while True:
        m = re.search(r"```", text[pos:])
        if not m:
            break
        start = pos + m.start()
        m2 = re.search(r"```", text[start + 3:])
        end = start + 3 + m2.end() if m2 else len(text)
        spans.append((start, end))
        pos = end
    # Inline code.
    for m in re.finditer(r"`[^`\n]+`", text):
        spans.append((m.start(), m.end()))
    return _mask_spans(text, spans)


def _quote_mask(text: str) -> list[bool]:
    spans = [(m.start(), m.end())
             for m in re.finditer(r'"[^"\n]*"|“[^”\n]*”', text)]
    return _mask_spans(text, spans)


def _masked(mask: list[bool], start: int, end: int) -> bool:
    return any(mask[start:end])


def _is_sentence_start(text: str, i: int) -> bool:
    j = i - 1
    while j >= 0 and text[j] in " \t":
        j -= 1
    if j < 0:
        return True
    return text[j] in ".!?\n"


def _after_clause_comma(text: str, i: int) -> bool:
    j = i - 1
    while j >= 0 and text[j] in " \t":
        j -= 1
    return j >= 0 and text[j] == ","


def _line_spans(text: str) -> list[tuple[int, int]]:
    spans, start = [], 0
    for m in re.finditer(r"\n", text):
        spans.append((start, m.start()))
        start = m.end()
    spans.append((start, len(text)))
    return spans


def _line_at(text: str, pos: int) -> str:
    ls = text.rfind("\n", 0, pos) + 1
    le = text.find("\n", pos)
    if le == -1:
        le = len(text)
    return text[ls:le]


_LIST_LINE = re.compile(r"\s*([-*+] |\d+[.)] )")


def _is_structural_line(line: str) -> bool:
    s = line.strip()
    return bool(_LIST_LINE.match(line)) or s.startswith(("```", "#", "|", ">"))


# ---------------------------------------------------------------------------
# Rule 1 — connectives
# ---------------------------------------------------------------------------

# Conservative subject/verb detection for the "complete clause (subject-verb
# detectable within the next 12 tokens)" requirement. Under-matching only.
_SUBJECT_WORDS = {
    "the", "a", "an", "this", "these", "those", "we", "i", "it", "he", "she",
    "they", "you", "one", "each", "every", "all", "both", "some", "any", "no",
    "our", "their", "its", "there", "everything", "nothing", "each",
}
_VERB_WORDS = {
    "is", "are", "was", "were", "be", "been", "being", "has", "have", "had",
    "do", "does", "did", "can", "cannot", "could", "will", "would", "shall",
    "should", "may", "might", "must", "equals", "equal", "gives", "give",
    "gets", "get", "follows", "follow", "holds", "hold", "becomes", "become",
    "yields", "yield", "needs", "need", "remains", "remain", "divides",
    "divide", "reduces", "reduce", "vanishes", "cancels", "applies", "apply",
    "stops", "stop", "stands", "stand", "starts", "start", "ends", "end",
    "lies", "lie", "exists", "exist", "takes", "take", "maps", "map",
    "satisfies", "satisfy", "implies", "imply", "means", "mean", "shows",
    "show", "tells", "tell", "requires", "require", "denotes", "denote",
    "says", "say", "stays", "stay", "grows", "grow", "goes", "go", "works",
    "work", "fails", "fail", "passes", "pass", "counts", "count", "know",
    "see", "obtain", "compute", "conclude", "concludes",
}
_PUNCT_STRIP = ".,;:!?()[]{}\"'"


def _is_symbolic_token(w: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z]\w{0,2}(\(\w*\))?", w) or re.fullmatch(r"\d+", w))


def _clause_follows(rest: str) -> bool:
    words = rest.split()[:12]
    if not words:
        return False
    first = words[0].strip(_PUNCT_STRIP)
    if not first:
        return False
    if first.lower() not in _SUBJECT_WORDS and not _is_symbolic_token(first):
        return False
    for w in words:
        bare = w.strip(_PUNCT_STRIP).lower()
        if bare in _VERB_WORDS or "=" in w:
            return True
    return False


def _match_connectives(text: str, code: list[bool], quote: list[bool]) -> list[Site]:
    sites = []
    pattern = re.compile(
        r"\b(" + "|".join(R1_MEMBERS + R1_MEMBERS_MID) + r")\b"
    )
    for m in pattern.finditer(text):
        word, start, end = m.group(1), m.start(1), m.end(1)
        if _masked(code, start, end) or _masked(quote, start, end):
            continue
        capitalized = word[0].isupper()
        if capitalized:
            if word not in R1_MEMBERS or not _is_sentence_start(text, start):
                continue
            candidates = [word] + [c for c in R1_MEMBERS if c != word]
        else:
            if word not in R1_MEMBERS_MID or not _after_clause_comma(text, start):
                continue
            candidates = [word] + [c for c in R1_MEMBERS_MID if c != word]

        rest = text[end:]
        following = rest.split()
        # 'so that' purpose clause / comparative-degree 'so' (table exclusions).
        if word.lower() == "so" and following:
            nxt = following[0].strip(_PUNCT_STRIP).lower()
            if nxt in {"that", "much", "many", "few", "little"}:
                continue
            if len(following) >= 2 and following[1].strip(_PUNCT_STRIP).lower() == "that":
                continue
        # must_be_followed_by: comma, or a detectable clause. Skip otherwise.
        stripped = rest.lstrip(" ")
        if stripped.startswith(","):
            pass
        elif not _clause_follows(rest):
            continue
        sites.append(Site(R1, "inferential", start, end, word, candidates))
    return sites


# ---------------------------------------------------------------------------
# Rule 2 — punctuation
# ---------------------------------------------------------------------------

def _match_punctuation(text: str, code: list[bool], quote: list[bool]) -> list[Site]:
    sites = []
    # Set A: optional comma after sentence-initial connective. Span includes
    # the connective, optional comma, and one trailing space.
    pat = re.compile(r"\b(" + "|".join(R2_CONNECTIVES) + r")(,?) (?=\S)")
    for m in pat.finditer(text):
        start, end = m.start(), m.end()
        word = m.group(1)
        if _masked(code, start, end) or _masked(quote, start, end):
            continue
        if not _is_sentence_start(text, start):
            continue
        nxt = text[end:].split()
        # Conservative guard for the "comma changes clause attachment"
        # exclusion: 'So that ...' / 'Then that ...' etc. — skip.
        if nxt and nxt[0].strip(_PUNCT_STRIP).lower() == "that":
            continue
        matched = m.group(0)
        with_comma, without = f"{word}, ", f"{word} "
        other = without if matched == with_comma else with_comma
        sites.append(Site(R2, "comma_after_initial_connective",
                          start, end, matched, [matched, other]))

    # Set B: optional final period on a short standalone display line. A line
    # qualifies only if it is symbolic: contains '=', and every alphabetic word
    # of length >= 2 is a known math word. Prose lines never qualify.
    allowed_words = {"mod", "div", "gcd", "lcm", "log", "exp", "min", "max"}
    for ls, le in _line_spans(text):
        line = text[ls:le]
        s = line.strip()
        if not s or len(s) > 60 or "=" not in s:
            continue
        if _masked(code, ls, le):
            continue
        if _is_structural_line(line):
            continue
        if not re.fullmatch(r"[\w\s()+\-*/=%.]+", s):
            continue
        words = re.findall(r"[A-Za-z]{2,}", s)
        if any(w.lower() not in allowed_words for w in words):
            continue
        # Never when the period disambiguates structure: require at most one
        # '.' and only in final position (numeral-internal dots disqualify
        # the site rather than risk a decimal).
        core = s[:-1] if s.endswith(".") else s
        if "." in core:
            continue
        a = ls + (len(line) - len(line.lstrip()))
        b = a + len(s)
        sites.append(Site(R2, "final_period_on_display_line",
                          a, b, s, [s, core if s.endswith(".") else s + "."]))
    return sites


# ---------------------------------------------------------------------------
# Rule 3 — discourse markers
# ---------------------------------------------------------------------------

def _match_discourse(text: str, code: list[bool], quote: list[bool]) -> list[Site]:
    sites = []
    has_enumeration = bool(re.search(r"\b(Second|Third|Fourth|Fifth)\b", text))
    for set_id, members in R3_SETS.items():
        if set_id == "initiation" and has_enumeration:
            # Table exclusion: drop the whole set when the trace enumerates.
            continue
        for member in members:
            for m in re.finditer(re.escape(member), text):
                start, end = m.start(), m.end()
                if _masked(code, start, end) or _masked(quote, start, end):
                    continue
                if not _is_sentence_start(text, start):
                    continue
                candidates = [member] + [c for c in members if c != member]
                sites.append(Site(R3, set_id, start, end, member, candidates))
    return sites


# ---------------------------------------------------------------------------
# Rule 4 — contractions
# ---------------------------------------------------------------------------

def _match_case(member: str, actual_first: str) -> str:
    if actual_first.isupper():
        return member[0].upper() + member[1:]
    return member


def _match_contractions(text: str, code: list[bool], quote: list[bool]) -> list[Site]:
    sites = []
    for set_id, members in R4_SETS.items():
        for member in members:
            other = [c for c in members if c != member][0]
            first = member[0]
            pat = re.compile(
                r"(?<![\w'])[" + first.upper() + first.lower() + r"]"
                + re.escape(member[1:]) + r"(?![\w'])"
            )
            for m in pat.finditer(text):
                start, end = m.start(), m.end()
                if _masked(code, start, end) or _masked(quote, start, end):
                    continue
                matched = text[start:end]
                if set_id == "lets" and not _is_sentence_start(text, start):
                    # Table note: clause-initial hortative only.
                    continue
                sites.append(Site(R4, set_id, start, end, matched,
                                  [matched, _match_case(other, matched[0])]))
    return sites


# ---------------------------------------------------------------------------
# Rule 5 — whitespace
# ---------------------------------------------------------------------------

def _match_whitespace(text: str, code: list[bool]) -> list[Site]:
    sites = []
    for m in re.finditer(r"\n+", text):
        run = m.group(0)
        if len(run) > 2:
            continue  # unusual gap; ambiguous, skip
        start, end = m.start(), m.end()
        if _masked(code, max(0, start - 1), min(len(text), end + 1)):
            continue
        prev_line = _line_at(text, start - 1) if start > 0 else ""
        next_line = _line_at(text, end) if end < len(text) else ""
        if not prev_line.strip() or not next_line.strip():
            continue
        if _is_structural_line(prev_line) or _is_structural_line(next_line):
            continue
        sites.append(Site(R5, "inter_paragraph_gap", start, end, run, [run, "\n" if run == "\n\n" else "\n\n"]))
    return sites


# ---------------------------------------------------------------------------
# Rule 6 — operator spacing
# ---------------------------------------------------------------------------

_OPERAND = re.compile(r"([A-Za-z]\w{0,2}(?:\([^()\s]{0,12}\))?|\d+)$")
_OPERAND_FWD = re.compile(r"^([A-Za-z]\w{0,2}(?:\([^()\s]{0,12}\))?|\d+)")
_OP_SETS = {"=": "equals", "+": "plus", "*": "times", "-": "binary_minus"}


def _match_operators(text: str, code: list[bool]) -> list[Site]:
    sites = []
    for m in re.finditer(r"[=+*-]", text):
        op, pos = m.group(0), m.start()
        if _masked(code, pos, pos + 1):
            continue
        # Two-character operators and arrows: never sites.
        prev_c = text[pos - 1] if pos > 0 else ""
        next_c = text[pos + 1] if pos + 1 < len(text) else ""
        if prev_c in "=+*-<>!" or next_c in "=+*->":
            continue
        # Optional single space each side.
        ls = pos - (1 if prev_c == " " else 0)
        re_ = pos + 1 + (1 if next_c == " " else 0)
        spaced_left = prev_c == " "
        spaced_right = next_c == " "
        if spaced_left != spaced_right:
            continue  # asymmetric spacing: ambiguous formatting, skip
        lhs_m = _OPERAND.search(text[:ls])
        rhs_m = _OPERAND_FWD.match(text[re_:])
        if not lhs_m or not rhs_m:
            continue  # unary or no operands provable
        lhs, rhs = lhs_m.group(1), rhs_m.group(1)
        # Operands must sit on clean boundaries — otherwise the "operand" is a
        # fragment of a larger token (e.g. the 'e' of '1e-5'): skip.
        if lhs_m.start(1) > 0 and (text[lhs_m.start(1) - 1].isalnum() or text[lhs_m.start(1) - 1] == "_"):
            continue
        after = re_ + rhs_m.end(1)
        if after < len(text) and (text[after].isalnum() or text[after] == "_"):
            continue
        if op == "-":
            # Binary reading must be PROVABLE: two numeric operands could be
            # a range (5-10); an operand like '1e' is scientific notation.
            if lhs.isdigit() and rhs.isdigit():
                continue
            if re.fullmatch(r"\d+[eE]", lhs):
                continue
        matched = text[ls:re_]
        spaced, unspaced = f" {op} ", op
        other = unspaced if matched == spaced else spaced
        sites.append(Site(R6, _OP_SETS[op], ls, re_, matched, [matched, other]))
    return sites


# ---------------------------------------------------------------------------
# Rule 7 — list markers
# ---------------------------------------------------------------------------

def _match_list_markers(text: str, code: list[bool]) -> list[Site]:
    sites = []
    for ls, le in _line_spans(text):
        line = text[ls:le]
        m = re.match(r"(\s*)([-*] )(?=\S)", line)
        if not m:
            continue
        start = ls + m.end(1)
        end = ls + m.end(2)
        if _masked(code, start, end):
            continue
        matched = m.group(2)
        other = [g for g in R7_GLYPHS if g != matched][0]
        sites.append(Site(R7, "bullet_glyph", start, end, matched, [matched, other]))
    return sites


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def match_sites(text: str) -> list[Site]:
    if not text:
        return []
    code = _code_mask(text)
    quote = _quote_mask(text)
    all_sites = (
        _match_connectives(text, code, quote)
        + _match_punctuation(text, code, quote)
        + _match_discourse(text, code, quote)
        + _match_contractions(text, code, quote)
        + _match_whitespace(text, code)
        + _match_operators(text, code)
        + _match_list_markers(text, code)
    )
    # Overlap resolution: lowest rule_id wins; within a rule, earlier site wins.
    accepted: list[Site] = []
    for site in sorted(all_sites, key=lambda s: (s.rule_id, s.start)):
        if all(site.end <= a.start or site.start >= a.end for a in accepted):
            accepted.append(site)
    accepted.sort(key=lambda s: s.start)
    return accepted
