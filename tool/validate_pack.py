#!/usr/bin/env python3
"""Static regression checks for Newb X Bare Visuals B0.4.1 forest performance / Overworld O6.0."""
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
    require(pack.get("version") == [0, 4, 1], "manifest version must be [0, 4, 1]")
    require(pack.get("development_version") == "B0.4.1", "simple version must be B0.4.1")
    require(pack.get("minecraft_target_version") == "26.52", "declared Minecraft target must remain 26.52")
    require("Newb X Bare Visuals" in pack.get("name", ""), "pack identity must remain Newb X Bare Visuals")
    require("%w" in pack.get("description", "") and "%v" in pack.get("description", ""), "patch warning/version placeholders must remain")
    sys.path.insert(0, str(ROOT / "tool"))
    from versioning import get_version_identity
    display, target, full = get_version_identity(pack)
    require((display, target, full) == ("B0.4.1", "26.52", "B0.4.1.2652"), "canonical version identity must be correct")
    subpacks = pack.get("subpack", [])
    names = [item.get("define") for item in subpacks]
    require(names == ["DEFAULT", "POOTAYTOE", "BARE_VISUALS", "EXPERIMENTAL"], "profile order must remain stable")
    profiles = {item["define"]: item for item in subpacks}
    require(not profiles["DEFAULT"].get("materials"), "Default must inherit root materials")
    base_materials = set(pack.get("materials", []))
    for name in ("POOTAYTOE", "BARE_VISUALS", "EXPERIMENTAL"):
        require(set(profiles[name].get("materials", [])) == base_materials, f"{name} must compile its own profile materials")
    require("fake terrain shadows" in profiles["EXPERIMENTAL"]["description"].lower(), "Experimental description must remain accurate")
    cfg = read("src/newb/config.h")
    require("#define NL_TONEMAP_TYPE 4" in cfg and "#define NL_SATURATION 1.04" in cfg, "preserve approved color/tone mapping")
    require("#define NL_DISABLE_ALL_WAVING" in cfg, "global no-waving guard must be enabled")
    for macro in ("NL_WATER_WAVE","NL_PLANTS_WAVE","NL_LANTERN_WAVE","NL_EXTRA_PLANTS_WAVE","NL_UNDERWATER_WAVE","NL_CLOUD_SHADOW","NL_CLOUDY_FOG","NL_VANILLA_WATER"):
        require(not re.search(rf"(?m)^\s*#define\s+{macro}\b", cfg), f"{macro} must not be enabled")
    require("#define NL_CLOUD_AURORA_REFLECTION" in cfg, "Newb reflection detail must remain enabled")
    require("#define NL_GROUND_REFL 0.18" in cfg, "terrain Always Reflection must stay enabled")
    require("#define NL_GROUND_REFL_MAX_DISTANCE 22.0" in cfg, "base terrain reflection must retain a bounded range")
    require(" #define NL_GROUND_REFL_MAX_DISTANCE 16.0" in cfg and "#define NL_GROUND_REFL_MAX_DISTANCE 22.0" in cfg and "#define NL_GROUND_REFL_MAX_DISTANCE 20.0" in cfg, "profile-specific terrain reflection limits must remain tuned")
    for distance in ("18.0","12.0","20.0","14.0"): 
        require(f"#define NL_WATER_DETAIL_REFLECTION_DISTANCE {distance}" in cfg, "each profile must have a reflection detail range")
    for required in ("#define NL_MIST_DENSITY 0.12","#define NL_RAIN_MIST_OPACITY 0.08","#define NL_WEATHER_SPECK 0.18","#define NL_CLOUD2_STEPS 2","#define NL_WATER_TINT vec3(0.90,0.94,0.93)","#define NL_WATER_STYLE_STRENGTH 0.42","#define NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH 0.10"):
        require(required in cfg, f"missing O6.0 configuration: {required}")
    require(all(f"#ifdef {name}" in cfg for name in names), "all profile blocks must exist")
    fog = read("src/newb/functions/fog.h")
    require("smoothstep(0.0, 0.85" in fog and "exp(" not in fog and "rain*0.06" in fog, "mist must use the low-cost restrained curve")
    lighting = read("src/newb/functions/lighting.h")
    require("if (!isTree || dawnFactor >= 0.02)" in lighting, "tree lighting fast path must exist")
    require("sunLightTint(env.dayFactor, env.rainFactor, dawnFactor, nightFactor)" in lighting, "sun-light factors must be reused")
    require("#if defined(NL_UNDERWATER_WAVE) && !defined(NL_DISABLE_ALL_WAVING)" in lighting, "underwater waving must be globally blocked")
    clouds = read("src/newb/functions/clouds.h")
    require("if (dayFactor >= 0.0)" in clouds, "daytime aurora early-out must remain")
    glow = read("src/newb/functions/glow.h")
    for unused in ("vec3 c1 =","vec3 c3 =","vec3 c5 =","vec3 c7 ="):
        require(unused not in glow, f"unused glow sample remains: {unused}")
    water = read("src/newb/functions/water.h")
    require("camDist < NL_WATER_DETAIL_REFLECTION_DISTANCE" in water and "nlRenderSky(skycol, env, viewDir, t, false)" in water, "base water reflection and detail gate must remain")
    require("NL_WATER_FULL_REFLECTION_DISTANCE" in water and "mix(skycol.horizon, skycol.zenith, reflectionHeight)" in water, "far water must retain a cheaper sky-gradient reflection")
    require("#define NL_WATER_FULL_REFLECTION_DISTANCE 42.0" in cfg and "#define NL_WATER_FULL_REFLECTION_DISTANCE 24.0" in cfg and "#define NL_WATER_FULL_REFLECTION_DISTANCE 48.0" in cfg and "#define NL_WATER_FULL_REFLECTION_DISTANCE 32.0" in cfg, "all profiles must define the full water reflection range")
    ground = read("src/newb/functions/rain.h")
    require("camDist < NL_WATER_DETAIL_REFLECTION_DISTANCE" in ground, "ground aurora detail must be distance-gated")
    vertex = read("src/materials/RenderChunk/vertex.sc")
    require("!defined(NL_DISABLE_ALL_WAVING)" in vertex and "refl = nlWater(color, worldPos" in vertex, "wave guard and custom water path must be active")
    require("NL_VANILLA_WATER" not in vertex, "vanilla-water bypass must not disable reflection")
    require("Alpha-tested foliage/billboards cannot display the horizontal terrain reflection mask" in vertex, "foliage must skip unused terrain-reflection work")
    require("defined(ALPHA_TEST))" in vertex and "defined(ALPHA_TEST)" in vertex.split("float shimmer", 1)[0].split("#if defined(NL_GLOW_SHIMMER)", 1)[-1], "foliage must skip vertex glow-shimmer work")
    require("fogColor.a > 0.001 || env.rainFactor > 0.0" in vertex, "nearby clear-weather terrain must skip unused sky fog calculations")
    terrain = read("src/materials/RenderChunk/fragment.sc")
    require("waterLuma * NL_WATER_TINT" in terrain and "diffuse.rgb = mix(diffuse.rgb, v_fog.rgb, v_fog.a);" in terrain, "water palette and fog blend must remain")
    weather = read("src/materials/Weather/fragment.sc")
    require("texture2D(s_WeatherTexture, UVOffsetAndScale.xy" not in weather and "B0.4.0: derive the subtle particle speck modulation" in weather, "weather particles must not make the redundant second texture fetch")
    require("glintColor.a <= 0.001" in glow, "transparent actor glint must skip glint texture sampling")
    require("#elif defined(ALPHA_TEST) || defined(RENDER_AS_BILLBOARDS)" in terrain and "glowDetect(diffuse) * NL_GLOW_TEX" in terrain,
            "alpha-tested foliage must skip extra halo taps but retain base emissive glow")
    packer = read("tool/pack.py")
    require("get_version_identity" in packer and "full_version_slug" in packer and "Keep the simple B0.x.y label aligned" in packer, "shared versioning must remain")
    build, check = read(".github/workflows/build.yml"), read(".github/workflows/build-check.yml")
    require("default: 'Android'" in build, "manual build default must be Android")
    for name, workflow in (("build.yml",build),("build-check.yml",check)):
        require("tool/validate_pack.py" in workflow and "tool/versioning.py" in workflow and "tool/audit_duplicates.py" in workflow and "steps.version.outputs.full_version_slug" in workflow, f"{name} validation/artifact setup must remain")
    require("default: '0'" in build and "-v 0" in check and "--no-zip" not in check and "path: ./build/*.mcpack" in check, "workflow must publish a directly installable B0.4.1 mcpack")
    require("b0.4.1-forest-performance" in check and "b0.4.0-performance-fixes" in check and "multiplatform:" not in check and "android:" in check, "implementation checks must target Android on the B0.4.1 branch")
    print("B0.4.1 forest performance static regression checks passed.")
    return 0
if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"B0.4.0 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
