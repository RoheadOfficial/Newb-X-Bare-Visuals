# AIREADME — Newb X Bare Visuals

This file is project-specific context for AI-assisted maintenance. It is not a player-facing marketing document.

## Identity and scope

- Project name: **Newb X Bare Visuals**.
- Android-focused RenderDragon shader variant for Minecraft Bedrock through MB Loader.
- Current development identity: `B0.3.7`; advanced identity: `B0.3.7.2652`; declared target: `26.52`; numeric manifest version: `[0, 3, 7]`.
- Source lineage, attribution, and licensing are described in `COPYRIGHT.txt` and `LICENSE`. Preserve the original upstream `README.md`; use `About.md`, `GUIDE.md`, `Plans.md`, and `CHANGELOG.md` for variant-specific documentation.

## Non-negotiable visual constraints

- Preserve the creator-approved `NL_SATURATION 1.04` unless explicitly authorized otherwise.
- Keep the Vanilla Minecraft but with shaders direction: natural colors, cozy atmosphere, recognizable blocks, restrained cinematic lighting.
- Preserve rain, rain fog, wet-ground response, rounded clouds, and nighttime atmosphere.
- Do not reintroduce godrays/sunrays, water waves, waving vegetation, box clouds, custom water reflections, or custom player/mob shadows.
- Do not claim zero lag, a specific FPS, or compatibility without evidence.

## Profiles (ordered)

1. `DEFAULT`: balanced main profile; inherits the root material set.
2. `POOTAYTOE`: performance-first; must skip the extra terrain glow texture sample.
3. `BARE_VISUALS`: richer cozy atmosphere and subtle material highlights.
4. `EXPERIMENTAL`: optional fake terrain shading based on existing vertex-lighting gradients. It is not a shadow map and cannot create reliable tree-canopy cast shadows.

Profile-specific changes must stay isolated. Keep the profile order consistent in `src/newb/pack_config.toml`, `tool/validate_pack.py`, and documentation.

## Build and release workflow

- Work on a dedicated implementation branch; keep `main` untouched until the creator explicitly approves a merge.
- During implementation, run static checks and the Android GitHub Actions build only.
- Defer multiplatform builds to release preparation.
- Preserve numeric manifest versioning and use `tool/versioning.py` as the canonical source for display/full version labels.
- Run `tool/audit_duplicates.py` and review its findings. Do not automatically delete byte-identical files: repeated assets, upstream notices, or license files may be intentional.
- Treat compile/CI success as build evidence only. Visual quality, device FPS, and Minecraft/MB Loader compatibility require separate testing on the target Android setup.

## B0.3.7 focus

Polish the B0.3.6 result, preserve saturation, remove the aggressive sky-source brightness boost, gently reduce water's blue channel while retaining the vanilla-water path, correct Pootaytoe's profile define for its glow optimization, and evaluate the Experimental fake-shadow prototype. Avoid unrelated redesigns.
