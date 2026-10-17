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

- **Default:** The balanced main profile, with natural daylight, warmer sunsets and evenings, soft-blue believable water, rounded clouds, rain atmosphere, wet ground, aurora, and restrained local glow.
- **Pootaytoe:** The performance-focused profile. It keeps the recognizable look while reducing selected rendering work more aggressively where the trade-off is worthwhile.
- **Bare Visuals:** The most atmospheric profile, built around cozy peach-golden sunrises and sunsets, softer blue skies, rounded clouds, gentle atmospheric depth, and subtle material highlights.

The selectable order is Default, Pootaytoe, Bare Visuals. The names and descriptions reflect the intended character of each profile; the visual percentages used during planning are internal creative notes, not player-facing labels.

## B0.3.2 — Beauty and Performance

B0.3.2 builds on B0.2.9's terrain-performance work instead of replacing it. All three profiles receive performance-minded tuning. Default stays balanced, Pootaytoe makes more aggressive simplifications, and Bare Visuals keeps the strongest cozy atmosphere while bounding expensive terrain-reflection work.

The visual direction is inspired by the welcoming, cozy feel of Prizma Visuals without copying it. Colors remain restrained rather than oversaturated. Water keeps its vanilla rendering path; there are no water waves, always-on water reflections, godrays, box clouds, plant/lantern waving, or custom player/mob shadows. The material-highlight experiment is a small color-based approximation, not a full PBR renderer or environment-reflection pass.

The update includes a static regression validator, GitHub Actions build checks, and a restrained texture-only readability pass for the nine existing ore textures. The ore treatment adds no emissive glow. Actual visual acceptance, generated subpack selection, frame-rate gains, and MCBE 26.50 + MB Loader 26.52 behavior still require artifact inspection and in-game testing on the target vivo Y22s. No zero-lag guarantee is made.

## Source and credits

Newb X Bare Visuals is a community-made variant based on the Newb X MCBE source project. Credit remains with the Newb Shader contributors and RoheadOfficial. See [COPYRIGHT.txt](COPYRIGHT.txt) and [LICENSE](LICENSE) for the applicable notices and licensing details.
