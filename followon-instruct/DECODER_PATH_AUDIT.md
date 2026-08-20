# Decoder mutation-path audit (Fable's tenth-relay precondition iv)

One frozen semantic was violated (terminal-pass regeneration), so every
path that mutates decoder state was re-audited against the frozen
splice-and-regenerate semantics. Path -> verdict -> pinning test.

| # | Path | Verdict | Test |
|---|---|---|---|
| 1 | Greedy append (native + between sites) | correct | test_native_greedy_reproduces_script; HF bit-identity replay (native arms, both pins) |
| 2 | Terminal detection, frozen single-EOS | correct | test_without_terminal_ids_attribute_behavior_is_frozen |
| 3 | Terminal detection, 8.1(b) terminal set | correct | test_extra_terminal_token_stops_generation |
| 4 | max_tokens budget | correct | test_max_tokens_budget_respected |
| 5 | Mid-gen intervene: splice + regenerate | correct | test_uniform_sample_among_eligible_and_splice |
| 6 | Mid-gen keep (chosen == matched): tail kept | correct | test_choosing_the_native_candidate_keeps_the_tail |
| 7 | Mid-gen skip (<2 eligible): no mutation | correct | test_fewer_than_two_eligible_skips |
| 8 | Frontier monotonicity (site decided once) | correct | test_site_decided_exactly_once |
| 9 | Prompt-region sites never decided | correct | test_prompt_sites_never_decided |
| 10 | Lookahead deferral of unconfirmed sites | correct | test_initiation_set_deferred_by_decoder |
| 11 | Per-rule arm filtering | correct | test_rules_subset_restricts_interventions |
| 12 | **Terminal-pass intervene: regenerate** | **was DEFECTIVE, fixed** | test_terminal_pass_substitution_regenerates_tail (new) |
| 13 | Terminal-pass keep: tail preserved | correct | test_terminal_pass_keep_choice_preserves_tail (new) |
| 14 | Terminal-pass skip: generation still ends | correct | test_terminal_pass_skip_does_not_resume (new) |
| 15 | KV cache vs naive path equivalence | correct | test_kv_cache_* (3 tests) + truncate-swap-reencode probe (79 splits, 0 mismatches) |

Also re-verified during diagnosis: canonical re-encode after splice is the
same operation in from-scratch and resumed decoding (basis of the 10.1(d)
state-equivalence argument), and the density/skip-count formulas read only
site records, which the defect did not corrupt.

Conclusion: the defect was confined to path 12's missing `ended` reset.
Suite: 15 decoder tests, 137 total, all passing at the repair freeze.
