## B0.4.6 — O8 Performance & Visual Refinement

**Version:** `B0.4.6.2652` (Minecraft target label `26.52`)  
**Overworld milestone:** `O8`  
**Branch:** `b0.4.6-o8-performance-overhaul`  
**Base:** B0.4.5 implementation candidate, kept separate from `main`  
**Build scope:** Android during implementation; multiplatform during release preparation.

### Required implementation
1. Compile out terrain Always Reflection and water sky/aurora/torch reflections. Keep calling the compile-time reflection-free terrain path so rain-darkened ground and puddle variation still execute without sky-reflection calculations.
2. Add a reflection-free water path with clear transparency, low texture opacity, and a restrained soft-blue palette inspired by Newb X Future's water appearance. No waves or water reflections.
3. Restore the vanilla Minecraft cloud path, shelve Cloud Type 1, remove the pack's custom cloud texture override, and keep baseline cloud-plane thickness/opacity vanilla-like (rain changes tint rather than geometry).
4. Refine day/night and rain-driven sky transitions while keeping a clean vanilla-rooted sky gradient and the existing cozy, cinematic Bare Visuals identity.
5. Implement coordinated RenderChunk foliage optimizations: route detected tree/leaf vertices through dedicated lower-cost lighting that omits terrain spatial sun projection/cloud-shadow work; use a foliage-only environment initializer without rotated sun/moon vectors for eligible nearby clear-weather leaves; resolve fog alpha once and reuse it; and select a cheaper ambient palette only when foliage fog is negligible. Fall back to full environment/sky evaluation for rain, visible fog, underwater, Nether, and End scenes.
6. Preserve the approved 1.06 saturation, lighting identity, lightweight rain, wet-ground response, no-waving rule, and each active profile's purpose.
7. Keep only Default, Pootaytoe, and Bare Visuals selectable; Experimental is shelved, not erased from history.
8. Update source and artifact validators, version metadata, changelog, docs, and Android workflows. Verify the generated MCpack contains all expected compiled materials. Do not modify upstream README content.

### Acceptance gate
- [ ] Static validator passes and duplicate-file audit has no unexpected regression.
- [ ] Android build succeeds and produces a directly installable `.mcpack`; inspect generated manifest, version `B0.4.6.2652`, three-profile order, and compiled material outputs.
- [ ] Compare B0.4.5 with O8 on the same Vivo Y22s, world, render distance, and comparable conditions: dense forest while stationary, turning, and moving.
- [ ] Test weather, wet ground, water, sky transitions, and all three active profiles for visual regressions.
- [ ] Target 30–49 FPS, but record measured FPS and stutters rather than asserting an unmeasured result. A successful build does not prove runtime performance.
- [ ] Keep `main` untouched until review and explicit merge approval.

---

# Plans

## B0.4.5 — All-in-One Performance Overhaul

**Version:** `B0.4.5.2652` (Minecraft target label `26.52`)  
**Overworld milestone:** `O7` (proposed; use a patch suffix only if a subversion patch is needed)  
**Branch:** `b0.4.5-performance-overhaul`  
**Base:** current `main` at branch creation  
**Build scope:** Android during implementation; multiplatform during release preparation.

### Scope

1. Prioritize dense forests, foliage, mountains, and terrain rendering; preserve the B0.4.0/B0.4.1 fast paths and measure rather than promise FPS gains.
2. Activate lightweight custom Cloud Type 1. Shelve rounded Type 2 and realistic Type 3; do not substitute vanilla clouds.
3. Raise saturation from 1.04 to 1.06 as a restrained test value while retaining tone mapping and natural color.
4. Keep the custom Newb water reflection path, water reflections, terrain Always Reflection, rain, wet ground, aurora, and the no-waving guard. No water waves.
5. Audit atmosphere/horizon/fog, weather particles, and Actor Glint for additional redundant work without removing their recognizable effects.
6. Preserve Default, Pootaytoe, Bare Visuals, and Experimental and their distinct purposes.
7. Polish manifest descriptions; update validator, version metadata, docs, and Android build-check branch filters. Keep upstream `README.md` untouched.

### Acceptance

- [ ] Duplicate audit and updated static validator pass.
- [ ] Android build succeeds and yields a directly installable `.mcpack` with all expected profile materials/binaries.
- [ ] Inspect generated manifest, B0.4.5 version identity, profile order, and Cloud Type 1 selection.
- [ ] Compare B0.4.1 and B0.4.5 under matching device/world/settings in dense forest, open terrain, weather, water, horizon, and Actor Glint scenes.
- [ ] Confirm no regression to water/terrain reflections, rain/wet ground, natural colors, night atmosphere, or the four profile identities.
- [ ] Record actual FPS/stutter observations; compilation and source inspection are not FPS proof.
- [ ] Keep `main` untouched until review and explicit merge approval.

---

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
