"""Tenth-relay repair: deterministic resume-and-complete of chopped records.

Unanimous ruling 10.1(d) with both parties' preconditions (REVIEW_LOG tenth
reconciliation). Frozen before execution; the executing commit hash is
recorded in REPAIR_PLAN.md. Original datasets are read-only inputs;
corrected datasets are written to new directories with per-record
provenance. Zero tolerance: any RNG-replay mismatch or any failed
byte-identity validation record fails the method for that rung (automatic
full-rerun fallback).

Subcommands (run in order):
  sweep     CPU  Programmatic defect-signature census of EVERY randomized
                 record (Fable iii). Writes chop_census.json.
  plan      CPU  Stratified validation sample, >=100 per rung, proportional
                 across arm x cell strata, small strata taken whole (Sol 2).
                 Writes validation_plan.json.
  execute   GPU  RNG-replay (verified draw-by-draw) + resume the FIXED
                 decoder from the logged splice prefix for every chopped
                 record; copy non-chopped records verbatim. Writes corrected
                 dataset + repair_report.json.
  validate  GPU  Full from-scratch regeneration of every planned validation
                 record via harness.runner.run_problems under the fixed
                 decoder; require exact record identity (text, sites,
                 ended, generated_tokens, answer_extracted, correct,
                 density). Writes validation_report.json.

Rung configs are hard-coded from the frozen manifests: no CLI knobs that
could vary the science.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import random
from collections import defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUNGS = {
    "followon": {
        "grid": "runs/followon/grid",
        "out": "runs/corrected/followon",
        "model_id": "Qwen/Qwen2.5-7B-Instruct",
        "revision": "a09a35458c702b33eeacc393d103063234e8bc28",
        "extra_terminal_tokens": ["<|endoftext|>"],
        "extended_extraction": True,
    },
    "rung1": {
        "grid": "runs/rung1-check/runs",
        "out": "runs/corrected/rung1",
        "model_id": "Qwen/Qwen2.5-7B",
        "revision": "d149729398750b98c0af14eb82c78cfe92750796",
        "extra_terminal_tokens": None,
        "extended_extraction": False,
    },
}
MAX_NEW_TOKENS = 1024
LOOKAHEAD_CHARS = 100
VALIDATION_N = 100
VALIDATION_SEED = "repair-validation:314159"


def randomized_files(cfg: dict) -> list[str]:
    return sorted(glob.glob(os.path.join(REPO, cfg["grid"], "randomized-*", "*.jsonl")))


def load(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def is_chopped(r: dict) -> bool:
    iv = [s for s in r.get("sites", []) if s.get("intervened")]
    if not iv:
        return False
    last = max(iv, key=lambda s: s["start"])
    return r["text"].endswith(last["chosen"]) and \
        len(r["text"]) == last["start"] + len(last["chosen"])


def arm_of(path: str) -> str:
    return os.path.basename(os.path.dirname(path))


def cell_of(path: str) -> str:
    return os.path.basename(path)[:-6]


def cmd_sweep(rung: str) -> None:
    cfg = RUNGS[rung]
    census: dict = defaultdict(lambda: defaultdict(
        lambda: {"records": 0, "touched": 0, "chopped": 0,
                 "chopped_no_answer": 0}))
    for f in randomized_files(cfg):
        arm, cell = arm_of(f), cell_of(f)
        for r in load(f):
            c = census[arm][cell]
            c["records"] += 1
            if any(s.get("intervened") for s in r.get("sites", [])):
                c["touched"] += 1
                if is_chopped(r):
                    c["chopped"] += 1
                    if r["answer_extracted"] is None:
                        c["chopped_no_answer"] += 1
    out = {a: dict(cells) for a, cells in census.items()}
    tot = {k: sum(c[k] for cells in out.values() for c in cells.values())
           for k in ("records", "touched", "chopped", "chopped_no_answer")}
    path = os.path.join(REPO, "runs", "corrected", f"chop_census_{rung}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({"per_arm": out, "total": tot}, open(path, "w", encoding="utf-8"), indent=1)
    print(f"[{rung}] census: {tot} -> {path}")


def cmd_plan(rung: str) -> None:
    census = json.load(open(os.path.join(
        REPO, "runs", "corrected", f"chop_census_{rung}.json"), encoding="utf-8"))
    strata: dict[tuple[str, str], int] = {}
    for arm, cells in census["per_arm"].items():
        for cell, c in cells.items():
            if c["chopped"]:
                strata[(arm, cell)] = c["chopped"]
    total = sum(strata.values())
    n_target = min(VALIDATION_N, total)
    # proportional allocation, minimum 1 per stratum, small strata whole
    alloc = {}
    for key, n in sorted(strata.items()):
        share = max(1, round(n_target * n / total))
        alloc[key] = min(n, share)
    rng = random.Random(f"{VALIDATION_SEED}:{rung}")
    cfg = RUNGS[rung]
    plan = []
    for (arm, cell), k in sorted(alloc.items()):
        f = os.path.join(REPO, cfg["grid"], arm, cell + ".jsonl")
        idx = [i for i, r in enumerate(load(f)) if is_chopped(r)]
        take = idx if len(idx) <= k else sorted(rng.sample(idx, k))
        plan += [{"arm": arm, "cell": cell, "index": i} for i in take]
    path = os.path.join(REPO, "runs", "corrected", f"validation_plan_{rung}.json")
    json.dump({"seed": f"{VALIDATION_SEED}:{rung}", "n": len(plan),
               "strata": {f"{a}/{c}": k for (a, c), k in sorted(alloc.items())},
               "records": plan}, open(path, "w", encoding="utf-8"), indent=1)
    print(f"[{rung}] validation plan: {len(plan)} records "
          f"across {len(alloc)} strata -> {path}")


def make_lm(cfg: dict, device: str = "cuda"):
    from harness.scoring import HFCausalLM
    return HFCausalLM(cfg["model_id"], revision=cfg["revision"],
                      device=device, dtype="bfloat16",
                      extra_terminal_tokens=cfg["extra_terminal_tokens"])


def replay_rng(rec: dict):
    """Rebuild the per-problem RNG positioned after the logged draws,
    verifying every replayed draw against the log (zero tolerance)."""
    from harness.runner import _problem_rng
    rng = _problem_rng(rec["seed"], rec["id"])
    for s in rec["sites"]:
        if s.get("chosen") is not None:
            draw = rng.choice(list(s["eligible"]))
            if draw != s["chosen"]:
                raise RuntimeError(
                    f"RNG replay mismatch on {rec['id']} site@{s['start']}: "
                    f"replayed {draw!r} != logged {s['chosen']!r}")
    return rng


def rules_of(rec: dict) -> set[str] | None:
    ra = rec["rules_arm"]
    return None if ra == "all" else set(ra)


def density_of(sites: list[dict], generated_tokens: int) -> dict[str, float]:
    out: dict[str, float] = {}
    if generated_tokens == 0:
        return out
    for s in sites:
        if len(s["eligible"]) >= 2 and s.get("skip_reason") != \
                "global_exclusion_undecidable_mid_generation":
            out[s["rule_id"]] = out.get(s["rule_id"], 0.0) + 1.0
    return {r: n * 1000.0 / generated_tokens for r, n in out.items()}


def resume_record(lm, rec: dict, cfg: dict) -> dict:
    from harness.decoder import InterventionDecoder
    from harness.runner import extract_answer, extract_answer_extended
    from harness.scoring import EligibilityScorer

    prompt = rec["text"][:rec["prompt_chars"]]
    chopped = rec["text"]
    rng = replay_rng(rec)
    pre_tokens = len(lm.encode(chopped)) - len(lm.encode(prompt))
    remaining = MAX_NEW_TOKENS - pre_tokens
    dec = InterventionDecoder(
        lm=lm, scorer=EligibilityScorer(lm), rng=rng,
        lookahead_chars=LOOKAHEAD_CHARS, intervene=True, rules=rules_of(rec))
    res = dec.generate(chopped, max_new_tokens=max(0, remaining))

    extractor = (extract_answer_extended if cfg["extended_extraction"]
                 else extract_answer)
    text = res.text
    gen_tokens = pre_tokens + res.generated_tokens
    sites = rec["sites"] + [s.to_dict() for s in res.sites]
    extracted = extractor(text[len(prompt):])
    out = dict(rec)
    out.update({
        "text": text,
        "generated_tokens": gen_tokens,
        "ended": res.ended,
        "sites": sites,
        "density": density_of(sites, gen_tokens),
        "answer_extracted": extracted,
        "correct": (extracted is not None
                    and extracted == str(rec["answer_expected"])),
        "repair": {"resumed": True, "original_ended": rec["ended"],
                   "original_len": len(rec["text"]),
                   "resumed_tail_tokens": res.generated_tokens},
    })
    return out


def cmd_execute(rung: str) -> None:
    cfg = RUNGS[rung]
    lm = make_lm(cfg)
    report: dict = {"rung": rung, "resumed": 0, "copied": 0,
                    "per_arm_cell": {}}
    for f in randomized_files(cfg):
        arm, cell = arm_of(f), cell_of(f)
        out_dir = os.path.join(REPO, cfg["out"], arm)
        os.makedirs(out_dir, exist_ok=True)
        n_res = 0
        rows = []
        for r in load(f):
            if is_chopped(r):
                rows.append(resume_record(lm, r, cfg))
                n_res += 1
            else:
                rr = dict(r)
                rr["repair"] = {"resumed": False}
                rows.append(rr)
        with open(os.path.join(out_dir, cell + ".jsonl"), "w",
                  encoding="utf-8") as fo:
            for row in rows:
                fo.write(json.dumps(row) + "\n")
        report["resumed"] += n_res
        report["copied"] += len(rows) - n_res
        report["per_arm_cell"][f"{arm}/{cell}"] = n_res
        print(f"[{rung}] {arm}/{cell}: resumed {n_res}/{len(rows)}")
    json.dump(report, open(os.path.join(
        REPO, "runs", "corrected", f"repair_report_{rung}.json"), "w",
        encoding="utf-8"), indent=1)
    print(f"[{rung}] TOTAL resumed {report['resumed']}, "
          f"copied {report['copied']}")


COMPARE_KEYS = ["text", "generated_tokens", "ended", "sites", "density",
                "answer_extracted", "correct"]


def cmd_validate(rung: str) -> None:
    from harness.runner import run_problems
    cfg = RUNGS[rung]
    plan = json.load(open(os.path.join(
        REPO, "runs", "corrected", f"validation_plan_{rung}.json"),
        encoding="utf-8"))
    lm = make_lm(cfg)
    results = []
    n_fail = 0
    for item in plan["records"]:
        f_orig = os.path.join(REPO, cfg["grid"], item["arm"],
                              item["cell"] + ".jsonl")
        f_corr = os.path.join(REPO, cfg["out"], item["arm"],
                              item["cell"] + ".jsonl")
        orig = load(f_orig)[item["index"]]
        corr = load(f_corr)[item["index"]]
        prob = {"id": orig["id"], "family": orig["family"],
                "depth": orig["depth"], "answer": orig["answer_expected"],
                "prompt": orig["text"][:orig["prompt_chars"]]}
        [scratch] = list(run_problems(
            lm, [prob], mode="randomized", seed=orig["seed"],
            rules=rules_of(orig), max_new_tokens=MAX_NEW_TOKENS,
            lookahead_chars=LOOKAHEAD_CHARS,
            extended_extraction=cfg["extended_extraction"]))
        diffs = [k for k in COMPARE_KEYS if scratch[k] != corr[k]]
        ok = not diffs
        n_fail += (not ok)
        results.append({"arm": item["arm"], "cell": item["cell"],
                        "index": item["index"], "id": orig["id"],
                        "identical": ok, "diff_keys": diffs})
        print(f"[{rung}] {item['arm']}/{item['cell']}#{item['index']}: "
              f"{'OK' if ok else 'FAIL ' + str(diffs)}")
    verdict = "PASS" if n_fail == 0 else "FAIL_FALLBACK_TO_FULL_RERUN"
    json.dump({"rung": rung, "n": len(results), "failures": n_fail,
               "verdict": verdict, "records": results},
              open(os.path.join(REPO, "runs", "corrected",
                                f"validation_report_{rung}.json"), "w",
                   encoding="utf-8"), indent=1)
    print(f"[{rung}] VALIDATION {verdict} "
          f"({len(results) - n_fail}/{len(results)} identical)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sweep", "plan", "execute", "validate"])
    ap.add_argument("--rung", choices=list(RUNGS), required=True)
    args = ap.parse_args()
    {"sweep": cmd_sweep, "plan": cmd_plan,
     "execute": cmd_execute, "validate": cmd_validate}[args.cmd](args.rung)


if __name__ == "__main__":
    main()
