# Freeze Mechanics (per SPEC section 10)

1. Complete candidate tables and contextual matching rules are hash-committed —
   the tables themselves, not prose descriptions.
2. Tokenizer AND decoding implementation are pinned in environment.json
   (model version alone is insufficient: the experiment is tokenizer-level).
3. Delta = 1.5 natural-logit units, frozen in SPEC. No length normalization.
4. Judge: frozen model version, frozen prompt, temperature 0. Human audit blinded
   to outcome and condition; two raters on disagreements.
5. Audit sample drawn BEFORE outcome analysis; audit_sample_seed committed in
   seeds.json first.
6. Per-rule intervention density (eligible sites / 1,000 generated tokens) is
   reported for every rule. Low-density valid runs are reported with power, not
   discarded.
7. Validation failure is RULE-LEVEL: a rule scoring < 98% on the five-property
   audit is removed entirely and the experiment rerun under a new manifest.
   No example-level excision, ever.
8. Amendments of any kind = new pre-registration + new manifest + fresh run.
   No edits to a live experiment.

Run `python scripts/hash_commit.py  # PRIOR_ART.md and writeup/ are non-frozen context` from repo root after filling seeds.json and
environment.json. The printed manifest_hash is the experiment's identity. Publish
it (commit, gist, or timestamped post) before the first generation run.
