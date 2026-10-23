#!/usr/bin/env python3
"""Current-source regression checks for Newb X Bare Visuals."""
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
    require("#define NL_TONEMAP_TYPE 4" in cfg, "preserve the B0.3.6 ACES tone-mapping pipeline")
    require("#define NL_SATURATION 1.04" in cfg, "preserve the approved B0.3.6 saturation")
    require("#define NL_VANILLA_WATER" in cfg, "vanilla water path must remain enabled")
    for required in (
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
            "B0.3.6 horizon blend must remain present")
    fog = read("src/newb/functions/fog.h")
    require("12.0 - 11.0*FOG_COLOR.g" in fog and "rain*0.12" in fog,
            "restrained mist and rain atmosphere must remain")
    lighting = read("src/newb/functions/lighting.h")
    require(lighting.count("*NL_SKY_AMBIENT_STRENGTH") >= 2,
            "terrain and entity lighting must both use the balanced ambient response")
    clouds = read("src/newb/functions/clouds.h")
    require("if (dayFactor >= 0.0)" in clouds, "daytime aurora early-out must remain")
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
    require("get_version_identity" in packer, "pack builder must use the shared versioning logic")
    require("full_version_slug" in packer, "artifact naming must include the advanced version")
    require("Keep the simple B0.x.y label aligned" in packer,
            "manual manifest patch overrides must not create conflicting version labels")
    for workflow_path in (".github/workflows/build.yml", ".github/workflows/build-check.yml"):
        workflow = read(workflow_path)
        require("tool/validate_pack.py" in workflow, f"{workflow_path} must run the shared validator")
        require("tool/versioning.py" in workflow, f"{workflow_path} must emit canonical version outputs")
        require("tool/audit_duplicates.py" in workflow, f"{workflow_path} must audit duplicate files")
        require("steps.version.outputs.full_version_slug" in workflow,
                f"{workflow_path} artifact names must use the canonical full version")
    build = read(".github/workflows/build.yml")
    check = read(".github/workflows/build-check.yml")
    require("default: '7'" in build, "manual build default must use manifest sub-version 7")
    require("-v 7 --no-zip" in check, "build-check must compile manifest sub-version 7")
    require("b0.3.7-polish-performance-compat" in check,
            "build-check must run on the B0.3.7 development branch")

    print("B0.3.7 static regression checks passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"B0.3.7 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
