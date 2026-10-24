# Important

## Identity and direction

- **Project:** Newb X Bare Visuals.
- **Source lineage:** Newb X Legacy / Newb X MCBE.
- **Primary inspiration:** Newb X Future.
- **Earlier inspiration:** Prizma Visuals informed earlier planning; it is not the current primary reference.
- **Internal family name:** BONES, for the B/O/N/E/S version series. It is not a pack rename.
- **Visual target:** natural color, cozy cinematic atmosphere, recognizable vanilla Minecraft, and mobile-minded rendering.
- **Accepted baseline:** B0.3.6's color balance and saturation, unless testing identifies a specific regression.

Newb X Future is an inspiration source, not a source-tree replacement. Review the exact license and notices before reusing any code, textures, compiled materials, or other assets.

## BONES series

| Prefix | Scope |
|---|---|
| B | Overall Newb X Bare Visuals release |
| O | Overworld-specific work |
| N | Nether-specific work |
| E | End-specific work |
| S | The Sift, if available and testable |

O/N/E/S counters are independent of each other and of B. An Overworld release such as O0.3.8 does not imply B0.3.8. A dimension may receive several updates without a B-Series bump. B-Series numbering reflects the scope of the overall project update, by deliberate release decision.

### Dimension numbering proposal

The following major/minor/patch interpretation remains provisional:
- **Patch:** narrow fix.
- **Minor:** meaningful feature or optimization milestone within that dimension.
- **Major:** substantial redesign of that dimension's work.
- Use the short `O7` label when no patch-level suffix is needed; add a suffix only when a real subversion patch is required.

### Retrospective O-Series map

These labels are planning references for past milestones, not published releases or pack metadata.

| B-Series milestone | Proposed O-Series label |
|---|---|
| B0.1 foundation | O0.1.0 |
| B0.1.1 | O0.1.1 |
| B0.1.7 | O0.2.0 |
| B0.1.7 Deluxe | O0.2.1 |
| B0.1.9 | O0.2.2 |
| B0.2.2 | O0.3.0 |
| B0.2.5 | O0.3.1 |
| B0.2.6 | O0.3.2 |
| B0.2.9 | O0.4.0 |
| B0.3.2 | O0.5.0 |
| B0.3.6 | O0.6.0 |
| B0.4.5 | O7 (proposed active Overworld milestone) |

O0.6.0 is an unconfirmed retrospective baseline. N0.0.0, E0.0.0, and S0.0.0 are placeholders only; they do not indicate completed work.

## B-Series release identity

- Previous recorded development version: **B0.3.7**; B0.4.5 is the current implementation branch milestone.
- **B1** is the intended first full-release identity, once the project meets its release criteria. B1.0.0 is only needed if stable subversions prove useful.
- Version progression follows actual update scope, not a calendar and not dimension counters.

## Minecraft target suffix

The compact identity combines the simple B-Series version and the declared Minecraft target:

| Field | Example |
|---|---|
| Simple version | B0.3.7 |
| Target label | 26.52 |
| Compact identity | B0.3.7.2652 |
| Manifest version | [0, 3, 7] |

The target belongs in `minecraft_target_version`. The manifest version remains a valid numeric array. A suffix such as 2652 is a label derived from target 26.52, not evidence of compatibility. Minecraft and MB Loader support require separate verification. Shared versioning logic generates full identities and artifact labels; duplicated hard-coded labels are not canonical.

## Profile roles

- **Default:** balanced main profile.
- **Pootaytoe:** performance-first profile.
- **Bare Visuals:** fuller cozy atmosphere while remaining playable.

The order is Default, Pootaytoe, Bare Visuals. Internal inspiration percentages are not player-facing metadata.

## Performance and acceptance

Tree-heavy rendering and nearby fog/haze are separate investigations until evidence connects them. Compare equivalent scenes and distinguish shader rendering from chunk loading or world-generation stutter. Static validation and compilation do not prove runtime compatibility, visual quality, or FPS gains.

Performance claims require build evidence and comparable in-game observations. The 50–60+ FPS target is aspirational, not guaranteed. Preserve the accepted color balance and the established visual identity while testing targeted optimizations.

## Repository and release rules

- Keep `main` stable; isolate work on a dedicated branch.
- Source or pack-metadata changes require explicit implementation authorization.
- Merge only with explicit approval.
- Report builds, CI, audits, compatibility, and device tests only when supported by actual results.
- Review duplicate-file findings manually; identical files can be intentional.
- Android is the development build target. Multiplatform validation belongs to release preparation unless the scope changes.
- Retain the required source attribution, copyright/license notices, pack identity, and patch warning for the applicable Newb source and variant.

## Documentation boundaries

- `README.md`: upstream Newb X Legacy documentation; retain its original content.
- `About.md`: concise player-facing overview and profile descriptions.
- `Plans.md`: active priorities, test plan, and future roadmap.
- `Important.md`: durable project-wide conventions.
- `CHANGELOG.md`: release history and the evidence/status associated with each version.

Release checklists belong in `Plans.md` while work is active. Once a result is verified, record the actual change and its validation status in `CHANGELOG.md`. Keep player-facing explanations out of internal planning documents, and do not duplicate entire feature lists or old implementation checklists across files.