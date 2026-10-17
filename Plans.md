# Plans

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
