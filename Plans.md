# Plans

## B0.2.9 — The Performance Update

**Status:** Discussion and repository investigation only. No B0.2.9 shader code changes have been approved or started.

### Main goal

Improve performance on Android, especially on the vivo Y22s, by investigating the noticeable FPS drops that happen when facing mountains, forests, and other large or complex terrain.

The goal is to reduce unnecessary rendering work while preserving the project's natural, cinematic Minecraft look. Do not promise a specific FPS gain until it has been tested on-device.

### Observed issue

- **Main symptom:** Noticeable FPS drops when facing mountains, forests, and large terrain.
- **Severity:** Noticeable FPS drops.
- **Primary target:** Android / vivo Y22s.
- **Important distinction:** Stutters can come from shader rendering, Minecraft chunk loading, or both. Do not assume the shader is the only cause without evidence.

### Repository investigation so far

The B0.2.6 implementation branch has been inspected for the main terrain and supporting shader paths. These are investigation candidates, not confirmed bottlenecks:

1. **Terrain rendering (`src/materials/RenderChunk/vertex.sc` and `fragment.sc`)**
   - Terrain vertex processing includes environment detection, lighting, fog, and optional wave logic.
   - Terrain fragment processing includes texture sampling, optional glow, terrain shading correction, reflection-related work, and fog/color correction.
   - Large views can multiply per-fragment costs. Investigate what can be reduced safely before changing appearance.

2. **Glow (`src/newb/functions/glow.h` and the RenderChunk fragment shader)**
   - Default calls `nlGlow` on terrain fragments; Lite skips the additional glow calculation.
   - Glow is a concrete candidate for comparison, but its actual impact on the observed drops is not yet measured.

3. **Terrain reflection (`src/newb/functions/rain.h` and RenderChunk shaders)**
   - B0.2.6 limits the reflection distance, but terrain reflection-related logic remains in the shader.
   - Inspect how it is enabled and evaluated. Do not assume it is the main cause without testing.

4. **Cloud rendering (`src/materials/Clouds/vertex.sc` and cloud functions)**
   - The rounded-cloud path performs repeated density calculations.
   - B0.2.6 reduced the main cloud step setting from five to four.
   - Investigate whether further simplification could help without making the sky look poor.

5. **Other rendering paths**
   - Check lighting, fog, transparent materials, weather rendering, and shared shader functions for unnecessary repeated work.
   - Plant and lantern waving were disabled in B0.2.6, so do not reintroduce them as part of this update.
   - Water reflections were disabled in B0.2.6 per the project's direction; preserve that decision unless explicitly revisited.

### Proposed discussion priorities

- **Priority A — Large terrain views:** Investigate the main terrain shader and the cost of reflection-related and fragment-level effects.
- **Priority B — Optional effects:** Compare glow and other optional calculations, especially the difference between Lite and Default.
- **Priority C — Clouds:** Review rounded-cloud calculations and possible lower-cost alternatives.
- **Priority D — Whole-repository review:** Inspect all relevant shader functions, materials, configuration, subpack definitions, and build workflow before proposing code changes.

These priorities are not implementation approval. No feature should be removed or visually downgraded without discussing the trade-off first.

### Visual and feature constraints

- Keep the project's identity: vanilla Minecraft with natural, refined, cinematic visuals.
- Preserve balanced, natural lighting and avoid oversaturation.
- Keep attractive atmosphere, fog, rain particles, and wet-ground effects where practical.
- Do not add dramatic sky events, custom water waves, tree waving, or player/mob shadows.
- Do not reintroduce water reflections or plant/lantern waving that were disabled in B0.2.6.
- Avoid making terrain excessively flat, dark, or visually stripped down just to chase performance.
- Be honest about what is implemented, what is only a proposal, and what still needs testing.

### Subpack direction — decision still needed

The current question for discussion is whether:

- **Option A:** Lite becomes the main performance-first profile, while Default retains more visual effects; or
- **Option B:** Both Lite and Default receive similar optimizations, even if Default must also reduce some effects.

Current recommendation: optimize both profiles, then allow Lite to make more aggressive cuts. This is only a recommendation; the final direction has not been decided. Beta remains an intentionally empty experiment slot from B0.2.6.

### Testing plan after implementation is approved

Use the same Minecraft world, location, time of day, weather, render distance, and camera positions for comparisons where possible.

Compare at least:
- A relatively open view.
- A dense forest.
- A mountain or large terrain view.
- A village or similarly detailed area.
- A rainy scene, to check weather and atmosphere costs.

Record subjective stutter observations or FPS/frame-time readings if available. Compare Lite and Default separately. Do not claim a performance improvement based only on successful compilation.

### Workflow and rules

1. Inspect the whole relevant repository before proposing code changes.
2. Identify likely expensive paths and separate source-based findings from unverified assumptions.
3. Discuss the likely visual and performance trade-offs.
4. Agree on the B0.2.9 scope before editing shader code.
5. Implement only the agreed changes on a dedicated B0.2.9 branch.
6. Keep the build workflow and version metadata consistent with B0.2.9.
7. Build through GitHub Actions and check the build result.
8. Test the artifact in Minecraft on the target Android device.
9. Update the changelog and other project documentation to match the actual result.
10. Do not merge to `main` without explicit approval.

### Current stopping point

B0.2.9 is still in the discussion phase. The repository inspection has identified terrain rendering, glow, terrain reflection, and rounded-cloud calculations as areas to investigate. None has been confirmed as the dominant cause of the FPS drops.

The next discussion decision is the Lite-versus-Default optimization direction. After that, finish the whole-repository review and discuss the proposed changes before any shader code is modified.
