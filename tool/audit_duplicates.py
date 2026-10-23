#!/usr/bin/env python3
"""Report exact duplicate tracked files for a safe, review-first repository cleanup."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PREFIXES = (".git/", "build/", "tool/data/")


def main() -> int:
    try:
        listing = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"Could not list tracked files for duplicate audit: {exc}", file=sys.stderr)
        return 2

    groups: dict[str, list[str]] = defaultdict(list)
    for raw_path in listing.split(b"\0"):
        if not raw_path:
            continue
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if path.startswith(IGNORED_PREFIXES):
            continue
        full_path = ROOT / path
        if not full_path.is_file():
            continue
        try:
            digest = sha256(full_path.read_bytes()).hexdigest()
        except OSError as exc:
            print(f"Could not read {path}: {exc}", file=sys.stderr)
            return 2
        groups[digest].append(path)

    duplicates = [paths for paths in groups.values() if len(paths) > 1]
    if not duplicates:
        print("Duplicate audit: no byte-identical tracked files found (generated/cache paths excluded).")
        return 0

    print("Duplicate audit: byte-identical tracked files found; review before deleting because some copies may be intentional:")
    for paths in sorted(duplicates, key=lambda group: group[0].lower()):
        print("  - " + " == ".join(sorted(paths, key=str.lower)))
    # Informational only: identical assets/docs may be intentional, so do not break builds automatically.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
