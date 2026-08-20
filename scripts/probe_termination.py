"""Diagnostic probe for the follow-on connectives no-answer mechanism.

CLAUDE.md rule 5 duty: suspect the harness before the science. Two parts:

A. Bit-identity sanity check (exact-prefix rebuild, cache OFF): re-generate
   native traces greedily and compare byte-for-byte with recorded output.
   Validates the decoder/scoring stack on the instruct pin.

B. Terminal-token probe: for touched no-parseable-answer traces (which all
   end exactly at the substituted connective), report the next-token
   distribution after (i) the substituted token and (ii) the native token —
   specifically P(<|im_end|>), P(<|endoftext|>), and the top-5. This
   identifies WHICH terminal token fires and whether the native counterfactual
   would have continued.

Diagnostic only. Touches no frozen artifact; changes no registered number.

Usage (on GPU box):
    python scripts/probe_termination.py --input probe_input.json \
        --out probe_result.json
"""

from __future__ import annotations

import argparse
import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = "Qwen/Qwen2.5-7B-Instruct"
REV = "a09a35458c702b33eeacc393d103063234e8bc28"


def top_probs(model, tok, device, text: str, k: int = 5) -> dict:
    ids = tok.encode(text, add_special_tokens=False)
    with torch.no_grad():
        logits = model(torch.tensor([ids], device=device)).logits[0, -1]
    probs = torch.softmax(logits.float(), dim=-1)
    top = torch.topk(probs, k)
    im_end = tok.convert_tokens_to_ids("<|im_end|>")
    endoftext = tok.convert_tokens_to_ids("<|endoftext|>")
    return {
        "top": [{"token": tok.decode([i]), "id": int(i), "p": float(p)}
                for p, i in zip(top.values, top.indices)],
        "p_im_end": float(probs[im_end]),
        "p_endoftext": float(probs[endoftext]),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--replay-tokens", type=int, default=1024)
    args = ap.parse_args()

    data = json.load(open(args.input, encoding="utf-8"))
    tok = AutoTokenizer.from_pretrained(MODEL, revision=REV)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL, revision=REV, dtype=torch.bfloat16).to("cuda").eval()

    out = {"bit_identity": [], "probes": []}

    # A. bit-identity replay, cache-free naive path
    im_end = tok.convert_tokens_to_ids("<|im_end|>")
    endoftext = tok.convert_tokens_to_ids("<|endoftext|>")
    terminal = {im_end, endoftext}
    for rec in data["native"][:3]:
        ids = tok.encode(rec["prompt"], add_special_tokens=False)
        gen: list[int] = []
        with torch.no_grad():
            for _ in range(args.replay_tokens):
                logits = model(torch.tensor([ids + gen], device="cuda")).logits[0, -1]
                nxt = int(torch.argmax(logits))
                if nxt in terminal:
                    break
                gen.append(nxt)
        text = tok.decode(gen, skip_special_tokens=False,
                          clean_up_tokenization_spaces=False)
        out["bit_identity"].append({
            "id": rec["id"],
            "match": text == rec["text"],
            "len_recorded": len(rec["text"]),
            "len_replayed": len(text),
            "first_divergence": next(
                (i for i, (a, b) in enumerate(zip(text, rec["text"])) if a != b),
                min(len(text), len(rec["text"])) if text != rec["text"] else None),
        })
        print(f"bit-identity {rec['id']}: match={text == rec['text']}")

    # B. terminal-token probe
    for rec in data["touched"]:
        full = rec["prompt"] + rec["text"]
        native_text = (rec["text"][:rec["site_start"]] + rec["matched"])
        full_native = rec["prompt"] + native_text
        row = {
            "id": rec["id"], "seed": rec["seed"],
            "chosen": rec["chosen"], "matched": rec["matched"],
            "after_substituted": top_probs(model, tok, "cuda", full),
            "after_native": top_probs(model, tok, "cuda", full_native),
        }
        out["probes"].append(row)
        a, b = row["after_substituted"], row["after_native"]
        print(f"{rec['id']} s{rec['seed']}: sub-> im_end {a['p_im_end']:.3f} "
              f"eot {a['p_endoftext']:.3f} top='{a['top'][0]['token']}' | "
              f"nat-> im_end {b['p_im_end']:.3f} eot {b['p_endoftext']:.3f} "
              f"top='{b['top'][0]['token']}'")

    json.dump(out, open(args.out, "w", encoding="utf-8"), indent=1)
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
