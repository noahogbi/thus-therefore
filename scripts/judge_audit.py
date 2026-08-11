"""Run the frozen post-hoc audit (SPEC section 8).

Judges the blinded excerpt pairs produced by harness.audit against the
pinned judge in environment.json, at temperature 0 with thinking omitted.
Verdicts are written raw; joining to provenance happens separately, so the
judging step itself never sees rule identity.

Usage:
    python scripts/judge_audit.py --items runs/audit_items.jsonl \
        --out runs/audit_verdicts.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor

import anthropic

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_print_lock = threading.Lock()


def load_env() -> dict:
    with open(os.path.join(REPO, "environment.json"), encoding="utf-8") as f:
        return json.load(f)


def judge_one(client, template: str, model: str, temperature: float,
              item: dict) -> dict:
    prompt = (template
              .replace("{original}", item["original"])
              .replace("{modified}", item["modified"])
              .replace("{span_before}", item["span_before"])
              .replace("{span_after}", item["span_after"]))
    last_err = None
    for attempt in range(4):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=300,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            text = next((b.text for b in resp.content if b.type == "text"), "")
            row = {
                "audit_id": item["audit_id"],
                "served_model": resp.model,
                "stop_reason": resp.stop_reason,
                "raw": text,
            }
            try:
                row["verdict"] = json.loads(text.strip())
            except json.JSONDecodeError:
                row["verdict"] = None
                row["parse_error"] = True
            return row
        except Exception as e:  # noqa: BLE001 - retry on any transport error
            last_err = e
    return {"audit_id": item["audit_id"], "error": str(last_err),
            "verdict": None}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    env = load_env()
    model = env["judge_model_id"]
    temperature = env["judge_temperature"]
    with open(os.path.join(REPO, "judge", "judge_prompt.txt"), encoding="utf-8") as f:
        template = f.read()

    items = [json.loads(l) for l in open(args.items, encoding="utf-8") if l.strip()]
    print(f"judging {len(items)} items with {model} @ temperature {temperature}")

    client = anthropic.Anthropic()
    done = [0]

    def work(item):
        row = judge_one(client, template, model, temperature, item)
        with _print_lock:
            done[0] += 1
            if done[0] % 50 == 0:
                print(f"  [{done[0]}/{len(items)}]")
        return row

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        rows = list(ex.map(work, items))

    rows.sort(key=lambda r: r["audit_id"])
    with open(args.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    ok = sum(1 for r in rows if r.get("verdict"))
    print(f"wrote {len(rows)} verdicts -> {args.out} ({ok} parsed cleanly)")


if __name__ == "__main__":
    main()
