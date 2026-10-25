# Newb X Bare Visuals — Android Guide

Newb X Bare Visuals is a community-made Newb Shader variant intended for Minecraft Bedrock on Android using RenderDragon through MB Loader. It is not an official Minecraft shader feature.

## Before installing

- Use a compatible Minecraft Bedrock version and MB Loader build. The pack's declared target is 26.52, but a version label does not guarantee runtime compatibility.
- Keep a backup of important worlds before testing shader loaders or changing resource packs.
- Import the generated Android resource pack, then activate it from Minecraft's resource-pack settings as directed by the loader.
- If the pack fails to load, confirm Minecraft was launched through the intended MB Loader build and that the pack is enabled in the correct resource scope.

## Choosing a profile

The selectable order is **Default**, **Pootaytoe**, **Bare Visuals**, **Experimental**.

- **Default:** balanced main look, with natural lighting, atmospheric sky, rain, wet-ground response, soft procedural clouds, and restrained emissive glow.
- **Pootaytoe:** performance-first. It preserves the core atmosphere while skipping the extra terrain glow texture sample.
- **Bare Visuals:** fuller cozy atmosphere with warmer dawn/sunset colors and subtle material highlights.
- **Experimental:** tests a lightweight fake-shadow approximation using existing terrain vertex-lighting data. It is not a true shadow map and cannot reliably cast tree-canopy shadows.

Experimental is optional. If it looks too dark, creates visible bands, or performs worse in your world, switch back to Default and report the scene and conditions tested.

## Testing and reporting

For useful comparisons, use the same world, location, time of day, weather, render distance, and camera direction for each profile. Check dense forests, mountains, villages/builds, open terrain, water, rain/storms, and nighttime. Record FPS or stutter observations rather than relying only on memory.

Report Minecraft version, MB Loader version, phone model, selected profile, location/scene, weather/time, and whether the problem repeats.

## Known limitations

- Shader compilation and successful import do not prove visual quality or compatibility.
- Fake terrain shading is an approximation, not genuine dynamic shadows.
- Water uses the custom Newb reflection path with a restrained mineral-gray palette; the surface remains wave-free to keep the look calm and the rendering cost controlled.
- No water waves, godrays, waving vegetation, box clouds, or custom player/mob shadows are intended. Cloud Type 1 is the active lightweight preset; rounded Type 2 and realistic Type 3 are shelved for now.

For project background and licensing/credits, see [About.md](About.md), [COPYRIGHT.txt](COPYRIGHT.txt), and [LICENSE](LICENSE).
