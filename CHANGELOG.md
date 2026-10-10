# Changelog

## B0.1.7 — Original Sky Restoration & Visual Identity

### Sky restoration
- Restored `src/newb/functions/sky.h` byte-for-byte from upstream Newb X Legacy commit `c57aefa9309ec76c2e9bb500492b6b389321878a`.
- Restored the upstream sky configuration block, including original day/night, dawn/dusk, and rain-sky colors and rain blending.
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
