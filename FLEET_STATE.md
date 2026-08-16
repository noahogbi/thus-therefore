# FLEET_STATE.md — live follow-on main run (started 2026-08-16 19:12 UTC)

Operational scratch file, not an experimental artifact. Updated as the run
proceeds so any session (or a session after a crash) can resume without
reconstructing state. Delete after results are collected.

## Ruling being executed

Ninth relay 9.1(c) union grid, n=400, 8 cells:
reachability d2/d4/d6/d8/d10, multiplication d2, composition d2/d4.
Measurement per 8.1(b): `--extended-extraction --extra-terminal-token <|endoftext|>`.
Model pin: Qwen/Qwen2.5-7B-Instruct rev a09a35458c702b33eeacc393d103063234e8bc28.
Task generation seed 2026. Intervention seeds 271828 / 161803 / 141421.

## Pods (SSH key: ~/.ssh/thus_therefore_gpu, user root)

| Pod | RunPod ID | IP:port | $/hr | Passes assigned |
|---|---|---|---|---|
| A | yqu2uhlc589efy | 213.173.98.23:21527 | 0.74 | native, agg x3 seeds |
| B | a4do807wrv5zvm | 213.173.108.135:15394 | 0.74 | r02_punctuation x3, r01_connectives:271828 |
| C | ww4ts4k9psivos | 213.173.103.151:33857 | 0.74 | r04_contractions x3, r01_connectives:161803 |
| D | yga96zcmur278z | 213.173.110.102:10926 | 0.74 | r06_operator_spacing x3, r01_connectives:141421 |
| H | ff2uqlt3u4i485 | 38.65.239.10:12108 | 0.34 | r05_whitespace x3, r07_list_markers:161803, :141421 |

Assigned: 21 of 25 passes. Spend rate $3.34/hr.

**ORPHANED — NOT YET ASSIGNED (4 passes):**
`randomized:tier_a_03_discourse_markers` x {271828, 161803, 141421}
`randomized:tier_a_07_list_markers:271828`
These were on pod E (community, terminated: broken outbound networking —
could not reach github even forced to IPv4). They must be run before the
grid is complete. Assign to a new pod, or to the first pod that finishes.

## Launch pattern (reuse verbatim)

```bash
ssh -n -i ~/.ssh/thus_therefore_gpu -p PORT root@IP \
  "curl -4 -sfL https://raw.githubusercontent.com/noahogbi/thus-therefore/master/scripts/fleet_bootstrap_followon.sh -o /workspace/bs.sh; \
   setsid nohup bash /workspace/bs.sh POD_ID SPEC [SPEC...] < /dev/null > /workspace/fleet.log 2>&1 & echo started"
```
Specs are `MODE:RULES:SEED` (e.g. `native:-:271828`, `randomized:all:161803`,
`randomized:tier_a_02_punctuation:271828`). Idempotent: completed cells are
skipped, a partially written cell is redone whole.

## Traps hit this run (do not rediscover)

1. **SSH hangs unless stdin is detached.** Use `-n` on ssh AND `< /dev/null`
   on the backgrounded command, and do NOT append `sleep`/`echo` after `&`.
2. **`pkill -f bootstrap.sh` kills the SSH wrapper itself** (its own command
   line contains the pattern). Use bracket patterns (`'bootstra[p]'`,
   `'harness.runn[e]r'`, `'run_pas[s]'`) AND put the kill in a separate ssh
   call from the relaunch. Same hazard applies to `pgrep -c -f` — counts
   include the wrapper, so use `ps -eo args | grep -cE 'pattern[x]'`.
3. **Community pods: IPv6-only DNS with dead IPv6 routing.** Append
   `precedence ::ffff:0:0/96  100` to /etc/gai.conf and use `curl -4`.
   One community pod (E) had no working egress at all and was terminated.
4. **Community capacity is scarce** — 2 of 10 creation attempts succeeded.
   Secure is what reliably deploys, at 2.2x the price.
5. **Pod self-stop via runpodctl is unreliable** (container resets wipe its
   config). Verify EXITED via the API; stop manually if needed.

## Throughput / cost, measured (not estimated)

- ~4.3-4.7 records/min/pod on reachability-d2; native and randomized arms
  run at the same rate.
- Mean 643 generated tokens on reachability-d2, 33% of generations hitting
  the 1024-token cap. The instruct checkpoint is far more verbose than the
  rung 1 base checkpoint — this is why the original $150-180 estimate was
  low. Deeper cells will average higher.
- Total work ~330 pod-hours for 25 passes / 80,000 generations.
- Projected total cost ~$205-225 on the current mix; ~2.5 days wall-clock
  for the 21 assigned passes.

## Sanity check already done

Pod A native reachability-d2: 0.796 correct over first 49 records, against
calibration's 0.925 (n=40, different problem set). Within sampling noise
(~1.8 SE); harness behaving as expected. NOT to be treated as a result —
the frozen analysis runs post-hoc over complete cells.

## After the run (do not skip)

1. Collect `runs/` from every pod before terminating it (volumes die with
   the pod). Nothing is auto-synced.
2. Judge determinism gate per writeup/watermarking_context.md section 5:
   re-run JUDGE_SMOKE_TEST.json before the audit phase.
3. Then audit (blinded, seed 314159), then O1/O2 analysis per RUNBOOK.
