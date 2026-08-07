"""Depth-parametrized task generator — frozen task families per SPEC section 7.

Three families with a scalar depth parameter d:

  1. multiplication : d = digit count per operand (serial depth ~ d^2 partial products)
  2. composition    : d = number of chained affine/mod function applications
  3. reachability   : d = length of the unique witness path in a random digraph

Depth calibration protocol (SPEC 7): required serial depth for a (family, d, model)
triple is calibrated by the with-trace vs. without-trace accuracy gap. This module
only GENERATES problems; calibration happens in the harness.

Determinism: every problem is a pure function of (family, d, seed). The seed list for
each run is part of the freeze manifest.

Usage:
    python generate_tasks.py --family composition --depth 8 --n 200 --seed 1337 \
        --out problems.jsonl
"""

import argparse
import json
import random


# ----------------------------------------------------------------------------- 
# Family 1: multi-digit multiplication
# -----------------------------------------------------------------------------

def gen_multiplication(d: int, rng: random.Random) -> dict:
    lo, hi = 10 ** (d - 1), 10 ** d - 1
    a, b = rng.randint(lo, hi), rng.randint(lo, hi)
    return {
        "family": "multiplication",
        "depth": d,
        "prompt": f"Compute {a} * {b}. Reason step by step, then give the final "
                  f"answer as 'ANSWER: <number>'.",
        "answer": str(a * b),
    }


# -----------------------------------------------------------------------------
# Family 2: iterated function composition (affine maps mod m)
# -----------------------------------------------------------------------------

def gen_composition(d: int, rng: random.Random) -> dict:
    m = 97  # fixed prime modulus; keeps values small and uniform
    x = rng.randint(0, m - 1)
    steps, val = [], x
    for i in range(d):
        a = rng.randint(2, m - 1)
        b = rng.randint(0, m - 1)
        val = (a * val + b) % m
        steps.append(f"f{i + 1}(x) = ({a}*x + {b}) mod {m}")
    fn_defs = "\n".join(steps)
    chain = "(".join(f"f{i}" for i in range(d, 0, -1)) + f"({x}" + ")" * d
    return {
        "family": "composition",
        "depth": d,
        "prompt": f"Define:\n{fn_defs}\n\nCompute {chain}. Reason step by step, "
                  f"then give the final answer as 'ANSWER: <number>'.",
        "answer": str(val),
    }


# -----------------------------------------------------------------------------
# Family 3: graph reachability with parametric witness-path length
# -----------------------------------------------------------------------------

def gen_reachability(d: int, rng: random.Random) -> dict:
    """Random digraph containing a unique simple path of length d from S to T.

    Construction: build the witness chain S=v0 -> v1 -> ... -> vd=T, then add
    distractor edges among decoy nodes and from chain nodes into decoys, never
    creating a second S->T path (decoys have no edges back into the chain and
    no edges to T).
    """
    n_decoys = max(4, d)
    chain = [f"N{i}" for i in range(d + 1)]
    decoys = [f"D{i}" for i in range(n_decoys)]
    edges = [(chain[i], chain[i + 1]) for i in range(d)]
    for _ in range(2 * n_decoys):
        u = rng.choice(chain[:-1] + decoys)          # never out of T
        v = rng.choice(decoys)                       # never back into chain, never T
        if u != v and (u, v) not in edges:
            edges.append((u, v))
    rng.shuffle(edges)
    edge_str = ", ".join(f"{u}->{v}" for u, v in edges)
    return {
        "family": "reachability",
        "depth": d,
        "prompt": f"Directed graph edges: {edge_str}.\nIs there a path from "
                  f"{chain[0]} to {chain[-1]}? If yes, give its length (number of "
                  f"edges). Reason step by step, then answer as 'ANSWER: <number>' "
                  f"or 'ANSWER: none'.",
        "answer": str(d),
    }


FAMILIES = {
    "multiplication": gen_multiplication,
    "composition": gen_composition,
    "reachability": gen_reachability,
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--family", choices=FAMILIES, required=True)
    p.add_argument("--depth", type=int, required=True)
    p.add_argument("--n", type=int, default=200)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    rng = random.Random(args.seed)
    with open(args.out, "w") as f:
        for i in range(args.n):
            prob = FAMILIES[args.family](args.depth, rng)
            prob["id"] = f"{args.family}-d{args.depth}-s{args.seed}-{i:04d}"
            f.write(json.dumps(prob) + "\n")
    print(f"wrote {args.n} problems to {args.out}")


if __name__ == "__main__":
    main()
