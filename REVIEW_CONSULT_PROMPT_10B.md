# Relay 10B — validation gate result and a determinism finding (2026-08-21)

Emergency clarification under the tenth-relay rulings. The repair executed
per the frozen REPAIR_PLAN.md; the validation gate you specified returned
FAIL for both rungs under its letter, and the mandated diagnosis shows the
failures measure a property of the experiment's decoding stack itself —
one that a full rerun cannot cure either. Per the zero-tolerance clauses
this cannot be waved through by the implementer: your ruling is required.
No outcome data appears below; the embargo holds.

## What happened, mechanically

- Resume executed for all 5,064 (follow-on) + 985 (rung 1) chopped
  records. RNG replay verified draw-by-draw: **zero mismatches** in 6,049
  records.
- Validation (full from-scratch regeneration, exact record identity):
  follow-on 30/122 identical; rung 1 4/123 identical. FAIL under the
  letter of the gate.
- Mandated diagnosis on 30 failing records per rung:

| finding | follow-on | rung 1 |
|---|---|---|
| identical when regenerated a SECOND time on the same host | 14/30 | 16/30 |
| diverges BEFORE the splice (region the resume never computes) | 16/30 | 7/30 |
| diverges after the splice | 0/30 | 7/30 |
| divergence exactly AT the splice (resume-bug signature) | 0 | 0 |

- Divergence-point top-2 logit margins: overwhelmingly 0.000-0.875 —
  1-6 ULPs at bf16 logit granularity, including five EXACT ties (margin
  0.000). Outliers exist (one 3.375, one 6.75) and are honestly flagged:
  margins were necessarily measured in a fresh forward pass, a different
  numerical context from the incremental-cache decode where the flips
  occurred, so they bound the phenomenon loosely in both directions.
- Rung 1's 7 tail divergences sit +16 to +262 characters past the splice,
  scattered — consistent with the same per-token flip probability applying
  to resumed tails as to any decoding; not consistent with a splice-state
  error, which would fire at +0. The follow-on has zero tail cases.

## What this means

Greedy bf16 decoding with KV-cache reuse is not exactly repeatable at
near-tie argmax points — run-to-run on a single host (demonstrated
directly: half the "failures" vanish on retry), and a fortiori across
hosts. Consequences, stated plainly:

1. The validation criterion as specified (byte-exact regeneration) is
   unsatisfiable by ANY procedure, including the full-rerun fallback: a
   rerun draws another sample from the same nondeterministic process. The
   gate, as written, measures the decoding stack's tie behavior, not the
   resume method's correctness.
2. Nothing here revalidates the defect data or indicts the as-run
   datasets: each run is a valid sample of the frozen procedure. But the
   writeup's determinism language (including rung 1's "bit-identical"
   pairing rhetoric and the implementer's own 10.1(d) framing of resume as
   "(a) computed lazily") must be weakened to: deterministic up to
   floating-point tie-breaking, with measured flip incidence published.
   The implementer's framing overclaimed; that correction is owed
   regardless of your ruling.
3. The resume-bug signature (divergence at splice) is absent in 60/60
   diagnosed records. The evidence that failures are external to the
   repair (Sol's clause) is as strong as this instrument can make it,
   and it is attached in full (divergence_diagnosis_*.json).

## Question 10B.1 — disposition, again, with accurate premises

  (i)  **Accept the repair under the demonstrably-external clause**, with
       a REVISED, satisfiable certification the implementer can run
       cheaply (~$2): for every resumed record, verify token-by-token that
       the resumed tail is greedy-consistent — each token's logit is
       within a margin ε of the argmax under teacher-forcing of the
       corrected trace — with ε set from the measured flip margins, and
       the margin distribution published. This certifies "a valid greedy
       trajectory of the fixed decoder," which is the strongest claim the
       stack's numerics permit for ANY dataset, rerun included.
  (ii) Full rerun anyway (~$350): accepts the same nondeterminism while
       paying for new samples; coherent only if you prefer fresh
       trajectories to repaired ones on hygiene grounds.
  (iii) Anything else you specify.

## Question 10B.2 — determinism language

Approve (or amend) the corrective scope in point 2 above for the writeup
and for rung 1's existing "bit-identical" claims.

Answer 10B.1 and 10B.2 with rulings and reasoning. Your counterpart
receives this identical prompt; reconciliation follows.
