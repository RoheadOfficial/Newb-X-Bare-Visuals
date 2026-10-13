#!/usr/bin/env python3
"""Static regression checks for the B0.2.9 performance update."""
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    config = tomllib.loads(read("src/newb/pack_config.toml"))
    require(config.get("version") == [0, 2, 9], "pack manifest version must be [0, 2, 9]")
    require(config.get("development_version") == "B0.2.9", "display version must be B0.2.9")

    subpacks = config.get("subpack", [])
    names = [item.get("define") for item in subpacks]
    require(names == ["LITE", "BETA", "DEFAULT"], "subpack order must be Lite, Beta, Default")
    base_materials = set(config.get("materials", []))
    lite = next(item for item in subpacks if item.get("define") == "LITE")
    beta = next(item for item in subpacks if item.get("define") == "BETA")
    default = next(item for item in subpacks if item.get("define") == "DEFAULT")
    require(set(lite.get("materials", [])) == base_materials, "Lite must compile the full material set")
    require(not default.get("materials"), "Default should inherit the root material set rather than duplicate all shader binaries")
    require(not beta.get("materials"), "Beta must remain an empty experimental slot")

    cfg = read("src/newb/config.h")
    require("#define NL_VANILLA_WATER" in cfg, "vanilla-water path must remain active")
    require("#define NL_GROUND_RAIN_WETNESS" in cfg, "wet-ground effect must remain configured")
    require(re.search(r"(?m)^\s*#define\s+NL_WEATHER_SPECK\b", cfg), "weather particle styling must remain enabled")
    for macro in ("NL_WATER_WAVE", "NL_PLANTS_WAVE", "NL_LANTERN_WAVE"):
        require(not re.search(rf"(?m)^\s*#define\s+{macro}\b", cfg), f"{macro} must not be enabled")

    rain = read("src/newb/functions/rain.h")
    require("if (wPos.y < 0.0)" in rain, "terrain reflection must remain limited to the horizontal-plane branch")
    require("wetness *= puddles;" in rain, "puddle variation must continue affecting wet-ground response")
    require("float reflectionWetness = wetness;" in rain, "reflection blend must retain its pre-puddle wetness input")

    clouds = read("src/newb/functions/clouds.h")
    require("if (dayFactor >= 0.0)" in clouds, "daytime aurora early-out is missing")
    glow = read("src/newb/functions/glow.h")
    for unused in ("vec3 c1 =", "vec3 c3 =", "vec3 c5 =", "vec3 c7 ="):
        require(unused not in glow, f"unused glow corner sample remains: {unused}")

    packer = read("tool/pack.py")
    require('"B0.2.9"' in packer, "pack builder fallback must be B0.2.9")
    require('_build(status, args.p, "default", pack_config[\'materials\'], mats_dir)' in packer,
            "root materials must be compiled using the DEFAULT profile define")
    require("MacroDefine.from_string(subpack.upper())" in packer,
            "subpack-specific defines must be passed into compilation")
    build = read(".github/workflows/build.yml")
    check = read(".github/workflows/build-check.yml")
    require("default: '9'" in build, "manual build default must use manifest sub-version 9")
    require("b0.2.9" in build, "manual build artifact labels must use B0.2.9")
    require("tool/validate_b029.py" in build and "tool/validate_b029.py" in check,
            "both build workflows must run the B0.2.9 static validator")
    require(" -v 9 " in check, "build-check must use manifest sub-version 9")
    require("b0.2.9-implementation" in check, "build-check must run on the implementation branch")

    print("B0.2.9 static regression checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError) as exc:
        print(f"B0.2.9 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
