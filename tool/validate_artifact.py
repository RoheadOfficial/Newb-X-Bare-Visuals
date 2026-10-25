#!/usr/bin/env python3
"""Validate the generated Android MCpack payload, not just its source tree."""
from pathlib import Path
import json
import sys
import tempfile
import tomllib
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PROFILES = ["default", "pootaytoe", "bare_visuals"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_pack_tree(pack_root: Path) -> None:
    manifest_path = pack_root / "manifest.json"
    require(manifest_path.is_file(), "built pack must contain manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    header = manifest.get("header", {})
    config = tomllib.loads((ROOT / "src/newb/pack_config.toml").read_text(encoding="utf-8"))
    expected_materials = set(config.get("materials", []))
    require(header.get("name") == "Newb X Bare Visuals", "artifact name must remain Newb X Bare Visuals")
    require(header.get("version") == [0, 4, 6], "artifact manifest version must be [0, 4, 6]")
    require(header.get("uuid") == config.get("uuid"), "artifact UUID must match the pack source")
    require(header.get("min_engine_version") == [1, 26, 50], "artifact minimum engine version must remain compatible")
    profiles = manifest.get("subpacks", [])
    require([p.get("folder_name") for p in profiles] == EXPECTED_PROFILES,
            "artifact must expose Default, Pootaytoe, Bare Visuals in order")

    root_material_dir = pack_root / "renderer" / "materials"
    root_bins = {p.name for p in root_material_dir.glob("*.material.bin")}
    require(root_bins == {f"{name}.material.bin" for name in expected_materials},
            f"root/default compiled material set mismatch: expected {len(expected_materials)} bins, got {len(root_bins)}")

    total_bins = len(root_bins)
    for profile in ("pootaytoe", "bare_visuals"):
        material_dir = pack_root / "subpacks" / profile / "renderer" / "materials"
        bins = {p.name for p in material_dir.glob("*.material.bin")}
        require(bins == {f"{name}.material.bin" for name in expected_materials},
                f"{profile} compiled material set mismatch: expected {len(expected_materials)} bins, got {len(bins)}")
        total_bins += len(bins)

    default_dir = pack_root / "subpacks" / "default" / "renderer" / "materials"
    default_bins = list(default_dir.glob("*.material.bin")) if default_dir.exists() else []
    require(not default_bins, "Default must inherit root compiled materials instead of duplicating binaries")
    require(total_bins == 3 * len(expected_materials),
            f"expected {3 * len(expected_materials)} compiled material binaries across root and two custom profiles, got {total_bins}")
    require(not (pack_root / "textures" / "environment" / "clouds.png").exists(),
            "artifact must not bundle a custom clouds.png override")

    print(f"Artifact validation passed: {total_bins} compiled material binaries; profiles: {', '.join(EXPECTED_PROFILES)}.")


def validate_mcpack(path: Path) -> None:
    require(path.is_file() and zipfile.is_zipfile(path), f"expected a valid .mcpack ZIP: {path}")
    with tempfile.TemporaryDirectory(prefix="nxbv-artifact-") as temp:
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            require(bad is None, f"artifact ZIP integrity check failed at {bad}")
            archive.extractall(temp)
        validate_pack_tree(Path(temp))


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build"
    if target.is_dir() and (target / "manifest.json").is_file():
        validate_pack_tree(target)
        return 0
    if target.is_file():
        validate_mcpack(target)
        return 0
    if target.is_dir():
        packs = sorted(target.glob("*.mcpack"))
        require(len(packs) == 1, f"expected exactly one .mcpack in {target}, found {len(packs)}")
        validate_mcpack(packs[0])
        return 0
    raise AssertionError(f"artifact path does not exist: {target}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, json.JSONDecodeError, OSError, tomllib.TOMLDecodeError, zipfile.BadZipFile) as exc:
        print(f"Artifact validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
