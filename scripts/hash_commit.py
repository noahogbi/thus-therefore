"""Freeze-manifest generator. Run BEFORE any GPU generation run.

Hashes every frozen artifact (SPEC, rule tables, judge prompt, task generator,
seeds file, and the pinned environment description) into FREEZE_MANIFEST.json.
Any amendment => rerun this script => new manifest => new experiment.
"""
import hashlib, json, os, sys, datetime

FROZEN_PATHS = [
    "SPEC.md",
    "FREEZE.md",
    "judge/judge_prompt.txt",
    "tasks/generate_tasks.py",
    "seeds.json",
    "environment.json",
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    entries = {}
    paths = list(FROZEN_PATHS)
    for root, _, files in os.walk("rules"):
        for fn in sorted(files):
            paths.append(os.path.join(root, fn))
    missing = [p for p in paths if not os.path.exists(p)]
    if missing:
        sys.exit(f"REFUSING TO FREEZE — missing artifacts: {missing}")
    for p in sorted(paths):
        entries[p] = sha256(p)
    manifest = {
        "frozen_at_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "files": entries,
        "manifest_hash": hashlib.sha256(
            json.dumps(entries, sort_keys=True).encode()
        ).hexdigest(),
    }
    with open("FREEZE_MANIFEST.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("manifest_hash:", manifest["manifest_hash"])

if __name__ == "__main__":
    main()
