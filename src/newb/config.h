#ifndef NL_CONFIG_H
#define NL_CONFIG_H

/*
  NEWB SHADER MAIN CONFIG
  This part contains base configuration options for the shader.

  TOGGLES
  - If [toggle] is mentioned, then
    options can be commented to disable (by adding '//')
  - eg: #define PLANTS_WAVE    -> this is ON
        //#define PLANTS_WAVE  -> this is OFF

  COLOR VALUES
  - Color format: vec3(red,green,blue)
  - 1.0 means 100%, 0.0 means 0%
  - eg: vec3(1.0,1.0,0.0) = yellow

  VALUES
  - Values must be decimal
  - eg. 32 is wrong, 32.0 is correct

  TYPES
  - Should be integer. options to choose will be mentioned there
  - eg: #define NL_CLOUD_TYPE 2

  Remember to rebuild the shader after making changes.
*/

/* Color correction */
#define NL_TONEMAP_TYPE 4              // B0.3.6: ACES tone mapping for a more cinematic highlight roll-off
#define NL_GAMMA 1.36                  // B0.3.6: keep midtones readable with the ACES curve
//#define NL_EXPOSURE 1.3              // [toggle] 0.5 dark ~ 3.0 bright
#define NL_SATURATION 1.06            // B0.4.5: a small, natural saturation lift for a cozier palette
//#define NL_TINT                      // [toggle] enable light/dark tone tinting
#define NL_TINT_LOW  vec3(0.3,0.5,1.4) // color tint for dark tone
#define NL_TINT_HIGH vec3(1.4,0.7,0.3) // color tint for light tone

/* Lighting */
#define NL_SUNLIGHT_INTENSITY   3.16 // B0.3.6: clearer directional light for stronger terrain depth
#define NL_TORCHLIGHT_INTENSITY 1.0  // 0.5 weak ~ 3.0 bright
#define NL_SHADOW_INTENSITY     0.80 // Add gentle depth while keeping shadow detail readable
#define NL_MIN_LIGHTING_BOOST   1.12 // B0.3.6: retain readability while reducing flat ambient lift
//#define NL_BLINKING_TORCH  // [toggle] flickering light
//#define NL_CLOUD_SHADOW      // Disabled for the Android performance target

/* Ambient light for nether/end */
#define NL_NETHER_AMBIENT vec3(3.0,2.16,1.89)
#define NL_END_AMBIENT    vec3(1.98,1.25,2.3)

/* Sun/moon light color */
#define NL_DAWN_SUNLIGHT_COL   vec3(1.0,0.62,0.40) // Warm sunrise without orange oversaturation
#define NL_NOON_SUNLIGHT_COL   vec3(1.0,0.94,0.84) // Warm-neutral daytime light
#define NL_NIGHT_MOONLIGHT_COL vec3(0.035,0.055,0.12) // Gentle night readability, not daytime brightness

/* Torch colors */
#define NL_OVERWORLD_TORCH_COL  vec3(1.0,0.52,0.18)
#define NL_UNDERWATER_TORCH_COL vec3(1.0,0.52,0.18)
#define NL_NETHER_TORCH_COL     vec3(1.0,0.52,0.18)
#define NL_END_TORCH_COL        vec3(1.0,0.52,0.18)

/* Fog */
#define NL_FOG 1.0                // [toggle] 0.1 subtle ~ 1.0 blend with sky completely
#define NL_MIST_DENSITY 0.12      // O6.0: less nearby haze; distance fog remains active
#define NL_RAIN_MIST_OPACITY 0.08 // O6.0: retain rain atmosphere with less screen haze
// NL_CLOUDY_FOG disabled in O6.0: its per-vertex sine overlay added cost and near haze.

/* Sky */
#define NL_SKY_VOID_FACTOR     0.5
#define NL_SKY_VOID_DARKNESS   0.3
#define NL_SKY_RAIN_MIX_FACTOR 0.86
#define NL_SKY_HORIZON_GLOW 0.16       // B0.3.6: soft, readable horizon band without a heavy glow pass
#define NL_SKY_AMBIENT_STRENGTH 0.90  // B0.3.6: balance sky fill against directional terrain shading

/* Sky colors - zenith=top, horizon=bottom */
#define NL_DAWN_ZENITH_COL   vec3(0.22,0.38,0.60)
#define NL_DAWN_HORIZON_COL  vec3(1.0,0.62,0.42)
#define NL_DAWN_EDGE_COL     vec3(1.12,0.76,0.60)
#define NL_DAY_ZENITH_COL    vec3(0.32,0.61,0.92) // Softer blue, closer to a natural vanilla-plus sky
#define NL_DAY_HORIZON_COL   vec3(0.78,0.88,0.97)
#define NL_DAY_EDGE_COL      vec3(0.93,0.97,1.0)
#define NL_NIGHT_ZENITH_COL  vec3(0.020,0.034,0.080)
#define NL_NIGHT_HORIZON_COL vec3(0.040,0.060,0.110)
#define NL_NIGHT_EDGE_COL    vec3(0.055,0.080,0.13)
#define NL_RAIN_ZENITH_COL   vec3(0.36,0.42,0.50)
#define NL_RAIN_HORIZON_COL  vec3(0.53,0.59,0.66)

#define NL_END_ZENITH_COL    vec3(0.08,0.001,0.1)
#define NL_END_HORIZON_COL   vec3(0.6,0.02,0.6)


/* Rainbow */
//#define NL_RAINBOW           // Shelved: avoid additional dramatic sky events
#define NL_RAINBOW_CLEAR 0.0 // 0.3 subtle ~ 1.0 bright during clear weather
#define NL_RAINBOW_RAIN  0.4 // 0.3 subtle ~ 1.0 bright during rain weather

/* Light bloom / emissive glow */
#define NL_GLOW_TEX 2.3           // Existing emissive texture glow
#define NL_GLOW_LEAK 0.08         // B0.2.6: subtle, local bloom-like bleed (not screen-space bloom)
#define NL_GLOW_SHIMMER 0.8       // [toggle] 0.1 subtle ~ 1.0 100% shimmer
#define NL_GLOW_SHIMMER_SPEED 0.9 // 0.5 slow - 2.0 fast
//#define NL_GLOW_LEAK 0.6        // [toggle] 0.08 subtle ~ 1.0 100% brightness of NL_GLOW_TEX

/* Waving — globally disabled; profile overrides cannot re-enable it. */
#define NL_DISABLE_ALL_WAVING
//#define NL_PLANTS_WAVE 0.030   // Shelved: vegetation waving disabled
//#define NL_LANTERN_WAVE 0.080  // Shelved: lantern waving disabled
#define NL_WAVE_SPEED 2.8      // 0.5 slow wave ~ 5.0 very fast wave
//#define NL_EXTRA_PLANTS_WAVE // [toggle] !dont use! wave using texture coords (1.21.0 vanilla 2048x1024)
#define NL_WAVE_RANGE 9.0      // Keep plant/lantern movement close to the player for dense-scene performance

/* Water and Always Reflection */
// O6.0: custom Newb water and base sky reflection are active; no vanilla-water bypass.
#define NL_WATER_TRANSPARENCY 0.92 // Keep the surface readable while preserving depth
#define NL_WATER_BUMP 0.0           // Flat surface: no water-wave distortion
#define NL_WATER_WAVE_SPEED  0.8    // Retained for underwater caustic timing
#define NL_WATER_TEX_OPACITY 0.3    // Retain recognizable vanilla water texture
#define NL_WATER_BLUE_REDUCTION 0.95 // Keep the existing restrained blue-channel correction
//#define NL_WATER_WAVE             // No water displacement or animated waves
//#define NL_WATER_REFL_MASK        // Keep sky reflections broad and natural
#define NL_WATER_TINT vec3(0.90,0.94,0.93) // Muted mineral-gray water, not a strong blue/green wash
#define NL_WATER_STYLE_STRENGTH 0.38 // Give water a distinct, restrained material identity
#define NL_WATER_DETAIL_REFLECTION_DISTANCE 18.0 // B0.4.0: limit extra aurora detail; base sky reflection stays active
#define NL_WATER_FULL_REFLECTION_DISTANCE 32.0 // Full sky shading nearby; use a cheap sky-gradient reflection farther out
#define NL_GROUND_REFL 0.18         // Restrained terrain reflection; water keeps its own sky reflection
#define NL_GROUND_REFL_DISTANCE 0.20 // B0.4.0: preserve nearby Always Reflection with less far-field work
#define NL_GROUND_REFL_MAX_DISTANCE 22.0 // B0.4.0: terrain reflection remains active at closer ranges
#define NL_MATERIAL_HIGHLIGHT_STRENGTH 0.016 // B0.3.6: restrained material separation without extra texture reads
#define NL_CLOUD_AURORA_REFLECTION // Keep Newb's sky/aurora reflection detail, with distance/night gating

/* Underwater */
#define NL_UNDERWATER_BRIGHTNESS 0.8         // 0.0 dark ~ 3.0 bright
#define NL_CAUSTIC_INTENSITY 1.9             // 0.5 weak ~ 5.0 bright
//#define NL_UNDERWATER_WAVE 0.1               // Underwater camera wave disabled
#define NL_UNDERWATER_STREAKS 1.0            // [toggle] 0.8 subtle - 2.0 bright streaks from top
#define NL_UNDERWATER_TINT vec3(0.9,1.0,0.9) // fog tint color when underwater

/* Cloud type */
//#define BOX_CLOUDS             // Disabled; keep custom clouds rather than vanilla/box clouds
#define NL_CLOUD_TYPE 1          // B0.4.5: lightweight soft procedural clouds; Types 2 and 3 shelved

/* Vanilla cloud settings - make sure to remove clouds.png when using this */
#define NL_CLOUD0_THICKNESS 2.1      // 0.5 slim ~ 8.0 fat
#define NL_CLOUD0_RAIN_THICKNESS 4.0 // 0.5 slim ~ 8.0 fat
#define NL_CLOUD0_OPACITY 0.9        // 0.0 invisible ~ 1.0 opaque
#define NL_CLOUD0_MULTILAYER         // [toggle] extra cloud layer

/* Soft cloud settings */
#define NL_CLOUD1_SCALE vec2(0.016, 0.022) // 0.003 large ~ 0.2 tiny
#define NL_CLOUD1_DEPTH 1.3                // 0.0 no bump ~ 10.0 large bumps
#define NL_CLOUD1_SPEED 0.04               // 0.0 static ~ 0.4 fast moving
#define NL_CLOUD1_DENSITY 0.54             // 0.1 less clouds ~ 0.8 more clouds
#define NL_CLOUD1_OPACITY 0.9              // 0.0 invisible ~ 1.0 opaque

/* Rounded cloud settings */
#define NL_CLOUD2_THICKNESS 2.3            // B0.3.6: fuller rounded cloud bodies at the same sample count
#define NL_CLOUD2_RAIN_THICKNESS 2.8       // Slightly fuller cloud cover in rain
#define NL_CLOUD2_STEPS 2                  // B0.4.0: two density samples per rounded-cloud fragment
#define NL_CLOUD2_SCALE vec2(0.033, 0.033) // 0.003 large ~ 0.3 tiny
#define NL_CLOUD2_SHAPE vec2(0.44, 0.34)   // B0.3.6: rounder cloud edges without adding ray samples
#define NL_CLOUD2_DENSITY 25.0             // 1.0 blurry ~ 100.0 sharp
#define NL_CLOUD2_VELOCITY 0.8             // 0.0 static ~ 4.0 very fast
//#define NL_CLOUD2_LAYER2                      // [toggle] extra cloud layer
#define NL_CLOUD2_LAYER2_OFFSET 143.0           // 30.0 near ~ 300.0 very high
#define NL_CLOUD2_LAYER2_THICKNESS 2.5          // 0.7 slim ~ 5.0 fat
#define NL_CLOUD2_LAYER2_RAIN_THICKNESS 3.0     // 0.7 slim ~ 5.0 fat
#define NL_CLOUD2_LAYER2_STEPS 3                // 3 low quality ~ 16 high quality
#define NL_CLOUD2_LAYER2_SCALE vec2(0.03, 0.03) // 0.003 large ~ 0.3 tiny
#define NL_CLOUD2_LAYER2_SHAPE vec2(0.5, 0.4)   // 0.0 round ~ 1.0 box vec2(horizontal shape, vertical shape)
#define NL_CLOUD2_LAYER2_DENSITY 25.0           // 1.0 blurry ~ 100.0 sharp
#define NL_CLOUD2_LAYER2_VELOCITY 0.8           // 0.0 static ~ 4.0 very fast

/* Realistic cloud settings */
#define NL_CLOUD3_SCALE vec2(0.03, 0.03) // 0.003 large ~ 1.0 tiny
#define NL_CLOUD3_SPEED 0.005            // 0.0 static ~ 4.0 fast moving
#define NL_CLOUD3_SHADOW 0.9             // 0.1 subtle ~ 1.0 dark
#define NL_CLOUD3_SHADOW_OFFSET 0.3      // 0.05 minimal ~ 1.0 large

/* Aurora settings */
#define NL_AURORA 0.90          // [toggle] restrained Legacy-inspired night aurora
#define NL_AURORA_VELOCITY 0.03 // 0.0 static ~ 0.3 very fast
#define NL_AURORA_SCALE 0.04    // 0.002 large ~ 0.4 tiny
#define NL_AURORA_WIDTH 0.22    // 0.04 thin line ~ 0.4 thick lines
#define NL_AURORA_COL1 vec3(0.1,1.0,0.0)
#define NL_AURORA_COL2 vec3(0.1,0.0,1.0)


/* Shooting star */
//#define NL_SHOOTING_STAR 1.0      // Shelved: Always Reflection keeps aurora as the Legacy sky tribute
#define NL_SHOOTING_STAR_PERIOD 6.0 // 0.4 fast ~ 12.0 slow (12 secs)
#define NL_SHOOTING_STAR_DELAY 64.0 // 0.0 no delay ~ 100.0 long time (100 secs)

/* Galaxy */
//#define NL_GALAXY_STARS 2.0           // [toggle] 0.1 dim - 4.0 bright
#define NL_GALAXY_VIBRANCE 0.7          // 0.0 white - 1.0 colorful
#define NL_GALAXY_SPEED 0.03            // 0.01 slow motion - 0.2 fast motion
#define NL_GALAXY_DAY_VISIBILITY 0.0    // 0.0 invisible - 1.0 visible

/* Chunk loading slide in animation */
//#define NL_CHUNK_LOAD_ANIM 100.0 // [toggle] -600.0 fall from top ~ 600.0 rise from bottom

/* Sun/Moon */
#define NL_SUN_SIZE  1.0           // 0.3 tiny ~ 4.0 massive
#define NL_MOON_SIZE 1.0           // 0.3 tiny ~ 4.0 massive
#define NL_SUN_PATH_YAW    15.0 //
#define NL_MOON_PATH_YAW   17.0 //
#define NL_SUN_PATH_TILT   31.0 //
#define NL_MOON_PATH_TILT -28.0 //
#define NL_SUN_TILT        45.0 // 0.0 no tilt ~ 90.0 tilt of 90 degrees
#define NL_MOON_TILT       45.0 // 0.0 no tilt ~ 90.0 tilt of 90 degrees

#define NL_GROUND_RAIN_WETNESS 0.70 // Visible but restrained rain wetness
#define NL_GROUND_RAIN_PUDDLES 0.35 // Subtle puddle variation

/* Entity (Actor, ItemInHand) */
#define NL_ENTITY_BRIGHTNESS     0.65 // 0.1 dark ~ 1.6 bright
//#define NL_ENTITY_EDGE_HIGHLIGHT 0.41 // Disabled for a lighter mob-heavy rendering path

/* Weather particles */
#define NL_WEATHER_SPECK 0.18        // B0.4.0: subtler analytic particle modulation; spawn count is engine-controlled
#define NL_WEATHER_RAIN_SLANT 3.0    // Moderate rain slant
#define NL_WEATHER_PARTICLE_SIZE 1.0 // 0.5 tiny ~ 4.0 large

/* Lava effects */
#define NL_LAVA_NOISE            // [toggle] darken lava in certain regions
//#define NL_LAVA_NOISE_BUMP 0.2 // [toggle] 0.1 subtle ~ 0.8 massive waves
#define NL_LAVA_NOISE_SPEED 0.2  // 0.0 still ~ 0.8 fast

/*
  NEWB SHADER SUBPACK CONFIG
  This part contains custom configuration options for each subpack.

  If a value is already defined,
  then you must undefine it before modifying:
  eg: #undef OPTION_NAME

  Subpack names and flags are inside `pack_config.toml`.
  Build tool will enable corresponding flags when compiling.
*/

#ifdef POOTAYTOE
  // Pootaytoe: performance-first settings; Cloud Type 1 is shared across all profiles.
  #undef NL_GROUND_REFL
  #define NL_GROUND_REFL 0.10
  #undef NL_GROUND_REFL_DISTANCE
  #define NL_GROUND_REFL_DISTANCE 0.13
  #undef NL_GROUND_REFL_MAX_DISTANCE
  #define NL_GROUND_REFL_MAX_DISTANCE 16.0
  #undef NL_WATER_DETAIL_REFLECTION_DISTANCE
  #define NL_WATER_DETAIL_REFLECTION_DISTANCE 12.0
  #undef NL_WATER_FULL_REFLECTION_DISTANCE
  #define NL_WATER_FULL_REFLECTION_DISTANCE 20.0
  #undef NL_SKY_HORIZON_GLOW
  #define NL_SKY_HORIZON_GLOW 0.10
  #undef NL_SKY_AMBIENT_STRENGTH
  #define NL_SKY_AMBIENT_STRENGTH 0.86
  #undef NL_GLOW_LEAK
  #undef NL_GLOW_SHIMMER
  #undef NL_LAVA_NOISE
  #undef NL_WEATHER_SPECK
  #undef NL_UNDERWATER_STREAKS
  #undef NL_RAIN_MIST_OPACITY
  #define NL_RAIN_MIST_OPACITY 0.06
  #undef NL_AURORA
  #define NL_AURORA 0.45
  #undef NL_MATERIAL_HIGHLIGHT_STRENGTH
  #undef NL_PLANTS_WAVE
  #undef NL_LANTERN_WAVE
  #undef NL_ENTITY_EDGE_HIGHLIGHT
#endif

#ifdef DEFAULT
  // Default: preserve the full established effects with B0.2.9-style terrain optimizations.
  #undef NL_GROUND_REFL_DISTANCE
  #define NL_GROUND_REFL_DISTANCE 0.20
  #undef NL_GROUND_REFL_MAX_DISTANCE
  #define NL_GROUND_REFL_MAX_DISTANCE 22.0
  #undef NL_WATER_DETAIL_REFLECTION_DISTANCE
  #define NL_WATER_DETAIL_REFLECTION_DISTANCE 18.0
  #undef NL_WATER_FULL_REFLECTION_DISTANCE
  #define NL_WATER_FULL_REFLECTION_DISTANCE 42.0
  #undef NL_SKY_HORIZON_GLOW
  #define NL_SKY_HORIZON_GLOW 0.16
  #undef NL_SKY_AMBIENT_STRENGTH
  #define NL_SKY_AMBIENT_STRENGTH 0.90
  #undef NL_WEATHER_SPECK
  #define NL_WEATHER_SPECK 0.18
#endif

#ifdef BARE_VISUALS
  // Bare Visuals: stronger cozy dawn/sunset identity, with a bounded reflection path and subtle highlights.
  #undef NL_GROUND_REFL_DISTANCE
  #define NL_GROUND_REFL_DISTANCE 0.19
  #undef NL_GROUND_REFL_MAX_DISTANCE
  #define NL_GROUND_REFL_MAX_DISTANCE 22.0
  #undef NL_WATER_DETAIL_REFLECTION_DISTANCE
  #define NL_WATER_DETAIL_REFLECTION_DISTANCE 20.0
  #undef NL_WATER_FULL_REFLECTION_DISTANCE
  #define NL_WATER_FULL_REFLECTION_DISTANCE 38.0
  #undef NL_SKY_HORIZON_GLOW
  #define NL_SKY_HORIZON_GLOW 0.24
  #undef NL_SKY_AMBIENT_STRENGTH
  #define NL_SKY_AMBIENT_STRENGTH 0.98
  #undef NL_MATERIAL_HIGHLIGHT_STRENGTH
  #define NL_MATERIAL_HIGHLIGHT_STRENGTH 0.024
  #undef NL_DAWN_SUNLIGHT_COL
  #define NL_DAWN_SUNLIGHT_COL vec3(1.0,0.68,0.46)
  #undef NL_DAWN_ZENITH_COL
  #define NL_DAWN_ZENITH_COL vec3(0.24,0.38,0.58)
  #undef NL_DAWN_HORIZON_COL
  #define NL_DAWN_HORIZON_COL vec3(1.0,0.66,0.49)
  #undef NL_DAWN_EDGE_COL
  #define NL_DAWN_EDGE_COL vec3(1.05,0.78,0.63)
  #undef NL_DAY_ZENITH_COL
  #define NL_DAY_ZENITH_COL vec3(0.30,0.54,0.84)
  #undef NL_DAY_HORIZON_COL
  #define NL_DAY_HORIZON_COL vec3(0.76,0.87,0.96)
  #undef NL_DAY_EDGE_COL
  #define NL_DAY_EDGE_COL vec3(0.91,0.95,1.0)
  #undef NL_WEATHER_SPECK
  #define NL_WEATHER_SPECK 0.18
#endif

#ifdef EXPERIMENTAL
  // Experimental only: reuse existing terrain vertex-lighting gradients for lightweight fake shading.
  // This does not create genuine tree-cast or entity shadows.
  #undef NL_WATER_DETAIL_REFLECTION_DISTANCE
  #define NL_WATER_DETAIL_REFLECTION_DISTANCE 14.0
  #undef NL_WATER_FULL_REFLECTION_DISTANCE
  #define NL_WATER_FULL_REFLECTION_DISTANCE 26.0
  #undef NL_GROUND_REFL_DISTANCE
  #define NL_GROUND_REFL_DISTANCE 0.18
  #undef NL_GROUND_REFL_MAX_DISTANCE
  #define NL_GROUND_REFL_MAX_DISTANCE 20.0
  #undef NL_CLOUD2_STEPS
  #define NL_CLOUD2_STEPS 2
  #undef NL_WEATHER_SPECK
  #define NL_WEATHER_SPECK 0.18
  #define NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH 0.10
#endif

#ifdef NO_WAVE_NO_FOG
  #define NO_WAVE
  #define NO_FOG
#endif

#ifdef NO_FOG
  #undef NL_FOG
#endif

#ifdef NO_WAVE
  #undef NL_PLANTS_WAVE
  #undef NL_LANTERN_WAVE
  #undef NL_UNDERWATER_WAVE
  #undef NL_WATER_WAVE
  #undef NL_RAIN_MIST_OPACITY
#endif

#ifdef CHUNK_ANIM
  #define NL_CHUNK_LOAD_ANIM 100.0
#endif

#ifdef BOX_CLOUDS
  #undef NL_CLOUD_TYPE
  #define NL_CLOUD_TYPE 0
  #undef NL_CLOUD_SHADOW
#endif

#endif
