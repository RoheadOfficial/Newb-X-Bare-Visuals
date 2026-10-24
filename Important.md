# Important — Project Logic & Non-Negotiable Decisions

> This file is the project's durable reference for decisions and reasoning that should not get lost between planning chats. It records current direction, working conventions, and explicitly provisional ideas. When a section is marked **proposal**, do not silently treat it as a shipped feature or final release decision.

## 1. Project identity

- **Official name:** Newb X Bare Visuals.
- **Creator / variant owner:** RoheadOfficial.
- **Foundation:** a community-made remix/variant based on the Newb X Legacy / Newb X MCBE shader source lineage.
- **Informal family codename:** **BONES** — B, O, N, E, S. This is an internal planning name for related project and dimension series, not a public pack rename.
- **Current development version recorded in the project:** B0.3.7.
- **Current declared Minecraft target label:** 26.52. This is configuration metadata, not evidence that the pack has been verified on every Minecraft or MB Loader build.
- **Current device focus:** Android, with the creator's Vivo Y22s (Android 14, Snapdragon 680, 8 GB RAM) as the main performance test device.
- **Build scope for current development:** Android first. Multiplatform work belongs in release preparation unless the creator explicitly changes that scope.

Newb X Bare Visuals must keep its own recognizable identity. It should not be presented as an official Newb Shader team release or as a direct copy of another variant.

## 2. Inspiration and source lineage

### Primary inspiration going forward: Newb X Future

Newb X Future is the primary visual and technical reference for future design discussions. Study its publicly documented visual direction and, where accessible and appropriate, inspect techniques that may be relevant to our goals:

- Lighting balance and tone mapping.
- Atmosphere and the relationship between fog, sky, and distant terrain.
- Cloud presentation and the trade-off between visual complexity and render cost.
- Night-sky treatment and dimension-specific effects.
- How visual options and performance-minded profiles are organized.
- Potentially transferable shader concepts that fit our target renderer and mobile budget.

This is a reference direction, **not** a decision to replace the current source tree with Newb X Future. Shared Newb roots may make some ideas technically related, but every technique still needs source inspection, compatibility checks, and visual/performance testing.

### Source foundation: Newb X Legacy / Newb X MCBE

The project remains a remix of the Newb X Legacy / Newb X MCBE lineage. Do not change that lineage merely because the inspiration changes. Future-inspired ideas should be adapted to Bare Visuals' own source and goals rather than blindly transplanted.

### Prizma Visuals

Prizma was a significant inspiration in earlier planning, especially for cozy mood and atmosphere. That remains historical context. The **current primary inspiration is Newb X Future**, not Prizma. Do not retroactively rewrite old release notes to pretend earlier decisions were made under the new direction; instead, current planning should clearly state that the direction has evolved.

### Inspiration is not permission to copy

- Visual analysis and feature-level inspiration do not by themselves grant rights to reuse source code, textures, compiled materials, or other assets.
- Review the applicable license and notices for any code or assets considered for direct reuse from Newb X Future.
- Do not assume a public repository or GitHub fork button permits redistribution of a modified compiled pack.
- Preserve upstream notices, required attribution, and Newb variant requirements.

## 3. Visual identity — what Bare Visuals should feel like

The core concept is **vanilla Minecraft, naturally enhanced with shaders**.

- Natural, readable block colors; no oversaturation as a design gimmick.
- Cozy, restrained, cinematic lighting rather than dramatic effects for their own sake.
- A recognizable Minecraft sky and world silhouette.
- Atmosphere that adds depth without obscuring nearby blocks or washing out forests and mountains.
- Performance-conscious rendering that preserves the shader's character.
- Future-inspired polish adapted to Bare Visuals, not an attempt to make the two packs identical.

The creator specifically approved the overall B0.3.6 result and its saturation. Treat that saturation as a protected baseline. Change it only when an observed regression or a clear, tested reason justifies the change.

### Effects and choices to preserve

- Vanilla-like water; no Always Reflection water or custom water waves.
- Lightweight rain particles, rain atmosphere/fog, and wet-ground response.
- Rounded, Minecraft-compatible clouds where the current profile supports them.
- Night atmosphere, including the existing aurora/light-cloud direction.
- The existing three profile identities and their intended trade-offs.

### Exclusions unless explicitly reconsidered

- No oversaturation.
- No godrays.
- No always-on custom water reflections or water waves.
- No waving vegetation/tree animation.
- No box clouds.
- No custom player or mob shadows.
- No dramatic sky event added just to make a version seem larger.
- No feature removal that strips away most of the shader's identity merely to advertise a performance update.
- No custom main Minecraft Settings page claimed through an ordinary resource pack; that earlier idea was scrapped.

These exclusions are project decisions, not a claim that every such effect is impossible in every technical context.

## 4. The three subpacks

Keep the names and order exactly as follows:

1. **Default** — balanced main profile. Preserve the complete intended visual identity while seeking low-risk efficiency gains.
2. **Pootaytoe** — performance-first profile. Retain the core atmosphere and visual identity while taking more targeted savings where the quality/performance trade-off is justified.
3. **Bare Visuals** — fullest cozy/atmospheric profile. Preserve the strongest intended mood while still avoiding unnecessary shader cost.

The selectable order is Default, Pootaytoe, Bare Visuals. Do not reintroduce old Lite/Beta names or add a fourth profile without a new explicit decision. Internal mood percentages discussed in older planning are not player-facing metadata and should not appear in pack descriptions.

## 5. BONES family and dimension work

BONES is the informal family structure:

- **B-Series — Bare Visuals:** the main project/release identity.
- **O-Series — Overworld:** dedicated Overworld work.
- **N-Series — Nether:** dedicated Nether work.
- **E-Series — End:** dedicated End work.
- **S-Series — The Sift:** a future/conditional series, only when the dimension is available and testable and the project is ready to support it.

The official pack name remains Newb X Bare Visuals. BONES is a useful internal shorthand, not a rebrand.

### Work priority

1. **Overworld:** current priority. The creator estimates it is around the mid-60% range complete; this is a subjective progress estimate, not a measured completion metric. It is not finished until the creator accepts its visuals and performance.
2. **Nether:** begin dedicated review and optimization after the Overworld is accepted.
3. **End:** begin dedicated review after the Nether is accepted.
4. **The Sift:** conditional future work; do not promise a release date or begin dimension-specific implementation before it is available and testable.

Shared shader changes can affect other dimensions even while the Overworld is the priority. Watch for regressions, but do not expand into a full Nether/End redesign before the sequence above allows it.

### Dimension series are independent

An O-Series, N-Series, E-Series, or S-Series version tracks work in that dimension. Its number does not automatically set the B-Series number, and the dimension counters do not need to match one another.

Examples:
- O0.3.8 does **not** mean B0.3.8.
- Several Overworld patches may be completed while the B-Series version stays unchanged.
- A major dimension milestone can influence the next B-Series version if the overall significance warrants it, but this must be a deliberate release decision.
- A dimension-specific update should not be treated as a full-pack release unless it has been integrated and validated as such.

## 6. Versioning logic

Version labels have separate jobs. Never confuse the pack version, dimension-series version, Minecraft target, manifest version, or release status.

### B-Series — main project version

The B-Series is chosen according to the significance and scope of the **overall Bare Visuals update**. It must not mechanically mirror the current O/N/E/S number.

- Current recorded development identity: **B0.3.7**.
- **B0** represents the pre-full-release development identity.
- **B1** is the intended first full-release identity once the project's acceptance criteria are met.
- Use **B1.0.0** only if stable subversions become genuinely useful; B1 is the default preference for the first full release.
- Do not declare B1 simply because a calendar date arrives or a single dimension is complete. It should reflect overall readiness.

The current B labels are part of the project's evolving release scheme. Do not assume they follow strict SemVer in every detail or reinterpret old numbers without documenting the decision.

### BONES dimension version convention — working proposal

The working proposal is for each dimension series to use its own independent major/minor/patch-style progression:

- **Patch:** a narrow bug fix or low-risk correction within that dimension.
- **Minor:** a meaningful feature, optimization, or milestone within that dimension.
- **Major:** a major redesign or substantial change to that dimension's own experience.

This is a working convention and should remain marked as provisional until the creator explicitly confirms it as final. Whatever convention is chosen, dimension version counters remain independent from B-Series numbering.

### Historical O-Series mapping — retrospective proposal only

A prior planning pass proposed the following labels to organize documented historical Overworld-focused milestones:

| Historical milestone | Proposed O-Series label |
|---|---|
| B0.1 foundation: sky, clouds, atmosphere | O0.1.0 |
| B0.1.1 sky/time/weather/fog fixes | O0.1.1 |
| B0.1.7 sky restoration/natural lighting | O0.2.0 |
| B0.1.7 Deluxe lighting/mist/water/glow experiments | O0.2.1 |
| B0.1.9 profile reorganization/atmospheric profiles | O0.2.2 |
| B0.2.2 Overworld visual rework/terrain shading | O0.3.0 |
| B0.2.5 refinement/performance/Beta profile | O0.3.1 |
| B0.2.6 lighting/glow/effects | O0.3.2 |
| B0.2.9 terrain performance/profile tuning | O0.4.0 |
| B0.3.2 profiles/material highlights/night readability/ore textures | O0.5.0 |
| B0.3.6 cozy Java-inspired lighting/atmosphere revamp | O0.6.0 |

This mapping is a subjective retrospective organization of roughly eleven documented milestones, not a set of published releases. **O0.6.0 is only a proposed baseline** until the creator confirms it. Do not add these labels to pack metadata, release artifacts, or public claims as if they shipped.

### Initial placeholders for other dimensions

- N0.0.0 — no dedicated Nether series milestone established yet.
- E0.0.0 — no dedicated End series milestone established yet.
- S0.0.0 — placeholder only; The Sift work is conditional on availability and testability.

These are planning placeholders, not claims that the dimensions have been completed or that the labels have shipped.

### Advanced pack identity and Minecraft target

The current tooling derives an advanced identity by appending the declared Minecraft target with dots removed:

- Simple identity: `B0.3.7`
- Target label: `26.52`
- Advanced identity: `B0.3.7.2652`

The target is stored separately in `minecraft_target_version`. If the target label changes to 26.70, the derived identity would be B0.3.7.2670, but that does **not** establish compatibility.

- Keep the Minecraft manifest version as a valid numeric array such as `[0, 3, 7]`.
- Do not put the full display identity or target suffix into the manifest version array.
- Generate advanced version strings, artifact names, and workflow labels from the shared versioning helper rather than duplicating hard-coded values.
- Test Minecraft compatibility and MB Loader compatibility independently.
- A version suffix identifies the declared target; it is not a certification badge.

## 7. Performance philosophy and current investigations

Performance work is now the main development focus until the creator considers it good enough to resume larger shader updates.

### Current reported problems

- Lag remains noticeable, with trees/dense terrain suspected as one contributor.
- Fog/haze is too noticeable even nearby.
- The B0.3.6 look and saturation should be preserved while these problems are investigated.

These are reported symptoms and investigation targets, not yet proof of a particular shader bottleneck.

### Investigation rules

1. Treat every suspected bottleneck as a hypothesis until supported by controlled comparisons.
2. Inspect tree/terrain rendering and fog/atmosphere as separate investigation tracks so one change does not hide the cause of another.
3. Nearby haze should be diagnosed through the interaction between baseline mist and the normal distance-fog curve; do not assume the horizon band is responsible without evidence.
4. Fog math alone may not explain broad FPS drops. Measure the cost and distinguish shader rendering from chunk loading, world generation, or general game-side stutter.
5. Preserve features unless a measured cost and an explicit trade-off justify changing them.
6. Do not promise 50–60+ FPS. It is a target to investigate, not a guarantee.
7. Do not claim an optimization improved FPS without comparable in-game observations.
8. Static validation and successful compilation are necessary checks, but do not prove visual quality, runtime compatibility, or performance.

### Useful comparison scenes

Use comparable camera positions and conditions when possible:

- Clear open plains.
- Dense forest, including looking through tree canopies.
- Forest edge looking toward distant terrain.
- Mountains and broad terrain views.
- Water and wet ground.
- Rain and thunderstorms in open terrain and forests.
- Cloudy skies and night scenes.

Record which profile is active, Minecraft version, MB Loader version, scene/weather, perceived stutter, and any available FPS/frame-time observations. Compare B0.3.6 with the candidate build when both artifacts are available.

## 8. Roadmap shape

This is a direction, not a guarantee that each version will ship on a fixed date.

- **B0.3.7:** establish/continue the polish, compatibility, and investigation baseline. Documentation/tooling merged into main does not mean all visual optimization and on-device acceptance are complete.
- **B0.3.8:** candidate for the first targeted performance pass if the next change set is narrow; use a larger B bump only if the scope justifies it.
- **B0.3.9 and later:** continue focused optimization, regression fixes, and stability work as evidence requires.
- **B1:** first full release only after the overall pack is accepted for visual identity, performance, profile behavior, build integrity, licensing/credits, and compatibility claims.

Do not lock the next B version solely because a dimension-series version advances. Decide the B version after the scope of the actual update is understood. If a performance pass becomes substantial enough to justify a higher B minor series, discuss that before changing version labels.

## 9. Development and repository rules

- Inspect the current repository and relevant source before planning implementation.
- Do not edit shader source or build code without explicit implementation authorization.
- Keep main stable. Work on a dedicated branch and review changes before merging; merge to main only with explicit approval.
- Do not claim that a build, CI run, duplicate audit, compatibility check, or device test passed unless the corresponding result is available.
- Duplicate-file audits are review tools. Never automatically delete files merely because their bytes match; preserve intentional duplicate assets, notices, or required pack content.
- Make changes narrowly and explain the expected visual/performance trade-off.
- For Android-focused development, prioritize an Android build and on-device test. Multiplatform preparation is a separate release-stage task unless explicitly requested earlier.
- Preserve the original upstream README when required; keep project-specific explanation in About.md, Plans.md, Important.md, and the relevant changelog.
- Keep plans, changelogs, pack metadata, and actual implementation status aligned. A planned item is not a completed item.

## 10. Licensing, credits, and release hygiene

- Retain the upstream Newb Shader license and copyright notices required for the source.
- Keep `COPYRIGHT.txt`, `LICENSE`, pack metadata, and credit text consistent with the actual source lineage and distribution.
- The repository currently distinguishes the MIT-licensed source from restrictions that apply to compiled Newb Shader resource packs. Follow the applicable upstream and Newb variant rules for compiled distributions.
- Credit Newb Shader and the variant creator(s) as required; do not imply official endorsement unless it has been confirmed.
- Keep a unique pack name, UUID, and icon, and retain the required patch warning in the pack description.
- If direct code/assets from Newb X Future are ever considered, review the exact files and applicable license/permission first. Its status as a Newb-family project does not automatically grant permission to redistribute a derivative compiled pack.
- Public compiled packs are currently intended for GitHub Actions testing artifacts until release preparation is explicitly undertaken.

## 11. Release acceptance checklist

Before calling an update complete or release-ready, check all applicable items:

- [ ] The actual change set matches the stated goals and this project's visual direction.
- [ ] Static validation passes.
- [ ] Android build succeeds and generated artifacts are present.
- [ ] Multiplatform builds are completed during the designated release-preparation stage.
- [ ] Manifest version, pack identity, target metadata, unique UUID, and subpack order are correct.
- [ ] Default, Pootaytoe, and Bare Visuals each compile and behave according to their intended roles.
- [ ] All planned features/exclusions are checked in the actual source and compiled artifact.
- [ ] CI output and duplicate-audit findings are reviewed; no files are deleted solely because they are identical.
- [ ] Import and activation are tested on the target Minecraft/MB Loader setup.
- [ ] Visual comparisons cover the relevant scenes and dimensions.
- [ ] Performance observations are recorded without attributing game-side chunk-loading stalls to shader code without evidence.
- [ ] Minecraft and MB Loader compatibility claims are separately verified.
- [ ] Licensing, attribution, README, About.md, Plans.md, Important.md, and CHANGELOG.md are consistent.
- [ ] The creator has reviewed and accepted the on-device result before merge/release.

---

**Rule of thumb:** Future inspires the ideas; Legacy is the foundation; Bare Visuals owns the final decisions. BONES organizes the work; it does not force the versions to match. Performance evidence and creator acceptance decide when we move forward.
