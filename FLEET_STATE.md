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

Allocation below is the REBALANCED one (2026-08-17 ~03:00 UTC), sized to each
pod's measured throughput so all five finish together. No orphans remain.

Second rebalance 2026-08-18 17:10 UTC: pod A's measured rate (~206 rec/hr vs
~318 on B/C/D) made it a 40-hour straggler, so its two unstarted passes moved
to B and C. A now finishes its in-flight aggregate pass and stops early.

| Pod | RunPod ID | IP:port | $/hr | rec/hr | Passes assigned |
|---|---|---|---|---|---|
| A | yqu2uhlc589efy | 213.173.98.23:21527 | 0.74 | 206 | native, agg:271828, agg:161803 |
| B | a4do807wrv5zvm | 213.173.108.135:15394 | 0.74 | 318 | r02_punctuation x3, r01_connectives:271828, r03_discourse:271828, r07_list:271828, agg:141421 |
| C | ww4ts4k9psivos | 213.173.103.151:33857 | 0.74 | 320 | r04_contractions x3, r01_connectives:161803, r03_discourse:161803, r07_list:161803, r05_whitespace:141421 |
| D | yga96zcmur278z | 213.173.110.102:10926 | 0.74 | 308 | r06_operator_spacing x3, r01_connectives:141421, r03_discourse:141421, r07_list:141421 |
| H | ff2uqlt3u4i485 | 38.65.239.10:12108 | 0.34 | 119 | r05_whitespace:271828, r05_whitespace:161803 |

Coverage check: native 1 + aggregate 3 + (r01,r02,r03,r04,r05,r06,r07) x 3
= 25 passes. All assigned. Spend rate $3.34/hr.

Pod E (community) was terminated — broken outbound networking, could not
reach github even forced to IPv4. Its 4 passes were absorbed above.

Pod H is a slow host (117 rec/hr vs ~259 on Secure). Cost per generation is
a wash ($2.91 vs $2.86 per 1000), so it is not wasting money, but it must be
given proportionally less work or it strands the run by days. If H finishes
early, hand it more; do not assume equal pods.

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
- Fleet aggregate 1,102 rec/hr across the five pods.
- Total work ~330 pod-hours for 25 passes / 80,000 generations.
- Measured at 7,363/80,000 done after 6.7h: ~66 more hours and ~$220 more.
  Full-run total ~$245 against the original $150-180 estimate.
- Balance was $149 at 2026-08-17 02:28 UTC; ~45 hours of runway at $3.34/hr.
  Noah topping up ~$100 on the morning of 2026-08-17.

## Completion log

- **Pod A — COMPLETE 2026-08-19 05:21 UTC.** 3 passes (native, agg:271828,
  agg:161803) = 24 cells x 400 = 9,600 records, verified locally (no short
  files). Pulled to runs/followon/podA.tgz, pod TERMINATED 05:25 UTC.
  Its self-stop FAILED as expected ("Runpod config file not found") — caught
  by the monitor within 4 minutes. Expect the same on B, C, D, H: every pod
  must be stopped manually via the API after its results are pulled.

## If pods die (zero balance) — restore procedure

Pod volumes do not survive termination, so a dead pod means re-creating it and
restoring the backup so completed cells are skipped rather than regenerated:

1. Create a replacement pod (see recipe above), note its id/ip/port.
2. Run the bootstrap once with a trivial spec so it clones the repo and
   generates the problem sets, or let step 3 precede the real launch.
3. Push the backup back in BEFORE launching real passes:
   ```bash
   scp -i ~/.ssh/thus_therefore_gpu -P PORT runs/followon/podX.tgz root@IP:/tmp/
   ssh ... "mkdir -p /workspace/thus-therefore/runs && \
            tar xzf /tmp/podX.tgz -C /workspace/thus-therefore/runs"
   ```
4. Launch with that pod's full spec list. run_pass.sh skips any cell whose
   output already has exactly 400 lines; partial cells are redone whole.

Because of this, keeping runs/followon/*.tgz current is the difference
between losing GPU hours and losing data. Re-pull after any long stretch.

## Backups

Completed cells pulled to `runs/followon/pod{A,B,C,D,H}.tgz` (gitignored) at
2026-08-17 ~02:45 UTC. Re-pull periodically — pod volumes die with the pod
and nothing is auto-synced. Command used:
```bash
ssh -n -i ~/.ssh/thus_therefore_gpu -p PORT root@IP \
 "cd /workspace/thus-therefore/runs && tar czf - --exclude=problems \
  \$(ls -d */ | grep -v problems)" > podX.tgz
```

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
