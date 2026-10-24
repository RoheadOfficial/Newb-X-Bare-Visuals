#ifndef GLOW_H
#define GLOW_H

#include "sky.h"

vec3 glowDetect(vec4 diffuse) {
  // Texture alpha: diffuse.a
  // 252/255 = max glow
  // 253/255 = partial glow
  if (diffuse.a > 0.988 && diffuse.a < 0.993) {
    vec3 glow = diffuse.rgb * diffuse.rgb;
    if (diffuse.a > 0.989) {
      return 0.4 * glow;
    }
    return glow;
  }
  return vec3(0.0,0.0,0.0);
}

vec3 glowDetectC(sampler2D tex, vec2 uv) {
  return glowDetect(texture2DLod(tex, uv, 0.0));
}

vec3 glowDetectD(sampler2D tex, vec2 uv, vec2 offset, vec2 st) {
  // edge fix. dont sample from outside bounds
  offset *= step(offset*st, vec2_splat(0.0));

  return glowDetectC(tex, uv+offset);
}

vec3 nlGlow(sampler2D tex, vec2 uv, float shimmer) {
  vec3 glow = glowDetectC(tex, uv);
  #ifdef NL_GLOW_LEAK
    // Four cardinal samples provide the local halo; corner samples are not used.
    // c3 c4 c5
    // c2    c6
    // c1 c8 c7
    vec2 texSize = vec2(textureSize(tex, 0));
    vec2 offset = 1.0 / texSize;

    // detect edge pixel and direction (assuming 64x32 texture atlas)
    // 0.01 extra offset to fix precision issue on some devices
    float boundSize = texSize.x/64.0;
    vec2 st = boundSize*fract(64.0*uv*(texSize/texSize.x)) - 0.5*boundSize;
    st = sign(st)*step(vec2_splat(0.5*boundSize-1.01), abs(st));

    vec3 c2 = glowDetectD(tex, uv, offset*vec2(-1, 0), st);
    vec3 c4 = glowDetectD(tex, uv, offset*vec2( 0, 1), st);
    vec3 c6 = glowDetectD(tex, uv, offset*vec2( 1, 0), st);
    vec3 c8 = glowDetectD(tex, uv, offset*vec2( 0,-1), st);

    vec2 p = uv * texSize;
    vec2 u = fract(p);
    //u *= u*(3.0 - 2.0*u);
    vec2 v = 1.0 - u;

    // B0.2.6 lightweight bloom approximation: four cardinal taps only.
    // Avoid corner samples to keep the added texture work lower on mobile.
    vec3 g = max(max(c2*(1.0-u.x), c6*u.x), max(c8*(1.0-u.y), c4*u.y));

    // Keep the halo faint and local; this is not a screen-space bloom pass.
    g = g*g*(0.5 + 0.5*g);
    glow = max(glow, g*NL_GLOW_LEAK);
  #endif

  #ifdef NL_GLOW_SHIMMER
    glow *= shimmer;
  #endif

  return glow * NL_GLOW_TEX;
}

#ifdef NL_GLOW_SHIMMER
float nlGlowShimmer(vec3 cPos, float t) {
  float shimmer = sin(0.7*dot(cPos, vec3(1.0, 1.0, 1.0)) - NL_GLOW_SHIMMER_SPEED*t);
  shimmer = sin(1.2*shimmer + 0.7*dot(cPos, vec3(-1.0, -1.0, 1.0)));
  shimmer *= shimmer;
  return mix(1.0, shimmer*shimmer, NL_GLOW_SHIMMER);
}
#endif

vec4 nlGlint(vec4 light, vec4 layerUV, sampler2D glintTexture, vec4 glintColor, vec4 tileLightColor, vec4 albedo) {
  float d = fract(dot(albedo.rgb, vec3_splat(4.0)));

  // Keep both animated glint layers, but skip their texture work when the effect is transparent.
  if (glintColor.a <= 0.001) {
    return light;
  }

  vec4 tex1 = texture2D(glintTexture, fract(layerUV.xy+0.1*d)).rgbr;
  vec4 tex2 = texture2D(glintTexture, fract(layerUV.zw+0.1*d)).rgbr;

  vec4 glint = (tex1*tex1 + tex2*tex2) * tileLightColor * glintColor;

  light.rgb = light.rgb*(1.0-0.4*glint.a) + 80.0*glint.rgb;
  light.rgb += vec3(0.1,0.0,0.1) + 0.2*spectrum(sin(layerUV.x*9.42477 + 2.0*glint.a + d));

  return light;
}

#endif
