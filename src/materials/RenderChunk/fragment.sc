$input v_color0, v_color1, v_fog, v_refl, v_texcoord0, v_lightmapUV, v_extra

#include <bgfx_shader.sh>
#include <newb/main.sh>

SAMPLER2D_AUTOREG(s_MatTexture);
SAMPLER2D_AUTOREG(s_SeasonsTexture);
SAMPLER2D_AUTOREG(s_LightMapTexture);
// B0.2.2 terrain shading correction. This is only compiled into RenderChunk.
// Actor materials use a separate shader and receive no custom player/mob shadows.
float nlBareTerrainShade(vec4 vertexColor) {
  float shade = 1.0;

  if (vertexColor.a > 0.0) {
    // Smoothly map the community snippet's green-channel range into one bounded ramp.
    // Replacing cumulative threshold multipliers prevents black bands on distant terrain.
    float shadeRange = clamp((0.640 - vertexColor.g) / 0.012, 0.0, 1.0);
    shadeRange = shadeRange * shadeRange * (3.0 - 2.0 * shadeRange);
    shade = 1.0 - 0.18 * shadeRange;
  } else {
    // Retain the original alpha-zero branch's color correction, but cap its influence.
    shade = clamp(vertexColor.g * 1.55 * 1.3, 0.88, 1.12);
  }

  float c = vertexColor.r;
  if (vertexColor.a <= 0.1) {
    c = vertexColor.g * 1.999;
  }
  if (c < 0.638) {
    shade *= 0.97;
  }

  return clamp(shade, 0.84, 1.12);
}


#ifdef NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH
// Cheap fake-shadow approximation for Experimental only. Reuses the terrain vertex-lighting
// gradient already passed to this shader: no extra texture reads, normals, shadow maps, or passes.
// It deepens existing darker regions rather than pretending to create real cast shadows.
float nlExperimentalFakeShadow(vec4 vertexColor) {
  float shadowBand = 1.0 - smoothstep(0.617, 0.642, vertexColor.g);
  shadowBand = shadowBand * shadowBand * (3.0 - 2.0 * shadowBand);
  float strength = NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH * shadowBand;
  return clamp(1.0 - strength, 0.90, 1.0);
}
#endif

void main() {
  #if defined(DEPTH_ONLY_OPAQUE) || defined(DEPTH_ONLY) || defined(INSTANCING)
    gl_FragColor = vec4(1.0,1.0,1.0,1.0);
    return;
  #endif

  vec4 diffuse = texture2D(s_MatTexture, v_texcoord0);
  vec4 color = v_color0;


  #ifdef ALPHA_TEST
    if (diffuse.a < 0.6) {
      discard;
    }
  #endif

  #if defined(SEASONS) && (defined(OPAQUE) || defined(ALPHA_TEST))
    diffuse.rgb *= mix(vec3(1.0,1.0,1.0), texture2D(s_SeasonsTexture, v_color1.xy).rgb * 2.0, v_color1.z);
  #endif

  #if defined(LITE) || defined(POOTAYTOE)
    // Pootaytoe is the current performance profile define; it also skips the extra glow texture sample.
    vec3 glow = vec3_splat(0.0);
  #else
    vec3 glow = nlGlow(s_MatTexture, v_texcoord0, v_extra.a);
  #endif

  diffuse.rgb *= diffuse.rgb;

  #if defined(TRANSPARENT) && !(defined(SEASONS) || defined(RENDER_AS_BILLBOARDS))
    if (v_extra.b > 0.9) {
      diffuse.rgb = vec3_splat(1.0 - NL_WATER_TEX_OPACITY*(1.0 - diffuse.b*1.8));
      diffuse.a = color.a;
    }
  #else
    diffuse.a = 1.0;
  #endif

  diffuse.rgb *= color.rgb;

  // O6.0: shift water toward muted mineral-gray/cool-glass instead of a strong blue/green wash.
  // Reuse the already sampled color; no extra texture reads or render passes.
  if (v_extra.b > 0.9) {
    float waterLuma = dot(diffuse.rgb, vec3(0.2126, 0.7152, 0.0722));
    diffuse.rgb = mix(diffuse.rgb, waterLuma * NL_WATER_TINT, NL_WATER_STYLE_STRENGTH);
  }

  // Keep a small blue-channel correction in addition to the broader water palette.
  if (v_extra.b > 0.9) {
    diffuse.b *= NL_WATER_BLUE_REDUCTION;
  }

  // Apply only to RenderChunk terrain; skip water and glass.
  // Smooth bounded shading avoids cumulative dark stripes from repeated g-thresholds.
  #if !defined(TRANSPARENT) && !defined(SEASONS)
    diffuse.rgb *= nlBareTerrainShade(v_color1);
    #ifdef NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH
      diffuse.rgb *= nlExperimentalFakeShadow(v_color1);
    #endif
  #endif

  diffuse.rgb += glow;

  // B0.3.6: refine the inexpensive material response for clearer terrain separation.
  // This is deliberately not a reflection pass: it uses no extra texture samples,
  // normals, ray marching, or environment rendering.
  #if !defined(TRANSPARENT) && !defined(SEASONS) && defined(NL_MATERIAL_HIGHLIGHT_STRENGTH)
    float materialLuma = dot(diffuse.rgb, vec3(0.2126, 0.7152, 0.0722));
    float materialMax = max(max(diffuse.r, diffuse.g), diffuse.b);
    float materialMin = min(min(diffuse.r, diffuse.g), diffuse.b);
    float materialChroma = materialMax - materialMin;
    float neutralMaterial = 1.0 - smoothstep(0.16, 0.48, materialChroma);
    float brightMaterial = smoothstep(0.38, 0.82, materialLuma);
    float materialHighlight = neutralMaterial * brightMaterial;
    diffuse.rgb += vec3(1.0, 0.97, 0.91) *
                   (NL_MATERIAL_HIGHLIGHT_STRENGTH * materialHighlight);
  #endif

  if (v_extra.b > 0.9) {
    diffuse.rgb += v_refl.rgb*v_refl.a;
  } else if (v_refl.a > 0.0) {
    // reflective effect - only on xz plane
    float dy = abs(dFdy(v_extra.g));
    if (dy < 0.0002) {
      float mask = v_refl.a*(clamp(v_extra.r*10.0,8.2,8.8)-7.8);
      diffuse.rgb *= 1.0 - 0.6*mask;
      diffuse.rgb += v_refl.rgb*mask;
    }
  }

  diffuse.rgb = mix(diffuse.rgb, v_fog.rgb, v_fog.a);

  diffuse.rgb = colorCorrection(diffuse.rgb);


  gl_FragColor = diffuse;
}
