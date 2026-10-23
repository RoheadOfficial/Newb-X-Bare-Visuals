#!/usr/bin/env python3
"""Canonical B-Series and Minecraft-target version identity for pack builds."""
from __future__ import annotations

import os
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get_version_identity(pack_config: dict) -> tuple[str, str, str]:
    """Return (simple version, Minecraft target, full compact version).

    Example: B0.3.7 + 26.52 -> B0.3.7.2652.
    The target is metadata only; it does not prove runtime compatibility.
    """
    display_version = str(pack_config.get("development_version", "")).strip()
    target_version = str(pack_config.get("minecraft_target_version", "")).strip()
    if not re.fullmatch(r"B(?:0\.\d+\.\d+|1(?:\.\d+\.\d+)?)", display_version):
        raise ValueError(f"Invalid B-Series display version: {display_version!r}")
    if not re.fullmatch(r"\d+(?:\.\d+)+", target_version):
        raise ValueError(f"Invalid Minecraft target version: {target_version!r}")
    compact_target = target_version.replace(".", "")
    return display_version, target_version, f"{display_version}.{compact_target}"


def main() -> int:
    with (ROOT / "src/newb/pack_config.toml").open("rb") as file:
        config = tomllib.load(file)
    try:
        display, target, full = get_version_identity(config)
    except ValueError as exc:
        print(f"Version configuration error: {exc}", file=sys.stderr)
        return 1

    print(f"Simple version: {display}")
    print(f"Minecraft target: {target}")
    print(f"Full version: {full}")

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"display_version={display}\n")
            output.write(f"minecraft_target_version={target}\n")
            output.write(f"full_version={full}\n")
            output.write(f"full_version_slug={full.lower()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
