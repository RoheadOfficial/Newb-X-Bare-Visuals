## B0.4.1 — Forest Performance Pass

**Status:** Implementation on `b0.4.1-forest-performance`, based on B0.4.0. Build/static checks and on-device comparison are pending; no FPS gain is claimed before testing.

### Implemented source changes
- Add a foliage-specific fast path in RenderChunk: alpha-tested foliage and billboards retain the regular vertex lighting but skip the generic opaque-terrain shade ramp, which was designed for opaque terrain and adds fragment work in dense forests.
- Skip the optional material-highlight approximation on alpha-tested foliage/billboards; keep it on eligible opaque terrain.
- Skip per-vertex glow-shimmer trigonometry for alpha-tested foliage and billboards. The center emissive texel glow remains enabled; only its shimmer modulation is omitted for these materials.
- Preserve the four profiles, approved saturation/tone mapping, rounded clouds, rain and wet ground, terrain Always Reflection on opaque terrain, water reflections, and no-waving behavior.
- Bump pack identity to B0.4.1 / manifest `[0, 4, 1]`; target label remains 26.52 and Android is the implementation build target.

### Verification required
- [ ] Static validator and duplicate audit pass; Android build completes and produces a directly installable `.mcpack` with compiled materials for all four profiles.
- [ ] Compare B0.4.0 vs B0.4.1 in the same dense forest, stationary and moving, with matching settings.
- [ ] Check leaf brightness/tint, emissive textures, reflection behavior, and terrain appearance; reject or revise any visible regression.
- [ ] Test all four profiles separately and record FPS/stutter observations. Build success is not FPS proof.
- [ ] Separate new-chunk loading stutters from the shader's scene-dependent rendering cost; the pack cannot directly optimize Minecraft's internal chunk generation.

## B0.4.0 — Targeted Performance Fixes

**Status:** Source implementation on `b0.4.0-performance-fixes`. Android build/static checks and in-game acceptance are pending; FPS gains are not claimed until measured on-device.

### Implemented
- Skip terrain Always Reflection calculations for alpha-tested foliage and billboards, whose fragments cannot display the horizontal terrain-reflection mask; keep reflection on opaque terrain with shorter profile-specific far-field limits.
- Skip sky-color rendering for nearby terrain when clear-weather fog alpha is effectively zero; preserve sky-derived fog when fog can contribute or rain is active.
- Reuse sun dawn/night factors in sunlight tinting rather than recalculating them per terrain/entity vertex.
- Remove the second weather-texture lookup per particle and replace its overlay with cheaper analytic modulation. Minecraft's particle spawn count is unchanged.
- Reduce rounded-cloud density steps to two in all profiles; retain a sky reflection across visible water but use a cheap horizon-to-zenith gradient beyond each profile's full-reflection range, while separately limiting extra aurora detail.
- Guard transparent Actor Glint against unnecessary texture sampling; retain both glint layers when the effect is visible.
- Preserve approved saturation, natural color, rain/wet ground, rounded clouds, nighttime aurora, and terrain Always Reflection. No waving, godrays, or player/mob shadow systems were added.

### Verification required
- [ ] Static validator and duplicate audit pass.
- [ ] Android GitHub Actions build succeeds and artifact is a directly installable `.mcpack` containing all expected RenderChunk binaries.
- [ ] On-device A/B test in a fixed world for dense trees, clear-weather terrain, heavy rain, large water, wide sky, and enchanted actors.
- [ ] Check for reflection fade/pop-in, foliage wetness differences, cloud quality, rain appearance, and fog transitions in all four profiles.
- [ ] Confirm Minecraft 26.52 / MB Loader 26.52 runtime behavior; target metadata alone is not proof of compatibility.

## B0.3.8 / O6.0 — Performance, Atmosphere & Water Refinement

**Status:** Implementation on `b0.3.8-o6-performance-implementation`. Static checks and Android build are pending; no in-game FPS or visual acceptance is claimed.

### Implemented source changes
- Add a near-midday tree-foliage lighting fast path that skips spatial sun attenuation when its dawn contribution is negligible.
- Replace exponential mist with a lower-cost smooth curve, reduce mist and rain-mist strength, and disable the costly sinusoidal cloudy-fog overlay.
- Restore the custom Newb water path and base sky reflections; use a muted mineral-gray/cool-glass water tint without extra textures or render passes.
- Keep base water reflections active while limiting extra aurora reflection detail to night/twilight and profile-specific distances.
- Reduce rounded-cloud sampling in Default, Bare Visuals, and Experimental; Pootaytoe retains its lower-cost two-sample setting.
- Reduce weather-particle styling while keeping weather particles, rain atmosphere, wet ground, and auroras.
- Skip four extra glow-halo texture taps on alpha-tested foliage while retaining the center emissive glow.
- Add a global compile-time guard that blocks vegetation, lantern, water, and underwater waving.
- Bump the development and numeric manifest version to B0.3.8 / `[0, 3, 8]`; keep Android as the implementation build target.

### Verification still required
- [ ] Static validator and duplicate audit pass.
- [ ] Android GitHub Actions build succeeds; inspect generated manifest, profile order, and all compiled materials.
- [ ] Confirm terrain Always Reflection remains clearly visible nearby and its shorter far-field cutoff avoids distracting pop-out.
- [ ] Confirm custom water reflection compiles and is visible in-game without excessive cost.
- [ ] Compare tree-heavy scenes against B0.3.7 to quantify the 50% overhead target.
- [ ] Check fog, rain, water, cloud and aurora appearance across all four subpacks.
- [ ] Confirm no waving paths are active in compiled profiles.
- [ ] Verify Minecraft/MB Loader compatibility and visual quality in-game when storage permits.

## B0.3.7 — Polish, Performance & Compatibility

**Status:** Implementation changes are on `b0.3.7-implementation`. Android build and in-game acceptance are pending. Multiplatform builds are deferred until release preparation.

### GAME
- Preserve the B0.3.6 visual foundation and creator-approved saturation.
- Remove the aggressive sun-source brightness boost; retain the normal sky gradient and sun/moon disk.
- Keep vanilla-water rendering and subtly reduce its blue channel by 8%, without adding water reflections or waves.
- Preserve Default, Pootaytoe, and Bare Visuals, and add Experimental as profile four.
- Experimental uses bounded fake terrain shading from existing vertex-lighting gradients. It is not a shadow map and does not create genuine tree-canopy, player, or mob shadows.

### DEVELOPER
- Fix Pootaytoe's terrain glow-sample shortcut to recognize `POOTAYTOE` as well as legacy `LITE`.
- Add `NL_EXPERIMENTAL_FAKE_SHADOW_STRENGTH` only under Experimental.
- Reuse existing terrain vertex-color data; add no texture reads, shadow maps, normal reconstruction, or render passes.
- Update pack configuration, validator, docs, and CI for four profiles.
- Make implementation build-check Android-only and set the manual build default to Android. Keep the manual workflow available for multiplatform release builds.
- Preserve `B0.3.7`, `B0.3.7.2652`, target `26.52`, numeric manifest version `[0, 3, 7]`, attribution, patch warning, and licensing notices.

### Validation checklist
- [x] Create clean implementation branch from current `main`.
- [x] Add Experimental as profile four.
- [x] Remove aggressive sky-source boost and add restrained water blue reduction.
- [x] Fix Pootaytoe's glow shortcut define.
- [x] Update static validation, docs, and Android-only workflow.
- [x] Review duplicate-audit findings. The reported matches are shared material.json/config.json files across material definitions; retained these identical source templates because they appear intentional and removing them could break material compilation. No confirmed accidental duplicate was deleted.
- [ ] Pass static validation and Android-only GitHub Actions build.
- [ ] Inspect generated Android pack, manifest, profile order, and compiled materials.
- [ ] Test all four profiles on Vivo Y22s and compare visuals/FPS in equivalent scenes.
- [ ] Verify Minecraft and MB Loader compatibility independently.
- [ ] Run multiplatform build during release preparation only.
- [ ] Keep `main` untouched until creator acceptance.

---

---

## B0.3.6 — Java-Inspired Cozy Shader Revamp

**Status:** Merged into `main` via PR #10. The creator tested B0.3.6 and approved its overall look, especially its saturation. Measured FPS improvement, complete generated-artifact review, and compatibility beyond the tested setup remain unverified.

### GAME
- Begin a coordinated visual redesign across terrain lighting, sky/horizon, fog, rounded clouds, and the three established subpacks.
- Aim for a balanced Java-shader-inspired look on Bedrock: natural colors, clearer terrain depth, a soft integrated horizon, and cozy dawn/sunset atmosphere without oversaturation.
- Preserve Default as the balanced main experience, Pootaytoe as the performance-focused profile, and Bare Visuals as the full Prizma-inspired visual direction.
- Retain vanilla-like water, rain particles, rain atmosphere, wet-ground response, rounded clouds, and nighttime atmosphere.
- Keep water waves, Always Reflection, godrays, box clouds, plant/lantern waving, and player/mob shadows excluded.

### DEVELOPER
- Add a low-cost horizon band using the existing sky colors; no extra texture reads or render pass.
- Reduce the fog mist response and moderate rain-driven fog advance to protect distant-forest and mountain visibility.
- Move the shared color pipeline to ACES tone mapping with a matching inverse curve for fog-color compensation.
- Balance directional lighting against sky ambient contribution, with per-profile settings.
- Round and thicken cloud shapes without increasing the configured ray sample count; Pootaytoe remains at two samples while Default and Bare Visuals retain four.
- Retain the bounded terrain shading and reflection paths, and keep the terrain material response free of additional texture reads.
- Update B-Series metadata, pack-builder fallback, workflows, artifact names, and static validation for B0.3.6.

### Validation checklist
- [x] B0.3.6 static validator passed on the implementation branch.
- [ ] Android and multiplatform GitHub Actions builds pass.
- [ ] Generated manifest reports version 0.3.6 and subpack order Default, Pootaytoe, Bare Visuals.
- [ ] Inspect compiled output and confirm each subpack's profile-specific defines and materials.
- [ ] Compare old and new builds in open terrain, dense forests, mountains, water, rain/storms, and nighttime.
- [ ] Test on vivo Y22s with MCBE 26.50 + MB Loader 26.52, recording comparable FPS/frame-time observations.
- [ ] Verify the horizon blend, terrain lighting, reduced fog washout, rounded cloud shape, and each profile's distinct identity in-game.
- [ ] Do not claim the 50–60 FPS target or final visual acceptance until measured on-device.

---

## B0.3.2 — Beauty & Performance

**Status:** Implementation branch created; source changes are in progress. Static validation, GitHub Actions builds, generated-artifact inspection, and in-game visual/performance testing are required before acceptance.

### GAME
- Give Default, Pootaytoe, and Bare Visuals their own identities while keeping all three performance-minded.
- Default balances natural daylight, warmer sunsets/evenings, believable soft-blue water, rounded clouds, rain, wet-ground response, aurora, and restrained local glow.
- Pootaytoe makes more aggressive, targeted savings while preserving the core look, rain, wet ground, rounded clouds, and nighttime atmosphere where practical.
- Bare Visuals emphasizes cozy peach/golden sunrises and sunsets, softer blue skies, rounded clouds, gentle haze, and screenshot-worthy scenery without oversaturation.
- Keep the vanilla-water path. No always-on water reflections, water waves, godrays, box clouds, plant/lantern waving, or custom player/mob shadows.
- Add only subtle, inexpensive PBR-inspired material highlights; do not claim full PBR or use a costly environment-reflection pass.
- Apply restrained contrast/readability enhancement to the existing copper, diamond, emerald, gold, iron, lapis, nether gold, quartz, and redstone ore textures. Keep the treatment texture-only; do not add emissive ore glow.

### DEVELOPER
- Carry forward B0.2.9's bounded terrain-reflection work, daytime aurora early-out, cardinal-only glow sampling, and separate root/subpack compilation model.
- Reduce the shared terrain-reflection cap and tune each profile independently: Default 32 units, Pootaytoe 20, Bare Visuals 30.
- Retain four rounded-cloud samples for Default and Bare Visuals; reduce Pootaytoe to two as its intentional quality/performance trade-off.
- Use a color-based material-highlight approximation only on opaque, non-season terrain. It adds no texture reads and is disabled in Pootaytoe.
- Use the Default root material set for the Default subpack; compile the complete material set separately for Pootaytoe and Bare Visuals with their own defines.
- Update pack version metadata, builder fallback, workflows, artifact labels, and static validation for B0.3.2.
- Preserve the original Newb README and keep project-specific identity/documentation in About.md and the project docs.

### Validation checklist
- [ ] B0.3.2 static validator passes.
- [ ] Android and multiplatform GitHub Actions builds pass.
- [ ] Generated manifest reports version 0.3.2 and subpack order Default, Pootaytoe, Bare Visuals.
- [ ] Default uses the root materials compiled with DEFAULT; Pootaytoe and Bare Visuals compile their complete material lists with their own defines.
- [ ] Confirm all profiles preserve rain particles, rain fog/mist, wet-ground response, rounded clouds, readable night sky, and intended aurora behavior.
- [ ] Confirm vanilla water remains free of custom reflection/displacement and no godrays, box clouds, vegetation waving, or player/mob shadows are introduced.
- [ ] Compare mountains, dense forests, distant terrain, dense builds, water, rain, thunderstorms, particles, and night.
- [ ] Check Bare Visuals sunrise/sunset color transitions, terrain color readability, cloud shape, and soft-blue water; ensure the sky does not remain sunset-colored all night.
- [ ] Inspect the material-highlight approximation for visible but restrained results and ensure it does not tint unrelated blocks or wash out highlights.
- [ ] Test on the vivo Y22s using comparable scenes, recording FPS/frametime observations and separating shader load from chunk-loading stutter.
- [ ] Confirm compatibility with Minecraft Bedrock 26.50 + MB Loader 26.52 and inspect the final .mcpack artifact.
- [ ] Fix any CI, manifest, subpack, or in-game regressions before considering the update complete.

---

## B0.2.9 — Terrain Performance & Profile Tuning

**Status:** Merged into `main` via PR #8. The static regression validator and Android/multiplatform build checks passed on the implementation branch. In-game performance and visual acceptance remain pending.

### GAME
- Keep the natural, cinematic Newb X Bare Visuals look while targeting fewer shader-side stalls when facing forests, mountains, and wide terrain.
- Keep rain particles, rain atmosphere, wet-ground response, rounded clouds, night aurora, Default glow, and the existing sky pipeline.
- Lite uses a shorter terrain-reflection range and three rounded-cloud density samples; Default keeps four cloud samples and a modestly reduced reflection cap.
- No water waves, plant/lantern waving, godrays, custom sky replacement, or dramatic sky events are introduced.

### DEVELOPER
- Defer terrain-reflection cosine and blend-strength work until a vertex is on the reflective horizontal plane; keep puddle variation for wet-ground darkening.
- Add an exact daytime early-out to the aurora function where the existing output mask is already zero.
- Keep the local glow halo's four cardinal taps and remove unused corner sample declarations.
- Keep the root material set compiled with `DEFAULT` and Lite compiled separately with `LITE`; leave Default's subpack material list empty to avoid duplicating shader binaries.
- Align manifest/display versions, pack-builder fallback, workflow inputs, artifact names, and build-check version to B0.2.9.
- Add static regression validation for version/profile metadata and protected shader features.
- No claim of zero lag or visual equivalence until CI builds and in-game testing are complete.

### Validation checklist
- [x] Static B0.2.9 validator passes.
- [x] Android and multiplatform build-checks pass.
- [ ] Generated manifest reports version 0.2.9 and subpack order Lite, Beta, Default.
- [ ] Default actually compiles its own materials with the DEFAULT define; Lite compiles with LITE.
- [ ] Compare Lite and Default in forests, mountains, dense builds, rain, night, and aurora scenes.
- [ ] Confirm wet-ground darkening and puddle variation remain visible.
- [ ] Confirm glow remains visible in Default and rain particles remain enabled in both profiles.
- [ ] Test on the vivo Y22s with the same view/scene before and after; separate shader cost from chunk-loading stutter.
- [ ] Confirm no large visual regression in rounded clouds, daytime sky, night sky, fog, or lighting.

## B0.2.6 — Natural Lighting, Performance & Effects
**Status: implementation branch; build and in-game verification pending. B0.2.5 was accepted by the creator after testing.**

### Lighting
- Slightly enrich sunlight and color while preserving natural vanilla colors and avoiding oversaturation.
- Keep the existing sky/lighting architecture and use restrained tuning rather than a dramatic visual overhaul.

### Performance
- Disable plant and lantern waving to remove their per-vertex wave calculations from the active path.
- Reduce rounded-cloud ray steps from 5 to 4.
- Shorten the terrain-reflection distance and hard cap to reduce fragment work in large terrain views.
- Keep Lite's reflection range shorter and disable its glow-bleed samples.

### Water and glow
- Enable the existing vanilla-water path so custom water reflection and tinting are bypassed. Terrain-only reflection remains separate.
- Add a faint four-direction, texture-local bloom-like emissive halo. This is not screen-space bloom and avoids a separate render pass.

### Beta
- Remove the Beta-only dynamic-lighting and indoor contact-shading prototypes.
- Leave Beta as an empty experimental slot for future tests.

### Validation still required
- [ ] Android and multiplatform build checks pass.
- [ ] Generated manifest confirms version 0.2.6 and subpack order Lite, Beta, Default.
- [ ] Confirm water has no custom sky reflection in-game.
- [ ] Compare lighting with the creator's supplied natural-lighting references at noon, dawn/dusk, rain, and night.
- [ ] Test performance facing forests, mountains, dense villages, and distant terrain on the target Android device.
- [ ] Check the subtle glow on emissive textures and ensure it does not wash out nearby blocks.

# Changelog

## B0.2.5 — Visual Refinement, Performance & Beta Experiments
**Status: implementation in progress on `b0.2.5-implementation`; CI and in-game verification pending.**

### Current source changes
- Set display version B0.2.5 and numeric manifest version `[0, 2, 5]`; generated manifest inspection is still required.
- Configure MCpack order: Lite #1, Beta #2, Default #3.
- Switch active cloud type to rounded clouds; shelve box clouds.
- Disable the water-only Always Reflection macro while retaining the separate terrain reflection path.
- Add a nighttime alpha fade for rounded clouds and increase configured aurora intensity.
- Adjust base lighting toward restrained saturation, softer sunlight, and more readable terrain.
- Reduce Default's weather overlay from 0.35 to 0.3465 (1% relative).
- Add Beta-only prototypes for existing lightmap-driven torch response and terrain contact shading. These are not full dynamic-light injection, true indoor reflections, or shadow maps.
- Update workflow version defaults, artifact labels, and pack-builder fallback.

### Remaining implementation and verification
- Review all active shader paths to ensure godrays are absent; no active godray toggle was found in the current config.
- Build Android and multiplatform artifacts; inspect generated manifest and subpack order.
- Test rounded clouds, night fade, aurora, lighting, water, and performance in Minecraft.
- Continue investigating why B0.2.2's terrain correction was not visibly effective.
- Determine what true dynamic lighting and indoor reflections the Bedrock/MB Loader pipeline supports before claiming those features complete.

### Visual direction
- Replace box clouds with the existing `rounded_clouds` implementation in both Lite and Default.
- Reduce rain particles in Default by 1% relative to its current setting; keep rain visible.
- Rework lighting and overall shader style using the creator's supplied Minecraft screenshots as visual references: natural, lush, warm, cinematic, and atmospheric without harsh oversaturation.
- Remove godrays from the active shader path.
- Improve nighttime aurora appearance and make light clouds fade substantially at night/midnight instead of retaining daytime visibility.
- Remove the Always Reflection treatment from water while evaluating terrain reflection separately.

### Experimental Beta subpack
- Add a selectable Beta profile for testing features before deciding whether to promote them to Lite or Default.
- Planned experiments: dynamic lighting and indoor reflections/shadow behavior.
- Keep experimental features isolated from stable subpacks until they compile, look correct, and pass performance testing. Dynamic lighting and indoor reflections/shadows are goals, not confirmed existing features.

### Shadow-shading follow-up
- B0.2.2's terrain shading change was not visibly effective in the creator's test. Inspect the actual rendering path and material inputs before adjusting thresholds again; do not assume that the current color ramp creates real shadows.
- Keep terrain/block/foliage shading separate from actor materials. No player/mob shadow feature is requested by this correction.

### Validation priorities
- [ ] Compare rounded clouds in both subpacks in daytime and at night.
- [ ] Confirm Default rain-particle change is exactly 1% relative to its prior configured value.
- [ ] Verify day, dawn/dusk, night, midnight, rain, and aurora appearance against the supplied screenshots and intended style.
- [ ] Confirm godrays are not active in any subpack.
- [ ] Confirm water no longer receives Always Reflection while other intended reflection behavior is evaluated independently.
- [ ] Profile Lite, Default, and Beta on Android in forests, mountains, villages, rain, and night scenes.
- [ ] Validate dynamic lighting and indoor reflection/shadow experiments separately before considering promotion.

## B0.2.2 — Overworld Rework, Always Reflection & Terrain Shading
**Status: merged into `main`; Android build/artifact passed, but creator's in-game test found major visual and performance improvements are needed. B0.2.5 is the planned follow-up.**

### Visual identity
- Rework the Overworld palette toward warm, natural, semi-realistic vanilla lighting inspired by Newb Tropisphere's visual direction; no upstream shader code is copied as a substitute for original implementation.
- Reduce saturation and tame the earlier overly bright sky colors; coordinate dawn, daytime, night, rain and atmospheric fog.
- Restore more perceptible terrain depth while keeping block colors recognizable.

### Always Reflection tribute
- Re-enable the existing sky-reflection path for water and use a flat water normal; no animated water waves or displacement are added.
- Enable restrained always-on reflection for horizontal terrain, with stronger wet-ground response in rain and puddle variation.
- Enable aurora visuals and their reflection detail in Default; Lite retains a reduced-cost reflection path and the aurora itself at lower intensity, but disables aurora reflection detail. Rainbows, shooting stars, galaxy stars, and godrays remain excluded; the original Newb sky pipeline is retained.
- Bound terrain-reflection range, with a shorter range in Lite to reduce fragment work on mobile.

### Terrain shading and subpacks
- Replace cumulative green-channel threshold multipliers with a smooth, bounded RenderChunk terrain-shading ramp intended to avoid the black-striped distant-mountain artifact.
- Do not modify Actor shaders; the custom terrain correction does not add player or mob shadows.
- Replace five B0.1.9 profiles with exactly two options: Lite and Default, both using the parent `BOX_CLOUDS` style. This was later identified for reversal in B0.2.5.
- Shelve Soft Sunlight, Misty Mornings, Golden Hour, Rounded Clouds, Realistic Clouds, and Render Anim as selectable options.

### Build and documentation
- Set the display label to B0.2.2 and numeric manifest sub-version to 60.
- Update the pack-builder fallback and GitHub Actions workflow defaults.
- Add a source and in-game verification checklist; do not claim build success, exact visual results, or zero lag before verification.

### Verification still required
- [x] Android CI build compiled the current B0.2.2 branch and uploaded its Android artifact.
- [ ] Generated manifest contains version 0.16.60 and exactly Lite then Default subpacks.
- [ ] Both subpacks render box clouds; Default is the initial selection in Minecraft.
- [ ] Water reflections work without visible wave animation or displacement.
- [ ] Horizontal terrain reflection and rainy wet-ground response are visible without unacceptable performance cost.
- [ ] Aurora/night effects remain visible; Lite has the intended reduced-cost behavior.
- [ ] Nearby blocks, foliage, distant mountains and terrain transitions show no black stripes.
- [ ] Confirm player/mob materials remain untouched by the custom terrain shading.
- [x] Creator imported and tested B0.2.2 in-game; reported that the look needs major improvement and performance needs further optimization.
- [ ] Repeat visual and performance checks after B0.2.5 changes.


## B0.1.9 — Subpack Reorganization, Atmospheric Profiles & Performance
**Status: merged into main; later in-game testing found the overall visual result underwhelming. B0.2.2 supersedes this direction.**

### Subpacks and clouds
- Reorganized the player-facing choices into Default, Soft Sunlight, Misty Mornings, Golden Hour, and Lite, with descriptive labels for every option.
- Restored the realistic cloud renderer as the base/Default cloud style.
- Shelved the Render Anim subpack without deleting its source implementation.
- Moved Rounded Clouds into Lite; Lite also disables optional aurora, rainbow, shimmer, lava, and weather styling effects where applicable.

### Complete atmosphere profiles
- Added separate compile-time profiles for Soft Sunlight, Misty Mornings, and Golden Hour.
- Each profile coordinates sun/moon light, sky colors for day/night/dawn, rainy-sky colors, fog/mist, and water tint instead of only adjusting daytime light.
- Godrays are excluded from B0.1.9; the old hook and its active call were removed.

### Performance and maintenance
- Reduced the shared plant/lantern movement range from 13 to 9 blocks to limit distance movement work.
- Lite skips the extra glow texture sample on terrain fragments and disables several optional effects.
- Updated the display label to B0.1.9 and the numeric manifest sub-version to 59.
- Updated build workflow defaults and current subpack documentation.
- Added implementation notes and an in-game/performance verification checklist.

### Validation status
- Source changes are on b0.1.9-implementation.
- CI compilation, artifact inspection, in-game appearance, and vivo Y22s performance remain to be verified. No zero-lag or in-game visual result is claimed.


## B0.1.7 Deluxe — Natural Light, Mist, Water & Godrays

### Visual identity
- Reduced `NL_SATURATION` from 1.4 to 1.25 to let lighting and atmosphere carry the look.
- Softened direct sunlight intensity to 3.20 and adjusted noon light toward a warm-neutral tone.
- Tuned dawn/dusk sunlight to a restrained amber for the Golden Hour identity.
- Increased baseline mist slightly to 0.22; rain-mist opacity is reduced to 0.12 to avoid heavy weather fog.

### Water
- Added a restrained cool water tint in the existing vanilla water fragment path.
- Preserved engine-provided transparency and fog blending. No custom water waves, displacement, or reflection pass was added.

### Godrays and performance
- Enabled the existing lightweight fake-godray hook at strength 0.12. It is designed for sunrise/sunset and adds no separate render pass or texture.
- It still adds shader calculations and needs FPS testing on the vivo Y22s; performance is not assumed from source inspection alone.
- Kept the current Newb lighting pipeline, rounded clouds, and existing materials.

### Build identity
- Bumped the numeric manifest sub-version to 58 and the display label to `B0.1.7 Deluxe`.
- Updated the artifact filename slug and build workflows; corrected the build-check artifact directory to match the builder output.

### Validation status
- GitHub Actions Android and multiplatform artifact-generation workflows completed successfully for the tested Deluxe branch.
- PR #2 was merged into main at commit 3130ae86053ab1fa456b44ae1e186bef10f2af02.
- The user reported that the saturation reduction was visible but the sunlight, mist, and Golden Hour differences were too subtle. In-game visual acceptance was therefore not achieved for those changes; FPS testing remains unverified.


## B0.1.7 — Original Sky Restoration & Visual Identity

### Sky restoration
- Restored `src/newb/functions/sky.h` byte-for-byte from upstream Newb X Legacy commit `c57aefa9309ec76c2e9bb500492b6b389321878a`.
- Restored the upstream sky implementation, but the sky-color configuration in `src/newb/config.h` remained custom and was not fully restored to upstream. The earlier description overstated the scope of the configuration restoration.
- Removed the custom sky interpolation and horizon overlay by returning to the upstream sky implementation.

### Natural color and lighting
- Set `NL_SATURATION` to `1.4` as the starting baseline; in-game comparison is still required before deciding whether to reduce it further.
- Tuned daylight intensity, shadow intensity, and noon light color subtly without adding a new bloom/glare pass.
- Kept the upstream tonemapping and existing vanilla-style water path. Saturation is not the project's differentiator.

### Weather Improvements 2.0
- Retained rain-aware fog integration across the existing material vertex shaders.
- Made the rain-driven fog-start/end shift more restrained, reduced the rain-density multiplier, and softened the additional rain fade blend.
- Reduced baseline mist density and rain-mist opacity to avoid heavy grey fog and protect mobile performance.
- Shelved Misty Mornings and a separate Golden Hour sky tint unless real tests show they can be added without breaking original sky behavior.

### Pack identity and B-Series versioning
- Added `development_version = "B0.1.7"` to the pack configuration.
- Updated build output, compiled material labels, generated description, and artifact filename to use B-Series labels while preserving the numeric Minecraft manifest version.
- Added subtle Minecraft formatting-color accents and Unicode small-caps lettering to the generated manifest description; no unsupported manifest fields or fake font settings were added.
- Set the workflow's default numeric manifest sub-version to `57` and documented its relationship to the B-Series display label.

### Validation status
- Source and documentation updates are staged on the B0.1.7 implementation branch.
- GitHub Actions build, artifact inspection, Android import, weather/sky checks, compatibility, and vivo Y22s performance testing are pending. No successful build or in-game result is claimed.

## B0.1.1 — Foundation Fix

### Sky and time
- Replaced the overbright cyan daytime palette with a more natural blue zenith, a lighter atmospheric horizon, and a restrained neutral horizon edge.
- Tuned dawn/dusk colors toward warm peach and coral while preserving distinct daylight and nighttime palettes.
- Replaced the hard day/night sky switch with a smooth transition driven by the existing Minecraft time-of-day calculation.
- Added a restrained atmospheric horizon blend for a softer sky-to-distance transition.

### Weather and fog
- Strengthened the existing rainy-sky blend and kept rainy-night brightness lower than daytime rain.
- Passed the already-detected rain factor into the existing fog fade calls.
- Made fog begin sooner and mist density increase gradually during rain, without replacing the upstream fog pipeline.

### Preservation and correction
- Removed the added community-provided shadow-shading snippet from RenderChunk fragment shading.
- Corrected the saturation value to 1.442, which is 3% above the original 1.4 baseline.
- Preserved the existing Newb materials and rendering systems, rounded clouds, vanilla-style water path, and existing animation/weather features.

### Validation status
- Source and documentation edits are committed to main.
- Compilation and the generated Android artifact have not yet been confirmed.
- In-game visuals, time/weather transitions, compatibility, and performance still require testing on MCBE 26.50 with MB Loader 26.52.

## B0.1 — Foundation source pass

### Visual direction
- Set rounded clouds as the active cloud style and removed the realistic-cloud, box-cloud, no-wave, no-fog, and combined no-wave/no-fog subpack choices.
- Added a subtle 3% saturation increase, slightly warmer daylight, a balanced blue sky, and a small increase in atmospheric mist.
- Retained the existing Newb lighting pipeline and shadow system while adding the community-provided RenderChunk shadow-shading snippet.

### Animation and water
- Retained gentle plant movement and reduced lantern sway.
- Disabled tree-leaf waving and skip remaining wave calculations for tree leaves.
- Disabled optional entity edge highlighting to reduce shader work in mob-heavy scenes.
- Added a vanilla-style water path that skips shader-added water waves, custom surface reflections, and water displacement.

### Weather and performance
- Reduced rain-particle styling intensity without removing rain particles.
- Reduced rain-mist intensity.
- Kept the wet-ground effect during rain and thunderstorms while reducing its visible range and puddle intensity.

### Validation status
- Source edits are committed to main.
- A fresh artifact build has not yet been confirmed.
- Android in-game visuals, shader compatibility, and FPS performance remain unverified.
