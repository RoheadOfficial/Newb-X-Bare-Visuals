# Plans

## B0.2.9 — Terrain Performance Update

**Status:** Implementation is in progress on `b0.2.9-implementation`. The planning branch remains separate, and `main` has not been changed.

### Goal

Reduce shader-side performance drops when facing mountains, forests, dense builds, and wide terrain on Android, especially on the vivo Y22s. Preserve the project's natural, cinematic Minecraft look and keep the effect set intact wherever practical. A successful compile does not guarantee zero lag; chunk loading and shader rendering must be evaluated separately in-game.

### Agreed profile direction

- **Default:** Keep the full visual feature set, four rounded-cloud density samples, glow, rain styling, aurora, atmospheric fog, and wet-ground effects. Modestly reduce the terrain-reflection range cap from 40 to 36.
- **Lite:** Keep the core visual identity, rain particles, atmosphere, wet ground, rounded clouds, and reduced-intensity aurora. Use a 24-unit terrain-reflection cap and three rounded-cloud density samples instead of four.
- **Subpack order:** Lite #1, Beta #2, Default #3. Beta remains an empty experimental slot.
- **Separate compilation:** Lite and Default must each compile their own material set with their profile define. An empty Default material list would cause the intended Default-specific settings to be skipped, so Default's material list must be explicit.
- **Preserved exclusions:** No water waves or custom water reflections, no plant/lantern waving, no godrays, no custom sky replacement, no dramatic sky events, and no player/mob shadow feature.

### Implementation checklist

#### Terrain and reflection
- [x] Inspect RenderChunk vertex and fragment paths, shared lighting, fog, and terrain reflection.
- [x] Identify the reflection-distance guard and the horizontal-plane reflection branch.
- [ ] Keep puddle variation and wet-ground darkening intact while moving reflection-only cosine/blend calculations inside the horizontal-plane guard.
- [ ] Review terrain fragment shading for repeated work without stripping out core lighting or effects.
- [ ] Leave the previous terrain shading correction bounded and isolated; do not add actor/player/mob shadows.

#### Glow
- [x] Inspect Default's local emissive glow and Lite's compile-time skip.
- [ ] Keep the four-cardinal local halo; remove unused corner sample declarations.
- [ ] Preserve Default glow and shimmer; do not describe this material effect as screen-space bloom.

#### Clouds and aurora
- [x] Inspect rounded-cloud density sampling and the current four-step default.
- [ ] Keep four samples in Default and use three in Lite as a modest profile-specific trade-off.
- [ ] Return early from aurora rendering during daytime, where the existing mask already makes its output exactly zero.
- [ ] Preserve rounded clouds, nighttime aurora, rain transitions, and the existing sky pipeline.

#### Weather, fog, and entities
- [x] Inspect weather particle, occlusion, fog/mist, and actor/material paths.
- [ ] Preserve rain particles, rain mist, cloudy fog, and wet-ground effects.
- [ ] Keep the existing low-cost entity path; do not introduce new entity shadows or remove the main lighting system.
- [ ] Verify rain and entity-heavy scenes after building.

#### Profiles, build, and regression checks
- [ ] Set display and manifest versions to B0.2.9 / 0.2.9.
- [ ] Update the pack-builder fallback, workflow defaults, artifact labels, and build-check version.
- [ ] Keep the workflow building current source and uploading Android artifacts.
- [ ] Add static regression checks for version consistency, profile material compilation, feature-preservation constraints, and workflow labels.
- [ ] Run Android and multiplatform build checks; inspect generated manifest, subpack order, compiled material outputs, and artifact paths.
- [ ] Update the changelog and project-specific documentation to match the actual implementation status.

### Validation still required

- [ ] Static validation passes.
- [ ] GitHub Actions Android and multiplatform builds pass.
- [ ] Generated manifest shows version 0.2.9 and Lite, Beta, Default in that order.
- [ ] Lite compiles with `LITE`; Default compiles with `DEFAULT`.
- [ ] Compare forests, mountains, wide terrain, dense builds, weather, night, and aurora in both profiles.
- [ ] Confirm glow, rain particles, rain atmosphere, puddle variation, and wet-ground darkening remain visible.
- [ ] Test on the vivo Y22s using comparable scenes and distinguish shader load from chunk-loading stutter.
- [ ] Record visual regressions and performance observations before calling the update successful.

### Development rules

1. Make changes on `b0.2.9-implementation`, not `main`.
2. Keep changes targeted and explain the reason for each optimization.
3. Do not remove most shader effects to chase performance.
4. Treat source-based performance expectations as hypotheses until the shader compiles and the pack is tested in Minecraft.
5. Update build workflows and documentation alongside implementation.
6. Do not merge into `main` without explicit approval.
