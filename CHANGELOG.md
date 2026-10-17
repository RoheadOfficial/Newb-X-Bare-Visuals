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
