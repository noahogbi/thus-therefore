"""Freeze-manifest generator. Run BEFORE any GPU generation run.

Hashes every frozen artifact (SPEC, rule tables, judge prompt, task generator,
seeds file, and the pinned environment description) into FREEZE_MANIFEST.json.
Any amendment => rerun this script => new manifest => new experiment.
"""
import argparse, hashlib, json, os, sys, datetime

# Shared frozen artifacts. The environment and seeds files are supplied
# separately so a pre-registered follow-on (different model pin, same
# procedure) can generate its own manifest without disturbing the manifest
# of a completed run. Defaults reproduce the original invocation exactly.
SHARED_PATHS = [
    "SPEC.md",
    "FREEZE.md",
    "judge/judge_prompt.txt",
    "tasks/generate_tasks.py",
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default="environment.json")
    ap.add_argument("--seeds", default="seeds.json")
    ap.add_argument("--out", default="FREEZE_MANIFEST.json")
    args = ap.parse_args()

    entries = {}
    paths = list(SHARED_PATHS) + [args.seeds, args.env]
    for root, _, files in os.walk("rules"):
        for fn in sorted(files):
            paths.append(os.path.join(root, fn))
    missing = [p for p in paths if not os.path.exists(p)]
    if missing:
        sys.exit(f"REFUSING TO FREEZE — missing artifacts: {missing}")
    for p in sorted(paths):
        # Manifest keys are always POSIX-style so the manifest hash is
        # platform-independent (os.path.join yields backslashes on Windows,
        # which changed the aggregate hash; per-file hashes were unaffected).
        entries[p.replace(os.sep, "/")] = sha256(p)
    manifest = {
        "frozen_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "files": entries,
        "manifest_hash": hashlib.sha256(
            json.dumps(entries, sort_keys=True).encode()
        ).hexdigest(),
    }
    with open(args.out, "w") as f:
        json.dump(manifest, f, indent=2)
    print("manifest_hash:", manifest["manifest_hash"])

if __name__ == "__main__":
    main()
