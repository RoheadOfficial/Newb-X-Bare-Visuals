#ifndef FOG_H
#define FOG_H

float nlRenderFogFade(float relativeDist, vec3 FOG_COLOR, vec2 FOG_CONTROL, float rainFactor) {
  #ifdef NL_FOG
    // Rain brings the fog forward gradually instead of leaving a clear, distant horizon.
    float rain = clamp(rainFactor, 0.0, 1.0);
    // A gentle clear-weather haze gives distant terrain more atmospheric depth.
    float cozyFog = clamp(NL_COZY_FOG_STRENGTH, 0.0, 1.2);
    float fogStart = mix(FOG_CONTROL.x, FOG_CONTROL.x*0.98, cozyFog/1.2);
    float fogEnd = mix(FOG_CONTROL.y, FOG_CONTROL.y*0.965, cozyFog/1.2);
    fogStart = mix(fogStart, fogStart*0.88, rain);
    fogEnd = mix(fogEnd, fogEnd*0.93, rain);
    float fade = smoothstep(fogStart, fogEnd, relativeDist);

    // More depth without making the entire world uniformly grey.
    float density = NL_MIST_DENSITY*(19.0 - 18.0*FOG_COLOR.g)*(1.0 + 1.2*rain);
    float mistStrength = 0.28 + 0.055*cozyFog;
    float mist = mistStrength-mistStrength*exp(-relativeDist*relativeDist*density);
    fade += (1.0-fade)*mist;
    fade = mix(fade, max(fade, smoothstep(fogStart*0.65, fogEnd*0.78, relativeDist)), rain*0.16);

    return NL_FOG * clamp(fade, 0.0, 1.0);
  #else
    return 0.0;
  #endif
}

#endif
