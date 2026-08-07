# Self-review findings for the Step 2 adversarial review

Findings from the implementer's own pass over REVIEW_SITES.md, before Noah's
review. Items 1–2 are mechanical consequences of the frozen tables that the
parties may not have foreseen; they are candidates for pre-freeze table
amendment (the only window where tables can change, per CLAUDE.md Step 3).
Items 3–5 are conservative matcher-code decisions (code is not frozen).

## 1. Rule 3's "sequencing" set can never fire (table interaction)

Rule 2's comma set covers sentence-initial Thus/Therefore/Hence/So/Then/Next/
Now; its span (connective + optional comma + space) always overlaps rule 3's
sequencing members "Next," / "Then,". Overlap resolution is "lowest rule_id
wins", so rule 2 claims every such site and the sequencing set is dead code.
The registered predictions treat discourse markers as a high-entropy rule
("connectives, discourse markers first"), so the parties may want sequencing
sites to exist. Options: accept as frozen-mechanical, or amend a table before
hashing (e.g. exclude Then/Next from rule 2's connective list). NOT decided by
the implementer — flagged for Noah / both parties.

## 2. Display lines lose their operator-spacing sites (table interaction)

Rule 2's "final_period_on_display_line" members are the WHOLE line with and
without the trailing period, so the span covers every operator inside the
line, and rule 2 < rule 6 means each display line kills its interior operator
sites. Display lines are where operator sites are densest, so this reduces
rule 6's power specifically in math-heavy traces. Same disposition options as
item 1.

## 3. Single \n is never a whitespace site (conservative matcher decision)

A lone \n cannot be mechanically distinguished from a hard wrap inside a
paragraph; randomizing it to \n\n could insert a break inside a paragraph,
which rule 5's own note forbids. Only \n\n boundaries are sites. Cost: rule 5
density in single-newline-style traces. Contamination risk avoided: step-
granularity change (protected, channel 2).

## 4. Digit–digit minus is never a site (conservative matcher decision)

"169 - 3" is almost surely binary subtraction, but "5-10" is a range and the
matcher cannot PROVE the reading from local context; the table says skip when
binary is unprovable. Only minus with at least one identifier operand (e.g.
"x - 3") is a site. Cost: binary_minus density in arithmetic traces.

## 5. Rule 1 clause detection is whitelist-based (conservative matcher decision)

"Followed by a complete clause" is implemented as: next word in a subject
whitelist (or a short symbolic token), plus a known verb or '=' within 12
tokens, stopping at sentence-final punctuation. Unknown verbs cause skips
(density loss, never contamination). The verb list lives in harness/matcher.py
and can be extended freely — it is code, not table.
