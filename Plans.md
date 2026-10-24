# Plans

## B0.4.1 — Forest Performance Pass

**Version:** `B0.4.1.2652` (Minecraft target label `26.52`)  
**Branch:** `b0.4.1-forest-performance`  
**Base:** `b0.4.0-performance-fixes`  
**Build scope:** Android during implementation; multiplatform during release preparation.

### Targeted changes

1. Add a foliage-specific fragment fast path: retain normal vertex lighting, but skip the generic opaque-terrain shade ramp for alpha-tested foliage and billboards.
2. Skip the optional material-highlight approximation for alpha-tested foliage/billboards while retaining it on eligible opaque terrain.
3. Skip optional per-vertex glow-shimmer calculations for alpha-tested foliage/billboards while preserving their base emissive texture glow.
4. Preserve all four profiles, approved saturation, no-waving guard, rounded clouds, rain/wet ground, water reflection, and opaque-terrain Always Reflection.
5. Diagnose static forest FPS drops separately from chunk-loading/movement stutters; shader changes alone cannot guarantee fixes to engine-side chunk generation.

### Acceptance

- [ ] Static validator and duplicate-file audit pass.
- [ ] Android build succeeds and output is a directly installable `.mcpack` containing expected compiled materials for all profiles.
- [ ] Compare B0.4.0 and B0.4.1 in identical dense-forest scenes, both stationary and moving.
- [ ] Verify leaf lighting, glow, terrain reflection, rain, water, clouds, and all four profile identities in-game.
- [ ] Measure performance on-device; do not claim an FPS improvement based on source inspection or compilation alone.
- [ ] Keep `main` untouched until review and explicit merge approval.

---

## B0.4.0 — Targeted Performance Fixes

**Version:** `B0.4.0.2652` (Minecraft target label `26.52`)  
**Branch:** `b0.4.0-performance-fixes`  
**Build scope:** Android during implementation; multiplatform during release preparation.

### Fixes in this pass

1. Skip terrain-reflection sky calculations for alpha-tested foliage/billboards; preserve Always Reflection on opaque terrain with tighter profile-specific distance caps.
2. Avoid calculating unused sky fog colors for nearby clear-weather terrain.
3. Reuse sun-light dawn/night factors instead of calculating them twice.
4. Remove one redundant weather-texture sample per particle; particle spawn count remains engine-controlled.
5. Use two rounded-cloud density steps in all profiles; keep a sky reflection on all visible water while simplifying far-water reflections to a horizon/zenith gradient, and separately bound extra aurora detail.
6. Skip Actor Glint texture work only when the glint effect is transparent; preserve both layers for visible glint.
7. Preserve the approved saturation, four profiles, rounded clouds, base water sky reflection, terrain Always Reflection, rain, wet ground, and nighttime aurora.

### Acceptance

- [ ] Static validator and duplicate-file audit pass.
- [ ] Android build succeeds and artifact is a directly installable `.mcpack` with compiled RenderChunk material binaries for all profiles.
- [ ] Test Default, Pootaytoe, Bare Visuals, and Experimental on-device against B0.3.8 using the same world, render distance, weather, and camera position.
- [ ] Check trees, clear-weather fog/atmosphere, sunrise/sunset lighting, heavy rain, water, horizon/haze, Actor Glint, clouds, and general frame-time stutter.
- [ ] Check reflection cutoff/pop-in, foliage wetness, cloud quality, rain appearance, and fog transitions.
- [ ] Confirm Minecraft/MB Loader 26.52 runtime behavior.

A successful build proves packaging/compilation only. FPS gains, visual acceptance, and compatibility require in-game testing. Keep `main` untouched until review and explicit merge approval.

## BONES roadmap

- **B-Series:** overall Bare Visuals release progression.
- **O-Series:** Overworld-specific work; prioritize it before Nether and End.
- **N-Series:** Nether-specific work.
- **E-Series:** End-specific work.
- **S-Series:** The Sift, only if it becomes available and testable.

Dimension counters are independent from each other and from B-Series. The historical O-Series mapping and detailed naming rules live in [Important.md](Important.md).
