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

- **Lite:** A performance-focused profile with a shorter terrain-reflection range and fewer rounded-cloud density samples, while retaining the core atmosphere and weather effects.
- **Beta:** An empty experimental slot reserved for future tests.
- **Default:** The main profile, retaining the full intended effect set with a modest terrain-reflection range reduction.

The pack's selectable order is Lite, Beta, Default.

## B0.2.9 — Terrain Performance Update

B0.2.9 targets shader-side work that may contribute to frame drops when looking across mountains, forests, dense builds, and wide terrain. The implementation uses separate tuning for Lite and Default and focuses on avoiding calculations that cannot affect the current output.

Static regression validation and the Android/multiplatform GitHub Actions build checks have passed. In-game performance and visual acceptance remain unverified, especially on the target vivo Y22s. A successful build does not guarantee zero lag.

## Source and credits

Newb X Bare Visuals is a community-made variant based on the Newb X MCBE source project. Credit remains with the Newb Shader contributors and RoheadOfficial. See [COPYRIGHT.txt](COPYRIGHT.txt) and [LICENSE](LICENSE) for the applicable notices and licensing details.
