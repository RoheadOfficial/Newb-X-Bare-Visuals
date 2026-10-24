# Plans

## Current project direction — BONES roadmap

**Official project name:** Newb X Bare Visuals.  
**Informal series-family name:** BONES — B / O / N / E / S. This is a planning shorthand, not a rename of the shader pack.

- **Primary inspiration:** Newb X Future for visual ideas, shader techniques to investigate, atmospheric presentation, cloud design, and feature organization.
- **Source lineage:** Newb X Legacy / Newb X MCBE remains the foundation of this remix. Inspiration does not mean replacing the source tree with Future or copying its compiled assets.
- **Creative identity:** vanilla-recognizable Minecraft, natural and restrained color, cozy cinematic atmosphere, and mobile-minded performance. The creator approved B0.3.6's saturation; preserve it unless a tested regression gives a specific reason to change it.
- **Development order:** Overworld first; Nether only after Overworld acceptance; End only after Nether acceptance; The Sift only if it becomes available and testable and the project has reached that phase.
- **Current focus:** performance and polish, not another full visual redesign. Investigate tree-related lag and excessive nearby fog/haze before adding more effects.
- **Release philosophy:** do not claim FPS gains, compatibility, or release readiness from source inspection or a successful compile alone. Record comparable on-device observations.

The full project rules, version-family logic, profile roles, performance principles, licensing boundaries, and proposed retrospective mapping are recorded in [Important.md](Important.md). Historical sections below preserve what earlier versions aimed to do at the time; where they mention Prizma as inspiration, that is historical context and is superseded by the current Future-first direction.

## B0.3.7 — Polish, Performance & Compatibility

**Full version identity:** `B0.3.7.2652`  
**Simple version:** `B0.3.7`  
**Declared Minecraft target:** `26.52` (a target label, not proof of compatibility)  
**Status:** B0.3.7 versioning, documentation, validator, and duplicate-audit tooling have been merged into `main` via PR #12. CI results, duplicate-audit findings, visual/performance changes, and on-device acceptance remain to be verified.

### Goals

- Polish the existing B0.3.6 result rather than launch another full visual redesign.
- Use Newb X Future as the primary visual/technical reference going forward, while retaining Newb X Legacy as the source-code lineage and keeping Bare Visuals original.
- Treat Prizma Visuals as a historical mood reference from earlier planning, not the current primary inspiration.
- Preserve the creator-approved B0.3.6 saturation exactly unless testing identifies a concrete regression.
- Prioritize the Overworld until the creator accepts its performance and visuals. Current reported problems are persistent lag (especially around trees/dense terrain) and fog/haze that is too noticeable even nearby.
- Diagnose tree-related rendering cost and near fog independently; treat suspected bottlenecks as hypotheses until comparable in-game tests support them.
- Reduce visual clutter by checking how sky, fog, terrain lighting, clouds, water, and weather interact; do not add effects merely to enlarge the changelog.
- Investigate shader-side performance costs without removing effects blindly or promising FPS gains before comparable in-game tests.
- Prepare a compatibility check for the upcoming Minecraft drop and verify MB Loader support separately.
- Keep Default, Pootaytoe, and Bare Visuals distinct and in their existing order.
- Establish one canonical B-Series versioning implementation for metadata, logs, artifact filenames, and workflows.

### Versioning rules

- `B` identifies the main Bare Visuals project series. The B version is chosen according to the significance and scope of the overall project update; it is **not copied from** an Overworld, Nether, End, or Sift version.
- The current pre-release identity is `B0.3.7`. The planned stable-release identity is `B1`; use `B1.0.0` only if a stable subversion scheme proves useful.
- BONES dimension series use independent counters: `O` = Overworld, `N` = Nether, `E` = End, and `S` = The Sift (future/conditional). Their counters do not mirror the B-Series or one another. For example, `O0.3.8` does **not** imply `B0.3.8`.
- A dimension can receive several focused updates without forcing a B-Series bump. A substantial dimension milestone can influence the next B version when its scope justifies it, but this is a deliberate release decision—not an automatic conversion.
- For BONES-series labels, the working proposal is independent major/minor/patch-style progression: patch for narrow fixes, minor for a meaningful feature or optimization milestone within that dimension, and major for a major redesign of that dimension's work. Keep this interpretation marked as a working convention until the creator explicitly finalizes it.
- The full pack identity is derived from the simple B-Series version plus the declared Minecraft target with dots removed: `B0.3.7` + target `26.52` → `B0.3.7.2652`.
- If the declared target changes to `26.70`, the derived identity becomes `B0.3.7.2670`; this is metadata, **not proof of compatibility**.
- Keep the target in the separate `minecraft_target_version` config field. Keep the Minecraft manifest version numeric and valid; never put the full B-Series string into the manifest version array.
- Generate full version filenames and GitHub artifact labels through shared code, not duplicated hard-coded labels.
- The proposed historical O-Series mapping and `O0.6.0` baseline are retrospective planning aids, not manifest metadata or a claim that an O-Series release has already shipped. See `Important.md` for the complete logic and caveats.

### Profile roles

- **Default:** balanced main profile; preserve the complete visual identity and seek low-risk efficiency gains.
- **Pootaytoe:** performance-first profile; keep the core atmosphere while retaining the existing cheaper profile paths.
- **Bare Visuals:** fuller cozy atmosphere; prioritize visual character while still avoiding unnecessary shader cost.

Do not write internal inspiration percentages in player-facing metadata.

### Implementation checklist

- [x] Merge the creator-tested B0.3.6 source into `main` before basing B0.3.7 on it.
- [x] Create a dedicated B0.3.7 development branch.
- [x] Separate simple pack version and Minecraft target in pack configuration.
- [x] Centralize simple/full version derivation in `tool/versioning.py`.
- [x] Use the full version for build logs, output filenames, and dynamic GitHub Actions artifact labels.
- [x] Keep the manifest version numeric and the three subpacks in Default, Pootaytoe, Bare Visuals order.
- [x] Consolidate the active current-source validator rather than keep the B0.3.6-only validator wired into new builds.
- [x] Add a safe tracked-file duplicate audit; inspect and review its findings before deleting any identical copies.
- [ ] Run the duplicate audit in CI and review its report. Delete only verified redundant files; preserve intentional identical assets/notices.
- [ ] Inspect terrain fragment work, cloud sampling, fog/weather paths, and sky calculations for specific redundant cost.
- [ ] Make only source-level performance changes justified by inspection and visual-risk assessment; retain the approved saturation and visual features.
- [ ] Run B0.3.7 static validation and Android/multiplatform builds.
- [ ] Inspect generated manifest, subpack order, output paths, and artifact names.
- [ ] Test import, activation, and all three subpacks on the vivo Y22s.
- [ ] Compare B0.3.6 and B0.3.7 in equivalent dense forests, mountains, open terrain, water, clouds, rain/storms, and night scenes.
- [ ] Record FPS/stutter observations; distinguish shader rendering cost from chunk-loading or world-generation stutter.
- [ ] Test the current target and, when available, the upcoming stable Minecraft release; verify MB Loader compatibility separately.
- [ ] Do not claim 26.70 support or a 50–60+ FPS result without evidence.
- [ ] Keep changes isolated until CI passes and the creator approves the on-device result.

### Performance and safety rules

1. Treat potential shader bottlenecks as hypotheses until measured.
2. Do not lower cloud samples, remove atmosphere, or alter saturation just to claim a performance update.
3. Preserve vanilla-like water, lightweight rain, rain fog, wet-ground response, nighttime atmosphere, and the agreed exclusions: no godrays, water waves, waving vegetation, box clouds, or player/mob shadows.
4. Static validation and successful compilation do not establish visual quality, runtime compatibility, or FPS gains.
5. Treat the merge as implementation, not final acceptance. Review CI output, duplicate-audit findings, and on-device behavior before calling B0.3.7 complete or releasing it.

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
