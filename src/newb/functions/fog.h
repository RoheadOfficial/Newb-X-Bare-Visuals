#ifndef FOG_H
#define FOG_H

float nlRenderFogFade(float relativeDist, vec3 FOG_COLOR, vec2 FOG_CONTROL, float rainFactor) {
  #ifdef NL_FOG
    // Rain brings the fog forward gradually instead of leaving a clear, distant horizon.
    float rain = clamp(rainFactor, 0.0, 1.0);
    float fogStart = mix(FOG_CONTROL.x, FOG_CONTROL.x*0.92, rain);
    float fogEnd = mix(FOG_CONTROL.y, FOG_CONTROL.y*0.95, rain);
    float fade = smoothstep(fogStart, fogEnd, relativeDist);

    // Mist becomes denser during rain while retaining the existing fog pipeline.
    float density = NL_MIST_DENSITY*(12.0 - 11.0*FOG_COLOR.g)*(1.0 + 0.75*rain);
    float mist = 0.24-0.24*exp(-relativeDist*relativeDist*density);
    fade += (1.0-fade)*mist;
    // Keep weather visibly atmospheric without pulling the fog wall too close to the player.
    fade = mix(fade, max(fade, smoothstep(fogStart*0.72, fogEnd*0.84, relativeDist)), rain*0.12);

    return NL_FOG * clamp(fade, 0.0, 1.0);
  #else
    return 0.0;
  #endif
}

#endif
