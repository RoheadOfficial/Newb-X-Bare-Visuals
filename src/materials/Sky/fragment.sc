#ifndef INSTANCING
  $input v_worldPos, v_underwaterRainTimeDay
#endif

#include <bgfx_shader.sh>

#ifndef INSTANCING
  #include <newb/main.sh>
  uniform vec4 TimeOfDay;
  uniform vec4 FogColor;
  uniform vec4 FogAndDistanceControl;
#endif

void main() {
  #ifndef INSTANCING
    vec3 viewDir = normalize(v_worldPos);

    nl_environment env;
    env.end = false;
    env.nether = false;
    env.underwater = v_underwaterRainTimeDay.x > 0.5;
    env.rainFactor = v_underwaterRainTimeDay.y;
    env.dayFactor = v_underwaterRainTimeDay.w;
    env.fogCol = FogColor.rgb;
    env = calculateSunParams(env, TimeOfDay.x);

    nl_skycolor skycol = nlOverworldSkyColors(env);

    vec3 skyDir = vec3(-viewDir.x, viewDir.y, -viewDir.z);
    vec3 skyColor = nlRenderSky(skycol, env, skyDir, v_underwaterRainTimeDay.z, true);

    // O8.4: cloud coordinates follow the sky ray, not screen pixels or a near-zero Y divisor.
    #if NL_CLOUD_TYPE == 4
      vec4 bslClouds = renderCloudsBsl(skyDir, skycol, v_underwaterRainTimeDay.z, env.rainFactor, env.dayFactor);
      skyColor = mix(skyColor, bslClouds.rgb, bslClouds.a);
    #endif

    // O8.4: map aurora over the sky dome with bounded coordinates and a horizon-weighted fade.
    // This removes the old 1/abs(viewDir.y) projection that stretched the aurora across the map.
    #ifdef NL_AURORA
      vec3 auroraPos = vec3(skyDir.x * 187.0, skyDir.y * 96.0, skyDir.z * 187.0);
      vec4 aurora = renderAurora(auroraPos, v_underwaterRainTimeDay.z, env.rainFactor, env.dayFactor);
      float auroraHorizonFade = 1.0 - smoothstep(0.18, 0.72, abs(skyDir.y));
      skyColor += aurora.rgb * auroraHorizonFade;
    #endif

    #ifdef NL_SHOOTING_STAR
      skyColor += NL_SHOOTING_STAR*nlRenderShootingStar(viewDir, env.fogCol, v_underwaterRainTimeDay.z);
    #endif
    #ifdef NL_GALAXY_STARS
      skyColor += NL_GALAXY_STARS*nlRenderGalaxy(viewDir, env.fogCol, env, v_underwaterRainTimeDay.z);
    #endif

    skyColor = colorCorrection(skyColor);

    gl_FragColor = vec4(skyColor, 1.0);
  #else
    gl_FragColor = vec4(0.0, 0.0, 0.0, 0.0);
  #endif
}
