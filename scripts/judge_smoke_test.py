"""Judge smoke test — Sol's F3 pre-hash condition (REVIEW_LOG.md).

Sends ONE exact request in the shape the real audit will use: the frozen
judge prompt (judge/judge_prompt.txt) filled with a genuine site pair from
the matcher dry run, against the party-ruled pin:

    model       = claude-opus-4-5-20251101
    temperature = 0
    thinking    = omitted / not enabled

Per Sol's ruling: if this exact model/configuration is unavailable, do NOT
substitute another judge — return through the amendment protocol.

Usage (requires ANTHROPIC_API_KEY in the environment):
    python scripts/judge_smoke_test.py

Writes JUDGE_SMOKE_TEST.json next to the repo root on success or failure.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO = Path(__file__).resolve().parent.parent

JUDGE_MODEL = "claude-opus-4-5-20251101"
JUDGE_TEMPERATURE = 0

# A real rule-01 site from the dry run (trace 01_multiplication_basic.txt):
# sentence-initial "Thus" swapped for "Therefore" — the archetypal Tier A
# intervention. The excerpt shape matches what the audit sampler will emit.
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
    prompt_template = (REPO / "judge" / "judge_prompt.txt").read_text(encoding="utf-8")
    prompt = (
        prompt_template
        .replace("{original}", SAMPLE["original"])
        .replace("{modified}", SAMPLE["modified"])
        .replace("{span_before}", SAMPLE["span_before"])
        .replace("{span_after}", SAMPLE["span_after"])
    )

    record: dict = {
        "purpose": "REVIEW_LOG F3 pre-hash smoke test (Sol's condition)",
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
        record["result"] = "FAILED"
        record["error"] = {"status": e.status_code, "message": str(e.message)}
        (REPO / "JUDGE_SMOKE_TEST.json").write_text(
            json.dumps(record, indent=2), encoding="utf-8")
        print(f"SMOKE TEST FAILED: HTTP {e.status_code} — {e.message}")
        print("Per Sol's F3 ruling: no substitution; amendment protocol applies.")
        return 1

    text = next((b.text for b in response.content if b.type == "text"), "")
    record["result"] = "OK" if response.model.startswith("claude-opus-4-5") else "MODEL_MISMATCH"
    record["served_model"] = response.model
    record["stop_reason"] = response.stop_reason
    record["usage"] = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
    record["raw_verdict_text"] = text
    try:
        record["parsed_verdict"] = json.loads(text)
    except json.JSONDecodeError:
        record["parsed_verdict"] = None
        record["result"] = "VERDICT_NOT_JSON"

    (REPO / "JUDGE_SMOKE_TEST.json").write_text(
        json.dumps(record, indent=2), encoding="utf-8")
    print(f"result: {record['result']}")
    print(f"served model: {response.model}")
    print(f"verdict: {text}")
    return 0 if record["result"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
