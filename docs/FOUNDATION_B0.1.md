# B0.1.1 Foundation Fix

## Purpose

B0.1.1 fixes the first Newb X Bare Visuals foundation for Minecraft Bedrock on Android. The visual target is vibrant, cinematic scenery with restrained atmosphere and animation, while prioritizing stable performance on the baseline Android device.

## Visual scope

- Saturation set to 1.442, exactly 3% above Newb's original 1.4 baseline through the existing color-correction pipeline.
- A natural blue daytime zenith, bright atmospheric horizon, restrained neutral horizon edge, and warm peach/coral dawn and dusk colors.
- Smooth day/night sky transitions driven by the existing Minecraft time-of-day calculation.
- Existing Newb lighting retained, with a small increase in daylight intensity and slightly softer baseline shadow contrast.
- Atmospheric fog retained and made rain-aware: rainy weather advances fog onset and increases mist density gradually.
- Rounded Clouds is the only active cloud style. Realistic and box-cloud options are shelved.
- The added community-provided RenderChunk shadow-shading snippet has been removed. The existing upstream shading pipeline and the separate vanilla-style water path are preserved.

## Motion and water

- Plant movement remains enabled at reduced amplitude.
- Lantern movement remains enabled at reduced amplitude.
- Tree-leaf movement is excluded from the waving branch, and tree leaves return before the remaining per-vertex wave calculations.
- Optional entity edge highlighting is disabled to reduce shader work in mob-heavy scenes.
- A vanilla-style water path skips shader-added surface waves, custom water reflections, and water displacement. Engine transparency, the water texture, scene lighting, and fog remain part of the rendering path.

## Weather

- Rain particles remain enabled; the shader's particle-speck styling and rain slant are reduced.
- Rain mist remains enabled; the fog fade function receives the detected rain factor so rainy conditions increase atmospheric depth.
- The existing wet-ground effect remains active during rain and thunderstorms. Its reflection distance and puddle variation are reduced to limit overhead.

## Performance intent

The source changes aim to reduce avoidable rendering work while retaining the requested effects. They do not guarantee a specific FPS or zero performance impact. Results depend on the Minecraft version, device, scene complexity, and shader loader.

## Test checklist

- [ ] Build the Android artifact successfully.
- [ ] Import and enable the artifact on the target Android device.
- [ ] Confirm water has no shader-added waves or surface reflections.
- [ ] Confirm grass/plants and lanterns move while tree leaves remain still.
- [ ] Check rain particle visibility and rain/thunder wet-ground appearance.
- [ ] Check rounded clouds, noon sky color, dawn/dusk warmth, nighttime, horizon blending, and overall scenery.
- [ ] Confirm rainy skies become overcast and rain fog advances the horizon naturally.
- [ ] Confirm time and rain transitions change smoothly rather than abruptly.
- [ ] Confirm the unwanted added shadow shading is gone and original Newb shading remains intact.
- [ ] Compare FPS and frame stability against the original Newb demo in open terrain, dense forests, mob-heavy scenes, rain, and thunderstorms.

## Status

B0.1.1 source-level changes are committed. Build success, in-game appearance, compatibility, and performance have not yet been verified. Target setup: Minecraft Bedrock 26.50, MB Loader 26.52, RenderDragon shader support on Android; baseline device: vivo Y22s.
