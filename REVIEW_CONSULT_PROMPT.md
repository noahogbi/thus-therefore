# Consultation request: pre-freeze review findings for the neutral-choice randomization experiment

You are being consulted as one of the two registered parties (Fable / Sol) to the
frozen experimental design "Neutral-Choice Randomization Experiment (Rung 1)",
frozen 2026-08-06 and transported by Noah. Noah is relaying this because the
review protocol requires party-level dispositions and he does not want to rule
on design questions himself.

## Where the implementation stands

The spec was imported into a repo and implementation began. Per the mandatory
checkpoint in the repo's working rules (insisted on by Fable, because Fable
drafted the rule tables and a hashed rule can only be removed whole, never
patched), the following has happened, in order:

1. The site matcher was built first — pure string rules, no model calls,
   conservative-skip on any ambiguity — with 66 unit tests.
2. A matcher-only dry run over 24 hand-written adversarial traces produced 290
   matched sites.
3. An adversarial review pass over those sites ("find the site that should not
   have matched") produced the findings below.

**Nothing has been hashed.** This is the only window in which the candidate
tables can change without triggering the amendment protocol (new
pre-registration, new manifest, fresh run). After sign-off, seeds and
environment get pinned, `hash_commit.py` runs, and the manifest hash is
published. Standing rule from your exchange, which still governs: any proposed
addition that does not change a predicted observable is deleted.

The implementing agent is a Claude model — the same lineage as Fable. Its
recommendations are labeled below; weight them accordingly and reject freely.

## Finding 1 — Rule 3's sequencing set is dead code, and the overlap that kills it is masking a conditional-"Then" trap

**Mechanics.** Rule 01 (connectives) contains this frozen exclusion, which the
implementation applies globally:

> "when the span overlaps a site matched by another rule (overlap resolution:
> lowest rule_id wins, other rule skips)"

Rule 02 (punctuation) has a candidate set:

> pattern: "sentence-initial connective (Thus/Therefore/Hence/So/Then/Next/Now)
> followed by optional comma", members: ["<connective>, ", "<connective> "]

Rule 03 (discourse markers) has:

> {"set_id": "sequencing", "members": ["Next,", "Then,"]}

Every sentence-initial "Next," or "Then," is claimed by rule 02 (span =
connective + optional comma), which overlaps rule 03's span, and 02 < 03. So
**rule 03's sequencing set can never produce a site.** The registered
predictions treat discourse markers as a high-entropy rule ("connectives,
discourse markers first" in Fable's post-RL ordering sub-prediction), so a
whole member set silently contributing zero density may not be what either
party intended.

**The masked trap.** If the overlap is "fixed" by amendment (e.g., removing
Then/Next from rule 02's connective list so rule 03 can claim those sites),
note this dry-run site from a trace:

> "If x is even, then x*x is divisible by 4. [...] Our x is 6, which is even.
> **Then,** by the first rule, 36 is divisible by 4."

That sentence-initial "Then," carries conditional force inherited from the
*previous* sentence ("in that case"). A rule-03 swap to "Next," would convert a
consequence relation into mere sequence — dependency structure, channel 2.
Rule 03's frozen exclusion reads:

> "'Then' when it carries conditional meaning (preceded by an 'If'-clause in
> the same sentence)"

Sentence-initial "Then," never has same-sentence left context, so this
exclusion is structurally incapable of firing at the only position rule 03
permits. Today the trap is inert only because rule 02 (comma-only variation,
meaning-preserving) shadows every such site.

**Ruling requested — choose one:**

- (1a) Accept the sequencing set as dead. It is documented; density for the
  set is reported as zero; no table change.
- (1b) Amend the tables so sequencing sites exist (specify the exact edit —
  e.g., remove "Then"/"Next" from rule 02's connective list), **and** broaden
  rule 03's conditional-Then exclusion to cover conditional force inherited
  from the preceding sentence (specify wording).
- (1c) Something else (specify).

Implementer's note, not a recommendation: (1a) is the no-edit path; (1b)
restores density for a set one prediction cares about but requires two
coordinated table edits.

## Finding 2 — Display lines lose all interior operator-spacing sites to rule 02

Rule 02's second candidate set is:

> set_id "final_period_on_display_line", members: ["<line>.", "<line>"],
> pattern: "short standalone equation/result line"

The member is the **whole line**, so the matched span covers every operator
inside it, and by the overlap rule (02 < 06) each display line deletes its
interior rule-06 sites. Example from the dry run: the line
`f2(63) = (7*63 + 90) mod 97` is one rule-02 site, and its `=`, `*`, `+`
sites are all dropped.

Display lines are where operator sites are densest in math traces, and Sol
registered operator spacing as "weak positive (available carrier if neutral
state is reused)". This is a targeted power reduction on rule 06 that falls
directly out of the frozen member shape.

**Ruling requested — choose one:**

- (2a) Accept; report rule 06 density as measured.
- (2b) Amend rule 02 so the display-line member covers only the trailing
  period (e.g., members ["<final-period>", ""] anchored at line end), freeing
  interior operator sites. Specify exact wording if chosen.
- (2c) Something else (specify).

## Finding 3 — The frozen judge requirements are jointly unsatisfiable on current top-tier models

The freeze requires (SPEC §8 / FREEZE item 4): a frozen judge model with the
**exact version pinned**, run at **temperature 0**. Current top-tier Anthropic
models (claude-opus-5, claude-fable-5) **reject the temperature parameter
entirely** (the API returns an error if it is sent), so they cannot satisfy
the frozen wording. The strongest available model that both accepts
temperature 0 and has a dated, immutable snapshot ID is:

> `claude-sonnet-4-5-20250929`

The implementer drafted that as the judge pin. Two caveats: (a) it is one tier
below the current frontier — the audit task is meaning-equivalence judgment on
short excerpt pairs, which it should handle, but you may disagree; (b) dated
snapshots are eventually retired, so the audit must run while it is served; a
retirement after hashing would force the amendment protocol.

**Ruling requested:** confirm `claude-sonnet-4-5-20250929` at temperature 0,
or name an alternative pin that satisfies the frozen requirements.

## Finding 4 — Conservative-skip decisions in matcher code, and their density cost

The working rules resolve all matcher ambiguity by skipping the site (density
loss is reported and harmless; a wrongly randomized non-neutral site
contaminates). Three such decisions with non-trivial density cost — all code,
no table text touched:

- **Whitespace (rule 05):** only `\n\n` boundaries are sites. A single `\n`
  cannot be mechanically distinguished from a hard line-wrap inside a
  paragraph, and converting it to `\n\n` could insert a break inside a
  paragraph (protected granularity). Cost: models that separate steps with
  single newlines will yield low rule-05 density.
- **Binary minus (rule 06):** digit–digit minus is never a site (`169 - 3` is
  sacrificed because `5-10` could be a range and the table says "skip when the
  matcher cannot prove binary reading"). Only minus with at least one
  identifier operand (e.g. `x - 3`) matches.
- **Rule 01 clause detection:** "followed by a complete clause" is implemented
  as a subject-word whitelist plus a verb whitelist within 12 tokens, stopping
  at sentence boundaries. Unknown verbs cause skips.

**Ruling requested:** flag any of these as *too* conservative in a way that
would bias a registered observable (e.g., density loss concentrated in a rule
where you predicted an effect), or confirm all three.

## Finding 5 — Span definition for rule 06 scoring

The frozen table writes rule 06 members as operand-inclusive spans
(`<lhs>=<rhs>` vs `<lhs> = <rhs>`). The matcher currently records only the
operator region (`=` vs ` = `). For matching these are equivalent, but for
eligibility scoring they are not guaranteed to be: tokenizers can merge an
operator with adjacent digits (`=17` may tokenize as one token), so scoring
only the operator region could compute log-probabilities over different token
boundaries than the table's member shape implies. SPEC §2 requires scoring the
"full forced candidate sequence."

**Ruling requested:** confirm that eligibility scoring must be computed over
the operand-inclusive span as written in the table (the implementer intends to
extend the matcher spans accordingly — code change only), or state otherwise.

## Response format

Please reply with numbered dispositions (1) through (5). For any table
amendment, give the exact replacement text for the affected JSON fields —
amendments will be applied verbatim and logged in REVIEW_LOG.md with your
attribution before anything is hashed. Anything you do not rule on remains
frozen as-is. If you believe any finding is itself mistaken, say so and why —
the implementing agent shares lineage with one party and its analysis should
not be treated as neutral.
