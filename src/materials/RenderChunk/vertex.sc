$input a_color0, a_position, a_texcoord0, a_texcoord1
#ifdef INSTANCING
  $input i_data0, i_data1, i_data2, i_data3
#endif
$output v_color0, v_color1, v_fog, v_refl, v_texcoord0, v_lightmapUV, v_extra

#include <bgfx_shader.sh>
#include <newb/main.sh>

uniform vec4 RenderChunkFogAlpha;
uniform vec4 FogAndDistanceControl;
uniform vec4 ViewPositionAndTime;
uniform vec4 FogColor;
uniform vec4 TimeOfDay;
uniform vec4 CameraPosition;

SAMPLER2D_AUTOREG(s_MatTexture);
SAMPLER2D_AUTOREG(s_LightMapTexture);

void main() {
  #ifdef INSTANCING
    mat4 model = mtxFromCols(i_data0, i_data1, i_data2, i_data3);
  #else
    mat4 model = u_model[0];
  #endif

  vec3 worldPos = mul(model, vec4(a_position, 1.0)).xyz;

  #if !(defined(DEPTH_ONLY_OPAQUE) || defined(DEPTH_ONLY) || defined(INSTANCING))

  #ifdef NL_CHUNK_LOAD_ANIM
    worldPos.y -= NL_CHUNK_LOAD_ANIM*RenderChunkFogAlpha.x*RenderChunkFogAlpha.x*RenderChunkFogAlpha.x;
  #endif

  #ifdef RENDER_AS_BILLBOARDS
    worldPos += vec3(0.5,0.5,0.5);

    vec3 modelCamPos = ViewPositionAndTime.xyz - worldPos;
    float camDis = length(modelCamPos);
    vec3 viewDir = modelCamPos / camDis;

    vec3 boardPlane = normalize(vec3(-viewDir.z, 0.0, viewDir.x));
    worldPos -= (((viewDir.zxy * boardPlane.yzx) - (viewDir.yzx * boardPlane.zxy)) *
                 (a_color0.z - 0.5)) +
                 (boardPlane * (a_color0.x - 0.5));
    vec4 color = vec4(1.0,1.0,1.0,1.0);
  #else
    vec3 modelCamPos = ViewPositionAndTime.xyz - worldPos;
    float camDis = length(modelCamPos);
    vec3 viewDir = modelCamPos / camDis;

    vec4 color = a_color0;
  #endif

  float relativeDist = camDis / FogAndDistanceControl.z;

  vec3 gPos = worldPos.xyz + CameraPosition.xyz;
  vec3 cPos = a_position.xyz;
  vec3 bPos = fract(cPos);
  vec3 tiledCpos = fract(cPos*0.0625);

  // bit 16 for dithering??
  // bit 15-1 for texture mapping
  // uvec2 a16 = uvec2(round(a_texcoord0 * 65535.0));
  // vec2 uv0 = vec2((a16 & uvec2(32767u)) << uvec2(1)) / 65535.0;
  // uv0 += (2.0*vec2((a16 & uvec2(32768u)) >> uvec2(15)) - 1.0) / 32768.0;
  vec2 uv0 = 2.0*a_texcoord0.xy;
  uv0 = fract(uv0) + ((floor(uv0)-0.5)/16384.0);

  // bit 16 for dithering / mask tint
  // bits 15-9 for ??
  // bits 8-5 for x, bits 4-1 for y
  // uvec2 a16 = uvec2(round(a_texcoord1 * 65535.0));
  // vec2 uv1 = vec2(uvec2(a16.y >> 4u, a16.y) & uvec2(15u)) * vec2(0.06666667);
  vec2 uv1 = fract(a_texcoord1.y*vec2(256.0, 4096.0));
  vec2 lit = uv1*uv1;

  bool isColored = color.r != color.g || color.r != color.b;
  float shade = isColored ? color.g*1.5 : color.g;

  // tree leaves detection
  #if defined(ALPHA_TEST) && !defined(RENDER_AS_BILLBOARDS)
    bool isTree = (isColored && (bPos.x+bPos.y+bPos.z < 0.001)) || color.a == 0.0;
  #else
    bool isTree = false;
  #endif

  // Resolve the candidate foliage path before building sun/moon direction vectors.
  // The lightweight environment is retained only for clear, nearby Overworld foliage.
  float foliageRelativeDist = camDis / FogAndDistanceControl.z + RenderChunkFogAlpha.x;
  nl_environment env;
  if (isTree) {
    env = nlDetectFoliageEnvironment(TimeOfDay.x, FogColor.rgb, FogAndDistanceControl.xyz);
  } else {
    env = nlDetectEnvironment(TimeOfDay.x, FogColor.rgb, FogAndDistanceControl.xyz);
  }

  float foliageFogAlpha = nlRenderFogFade(foliageRelativeDist, FogColor.rgb, FogAndDistanceControl.xy, env.rainFactor);
  bool foliageFast = isTree && !env.end && !env.nether && !env.underwater &&
                     env.rainFactor <= 0.0 && foliageFogAlpha <= 0.20;
  // Distant/fog-visible foliage needs the complete sun/moon vectors for the original sky renderer.
  if (isTree && !foliageFast) {
    env = nlDetectEnvironment(TimeOfDay.x, FogColor.rgb, FogAndDistanceControl.xyz);
  }

  nl_skycolor skycol;
  if (foliageFast) {
    skycol = nlFoliageSkyColors(env);
  } else {
    skycol = nlSkyColors(env);
  }

  // time
  highp float t = ViewPositionAndTime.w;

  // convert color space to linear-space
  #ifdef SEASONS
    isTree = true;

    // season tree leaves are colored in fragment
    color.w *= color.w;
    color = vec4(color.www, 1.0);
  #else
    if (isColored) {
      color.rgb *= color.rgb*1.2;
    }
  #endif

  vec3 torchColor; // modified by nl_lighting
  vec3 light;
  // O8: foliage uses a dedicated lower-cost lighting path. This avoids the terrain-only
  // spatial sun projection and cloud-shadow path on the most overdraw-heavy forest material.
  if (isTree) {
    light = nlFoliageLighting(s_LightMapTexture, skycol, env, torchColor, a_color0.rgb, uv1, lit, shade, t);
  } else {
    light = nlLighting(s_LightMapTexture, skycol, env, worldPos, torchColor, a_color0.rgb, uv1, lit, isTree, shade, t, FogAndDistanceControl.z, TimeOfDay.x, CameraPosition.xyz);
  }

  #if !defined(NL_DISABLE_ALL_WAVING) && defined(ALPHA_TEST) && (defined(NL_PLANTS_WAVE) || defined(NL_LANTERN_WAVE)) && !defined(RENDER_AS_BILLBOARDS)
    nlWave(worldPos, light, env.rainFactor, uv1, lit, uv0, bPos, a_color0, cPos, tiledCpos, t, s_MatTexture, isColored, camDis, isTree);
  #endif

  // loading chunks
  relativeDist += RenderChunkFogAlpha.x;

  vec4 fogColor;
  fogColor.a = foliageFogAlpha;
  // The sky color is unused when fog alpha is zero. Avoid a full sky evaluation for nearby,
  // clear-weather terrain vertices; keep the sky-derived color whenever fog can contribute.
  if ((!isTree && fogColor.a > 0.001) || fogColor.a > 0.20 || env.rainFactor > 0.0) {
    fogColor.rgb = nlRenderSky(skycol, env, viewDir, t, true);
  } else {
    fogColor.rgb = FogColor.rgb;
  }
  if (env.nether) {
    // blend fog with void color
    fogColor.rgb = colorCorrectionInv(FogColor.rgb);
  }

  #if defined(NL_CLOUDY_FOG) && defined(NL_FOG)
    float fg = smoothstep(0.0, 1.0-NL_CLOUDY_FOG, relativeDist);
    fg *= sin(5.0*viewDir.y + 2.0*viewDir.x - 0.1*t);
    fg *= sin(5.0*viewDir.y - 2.0*viewDir.x + viewDir.z + 0.1*t);
    fogColor.a += (1.0-fogColor.a)*fg*fg;
  #endif

  float water = 0.0;
  vec4 refl = vec4(0.0,0.0,0.0,0.0);
  #if defined(TRANSPARENT) && !(defined(RENDER_AS_BILLBOARDS) || defined(SEASONS))
    if (a_color0.b > 0.3 && a_color0.a < 0.95) {
      water = 1.0;
      // O8: keep the custom water material but compile its reflection calculations out.
      color.a = mix(color.a, 1.0, 0.5*clamp(relativeDist, 0.0, 1.0));
      refl = nlWater(color, worldPos, skycol, env, a_color0, viewDir, cPos, tiledCpos, gPos, CameraPosition.xyz, light, torchColor, lit, bPos.y, camDis, t);
    } else {
      color.a = mix(color.a, 1.0, 0.5*clamp(relativeDist, 0.0, 1.0));
      // Always run the reflection-free nlRefl branch so rain can still darken ground
      // and vary puddle wetness. NL_DISABLE_GROUND_REFLECTIONS compiles out sky reflections.
      refl = nlRefl(color, skycol, env, viewDir, worldPos, tiledCpos, CameraPosition.xyz, torchColor, lit, camDis, FogAndDistanceControl.z, t);
    }
  #else
    // Alpha-tested foliage/billboards cannot display the horizontal terrain reflection mask.
    // Skip the expensive sky-reflection calculation for these heavily overdrawn materials.
    #if defined(ALPHA_TEST) || defined(RENDER_AS_BILLBOARDS)
      refl = vec4(0.0, 0.0, 0.0, 0.0);
    #else
      #if defined(NL_DISABLE_GROUND_REFLECTIONS)
        refl = vec4(0.0, 0.0, 0.0, 0.0);
      #else
        refl = nlRefl(color, skycol, env, viewDir, worldPos, tiledCpos, CameraPosition.xyz, torchColor, lit, camDis, FogAndDistanceControl.z, t);
      #endif
    #endif
  #endif

  vec4 pos = mul(u_viewProj, vec4(worldPos, 1.0));
  #if defined(NL_RAIN_MIST_OPACITY) && defined(NL_FOG)
    if (env.rainFactor > 0.0) {
      float humidAir = env.rainFactor*lit.y*lit.y*nlWindblow(pos.xyz, t);
      fogColor.a = mix(fogColor.a, 1.0, humidAir*NL_RAIN_MIST_OPACITY);
    }
  #endif

  if (env.underwater) {
    nlUnderwaterLighting(light, pos.xyz, lit, uv1, tiledCpos, cPos, t, skycol.horizon);
  }

  color.rgb *= light;

  #if defined(NL_GLOW_SHIMMER) && !(defined(RENDER_AS_BILLBOARDS) || defined(SEASONS) || defined(ALPHA_TEST))
    float shimmer = nlGlowShimmer(cPos, t);
  #else
    float shimmer = 1.0;
  #endif

  #ifdef NL_LAVA_NOISE
    bool isc = (a_color0.r+a_color0.g+a_color0.b) > 2.999;
    bool isb = bPos.y < 0.891 && bPos.y > 0.889;
    if (isc && isb && (uv1.x > 0.81 && uv1.x < 0.876) && uv0.y > 0.5) {
      vec4 lava = nlLavaNoise(gPos, t);
      #ifdef NL_LAVA_NOISE_BUMP
        worldPos.y += NL_LAVA_NOISE_BUMP*lava.a;
      #endif
      color.rgb *= lava.rgb;
    }
  #endif

  v_extra = vec4(shade, worldPos.y, water, shimmer);
  v_refl = refl;
  v_texcoord0 = uv0;
  v_lightmapUV = uv1;
  v_color0 = color;
  v_color1 = a_color0;
  v_fog = fogColor;

  #else

  vec4 pos = mul(u_viewProj, vec4(worldPos, 1.0));

  #endif

  gl_Position = pos;
}
