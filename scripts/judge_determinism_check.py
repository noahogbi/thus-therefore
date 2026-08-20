"""Judge determinism gate — pre-audit check for the instruct follow-on.

Re-runs the EXACT request recorded in JUDGE_SMOKE_TEST.json (frozen F3
smoke test, 2026-08-08) and compares the raw verdict text byte-for-byte.
Motivated by Anthropic's watermark retrofit of older models announced
2026-08-11 (see writeup/watermarking_context.md section 5): if the serving
stack starts re-settling near-argmax ties with a keyed function, pinned
temperature-0 outputs could drift. Any non-reproduction is an environment
break under FREEZE.md — consult both parties before auditing.

Does NOT modify JUDGE_SMOKE_TEST.json. Writes
followon-instruct/judge_determinism_check.json.

Usage: python scripts/judge_determinism_check.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO = Path(__file__).resolve().parent.parent

# Identical to scripts/judge_smoke_test.py (F3 artifact) by construction.
JUDGE_MODEL = "claude-opus-4-5-20251101"
JUDGE_TEMPERATURE = 0
SAMPLE = {
    "original": (
        "Now add the partial products. The sum is 3760 + 282 = 4042.\n\n"
        "Thus, the product is 4042."
    ),
    "modified": (
        "Now add the partial products. The sum is 3760 + 282 = 4042.\n\n"
        "Therefore, the product is 4042."
    ),
    "span_before": "Thus",
    "span_after": "Therefore",
}


def main() -> int:
    frozen = json.loads((REPO / "JUDGE_SMOKE_TEST.json").read_text(encoding="utf-8"))
    assert frozen["requested_model"] == JUDGE_MODEL

    prompt_template = (REPO / "judge" / "judge_prompt.txt").read_text(encoding="utf-8")
    prompt = (
        prompt_template
        .replace("{original}", SAMPLE["original"])
        .replace("{modified}", SAMPLE["modified"])
        .replace("{span_before}", SAMPLE["span_before"])
        .replace("{span_after}", SAMPLE["span_after"])
    )

    record: dict = {
        "purpose": "Pre-audit judge determinism gate (watermarking_context.md 5.2)",
        "baseline": "JUDGE_SMOKE_TEST.json (2026-08-08)",
        "requested_model": JUDGE_MODEL,
        "temperature": JUDGE_TEMPERATURE,
        "thinking": "omitted",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model=JUDGE_MODEL,
            max_tokens=256,
            temperature=JUDGE_TEMPERATURE,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIStatusError as e:
        record["result"] = "REQUEST_FAILED"
        record["error"] = {"status": e.status_code, "message": str(e.message)}
        out = REPO / "followon-instruct" / "judge_determinism_check.json"
        out.write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(f"GATE FAILED TO RUN: HTTP {e.status_code} — {e.message}")
        print("If the pin is unavailable: no substitution; amendment protocol.")
        return 1

    text = next((b.text for b in response.content if b.type == "text"), "")
    record["served_model"] = response.model
    record["stop_reason"] = response.stop_reason
    record["raw_verdict_text"] = text

    exact = text == frozen["raw_verdict_text"]
    record["byte_identical_to_baseline"] = exact
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    record["parsed_verdict"] = parsed
    semantic = (
        parsed is not None
        and frozen.get("parsed_verdict") is not None
        and parsed.get("verdict") == frozen["parsed_verdict"]["verdict"]
        and parsed.get("failed_criteria") == frozen["parsed_verdict"]["failed_criteria"]
    )
    record["semantically_identical_to_baseline"] = semantic

    if exact:
        record["result"] = "PASS_BYTE_IDENTICAL"
    elif semantic:
        # Same verdict, different wording: still an environment drift at
        # temperature 0 — flag for party consult rather than silently pass.
        record["result"] = "DRIFT_TEXT_ONLY"
    else:
        record["result"] = "DRIFT_VERDICT"

    out = REPO / "followon-instruct" / "judge_determinism_check.json"
    out.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"result: {record['result']}")
    print(f"served model: {response.model}")
    print(f"verdict text: {text}")
    if not exact:
        print("--- frozen baseline was:")
        print(frozen["raw_verdict_text"])
    return 0 if exact else 1


if __name__ == "__main__":
    sys.exit(main())
