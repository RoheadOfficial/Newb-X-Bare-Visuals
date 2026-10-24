#ifndef FOG_H
#define FOG_H

float nlRenderFogFade(float relativeDist, vec3 FOG_COLOR, vec2 FOG_CONTROL, float rainFactor) {
  #ifdef NL_FOG
    float rain = clamp(rainFactor, 0.0, 1.0);
    // Keep engine distance fog close to its original range; weather shifts it only slightly.
    float fogStart = mix(FOG_CONTROL.x, FOG_CONTROL.x*0.98, rain);
    float fogEnd = mix(FOG_CONTROL.y, FOG_CONTROL.y*0.98, rain);
    float fade = smoothstep(fogStart, fogEnd, relativeDist);

    // O6.0: polynomial mist avoids exponential work per terrain vertex and reduces nearby haze.
    float mistStrength = NL_MIST_DENSITY * (0.18 + 0.22*rain);
    float mist = mistStrength * smoothstep(0.0, 0.85, clamp(relativeDist, 0.0, 1.0));
    fade += (1.0-fade)*mist;
    fade = mix(fade, max(fade, smoothstep(fogStart*0.88, fogEnd*0.92, relativeDist)), rain*0.06);

    return NL_FOG * clamp(fade, 0.0, 1.0);
  #else
    return 0.0;
  #endif
}

#endif
