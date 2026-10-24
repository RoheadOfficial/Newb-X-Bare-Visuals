# Plans

## B0.3.7 — Polish, Performance & Compatibility

**Version:** `B0.3.7.2652` (simple `B0.3.7`, target label `26.52`)  
**Branch:** `b0.3.7-implementation`  
**Build scope:** Android only during implementation; multiplatform is reserved for release preparation.

### Goals and source changes
- Preserve the creator-approved B0.3.6 look and `NL_SATURATION 1.04`.
- Remove the aggressive sun-source brightness multiplier in `sky.h`; retain the normal sky gradient and sun/moon disk.
- Keep vanilla water rendering and reduce blue-channel output by 8% on pixels identified by the existing water flag. No custom water reflections, waves, or displacement.
- Fix Pootaytoe's glow-sample optimization to recognize its actual `POOTAYTOE` define, alongside legacy `LITE`.
- Add Experimental as profile four, with a smooth, bounded fake-shadow approximation that reuses existing terrain vertex-lighting gradients.
- Keep Default, Pootaytoe, and Bare Visuals identities and existing effects intact; don't claim FPS gains or zero lag without device testing.

### Profile roles and order
1. **Default:** balanced main profile with approved saturation and established effects.
2. **Pootaytoe:** performance-first profile; skips the extra terrain glow texture sample.
3. **Bare Visuals:** fuller cozy atmosphere and profile-specific highlights/palette.
4. **Experimental:** fake terrain-shadow prototype only; no shadow maps, extra texture reads, rendering passes, or player/mob shadows.

### Experimental limitations
- Uses existing `v_color1` terrain vertex-color/lighting gradients and only affects opaque terrain in this profile.
- Adds no texture sampling, normal reconstruction, shadow-map rendering, geometry pass, water effect, or actor-material change.
- Reinforces existing darker terrain regions; it cannot reliably create new tree-canopy cast shadows without additional spatial/shadow information.
- Compare it with Default in forests, around buildings, and on open terrain. Keep/refine only if visual benefit and measured cost justify it.

### Build and repository rules
- Preserve numeric manifest version `[0, 3, 7]`, patch warning, Newb attribution, original upstream README, unique pack identity, and licensing notices.
- Update static validation, docs, and workflows for four profiles.
- Run the duplicate audit and inspect its findings; delete only confirmed accidental duplicates, never intentional identical assets/notices.
- Build Android only during implementation. Do not run multiplatform until release preparation.
- Keep `main` untouched until the creator reviews and accepts the implementation.

### Validation checklist
- [x] Create a clean implementation branch from current `main`.
- [x] Preserve version identity and approved saturation.
- [x] Remove aggressive sky-source boost and add restrained water blue reduction.
- [x] Align Pootaytoe's glow shortcut with the actual profile define.
- [x] Add Experimental as the fourth profile and implement bounded fake terrain shading.
- [x] Update profile order, docs, validator, and Android-only development workflow.
- [x] Review duplicate-audit findings. The only reported matches are shared material.json/config.json files across material definitions; retained these identical source templates because they appear intentional and removing them could break material compilation. No confirmed accidental duplicate was deleted.
- [ ] Pass static validation and Android-only GitHub Actions build.
- [ ] Inspect generated Android pack, manifest, profile order, and compiled materials.
- [ ] Test all four profiles on Vivo Y22s; compare visuals/FPS in equivalent forests, mountains, open terrain, water, rain/storms, clouds, and night scenes.
- [ ] Compare Experimental vs Default around buildings and under trees.
- [ ] Verify Minecraft and MB Loader compatibility independently.
- [ ] Run multiplatform build during release preparation only; do not merge to `main` until creator acceptance.

### Performance and safety rules
1. Treat shader-cost estimates as hypotheses until measured.
2. Preserve saturation, rain, rain fog, wet ground, rounded clouds, and night atmosphere.
3. Keep water vanilla-like; no custom water reflections, waves, or displacement.
4. Keep godrays/sunrays, box clouds, waving vegetation, and custom player/mob shadows excluded.
5. Compilation does not establish visual quality, FPS gains, or runtime compatibility.

---

---

## B0.3.2 — Beauty & Performance

**Status:** Historical plan, superseded by B0.3.6 and the current B0.3.7 work. The checklist below records earlier implementation decisions; its unchecked in-game validations were not automatically completed by later updates.

### Main goal

Make Newb X Bare Visuals beautiful, recognizable, cozy, and more efficient in all three profiles. Prizma Visuals is the main mood inspiration, especially its welcoming cozy atmosphere, but the implementation must remain original. No oversaturation, visual gimmicks, or effects added just to make the changelog longer.

### Final subpacks

- **Default:** balanced main profile; natural daylight, warmer sunsets/evenings, believable soft-blue vanilla water, rounded clouds, restrained local glow, rain atmosphere, wet ground, and night aurora. Four rounded-cloud samples; 32-unit terrain-reflection cap.
- **Pootaytoe:** performance-focused profile; preserve the core look while making more aggressive targeted savings. Two rounded-cloud samples; 20-unit terrain-reflection cap; skip optional glow leak/shimmer, weather speck styling, lava noise, underwater streaks, and material highlights.
- **Bare Visuals:** strongest cozy Prizma-inspired mood; softer blue skies, peach/golden sunrise and sunset, rounded clouds, gentle depth, readable night transition, and subtle material highlights. Four rounded-cloud samples; 30-unit terrain-reflection cap.

The internal Prizma-inspired percentages are planning notes only. Never put them in pack descriptions or metadata. Player-facing descriptions may be playful, but must not disclose the percentages.

### Full feature checklist and disposition

- [x] **Performance Profiles:** Default, Pootaytoe, and Bare Visuals have separate compile-time profile behavior. Optimize every profile, not only Pootaytoe.
- [x] **Bare Mode principles:** Fold the lean, vanilla-recognizable, reduced-effects behavior into Pootaytoe instead of adding a fourth subpack.
- [x] **Comfort-first visuals:** maintain restrained saturation, natural sunlight, readable block colors, warm but controlled evenings, and no distracting effects.
- [x] **Night Visibility:** slightly lift the night palette and minimum-light contribution while preserving a clearly nighttime sky.
- [x] **Ore Visibility (texture pass):** apply restrained contrast/readability enhancement to the existing copper, diamond, emerald, gold, iron, lapis, nether gold, quartz, and redstone ore textures. This is texture-only; no emissive ore glow or shader color heuristic is used. In-game readability and color balance still need review.
- [x] **Animation Controls policy:** keep compile-time control points but leave plant/lantern waving, tree waving, and water waves disabled, as already agreed. No player-facing runtime toggle is claimed without a supported settings interface.
- [x] **Custom Main Settings Entry:** explicitly scrapped and excluded from B0.3.2. Do not attempt to add a custom page to Minecraft's main Settings menu through an ordinary resource pack.
- [x] **PBR-inspired material highlights:** add a restrained, inexpensive color-based approximation for Default and Bare Visuals; no extra texture reads, full PBR claims, or costly environment reflections.
- [x] **B0.2.9 performance foundation:** retain the terrain-reflection guard/range bounds, four-cardinal glow sampling, daytime aurora early-out, profile-specific cloud steps, and material compilation architecture.
- [x] **Water exclusions:** retain vanilla water; no always-on water reflections, water waves, or displacement.
- [x] **Weather/atmosphere preservation:** retain lightweight rain particles, rain fog/mist, wet ground and puddle variation, rounded clouds, night aurora/light night clouds, and the existing sky pipeline.
- [x] **Other exclusions:** no godrays, box clouds, vegetation waving, custom player/mob shadows, or unnecessary effect removals.

### Implementation checklist

- [x] Create b0.3.2-implementation from main.
- [x] Set display version B0.3.2 and manifest version [0, 3, 2].
- [x] Replace Lite/Beta/Default lineup with Default/Pootaytoe/Bare Visuals.
- [x] Configure Default to inherit root materials compiled with DEFAULT; compile all materials separately for Pootaytoe and Bare Visuals.
- [x] Apply profile-specific reflection caps and rounded-cloud sample counts.
- [x] Add lightweight terrain material highlights, skipped in Pootaytoe.
- [x] Improve night palette and minimum-light readability conservatively.
- [x] Update pack-builder fallback, workflow labels, workflow triggers, and build-check version.
- [x] Add a B0.3.2-specific static validator.
- [x] Update About.md and CHANGELOG.md and add docs/B0.3.2_IMPLEMENTATION.md.
- [x] Run B0.3.2 static validator; it passes on the Android and multiplatform CI jobs.
- [ ] Run Android and multiplatform GitHub Actions builds.
- [ ] Inspect generated manifest, subpack order, output paths, and artifact names.
- [ ] Inspect the material-highlight result and confirm no unintended tinting or washed-out surfaces.
- [ ] Verify sunrise, sunset, daytime, rain, nighttime, clouds, water, aurora, and wet-ground effects.
- [ ] Check all profiles in mountains, dense forests, distant terrain, dense builds, water, rain, thunderstorms, particles, and night.
- [x] Apply a restrained texture-only readability pass to the nine existing ore texture assets; static validation checks that each PNG exists.
- [ ] Inspect all nine texture results in Minecraft and confirm ore colors remain natural and readable. Do not add emissive ore glow or a speculative shader color heuristic.
- [ ] Test Minecraft Bedrock 26.50 + MB Loader 26.52 on the vivo Y22s.
- [ ] Compare equivalent scenes and record FPS/frametime observations; distinguish shader cost from chunk-loading stutter.
- [ ] Fix build, compatibility, manifest, profile, or visual regressions before acceptance.

### Performance and validation rules

1. Reuse B0.2.9 optimizations when they remain correct; don't assume they eliminate every performance problem.
2. Prefer cheaper calculations over removing effects, unless testing proves removal is necessary.
3. Treat performance gains as a goal until tested in Minecraft. Never promise zero lag or a specific FPS from source inspection alone.
4. Keep all changes on b0.3.2-implementation. Do not merge into main without explicit approval.
5. Keep the final subpack lineup at three profiles. Custom Main Settings Entry remains scrapped.

---

## B0.2.9 — Terrain Performance Update

**Status:** B0.2.9 has been merged into `main` via PR #8. Static regression validation and Android/multiplatform build checks passed; manual in-game performance and visual validation remain pending.

### Goal

Reduce shader-side performance drops when facing mountains, forests, dense builds, and wide terrain on Android, especially on the vivo Y22s. Preserve the project's natural, cinematic Minecraft look and keep the effect set intact wherever practical. A successful compile does not guarantee zero lag; chunk loading and shader rendering must be evaluated separately in-game.

### Agreed profile direction

- **Default:** Keep the full visual feature set, four rounded-cloud density samples, glow, rain styling, aurora, atmospheric fog, and wet-ground effects. Modestly reduce the terrain-reflection range cap from 40 to 36.
- **Lite:** Keep the core visual identity, rain particles, atmosphere, wet ground, rounded clouds, and reduced-intensity aurora. Use a 24-unit terrain-reflection cap and three rounded-cloud density samples instead of four.
- **Subpack order:** Lite #1, Beta #2, Default #3. Beta remains an empty experimental slot.
- **Profile compilation:** The pack builder compiles the root material set using the `DEFAULT` define. Lite separately compiles the full material set with `LITE`; the Default subpack stays empty to inherit root materials and avoid duplicating shader binaries.
- **Preserved exclusions:** No water waves or custom water reflections, no plant/lantern waving, no godrays, no custom sky replacement, no dramatic sky events, and no player/mob shadow feature.

### Implementation checklist

#### Terrain and reflection
- [x] Inspect RenderChunk vertex and fragment paths, shared lighting, fog, and terrain reflection.
- [x] Identify the reflection-distance guard and the horizontal-plane reflection branch.
- [x] Keep puddle variation and wet-ground darkening intact while moving reflection-only cosine/blend calculations inside the horizontal-plane guard.
- [x] Review the terrain reflection path and limit the optimization to reflection-only calculations without stripping out core lighting or effects.
- [x] Keep the change bounded to terrain reflection; do not add actor/player/mob shadows.

#### Glow
- [x] Inspect Default's local emissive glow and Lite's compile-time skip.
- [x] Keep the four-cardinal local halo; remove unused corner sample declarations.
- [x] Preserve Default glow and shimmer; this material effect is not screen-space bloom.

#### Clouds and aurora
- [x] Inspect rounded-cloud density sampling and the current four-step default.
- [x] Keep four samples in Default and use three in Lite as a modest profile-specific trade-off.
- [x] Return early from aurora rendering during daytime, where the existing mask already makes its output exactly zero.
- [x] Preserve rounded clouds, nighttime aurora, rain transitions, and the existing sky pipeline.

#### Weather, fog, and entities
- [x] Inspect weather particle, occlusion, fog/mist, and actor/material paths.
- [x] Preserve rain particles, rain mist, cloudy fog, and wet-ground effects.
- [x] Keep the existing low-cost entity path; do not introduce new entity shadows or remove the main lighting system.
- [ ] Verify rain and entity-heavy scenes after building.

#### Profiles, build, and regression checks
- [x] Set display and manifest versions to B0.2.9 / 0.2.9.
- [x] Update the pack-builder fallback, workflow defaults, artifact labels, and build-check version.
- [x] Keep the workflow building current source and uploading Android artifacts.
- [x] Add static regression checks for version consistency, profile material compilation, feature-preservation constraints, and workflow labels.
- [x] Run Android and multiplatform build checks.
- [ ] Inspect the generated manifest, subpack order, compiled material outputs, and artifact paths.
- [x] Update the changelog and project-specific documentation to match the actual implementation status.

### Validation still required

- [x] Static validation passes.
- [x] GitHub Actions Android and multiplatform builds pass.
- [ ] Generated manifest shows version 0.2.9 and Lite, Beta, Default in that order.
- [x] CI compiles the root material set with `DEFAULT` and Lite with `LITE`.
- [ ] Compare forests, mountains, wide terrain, dense builds, weather, night, and aurora in both profiles.
- [ ] Confirm glow, rain particles, rain atmosphere, puddle variation, and wet-ground darkening remain visible.
- [ ] Test on the vivo Y22s using comparable scenes and distinguish shader load from chunk-loading stutter.
- [ ] Record visual regressions and performance observations before calling the update successful.

### Deferred idea

- The proposed standalone custom in-game Settings interface discussed for B0.3.2 has been scrapped for now. It is not part of B0.2.9 and should only be reconsidered through a new planning decision.

### Development rules

1. Make changes on `b0.2.9-implementation`, not `main`.
2. Keep changes targeted and explain the reason for each optimization.
3. Do not remove most shader effects to chase performance.
4. Treat source-based performance expectations as hypotheses until the shader compiles and the pack is tested in Minecraft.
5. Update build workflows and documentation alongside implementation.
6. Merge into `main` only after explicit approval.
