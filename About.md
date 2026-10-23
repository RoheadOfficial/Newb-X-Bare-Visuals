# About Newb X Bare Visuals

**Newb X Bare Visuals** is a community-made Newb Shader variant by RoheadOfficial, built around vanilla Minecraft visuals with natural lighting, refined atmosphere, and a restrained cinematic finish.

The project is Android-focused and is designed for Minecraft Bedrock with RenderDragon shader support through MB Loader. The goal is to make the world feel more atmospheric without turning it oversaturated, overly dramatic, or unnecessarily expensive to render.

## Visual direction

- Natural, readable block colors and balanced sunlight
- Rounded clouds and a recognizable Minecraft sky
- Atmospheric fog and rain mist that support the scene without overwhelming it
- Lightweight rain particles and subtle wet-ground response
- Local emissive glow in Default
- No water waves, plant/lantern waving, godrays, dramatic sky events, or custom sky replacement

## Profiles

- **Default:** balanced main profile with natural lighting, rounded clouds, rain atmosphere, wet ground, night aurora, and restrained local glow.
- **Pootaytoe:** performance-first profile; preserves the core atmosphere and skips the extra terrain glow texture sample.
- **Bare Visuals:** fuller cozy atmosphere, warmer dawns/sunsets, gentle depth, and subtle material highlights.
- **Experimental:** optional fake-shadow prototype that reuses existing terrain vertex-lighting gradients. No shadow maps or extra texture samples; it does not create genuine tree-cast, player, or mob shadows.

Selectable order: Default, Pootaytoe, Bare Visuals, Experimental. Experimental is a visual experiment, not a promise of real dynamic shadows or zero performance cost.

## Current development — B0.3.7

B0.3.7 polishes the approved B0.3.6 foundation and keeps `NL_SATURATION 1.04`. It removes the aggressive sun-source brightness boost, gently reduces blue in the existing vanilla-water path, and fixes Pootaytoe's glow-sample shortcut to match its actual compile-time define. Experimental deepens existing terrain vertex-lighting gradients with a bounded fake-shadow approximation; it adds no shadow map, texture reads, normals, or render pass and cannot generate true tree-canopy cast shadows.

The declared target remains Minecraft `26.52` and full identity `B0.3.7.2652`; these labels do not prove compatibility. Implementation builds Android only. Multiplatform builds are reserved for release preparation. In-game appearance, FPS, and compatibility still require testing.

## B0.3.2 — Beauty and Performance

B0.3.2 builds on B0.2.9's terrain-performance work instead of replacing it. All three profiles receive performance-minded tuning. Default stays balanced, Pootaytoe makes more aggressive simplifications, and Bare Visuals keeps the strongest cozy atmosphere while bounding expensive terrain-reflection work.

The visual direction is inspired by the welcoming, cozy feel of Prizma Visuals without copying it. Colors remain restrained rather than oversaturated. Water keeps its vanilla rendering path; there are no water waves, always-on water reflections, godrays, box clouds, plant/lantern waving, or custom player/mob shadows. The material-highlight experiment is a small color-based approximation, not a full PBR renderer or environment-reflection pass.

The update includes a static regression validator, GitHub Actions build checks, and a restrained texture-only readability pass for the nine existing ore textures. The ore treatment adds no emissive glow. Actual visual acceptance, generated subpack selection, frame-rate gains, and MCBE 26.50 + MB Loader 26.52 behavior still require artifact inspection and in-game testing on the target vivo Y22s. No zero-lag guarantee is made.

## Source and credits

Newb X Bare Visuals is a community-made variant based on the Newb X MCBE source project. Credit remains with the Newb Shader contributors and RoheadOfficial. See [COPYRIGHT.txt](COPYRIGHT.txt) and [LICENSE](LICENSE) for the applicable notices and licensing details.
