# Changelog

## B0.2.2 — Overworld Rework, Always Reflection & Terrain Shading
**Status: implementation in progress; build and in-game verification pending.**

### Visual identity
- Rework the Overworld palette toward warm, natural, semi-realistic vanilla lighting inspired by Newb Tropisphere's visual direction; no upstream shader code is copied as a substitute for original implementation.
- Reduce saturation and tame the earlier overly bright sky colors; coordinate dawn, daytime, night, rain and atmospheric fog.
- Restore more perceptible terrain depth while keeping block colors recognizable.

### Always Reflection tribute
- Re-enable the existing sky-reflection path for water and use a flat water normal; no animated water waves or displacement are added.
- Enable restrained always-on reflection for horizontal terrain, with stronger wet-ground response in rain and puddle variation.
- Enable aurora visuals and their reflection detail in Default; Lite retains a reduced-cost reflection path and the aurora itself at lower intensity.
- Bound terrain-reflection range, with a shorter range in Lite to reduce fragment work on mobile.

### Terrain shading and subpacks
- Replace cumulative green-channel threshold multipliers with a smooth, bounded RenderChunk terrain-shading ramp intended to avoid the black-striped distant-mountain artifact.
- Do not modify Actor shaders; the custom terrain correction does not add player or mob shadows.
- Replace five B0.1.9 profiles with exactly two options: Lite (first) and Default (second/right-most), both using the parent `BOX_CLOUDS` style.
- Shelve Soft Sunlight, Misty Mornings, Golden Hour, Rounded Clouds, Realistic Clouds, and Render Anim as selectable options.

### Build and documentation
- Set the display label to B0.2.2 and numeric manifest sub-version to 60.
- Update the pack-builder fallback and GitHub Actions workflow defaults.
- Add a source and in-game verification checklist; do not claim build success, exact visual results, or zero lag before verification.

### Verification still required
- [ ] CI build compiles all materials and produces the Android artifact.
- [ ] Generated manifest contains version 0.16.60 and exactly Lite then Default subpacks.
- [ ] Both subpacks render box clouds; Default is the initial selection in Minecraft.
- [ ] Water reflections work without visible wave animation or displacement.
- [ ] Horizontal terrain reflection and rainy wet-ground response are visible without unacceptable performance cost.
- [ ] Aurora/night effects remain visible; Lite has the intended reduced-cost behavior.
- [ ] Nearby blocks, foliage, distant mountains and terrain transitions show no black stripes.
- [ ] Confirm player/mob materials remain untouched by the custom terrain shading.
- [ ] Import and compare in-game on the target Android device; record observed performance.


## B0.1.9 — Subpack Reorganization, Atmospheric Profiles & Performance
**Status: implementation branch; build and in-game verification still required.**

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
