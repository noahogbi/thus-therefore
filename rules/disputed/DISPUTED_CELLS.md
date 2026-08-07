# Disputed Cells — Separate Experimental Arms

Per SPEC section 5. Each cell runs as its own arm with its own hash. Results are
NEVER averaged into Tier A aggregates, including in any later analysis. Both parties'
sign predictions were registered before any run.

| # | Cell | Intervention sketch | Fable registered | Sol registered |
|---|------|--------------------|------------------|----------------|
| D1 | Intra-sentence independent-conjunct reordering | "A and B" -> "B and A" where A,B provably order-independent (no anaphora crossing, no computational dependency) | weak + penalty, FLAT depth interaction | + penalty, + depth (interpreted as schedule sensitivity, not covert state) |
| D2 | Sentence merge/split | Join two steps with "and"/semicolon, or split one compound step — granularity change only, content identical | + penalty, FLAT depth | + penalty, + depth (not covert state per se) |
| D3 | Pronominalization | "x" <-> "this value" / "that result" where referent unambiguous | + penalty, FLAT depth (anaphora cost) | + penalty, weak-moderate + depth (representational/attention sensitivity) |
| D4 | Digit <-> word numerals | "17" <-> "seventeen" | + penalty, **+ depth** — the ONE cell where Fable predicts depth-scaling on base models (arithmetic-circuit degradation compounding serially) | + penalty, + depth (representational sensitivity unless later evidence ties it to encoded state) |

D4 is the built-in demonstration that a positive depth interaction alone proves
neither hypothesis — which is exactly why disputed cells stay out of every aggregate.

Candidate tables for D1–D4 are NOT yet frozen. They require the same treatment as
Tier A (finite, local, tokenizer-deterministic matchers, hash-committed) before their
arms run. Tier A runs first; disputed arms are follow-on work.
