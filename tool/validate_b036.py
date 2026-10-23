#!/usr/bin/env python3
"""Static regression checks for the B0.3.6 Java-inspired cozy shader revamp."""
from pathlib import Path
import re
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_BRANCH = "b0.3.6-java-inspired-revamp"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    pack = tomllib.loads(read("src/newb/pack_config.toml"))
    require(pack.get("version") == [0, 3, 6], "manifest version must be [0, 3, 6]")
    require(pack.get("development_version") == "B0.3.6", "display version must be B0.3.6")
    require("Newb X Bare Visuals" in pack.get("name", ""), "pack identity must remain Newb X Bare Visuals")
    require("%w" in pack.get("description", "") and "%v" in pack.get("description", ""),
            "patch warning and generated version placeholders must remain")

    subpacks = pack.get("subpack", [])
    names = [item.get("define") for item in subpacks]
    require(names == ["DEFAULT", "POOTAYTOE", "BARE_VISUALS"],
            "subpack order must remain Default, Pootaytoe, Bare Visuals")
    profiles = {item["define"]: item for item in subpacks}
    require(not profiles["DEFAULT"].get("materials"),
            "Default must inherit the root material set compiled with DEFAULT")
    base_materials = set(pack.get("materials", []))
    for name in ("POOTAYTOE", "BARE_VISUALS"):
        require(set(profiles[name].get("materials", [])) == base_materials,
                f"{name} must compile the full material set with its own profile define")
    for name in names:
        require("%" not in profiles[name].get("description", ""),
                f"{name} description must not expose internal inspiration percentages")

    cfg = read("src/newb/config.h")
    require("#define NL_TONEMAP_TYPE 4" in cfg, "B0.3.6 must use the coordinated ACES tone-mapping pipeline")
    require("#if NL_TONEMAP_TYPE == 4" in read("src/newb/functions/tonemap.h"), "ACES inverse compensation must be defined")
    for required in (
        "#define NL_VANILLA_WATER",
        "#define NL_GROUND_RAIN_WETNESS",
        "#define NL_SKY_HORIZON_GLOW 0.16",
        "#define NL_SKY_AMBIENT_STRENGTH 0.90",
        "#define NL_CLOUD2_STEPS 4",
        "#define NL_GROUND_REFL_MAX_DISTANCE 32.0",
        "#define NL_GROUND_REFL_MAX_DISTANCE 20.0",
        "#define NL_GROUND_REFL_MAX_DISTANCE 30.0",
        "#define NL_CLOUD2_STEPS 2",
    ):
        require(required in cfg, f"required shader/profile setting missing: {required}")
    for macro in ("NL_WATER_WAVE", "NL_PLANTS_WAVE", "NL_LANTERN_WAVE", "NL_CLOUD_SHADOW"):
        require(not re.search(rf"(?m)^\s*#define\s+{macro}\b", cfg),
                f"{macro} must remain disabled in the shared configuration")
    require(all(f"#ifdef {name}" in cfg for name in ("DEFAULT", "POOTAYTOE", "BARE_VISUALS")),
            "all three profile configuration blocks must exist")

    sky = read("src/newb/functions/sky.h")
    require("float horizonBand =" in sky and "NL_SKY_HORIZON_GLOW" in sky,
            "the new low-cost horizon blend must be present")
    fog = read("src/newb/functions/fog.h")
    require("12.0 - 11.0*FOG_COLOR.g" in fog,
            "fog must use the reduced mist density response")
    require("rain*0.12" in fog, "rain atmosphere must remain but avoid excessive front fog")
    lighting = read("src/newb/functions/lighting.h")
    require(lighting.count("*NL_SKY_AMBIENT_STRENGTH") >= 2,
            "terrain and entity lighting must both use the balanced ambient response")
    clouds = read("src/newb/functions/clouds.h")
    require("if (dayFactor >= 0.0)" in clouds,
            "daytime aurora early-out must remain")
    glow = read("src/newb/functions/glow.h")
    for unused in ("vec3 c1 =", "vec3 c3 =", "vec3 c5 =", "vec3 c7 ="):
        require(unused not in glow, f"unused glow corner sample remains: {unused}")

    terrain = read("src/materials/RenderChunk/fragment.sc")
    require("nlBareTerrainShade" in terrain, "bounded terrain shading correction must remain")
    require("NL_MATERIAL_HIGHLIGHT_STRENGTH" in terrain,
            "the inexpensive material response must remain")
    highlight_start = terrain.index("B0.3.6: refine the inexpensive material response")
    highlight_end = terrain.index("if (v_extra.b > 0.9)", highlight_start)
    require("texture2D(" not in terrain[highlight_start:highlight_end],
            "material response must not add texture reads")
    require("diffuse.rgb = mix(diffuse.rgb, v_fog.rgb, v_fog.a);" in terrain,
            "terrain fog blending must remain")

    packer = read("tool/pack.py")
    require('pack_config.get("development_version", "B0.3.6")' in packer,
            "pack-builder fallback must be B0.3.6")
    build = read(".github/workflows/build.yml")
    check = read(".github/workflows/build-check.yml")
    for workflow in (build, check):
        require("tool/validate_b036.py" in workflow, "build workflows must run the B0.3.6 validator")
        require("newb-x-bare-visuals-b0.3.6" in workflow,
                "build artifact labels must use B0.3.6")
    require("default: '6'" in build, "manual build default must use manifest sub-version 6")
    require("-v 6 --no-zip" in check, "build-check must compile manifest sub-version 6")
    require(IMPLEMENTATION_BRANCH in check,
            "build-check must run on the B0.3.6 implementation branch")

    print("B0.3.6 static regression checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError) as exc:
        print(f"B0.3.6 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
