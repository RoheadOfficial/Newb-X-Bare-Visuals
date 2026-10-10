# B0.1.7 / B0.1.7 Deluxe — Foundation and Deluxe Addendum

## Purpose

B0.1.7 restores the original Newb X Legacy sky implementation and begins establishing the distinct visual identity of Newb X Bare Visuals. The guiding phrase is **“Vanilla Minecraft, naturally enhanced.”** Saturation is not the main differentiator; natural lighting, atmosphere, weather behavior, and consistency must do that work.

## Upstream sky

- Sky implementation restored from upstream Newb X Legacy commit `c57aefa9309ec76c2e9bb500492b6b389321878a`.
- Restores original day/night behavior, dawn/dusk colors, rain-sky blending, and horizon rendering.
- The sky-color configuration in `src/newb/config.h` still contains custom values; only `src/newb/functions/sky.h` was restored byte-for-byte from upstream. Do not describe the sky-color configuration as fully restored.
- Custom sky interpolation, custom rainy-night palette blending, and the extra horizon overlay are removed.
- Keep the existing Newb sky, sun/moon, clouds, and rendering pipeline as the source of truth.

## Color and lighting

- `NL_SATURATION` is `1.4` as an initial baseline. In-game comparison must determine whether a lower value is needed.
- Soft Sunlight uses subtle daylight and noon light-color tuning; no new bloom/glare pass is added.
- Preserve upstream tonemapping and existing lighting/shadow systems.
- Keep water on the existing vanilla-style path; do not add shader water waves, displacement, or new reflections.
- Retain rounded clouds and existing gentle plant/lantern motion unless testing reveals regressions.

## Weather Improvements 2.0

- Rain-aware fog remains integrated through the existing `nlRenderFogFade` function and all seven affected material vertex shaders.
- During rain, fog starts and ends somewhat nearer and mist density increases gradually.
- Rain-driven fog shift and density multiplier are restrained to avoid a uniform grey screen or excessively short view distance.
- Rain-mist opacity is kept low for visual balance and mobile performance.
- Misty Mornings and a separate Golden Hour sky tint are deferred until tests confirm they will not compromise original sky behavior.

## Manifest identity and B-Series versioning

- Pack name remains **Newb X Bare Visuals** and the tagline is **“Vanilla Minecraft, naturally enhanced.”**
- `src/newb/pack_config.toml` declares the display version `B0.1.7`.
- The builder uses B-Series labels in its output, compiled shader material labels, generated manifest description, and artifact filename.
- Minecraft's manifest keeps a numeric three-part version; B-Series branding is a separate display label, not an invalid string in the manifest version field.
- The generated description includes subtle Minecraft formatting colors and Unicode small-caps lettering as a harmless easter egg. This is not an embedded font or unsupported manifest property.
- Preserve UUIDs, Newb attribution, project URL, and the upstream patch warning.

## Source and variant integrity

- Preserve Newb X Legacy source attribution and the applicable MIT source-code notice.
- The current upstream compiled-pack notice identifies separate CC BY-ND 4.0 terms. Do not distribute modified compiled packs unless the applicable license and Newb Variant requirements allow it.
- A distinct visual identity must come from rendering choices and tested consistency, not saturation alone.

## Build and validation checklist

- [ ] Parse `src/newb/pack_config.toml` successfully.
- [ ] Run the GitHub Actions Android build and confirm the expected artifact is produced.
- [ ] Inspect generated `manifest.json`: pack name, description, UUID, authors, URL, and numeric version.
- [ ] Confirm B-Series labels appear in build output, compiled material labels, description, and artifact filename without a generic `v` prefix.
- [ ] Import on Minecraft Bedrock 26.50 with MB Loader 26.52.
- [ ] Check clear daytime, dawn/dusk, night, rain, and thunderstorms.
- [ ] Confirm original upstream sky behavior and absence of the custom horizon overlay.
- [ ] Evaluate saturation in-game and lower it further if needed.
- [ ] Confirm fog is gradual and not excessively grey or dense.
- [ ] Check clouds, vanilla-style water, plant/lantern motion, and existing shading for regressions.
- [ ] Compare performance on the vivo Y22s in open terrain, dense forests, mob-heavy scenes, rain, and thunderstorms.

## B0.1.7 Deluxe addendum

- Saturation reduced to `1.25`.
- Direct sunlight softened to `3.20`; noon tint is warm-neutral and dawn/dusk tint is restrained amber.
- `NL_MIST_DENSITY` is `0.22`; rain-mist opacity is `0.12` to keep weather fog restrained.
- The existing vanilla-water path receives a subtle cool tint while retaining engine alpha and fog. Custom water waves and reflections remain disabled.
- The existing fake-godray hook was part of B0.1.7 Deluxe, but is removed from the active shader path in B0.1.9.
- Numeric manifest version sub-version was `58`; display version was `B0.1.7 Deluxe`.
- B0.1.7 Deluxe was merged into `main` at commit `3130ae86053ab1fa456b44ae1e186bef10f2af02`. The user reported that the saturation reduction was visible but the other atmosphere changes were too subtle.

## B0.1.9 implementation addendum

- The five player-facing profiles are Default (realistic clouds), Soft Sunlight, Misty Mornings, Golden Hour, and Lite (rounded clouds).
- Render Anim is shelved; its macro/source is retained for possible future use.
- Atmospheric profiles coordinate day, dawn/dusk, night, rain, fog, and water color.
- Godrays are excluded from the active B0.1.9 path.
- Dense-terrain performance is a release priority. Lite omits the extra glow texture sample and disables optional effects; plant/lantern movement is limited to a shorter range. Device FPS is not inferred from compilation.
- See [B0.1.9 implementation notes](B0.1.9_IMPLEMENTATION.md) for the full scope and verification matrix.

## Status

B0.1.9 source changes are being assembled on `b0.1.9-implementation`. Compilation, artifact correctness, Android compatibility, visual appearance, subpack switching, and performance remain unverified until CI and in-game testing complete.
