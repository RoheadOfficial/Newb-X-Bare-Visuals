#!/usr/bin/env python3
"""Current-source regression checks for Newb X Bare Visuals B0.3.7."""
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
    pack = tomllib.loads(read("src/newb/pack_config.toml"))
    require(pack.get("version") == [0, 3, 7], "manifest version must be [0, 3, 7]")
    require(pack.get("development_version") == "B0.3.7", "simple version must be B0.3.7")
    require(pack.get("minecraft_target_version") == "26.52", "declared Minecraft target must be 26.52 until retargeted")
    require("Newb X Bare Visuals" in pack.get("name", ""), "pack identity must remain Newb X Bare Visuals")
    require("%w" in pack.get("description", "") and "%v" in pack.get("description", ""),
            "patch warning and generated version placeholders must remain")
    sys.path.insert(0, str(ROOT / "tool"))
    from versioning import get_version_identity
    display, target, full = get_version_identity(pack)
    require((display, target, full) == ("B0.3.7", "26.52", "B0.3.7.2652"),
            "canonical version identity must be B0.3.7 / 26.52 / B0.3.7.2652")

    subpacks = pack.get("subpack", [])
    names = [item.get("define") for item in subpacks]
    require(names == ["DEFAULT", "POOTAYTOE", "BARE_VISUALS", "EXPERIMENTAL"],
            "subpack order must be Default, Pootaytoe, Bare Visuals, Experimental")
    profiles = {item["define"]: item for item in subpacks}
    require(not profiles["DEFAULT"].get("materials"), "Default must inherit root materials compiled with DEFAULT")
    base_materials = set(pack.get("materials", []))
    for name in ("POOTAYTOE", "BARE_VISUALS", "EXPERIMENTAL"):
        require(set(profiles[name].get("materials", [])) == base_materials,
                f"{name} must compile the full material set with its own profile define")
    for name in names:
        require("%" not in profiles[name].get("description", ""),
                f"{name} description must not expose internal inspiration percentages")
    require("fake terrain shadows" in profiles["EXPERIMENTAL"]["description"].lower(),
            "Experimental must be described as a fake-shadow prototype")

    cfg = read("src/newb/config.h")
    require("#define NL_TONEMAP_TYPE 4" in cfg, "preserve ACES tone mapping")
    require("#define NL_SATURATION 1.04" in cfg, "preserve approved saturation")
    require("#define NL_VANILLA_WATER" in cfg, "vanilla water path must remain enabled")
    require("#define NL_WATER_BLUE_REDUCTION 0.92" in cfg, "water blue reduction must be configured")
    require("#define NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH 0.10" in cfg,
            "fake shadows must be an Experimental-only setting")
    for required in ("#define NL_SKY_HORIZON_GLOW 0.16", "#define NL_SKY_AMBIENT_STRENGTH 0.90",
                     "#define NL_CLOUD2_STEPS 4", "#define NL_GROUND_REFL_MAX_DISTANCE 32.0",
                     "#define NL_GROUND_REFL_MAX_DISTANCE 20.0", "#define NL_GROUND_REFL_MAX_DISTANCE 30.0",
                     "#define NL_CLOUD2_STEPS 2"):
        require(required in cfg, f"required shader/profile setting missing: {required}")
    for macro in ("NL_WATER_WAVE", "NL_PLANTS_WAVE", "NL_LANTERN_WAVE", "NL_CLOUD_SHADOW"):
        require(not re.search(rf"(?m)^\s*#define\s+{macro}\b", cfg),
                f"{macro} must remain disabled in shared configuration")
    require(all(f"#ifdef {name}" in cfg for name in names), "all four profile config blocks must exist")

    sky = read("src/newb/functions/sky.h")
    require("float horizonBand =" in sky and "NL_SKY_HORIZON_GLOW" in sky, "horizon blend must remain")
    require("float source = max(0.0, (mg8-0.22)/0.78);" not in sky, "aggressive sun-source boost must remain removed")
    fog = read("src/newb/functions/fog.h")
    require("12.0 - 11.0*FOG_COLOR.g" in fog and "rain*0.12" in fog, "restrained fog must remain")
    lighting = read("src/newb/functions/lighting.h")
    require(lighting.count("*NL_SKY_AMBIENT_STRENGTH") >= 2, "terrain/entity ambient lighting must remain balanced")
    clouds = read("src/newb/functions/clouds.h")
    require("if (dayFactor >= 0.0)" in clouds, "daytime aurora early-out must remain")
    glow = read("src/newb/functions/glow.h")
    for unused in ("vec3 c1 =", "vec3 c3 =", "vec3 c5 =", "vec3 c7 ="):
        require(unused not in glow, f"unused glow corner sample remains: {unused}")

    terrain = read("src/materials/RenderChunk/fragment.sc")
    require("nlBareTerrainShade" in terrain, "bounded terrain shading must remain")
    require("nlExperimentalFakeShadow" in terrain, "Experimental fake-shadow approximation must be present")
    require("#ifdef NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH" in terrain, "fake shadows must be profile-gated")
    require("#if defined(LITE) || defined(POOTAYTOE)" in terrain, "Pootaytoe glow optimization must use its actual define")
    require("diffuse.b *= NL_WATER_BLUE_REDUCTION;" in terrain, "water blue adjustment must be present")
    require("NL_MATERIAL_HIGHLIGHT_STRENGTH" in terrain, "inexpensive material response must remain")
    hs = terrain.index("B0.3.6: refine the inexpensive material response")
    he = terrain.index("if (v_extra.b > 0.9)", hs)
    require("texture2D(" not in terrain[hs:he], "material response must not add texture reads")
    require("diffuse.rgb = mix(diffuse.rgb, v_fog.rgb, v_fog.a);" in terrain, "terrain fog blend must remain")

    packer = read("tool/pack.py")
    require("get_version_identity" in packer and "full_version_slug" in packer, "shared versioning must remain active")
    require("Keep the simple B0.x.y label aligned" in packer, "manual version override must remain aligned")
    build, check = read(".github/workflows/build.yml"), read(".github/workflows/build-check.yml")
    require("default: 'Android'" in build, "manual build default must be Android during implementation")
    for name, workflow in (("build.yml", build), ("build-check.yml", check)):
        require("tool/validate_pack.py" in workflow and "tool/versioning.py" in workflow and
                "tool/audit_duplicates.py" in workflow, f"{name} must run validation, versioning, and duplicate audit")
        require("steps.version.outputs.full_version_slug" in workflow, f"{name} must use canonical artifact labels")
    require("default: '7'" in build and "-v 7 --no-zip" in check, "builds must use manifest sub-version 7")
    require("b0.3.7-implementation" in check, "Android build-check must run on implementation branch")
    require("multiplatform:" not in check and "android:" in check, "implementation build-check must build Android only")
    print("B0.3.7 static regression checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"B0.3.7 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
