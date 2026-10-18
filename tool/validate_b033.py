#!/usr/bin/env python3
"""Static regression checks for the B0.3.3 beauty and performance update."""
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
    require(config.get("version") == [0, 3, 3], "manifest version must be [0, 3, 3]")
    require(config.get("development_version") == "B0.3.3", "display version must be B0.3.3")
    require("Newb X Bare Visuals" in config.get("name", ""), "pack name must retain Newb X Bare Visuals identity")
    require("%w" in config.get("description", "") and "%v" in config.get("description", ""),
            "patch warning and generated version placeholders must remain")

    subpacks = config.get("subpack", [])
    names = [item.get("define") for item in subpacks]
    require(names == ["DEFAULT", "POOTAYTOE", "BARE_VISUALS"],
            "subpack order must be Default, Pootaytoe, Bare Visuals")
    base_materials = set(config.get("materials", []))
    profiles = {item["define"]: item for item in subpacks}
    require(not profiles["DEFAULT"].get("materials"),
            "Default must inherit the root material set compiled with DEFAULT")
    for name in ("POOTAYTOE", "BARE_VISUALS"):
        require(set(profiles[name].get("materials", [])) == base_materials,
                f"{name} must compile the full material set with its profile define")
    for name in names:
        description = profiles[name].get("description", "")
        require("%" not in description, f"{name} player-facing description must not expose internal vibe percentages")

    cfg = read("src/newb/config.h")
    require("#define NL_VANILLA_WATER" in cfg, "vanilla-water path must remain active")
    require("#define NL_GROUND_RAIN_WETNESS" in cfg, "wet-ground response must remain configured")
    require(re.search(r"(?m)^\s*#define\s+NL_WEATHER_SPECK\b", cfg),
            "base weather particle styling must remain enabled")
    for macro in ("NL_WATER_WAVE", "NL_PLANTS_WAVE", "NL_LANTERN_WAVE", "NL_CLOUD_SHADOW"):
        require(not re.search(rf"(?m)^\s*#define\s+{macro}\b", cfg),
                f"{macro} must not be enabled in the shared configuration")
    require("#ifdef POOTAYTOE" in cfg and "#ifdef DEFAULT" in cfg and "#ifdef BARE_VISUALS" in cfg,
            "all three profile-specific configuration blocks must exist")
    for macro in ("NL_COZY_SKY_STRENGTH", "NL_COZY_AMBIENT_STRENGTH", "NL_COZY_FOG_STRENGTH", "NL_COZY_CLOUD_SOFTNESS"):
        require(f"#define {macro}" in cfg, f"cozy atmosphere control is missing: {macro}")
    sky = read("src/newb/functions/sky.h")
    require("horizonBand" in sky and "cozyWarmth" in sky,
            "sky redesign must affect the rendered gradient and horizon warmth")
    fog = read("src/newb/functions/fog.h")
    require("mistStrength" in fog and "NL_COZY_FOG_STRENGTH" in fog,
            "fog redesign must provide profile-aware atmospheric depth")
    lighting = read("src/newb/functions/lighting.h")
    require("NL_COZY_AMBIENT_STRENGTH" in lighting,
            "lighting redesign must use the cozy ambient profile control")
    clouds = read("src/newb/functions/clouds.h")
    require("NL_COZY_CLOUD_SOFTNESS" in clouds,
            "rounded cloud shading must use the cozy atmosphere control")
    require("#define NL_GROUND_REFL_MAX_DISTANCE 20.0" in cfg,
            "Pootaytoe must use its shorter terrain-reflection cap")
    require("#define NL_GROUND_REFL_MAX_DISTANCE 32.0" in cfg,
            "Default must use the bounded B0.3.3 terrain-reflection cap")
    require("#define NL_GROUND_REFL_MAX_DISTANCE 30.0" in cfg,
            "Bare Visuals must retain a bounded terrain-reflection cap")
    require("#define NL_CLOUD2_STEPS 2" in cfg,
            "Pootaytoe must use reduced rounded-cloud sampling")
    require("#define NL_MATERIAL_HIGHLIGHT_STRENGTH 0.022" in cfg,
            "Bare Visuals material highlight tuning is missing")
    require("#undef NL_MATERIAL_HIGHLIGHT_STRENGTH" in cfg,
            "Pootaytoe must skip optional material highlights")

    ore_texture_names = (
        "copper_ore.png", "diamond_ore.png", "emerald_ore.png", "gold_ore.png",
        "iron_ore.png", "lapis_ore.png", "nether_gold_ore.png", "quartz_ore.png",
        "redstone_ore.png",
    )
    for name in ore_texture_names:
        ore_path = ROOT / "assets" / "textures" / "blocks" / name
        require(ore_path.is_file(), f"ore texture is missing: {name}")
        require(ore_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"),
                f"ore texture is not a valid PNG: {name}")

    rain = read("src/newb/functions/rain.h")
    require("if (wPos.y < 0.0)" in rain, "terrain reflection must remain limited to the horizontal-plane branch")
    require("wetness *= puddles;" in rain, "puddle variation must continue affecting wet-ground response")
    require("float reflectionWetness = wetness;" in rain,
            "reflection blend must retain its pre-puddle wetness input")
    clouds = read("src/newb/functions/clouds.h")
    require("if (dayFactor >= 0.0)" in clouds, "daytime aurora early-out must remain")
    glow = read("src/newb/functions/glow.h")
    for unused in ("vec3 c1 =", "vec3 c3 =", "vec3 c5 =", "vec3 c7 ="):
        require(unused not in glow, f"unused glow corner sample remains: {unused}")

    terrain = read("src/materials/RenderChunk/fragment.sc")
    require("NL_MATERIAL_HIGHLIGHT_STRENGTH" in terrain,
            "lightweight PBR-inspired terrain material lift is missing")
    require("texture2D(" not in terrain[terrain.index("inexpensive PBR-inspired material lift"):terrain.index("if (v_extra.b > 0.9)")],
            "material highlight block must not add texture reads")
    require("nlBareTerrainShade" in terrain, "existing bounded terrain shading correction must remain")
    require("diffuse.rgb = mix(diffuse.rgb, v_fog.rgb, v_fog.a);" in terrain,
            "terrain fog blending must remain")

    packer = read("tool/pack.py")
    require('pack_config.get("development_version", "B0.3.3")' in packer,
            "pack-builder fallback must be B0.3.3")
    require('_build(status, args.p, "default", pack_config[\'materials\'], mats_dir)' in packer,
            "root material set must compile using the DEFAULT define")
    require("MacroDefine.from_string(subpack.upper())" in packer,
            "profile-specific defines must be passed into compilation")

    build = read(".github/workflows/build.yml")
    check = read(".github/workflows/build-check.yml")
    require("default: '3'" in build, "manual build default must use manifest sub-version 2")
    require("b0.3.3" in build, "manual build artifact labels must use B0.3.3")
    require("tool/validate_b033.py" in build and "tool/validate_b033.py" in check,
            "both build workflows must run the B0.3.3 static validator")
    require(" -v 3 " in check, "build-check must use manifest sub-version 2")
    require("b0.3.3-implementation" in check, "build-check must run on the B0.3.3 implementation branch")
    require("branches: [main]" in check, "pull-request checks must target main")

    print("B0.3.3 static regression checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError) as exc:
        print(f"B0.3.3 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
