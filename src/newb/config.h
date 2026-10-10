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
#define NL_TONEMAP_TYPE 3              // 1:Exponential, 2:Reinhard, 3:Extended Reinhard, 4:ACES
#define NL_GAMMA 1.33                  // 0.3 low ~ 2.0 high
//#define NL_EXPOSURE 1.3              // [toggle] 0.5 dark ~ 3.0 bright
#define NL_SATURATION 1.08            // B0.2.2: natural warm-vanilla color without oversaturation
//#define NL_TINT                      // [toggle] enable light/dark tone tinting
#define NL_TINT_LOW  vec3(0.3,0.5,1.4) // color tint for dark tone
#define NL_TINT_HIGH vec3(1.4,0.7,0.3) // color tint for light tone

/* Lighting */
#define NL_SUNLIGHT_INTENSITY   3.15 // Warm, balanced direct sunlight
#define NL_TORCHLIGHT_INTENSITY 1.0  // 0.5 weak ~ 3.0 bright
#define NL_SHADOW_INTENSITY     0.74 // Preserve visible terrain depth without crushing shadows
#define NL_MIN_LIGHTING_BOOST   1.30 // Keep dark areas readable while restoring lighting contrast
//#define NL_BLINKING_TORCH  // [toggle] flickering light
//#define NL_CLOUD_SHADOW      // Disabled for the Android performance target

/* Ambient light for nether/end */
#define NL_NETHER_AMBIENT vec3(3.0,2.16,1.89)
#define NL_END_AMBIENT    vec3(1.98,1.25,2.3)

/* Sun/moon light color */
#define NL_DAWN_SUNLIGHT_COL   vec3(1.0,0.62,0.40) // Warm sunrise without orange oversaturation
#define NL_NOON_SUNLIGHT_COL   vec3(1.0,0.94,0.84) // Warm-neutral daytime light
#define NL_NIGHT_MOONLIGHT_COL vec3(0.025,0.045,0.12)

/* Torch colors */
#define NL_OVERWORLD_TORCH_COL  vec3(1.0,0.52,0.18)
#define NL_UNDERWATER_TORCH_COL vec3(1.0,0.52,0.18)
#define NL_NETHER_TORCH_COL     vec3(1.0,0.52,0.18)
#define NL_END_TORCH_COL        vec3(1.0,0.52,0.18)

/* Fog */
#define NL_FOG 1.0                // [toggle] 0.1 subtle ~ 1.0 blend with sky completely
#define NL_MIST_DENSITY 0.20      // Subtle atmospheric depth
#define NL_RAIN_MIST_OPACITY 0.12 // Keep rain mist restrained for mobile performance
#define NL_CLOUDY_FOG 0.1         // [toggle] 0.0 subtle - 0.8 dense fog clouds

/* Sky */
#define NL_SKY_VOID_FACTOR     0.5
#define NL_SKY_VOID_DARKNESS   0.3
#define NL_SKY_RAIN_MIX_FACTOR 0.9

/* Sky colors - zenith=top, horizon=bottom */
#define NL_DAWN_ZENITH_COL   vec3(0.22,0.38,0.60)
#define NL_DAWN_HORIZON_COL  vec3(1.0,0.62,0.42)
#define NL_DAWN_EDGE_COL     vec3(1.12,0.76,0.60)
#define NL_DAY_ZENITH_COL    vec3(0.34,0.66,1.0)
#define NL_DAY_HORIZON_COL   vec3(0.76,0.88,0.98)
#define NL_DAY_EDGE_COL      vec3(0.92,0.96,1.0)
#define NL_NIGHT_ZENITH_COL  vec3(0.012,0.024,0.065)
#define NL_NIGHT_HORIZON_COL vec3(0.025,0.045,0.09)
#define NL_NIGHT_EDGE_COL    vec3(0.04,0.065,0.11)
#define NL_RAIN_ZENITH_COL   vec3(0.36,0.42,0.50)
#define NL_RAIN_HORIZON_COL  vec3(0.53,0.59,0.66)

#define NL_END_ZENITH_COL    vec3(0.08,0.001,0.1)
#define NL_END_HORIZON_COL   vec3(0.6,0.02,0.6)


/* Rainbow */
#define NL_RAINBOW           // [toggle] enable rainbow in sky
#define NL_RAINBOW_CLEAR 0.0 // 0.3 subtle ~ 1.0 bright during clear weather
#define NL_RAINBOW_RAIN  0.4 // 0.3 subtle ~ 1.0 bright during rain weather

/* Ore glow intensity */
#define NL_GLOW_TEX 2.3           // 0.4 weak ~ 8.0 bright
#define NL_GLOW_SHIMMER 0.8       // [toggle] 0.1 subtle ~ 1.0 100% shimmer
#define NL_GLOW_SHIMMER_SPEED 0.9 // 0.5 slow - 2.0 fast
//#define NL_GLOW_LEAK 0.6        // [toggle] 0.08 subtle ~ 1.0 100% brightness of NL_GLOW_TEX

/* Waving */
#define NL_PLANTS_WAVE 0.030   // Gentle plant movement
#define NL_LANTERN_WAVE 0.080  // Subtle lantern movement
#define NL_WAVE_SPEED 2.8      // 0.5 slow wave ~ 5.0 very fast wave
//#define NL_EXTRA_PLANTS_WAVE // [toggle] !dont use! wave using texture coords (1.21.0 vanilla 2048x1024)
#define NL_WAVE_RANGE 9.0      // Keep plant/lantern movement close to the player for dense-scene performance

/* Water and Always Reflection */
#define NL_WATER_TRANSPARENCY 0.90 // Keep water clear while reflecting the sky
#define NL_WATER_BUMP 0.0           // Flat surface: no water-wave distortion
#define NL_WATER_WAVE_SPEED  0.8    // Also used by underwater effects
#define NL_WATER_TEX_OPACITY 0.3    // Retain recognizable vanilla water texture
//#define NL_WATER_WAVE             // No water displacement or animated waves
//#define NL_WATER_REFL_MASK        // Keep sky reflections broad and natural
#define NL_WATER_TINT vec3(0.72,0.88,0.96)
#define NL_WATER_STYLE_STRENGTH 0.16
#define NL_GROUND_REFL 0.22         // Always-on subtle sky reflection for horizontal terrain
#define NL_GROUND_REFL_DISTANCE 0.40 // Limit reflection work to nearer terrain
#define NL_CLOUD_AURORA_REFLECTION  // Legacy-inspired sky detail in water and wet-ground reflections

/* Underwater */
#define NL_UNDERWATER_BRIGHTNESS 0.8         // 0.0 dark ~ 3.0 bright
#define NL_CAUSTIC_INTENSITY 1.9             // 0.5 weak ~ 5.0 bright
//#define NL_UNDERWATER_WAVE 0.1               // Underwater camera wave disabled
#define NL_UNDERWATER_STREAKS 1.0            // [toggle] 0.8 subtle - 2.0 bright streaks from top
#define NL_UNDERWATER_TINT vec3(0.9,1.0,0.9) // fog tint color when underwater

/* Cloud type */
#define BOX_CLOUDS              // Parent Newb box-cloud implementation is used by both subpacks\n#define NL_CLOUD_TYPE 0          // Box clouds are the only active cloud style in B0.2.2

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
#define NL_CLOUD2_THICKNESS 2.1            // 0.5 slim ~ 5.0 fat
#define NL_CLOUD2_RAIN_THICKNESS 2.5       // 0.5 slim ~ 5.0 fat
#define NL_CLOUD2_STEPS 5                  // 3 low quality ~ 16 high quality
#define NL_CLOUD2_SCALE vec2(0.033, 0.033) // 0.003 large ~ 0.3 tiny
#define NL_CLOUD2_SHAPE vec2(0.5, 0.4)     // 0.0 round ~ 1.0 box vec2(horizontal shape, vertical shape)
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
#define NL_AURORA 0.75          // [toggle] restrained Legacy-inspired night aurora
#define NL_AURORA_VELOCITY 0.03 // 0.0 static ~ 0.3 very fast
#define NL_AURORA_SCALE 0.04    // 0.002 large ~ 0.4 tiny
#define NL_AURORA_WIDTH 0.18    // 0.04 thin line ~ 0.4 thick lines
#define NL_AURORA_COL1 vec3(0.1,1.0,0.0)
#define NL_AURORA_COL2 vec3(0.1,0.0,1.0)

//#define NL_CLOUD_AURORA_REFLECTION // Omitted to keep wet-ground rendering lightweight

/* Shooting star */
#define NL_SHOOTING_STAR 1.0        // [toggle] 0.2 dim ~ 1.0 bright
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

/* Sky reflection */
//#define NL_GROUND_REFL 0.4       // [toggle] 0.2 slightly reflective ~ 1.0 fully reflect sky
#define NL_GROUND_RAIN_WETNESS 0.70 // Visible but restrained rain wetness
#define NL_GROUND_RAIN_PUDDLES 0.35 // Subtle puddle variation

/* Entity (Actor, ItemInHand) */
#define NL_ENTITY_BRIGHTNESS     0.65 // 0.1 dark ~ 1.6 bright
//#define NL_ENTITY_EDGE_HIGHLIGHT 0.41 // Disabled for a lighter mob-heavy rendering path

/* Weather particles */
#define NL_WEATHER_SPECK 0.35        // Lightweight rain-particle styling; particles remain enabled
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

#ifdef LITE
  // Performance profile: keep the same box clouds and core Always Reflection identity.
  // Reduce reflection distance and secondary effects instead of removing the main look.
  #undef NL_GROUND_REFL
  #define NL_GROUND_REFL 0.16
  #undef NL_GROUND_REFL_DISTANCE
  #define NL_GROUND_REFL_DISTANCE 0.22
  #undef NL_CLOUD_AURORA_REFLECTION
  #undef NL_GLOW_SHIMMER
  #undef NL_LAVA_NOISE
  #undef NL_WEATHER_SPECK
  #undef NL_SHOOTING_STAR
  #undef NL_RAINBOW
  #undef NL_UNDERWATER_STREAKS
  #undef NL_RAIN_MIST_OPACITY
  #define NL_RAIN_MIST_OPACITY 0.07
  #undef NL_CLOUDY_FOG
  #define NL_CLOUDY_FOG 0.05
  #undef NL_AURORA
  #define NL_AURORA 0.45
  #undef NL_PLANTS_WAVE
  #define NL_PLANTS_WAVE 0.020
  #undef NL_LANTERN_WAVE
  #define NL_LANTERN_WAVE 0.050
  #undef NL_ENTITY_EDGE_HIGHLIGHT
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
