# B0.1 Foundation

## Purpose

B0.1 establishes the first Newb X Bare Visuals foundation for Minecraft Bedrock on Android. The visual target is vibrant, cinematic scenery with restrained atmosphere and animation, while prioritizing stable performance on the baseline Android device.

## Visual scope

- A subtle saturation increase of approximately 3% through the existing color-correction pipeline.
- Slightly warmer daylight and a balanced blue sky.
- Existing Newb lighting retained, with a small increase in daylight intensity and slightly softer baseline shadow contrast.
- Atmospheric fog retained with a modest increase in mist density.
- Rounded Clouds is the only active cloud style. Realistic and box-cloud options are shelved.
- The community-provided shadow-shading snippet is appended to src/materials/RenderChunk/fragment.sc after the existing color-correction step. Existing RenderChunk shading logic is preserved.

## Motion and water

- Plant movement remains enabled at reduced amplitude.
- Lantern movement remains enabled at reduced amplitude.
- Tree-leaf movement is excluded from the waving branch, and tree leaves return before the remaining per-vertex wave calculations.
- Optional entity edge highlighting is disabled to reduce shader work in mob-heavy scenes.
- A vanilla-style water path skips shader-added surface waves, custom water reflections, and water displacement. Engine transparency, the water texture, scene lighting, and fog remain part of the rendering path.

## Weather

- Rain particles remain enabled; the shader's particle-speck styling and rain slant are reduced.
- Rain mist remains enabled at a lower intensity.
- The existing wet-ground effect remains active during rain and thunderstorms. Its reflection distance and puddle variation are reduced to limit overhead.

## Performance intent

The source changes aim to reduce avoidable rendering work while retaining the requested effects. They do not guarantee a specific FPS or zero performance impact. Results depend on the Minecraft version, device, scene complexity, and shader loader.

## Test checklist

- [ ] Build the Android artifact successfully.
- [ ] Import and enable the artifact on the target Android device.
- [ ] Confirm water has no shader-added waves or surface reflections.
- [ ] Confirm grass/plants and lanterns move while tree leaves remain still.
- [ ] Check rain particle visibility and rain/thunder wet-ground appearance.
- [ ] Check rounded clouds, atmosphere, daylight, and the overall scenery.
- [ ] Inspect the added RenderChunk shadow shading for artifacts or excessive darkening.
- [ ] Compare FPS and frame stability against the original Newb demo in open terrain, dense forests, mob-heavy scenes, rain, and thunderstorms.

## Status

The source-level implementation is committed. Build success, in-game appearance, compatibility, and performance have not yet been verified.
