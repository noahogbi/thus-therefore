"""11.2(b) trace-position decomposition — outcome-blind, descriptive.

Blessed by both parties (eleventh relay); PRIORITY per Fable, whose 11.1
scoring is conditioned on it. For every candidate site (>=2 eligible) and
every realized intervention in the corrected randomized arms: normalized
character position, absolute token position, token distance to
termination, and (where mechanically identifiable) whether the site falls
before/within/after the final explicit reasoning step. No correctness
fields are read anywhere in this script.

Also emits the specific contrast Fable's condition names: the position
profile of AGGREGATE-arm interventions in follow-on reachability d6/d8
versus (i) the same arm's other cells and (ii) per-rule arms in the same
cells — testing "late-trace intervention pileup near answer statements."

Usage: python scripts/position_decomposition.py --rung followon
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from scripts.repair_resume import RUNGS, load  # noqa: E402

TOKENIZERS = {
    "followon": ("Qwen/Qwen2.5-7B-Instruct", "a09a35458c702b33eeacc393d103063234e8bc28"),
    "rung1": ("Qwen/Qwen2.5-7B", "d149729398750b98c0af14eb82c78cfe92750796"),
}
FINAL_STEP_RE = re.compile(
    r"(ANSWER\s*:|\\boxed\{|[Tt]he (?:final )?(?:answer|product|result|sum) is)")


def bucket(x: float) -> str:
    return f"{min(int(x * 10), 9) / 10:.1f}"


def main() -> None:
    from transformers import AutoTokenizer

    ap = argparse.ArgumentParser()
    ap.add_argument("--rung", choices=list(RUNGS), required=True)
    args = ap.parse_args()
    cfg = RUNGS[args.rung]
    mid, rev = TOKENIZERS[args.rung]
    tok = AutoTokenizer.from_pretrained(mid, revision=rev)

    stats: dict = {}
    for f in sorted(glob.glob(os.path.join(REPO, cfg["out"], "*", "*.jsonl"))):
        arm = os.path.basename(os.path.dirname(f))
        cell = os.path.basename(f)[:-6]
        key = f"{arm}/{cell}"
        s = stats.setdefault(key, {
            "opportunities": 0, "interventions": 0,
            "iv_norm_pos_hist": {}, "opp_norm_pos_hist": {},
            "iv_tok_dist_to_end": [], "iv_final_step_region":
                {"before": 0, "within_or_after": 0}})
        for r in load(f):
            if r.get("repair", {}).get("excluded_after_exceedance"):
                continue
            text = r["text"]
            p0 = r["prompt_chars"]
            gen_len_chars = max(len(text) - p0, 1)
            # char->token map lazily only for intervened records (cost)
            enc = None
            m = FINAL_STEP_RE.search(text[p0:])
            final_step_char = (p0 + m.start()) if m else None
            for site in r.get("sites", []):
                if len(site.get("eligible", [])) < 2:
                    continue
                rel = (site["start"] - p0) / gen_len_chars
                s["opportunities"] += 1
                b = bucket(rel)
                s["opp_norm_pos_hist"][b] = s["opp_norm_pos_hist"].get(b, 0) + 1
                if not site.get("intervened"):
                    continue
                s["interventions"] += 1
                s["iv_norm_pos_hist"][b] = s["iv_norm_pos_hist"].get(b, 0) + 1
                if enc is None:
                    enc = tok(text, return_offsets_mapping=True,
                              add_special_tokens=False)
                offs = enc["offset_mapping"]
                tok_idx = next((i for i, (a, b2) in enumerate(offs)
                                if a <= site["start"] < b2), len(offs) - 1)
                s["iv_tok_dist_to_end"].append(len(offs) - tok_idx)
                if final_step_char is not None:
                    region = ("before" if site["start"] < final_step_char
                              else "within_or_after")
                    s["iv_final_step_region"][region] += 1

    # summarize distance lists
    for key, s in stats.items():
        d = sorted(s.pop("iv_tok_dist_to_end"))
        if d:
            s["iv_tok_dist_to_end_summary"] = {
                "n": len(d), "min": d[0],
                "p25": d[len(d) // 4], "median": d[len(d) // 2],
                "p75": d[3 * len(d) // 4], "max": d[-1]}
        else:
            s["iv_tok_dist_to_end_summary"] = {"n": 0}

    path = os.path.join(REPO, "runs", "corrected",
                        f"position_decomposition_{args.rung}.json")
    json.dump(stats, open(path, "w", encoding="utf-8"), indent=1)
    print(f"wrote {path}")

    # Focused contrast for Fable's condition (follow-on only)
    if args.rung == "followon":
        def profile(key):
            s = stats.get(key)
            if not s or not s["interventions"]:
                return None
            h = s["iv_norm_pos_hist"]
            n = sum(h.values())
            late = sum(v for k, v in h.items() if float(k) >= 0.8) / n
            med = s["iv_tok_dist_to_end_summary"].get("median")
            reg = s["iv_final_step_region"]
            regn = reg["before"] + reg["within_or_after"]
            return {"n": n, "frac_in_last_20pct": round(late, 3),
                    "median_tok_to_end": med,
                    "frac_before_final_step":
                        round(reg["before"] / regn, 3) if regn else None}
        focus = {}
        for cell in ["reachability-d6", "reachability-d8", "reachability-d2",
                     "composition-d2", "multiplication-d2"]:
            for seed in ["271828", "161803", "141421"]:
                p = profile(f"randomized-all-s{seed}/{cell}")
                if p:
                    focus.setdefault(cell, {})[f"agg-s{seed}"] = p
            p = profile(f"randomized-tier_a_01_connectives-s271828/{cell}")
            if p:
                focus.setdefault(cell, {})["connectives-s271828"] = p
        fpath = os.path.join(REPO, "runs", "corrected",
                             "position_focus_followon.json")
        json.dump(focus, open(fpath, "w", encoding="utf-8"), indent=1)
        print(json.dumps(focus, indent=1)[:2400])


if __name__ == "__main__":
    main()
