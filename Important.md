# Important

This file defines project-wide versioning and planning conventions that are not tied to one release. Release-specific implementation details belong in `Plans.md`; shipped changes belong in `CHANGELOG.md`; player-facing project information belongs in `About.md`. AI maintenance context belongs in `AIREADME.md`.

## Project direction

- **Project name:** Newb X Bare Visuals.
- **Source lineage:** Newb X Legacy / Newb X MCBE.
- **Primary inspiration:** Newb X Future. Use it as a reference for visual ideas and techniques to investigate, not as a reason to replace the existing source tree or copy assets blindly.
- **Creative target:** recognizable vanilla Minecraft, natural color, cozy cinematic atmosphere, and mobile-minded rendering.
- **Current priority:** Overworld performance and polish, especially tree-related lag and excessive nearby fog/haze. Preserve the accepted B0.3.6 color balance unless testing gives a concrete reason to change it.
- **Dimension order:** Overworld → Nether → End → The Sift (only when available and testable).

Prizma Visuals was an earlier reference during development; Newb X Future is the current primary inspiration. The official project name remains Newb X Bare Visuals. “BONES” is an informal family name for the B/O/N/E/S series, not a pack rename.

Inspiration does not grant permission to reuse another project's code, textures, compiled materials, or other assets. Review the exact license and notices before any direct reuse.

## BONES series

| Prefix | Scope |
|---|---|
| **B** | Main Bare Visuals release series |
| **O** | Overworld-specific work |
| **N** | Nether-specific work |
| **E** | End-specific work |
| **S** | The Sift; future/conditional |

Dimension counters are independent of one another and of the B-Series. For example, O0.3.8 does not imply B0.3.8. Several dimension updates may occur without a B-Series bump. Choose the B-Series version according to the significance and scope of the overall project update; do not calculate it automatically from a dimension version.

## Version conventions

### Main B-Series

- Current recorded development version: `B0.3.7`.
- `B0` is the pre-full-release series.
- `B1` is the intended first full-release identity, once the overall project meets its acceptance criteria. Prefer `B1`; use `B1.0.0` only if stable subversions become useful.
- Version decisions follow the actual scope of the overall update, not a fixed calendar and not the dimension counters.

### Dimension-series numbering

**Working proposal, not yet a final rule:** use independent major/minor/patch-style progression within each dimension series:
- Patch: narrow correction or bug fix.
- Minor: meaningful feature or optimization milestone.
- Major: substantial redesign of that dimension's experience.

The exact convention can be finalized separately. Regardless of the chosen convention, dimension versions must remain independent of the B-Series.

### Historical O-Series mapping

The following retrospective mapping was proposed to organize documented Overworld milestones. These labels were not published releases and must not be inserted into pack metadata as if they had shipped.

| Historical milestone | Proposed label |
|---|---|
| B0.1 foundation: sky, clouds, atmosphere | O0.1.0 |
| B0.1.1 sky/time/weather/fog fixes | O0.1.1 |
| B0.1.7 sky restoration/natural lighting | O0.2.0 |
| B0.1.7 Deluxe lighting/mist/water/glow experiments | O0.2.1 |
| B0.1.9 profile reorganization/atmospheric profiles | O0.2.2 |
| B0.2.2 Overworld visual rework/terrain shading | O0.3.0 |
| B0.2.5 refinement/performance/profile experiments | O0.3.1 |
| B0.2.6 lighting/glow/effects | O0.3.2 |
| B0.2.9 terrain performance/profile tuning | O0.4.0 |
| B0.3.2 profiles/material highlights/night readability/ore textures | O0.5.0 |
| B0.3.6 cozy Java-inspired lighting/atmosphere revamp | O0.6.0 |

`O0.6.0` is a proposed retrospective baseline only; it remains unconfirmed. `N0.0.0`, `E0.0.0`, and `S0.0.0` are placeholder labels for series without an established dedicated release history, not completion claims.

## Minecraft target and pack identity

The tooling derives a compact full identity from the B-Series display version and the declared Minecraft target:

- Display version: `B0.3.7`
- Target label: `26.52`
- Compact identity: `B0.3.7.2652`

The target is metadata, not proof of compatibility. Minecraft and MB Loader support must be verified independently.

- Store the target in `minecraft_target_version`.
- Keep the manifest version as a valid numeric array, such as `[0, 3, 7]`.
- Do not put the display string or target suffix in the manifest version array.
- Generate artifact labels and full identities from the shared versioning helper rather than duplicating hard-coded strings.

## Performance and acceptance

Treat tree-related rendering cost and near fog/haze as separate investigations. Test comparable scenes and distinguish shader rendering from chunk loading or other game-side stutter. Static checks and successful compilation do not establish in-game performance or compatibility.

A performance change is accepted only after the relevant build and runtime checks, visual regression review, and device observations. Do not promise a specific FPS result before measurement. Optimize the existing experience before adding costly effects or removing large portions of the shader's identity.

## Repository rules

- Inspect the current source before planning implementation.
- Keep main stable; use a dedicated branch for changes and merge only with explicit approval.
- Do not change source code or pack metadata without explicit implementation authorization.
- Do not report a build, CI run, compatibility test, duplicate audit, or device test as passing without evidence.
- Review duplicate-file findings manually; identical files are not automatically safe to delete.
- Keep Android as the development build target; reserve multiplatform validation for release preparation unless the scope is explicitly changed.
- Keep licensing notices, attribution, pack identity, and patch warning consistent with the applicable Newb source and variant requirements.

**In short:** Newb X Future informs the direction; Newb X Legacy remains the foundation; Bare Visuals owns the final implementation and release decisions.
