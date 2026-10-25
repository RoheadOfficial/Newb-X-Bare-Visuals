#!/usr/bin/env python3
"""Static regression checks for Newb X Bare Visuals B0.4.6 / Overworld O8."""
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
    require(pack.get("version") == [0, 4, 6], "manifest version must be [0, 4, 6]")
    require(pack.get("development_version") == "B0.4.6", "simple version must be B0.4.6")
    require(pack.get("minecraft_target_version") == "26.52", "declared Minecraft target must remain 26.52")
    require("Newb X Bare Visuals" in pack.get("name", ""), "pack identity must remain Newb X Bare Visuals")
    require("%w" in pack.get("description", "") and "%v" in pack.get("description", ""), "patch warning/version placeholders must remain")
    sys.path.insert(0, str(ROOT / "tool"))
    from versioning import get_version_identity
    display, target, full = get_version_identity(pack)
    require((display, target, full) == ("B0.4.6", "26.52", "B0.4.6.2652"), "canonical version identity must be correct")

    subpacks = pack.get("subpack", [])
    names = [item.get("define") for item in subpacks]
    require(names == ["DEFAULT", "POOTAYTOE", "BARE_VISUALS"], "O8 must expose Default, Pootaytoe, Bare Visuals only")
    profiles = {item["define"]: item for item in subpacks}
    require(not profiles["DEFAULT"].get("materials"), "Default must inherit root materials")
    base_materials = set(pack.get("materials", []))
    for name in ("POOTAYTOE", "BARE_VISUALS"):
        require(set(profiles[name].get("materials", [])) == base_materials, f"{name} must compile its own profile materials")
    require("EXPERIMENTAL" not in names, "Experimental must remain shelved for O8")

    cfg = read("src/newb/config.h")
    require("#define NL_TONEMAP_TYPE 4" in cfg and "#define NL_SATURATION 1.06" in cfg, "approved tone mapping and saturation must remain")
    require("#define NL_DISABLE_ALL_WAVING" in cfg, "global no-waving guard must be enabled")
    for macro in ("NL_WATER_WAVE", "NL_PLANTS_WAVE", "NL_LANTERN_WAVE", "NL_EXTRA_PLANTS_WAVE",
                  "NL_UNDERWATER_WAVE", "NL_CLOUD_SHADOW", "NL_CLOUDY_FOG", "NL_GROUND_REFL",
                  "NL_CLOUD_AURORA_REFLECTION", "NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH"):
        require(not re.search(rf"(?m)^\s*#define\s+{macro}\b", cfg), f"{macro} must not be enabled")
    require("#define NL_DISABLE_WATER_REFLECTIONS" in cfg, "water reflection calculations must be compiled out")
    require("#define NL_DISABLE_GROUND_REFLECTIONS" in cfg, "Always Reflection terrain path must be disabled")
    require("#define BOX_CLOUDS" in cfg and "#define NL_CLOUD_TYPE 0" in cfg, "vanilla cloud rendering must be active")
    require("#define NL_CLOUD0_THICKNESS 1.0" in cfg and "#define NL_CLOUD0_RAIN_THICKNESS 1.0" in cfg and "#define NL_CLOUD0_OPACITY 1.0" in cfg,
            "vanilla cloud plane thickness and opacity must not be artificially inflated")
    require("#define NL_WATER_TINT vec3(0.62,0.78,0.92)" in cfg, "O8 water palette must be soft blue")
    require("#define NL_WATER_STYLE_STRENGTH 0.42" in cfg and "#define NL_WATER_TEX_OPACITY 0.08" in cfg and "#define NL_WATER_TRANSPARENCY 0.85" in cfg, "O8 water clarity and color styling must remain active")
    require("#define NL_SKY_HORIZON_GLOW 0.0" in cfg, "custom horizon glow must be disabled")
    require(all(f"#ifdef {name}" in cfg for name in names), "all active profile blocks must exist")

    vertex = read("src/materials/RenderChunk/vertex.sc")
    require("if ((!isTree && fogColor.a > 0.001) || fogColor.a > 0.20 || env.rainFactor > 0.0)" in vertex,
            "foliage low-contribution sky-fog fast path must exist")
    require("float foliageFogAlpha = nlRenderFogFade(" in vertex and "env.rainFactor <= 0.0 && foliageFogAlpha <= 0.20" in vertex,
            "foliage must select the cheaper sky palette only in clear, low-fog scenes")
    require("skycol = nlFoliageSkyColors(env);" in vertex and "skycol = nlSkyColors(env);" in vertex,
            "full sky colors must remain for rain, fog, underwater, Nether, and End scenes")
    require(vertex.count("refl = nlRefl(color, skycol, env, viewDir, worldPos, tiledCpos, CameraPosition.xyz, torchColor, lit, camDis, FogAndDistanceControl.z, t);") == 2,
            "both non-water RenderChunk branches must call the reflection-free wet-ground path")
    require("Always run the reflection-free nlRefl branch so rain can still darken ground" in vertex,
            "reflection removal must not bypass wet-ground darkening and puddle variation")
    require("Alpha-tested foliage/billboards cannot display the horizontal terrain reflection mask" in vertex,
            "existing foliage reflection avoidance must remain")
    require("#if defined(NL_GLOW_SHIMMER) && !(defined(RENDER_AS_BILLBOARDS) || defined(SEASONS) || defined(ALPHA_TEST)" in vertex,
            "foliage must skip vertex glow-shimmer work")
    terrain = read("src/materials/RenderChunk/fragment.sc")
    require("diffuse.rgb = mix(diffuse.rgb, v_fog.rgb, v_fog.a);" in terrain, "terrain fog blend must remain")
    require("#if !defined(NL_DISABLE_WATER_REFLECTIONS) || !defined(NL_DISABLE_GROUND_REFLECTIONS)" in terrain,
            "reflection fragment work must compile out when both reflection systems are disabled")

    water = read("src/newb/functions/water.h")
    require("#ifdef NL_DISABLE_WATER_REFLECTIONS" in water and "return vec4(0.0, 0.0, 0.0, 0.0);" in water,
            "water reflection implementation must compile to a no-reflection fast path")
    require("color.rgb = vec3_splat(1.0);" in water, "water tint must be applied once in the fragment material path")
    require("nlRenderSky(skycol, env, viewDir, t, false)" in water, "disabled reflection path must preserve source behind compile-time fallback")

    sky = read("src/newb/functions/sky.h")
    require("nl_skycolor nlFoliageSkyColors(nl_environment env)" in sky,
            "low-cost clear-weather foliage ambient palette must exist")
    require("1.0 - smoothstep(-0.12, 0.12, env.dayFactor)" in sky, "sky day/night blend must be smooth")
    require("smoothstep(0.0, 1.0, env.rainFactor)" in sky, "sky weather blend must be smooth")
    require("horizonGlow" not in sky, "custom horizon glow must not override the vanilla-style sky gradient")

    lighting = read("src/newb/functions/lighting.h")
    require("if (!isTree || dawnFactor >= 0.02)" in lighting, "existing tree lighting fast path must remain")
    require("vec3 nlFoliageLighting(" in lighting, "dedicated lower-cost foliage lighting function must exist")
    require("if (isTree) {\n    light = nlFoliageLighting(" in vertex, "RenderChunk must route detected foliage through the dedicated fast path")
    foliage = lighting.split("vec3 nlFoliageLighting(", 1)[1].split("vec3 nlLighting(", 1)[0]
    require("NL_CLOUD_SHADOW" not in foliage and "sunAttenuation" in foliage, "foliage fast path must avoid cloud-shadow and spatial sun projection work")
    require("1.0 - smoothstep(-0.12, 0.12, env.dayFactor)" in lighting, "terrain/entity lighting must blend through twilight")

    detection = read("src/newb/functions/detection.h")
    require("float detectRain(" in detection and "val*val*(3.0 - 2.0*val)" in detection,
            "rain detection must transition smoothly from clear to wet weather")
    require("nl_environment nlDetectFoliageEnvironment(" in detection and "env.dayFactor = cos(2.0 * PI * TIME_OF_DAY);" in detection,
            "foliage-only environment path must avoid full sun/moon vector rotations")
    require("if (isTree && !foliageFast)" in vertex and "env = nlDetectEnvironment(TimeOfDay.x, FogColor.rgb, FogAndDistanceControl.xyz);" in vertex,
            "foliage must fall back to the full environment when sky rendering may be needed")
    fog = read("src/newb/functions/fog.h")
    require("smoothstep(0.0, 0.85" in fog and "exp(" not in fog and "rain*0.06" in fog,
            "low-cost restrained mist must remain")
    rain = read("src/newb/functions/rain.h")
    require("#ifdef NL_DISABLE_GROUND_REFLECTIONS" in rain and "NL_GROUND_RAIN_PUDDLES*fastRand" in rain and "color.rgb *= 1.0 - 0.4*wetness*env.rainFactor" in rain,
            "wet-ground darkening and puddle variation must survive reflection removal")
    require("refl = nlRefl(color, skycol, env, viewDir, worldPos, tiledCpos" in vertex,
            "the reflection-free wet-ground path must actually be invoked from RenderChunk")
    weather_material = read("src/materials/Weather/fragment.sc")
    require("B0.4.0: derive the subtle particle speck modulation from the existing texel" in weather_material,
            "lightweight weather particle path must remain active")
    clouds = read("src/materials/Clouds/vertex.sc")
    require("#if NL_CLOUD_TYPE == 0" in clouds, "vanilla Minecraft cloud path must remain compiled")
    require(not (ROOT / "assets/textures/environment/clouds.png").exists(),
            "vanilla cloud texture must not be overridden by a pack-bundled clouds.png")
    sky_material = read("src/materials/Sky/fragment.sc")
    require("renderAurora(auroraPos" in sky_material and "skyColor += aurora.rgb" in sky_material, "night aurora must remain after restoring vanilla clouds")
    weather = read("src/materials/Weather/fragment.sc")
    require("texture2D(s_WeatherTexture, UVOffsetAndScale.xy" not in weather and "B0.4.0: derive the subtle particle speck modulation" in weather,
            "weather particles must not restore the redundant texture fetch")

    packer = read("tool/pack.py")
    require("get_version_identity" in packer and "full_version_slug" in packer, "shared versioning must remain")
    build, check = read(".github/workflows/build.yml"), read(".github/workflows/build-check.yml")
    require("default: 'Android'" in build, "manual build default must be Android")
    for name, workflow in (("build.yml", build), ("build-check.yml", check)):
        require("tool/validate_pack.py" in workflow and "tool/versioning.py" in workflow and "tool/audit_duplicates.py" in workflow,
                f"{name} validation/versioning steps must remain")
        require("steps.version.outputs.full_version_slug" in workflow, f"{name} artifact must use canonical version slug")
    require("default: '6'" in build and "-v 6" in check, "Android artifact manifest override must be 6")
    require("b0.4.6-o8-performance-overhaul" in check and "multiplatform:" not in check and "android:" in check,
            "O8 CI must target the Android implementation branch")
    print("B0.4.6 / O8 static regression checks passed.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, StopIteration, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"B0.4.6 validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
