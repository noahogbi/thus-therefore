"""S1 exposure reporting and Proposal A machinery (REVIEW_LOG, fifth relay).

Adopted supplementary reporting — raw O1/O2 remain primary and frozen:

- S1: mean/median/distribution of realized intervened-site counts per
  (family, depth) cell per arm, published beside the frozen density metric,
  descriptive only, never a denominator.
- Proposal A (Sol, double-consented): per-instance
  native_eligible_site_count measured on the deterministic native greedy
  trace (pre-treatment by construction), and a supplementary trace-level
  logistic model
      correct ~ arm + depth + native_count + arm*native_count + arm*depth
  fit within the calibrated reachability grid, per rule and aggregate.
  Native-vs-realized count divergence is published beside it.

The initiation set is excluded from native eligible counts: per IN-1 it is
never randomizable during generation, so it is not intervention
opportunity in Sol's sense.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from typing import Callable, Iterable, Iterator

from harness.decoder import GLOBALLY_EXCLUDED_MID_GENERATION
from harness.matcher import Site, match_sites
from harness.scoring import EligibilityScorer


def native_eligible_counts(records: Iterable[dict], scorer: EligibilityScorer,
                           matcher: Callable[[str], list[Site]] = match_sites,
                           ) -> Iterator[dict]:
    """Per-instance eligible-site counts on native traces (Proposal A)."""
    for rec in records:
        text = rec["text"]
        prompt_chars = rec.get("prompt_chars", 0)
        by_rule: dict[str, int] = defaultdict(int)
        total = 0
        for site in matcher(text):
            if site.start < prompt_chars:
                continue
            if (site.rule_id, site.set_id) in GLOBALLY_EXCLUDED_MID_GENERATION:
                continue
            if scorer.score_site(text, site).intervenable:
                by_rule[site.rule_id] += 1
                total += 1
        yield {
            "id": rec["id"],
            "family": rec.get("family"),
            "depth": rec.get("depth"),
            "native_eligible_total": total,
            "native_eligible_by_rule": dict(by_rule),
        }


def exposure_stats(records: Iterable[dict]) -> dict:
    """S1: realized intervened-site count stats per (family, depth) cell.

    Callers pass one arm's records at a time (arm identity is the caller's
    grouping key)."""
    counts: dict[tuple, list[int]] = defaultdict(list)
    for rec in records:
        k = sum(1 for s in rec.get("sites", []) if s.get("intervened"))
        counts[(rec.get("family"), rec.get("depth"))].append(k)
    out = {}
    for cell, ks in counts.items():
        ks_sorted = sorted(ks)
        n = len(ks_sorted)
        median = (ks_sorted[n // 2] if n % 2 == 1
                  else (ks_sorted[n // 2 - 1] + ks_sorted[n // 2]) / 2)
        out[cell] = {
            "mean": sum(ks_sorted) / n,
            "median": median,
            "distribution": dict(sorted(Counter(ks_sorted).items())),
            "n": n,
        }
    return out


def fit_logistic(xs: list[list[float]], ys: list[int],
                 l2: float = 1e-6, iters: int = 100) -> list[float]:
    """Logistic regression via IRLS with a tiny L2 ridge for stability
    (documented; negligible at these n). Pure python — no new deps."""
    p_dim = len(xs[0])
    beta = [0.0] * p_dim
    for _ in range(iters):
        grad = [0.0] * p_dim
        hess = [[0.0] * p_dim for _ in range(p_dim)]
        for x, y in zip(xs, ys):
            z = sum(b * v for b, v in zip(beta, x))
            z = max(-30.0, min(30.0, z))
            p = 1.0 / (1.0 + math.exp(-z))
            w = max(p * (1.0 - p), 1e-10)
            for i in range(p_dim):
                grad[i] += (y - p) * x[i]
                for j in range(p_dim):
                    hess[i][j] += w * x[i] * x[j]
        for i in range(p_dim):
            grad[i] -= l2 * beta[i]
            hess[i][i] += l2
        step = _solve(hess, grad)
        beta = [b + s for b, s in zip(beta, step)]
        if max(abs(s) for s in step) < 1e-8:
            break
    return beta


def _solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        d = m[col][col]
        if abs(d) < 1e-300:
            d = 1e-300
        m[col] = [v / d for v in m[col]]
        for r in range(n):
            if r != col and m[r][col] != 0.0:
                f = m[r][col]
                m[r] = [v - f * m[col][i] for i, v in enumerate(m[r])]
    return [m[i][n] for i in range(n)]


def proposal_a_rows(randomized: Iterable[dict], native: Iterable[dict],
                    exposure_by_id: dict[str, int]) -> tuple[list[list[float]], list[int]]:
    """Design matrix for the adopted supplementary model. Native rows enter
    with arm=0, randomized with arm=1; exposure is the native-path count of
    the matching problem instance for BOTH arms (pre-treatment)."""
    xs, ys = [], []
    for arm, records in ((0.0, native), (1.0, randomized)):
        for rec in records:
            k = exposure_by_id.get(rec["id"])
            if k is None:
                continue
            depth = float(rec["depth"])
            xs.append([1.0, arm, depth, float(k), arm * float(k), arm * depth])
            ys.append(1 if rec.get("correct") else 0)
    return xs, ys


def main() -> None:
    from harness.runner import load_problems

    ap = argparse.ArgumentParser(
        description="Compute native-path eligible-site counts (Proposal A)")
    ap.add_argument("--model-id", required=True)
    ap.add_argument("--revision", default=None)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--dtype", default="bfloat16")
    ap.add_argument("--native", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    from harness.scoring import HFCausalLM
    lm = HFCausalLM(args.model_id, revision=args.revision,
                    device=args.device, dtype=args.dtype)
    scorer = EligibilityScorer(lm)
    records = [r for p in args.native for r in load_problems(p)]
    with open(args.out, "w", encoding="utf-8") as f:
        for i, row in enumerate(native_eligible_counts(records, scorer)):
            f.write(json.dumps(row) + "\n")
            if (i + 1) % 50 == 0:
                print(f"[{i + 1}/{len(records)}]")
    print(f"wrote {len(records)} exposure rows -> {args.out}")


if __name__ == "__main__":
    main()
