# Plans

## B0.3.8 — O6.0 Performance & Water Refinement

**Version:** `B0.3.8.2652` (Minecraft target label `26.52`)  
**Branch:** `b0.3.8-o6-performance-implementation`  
**Build scope:** Android during implementation; multiplatform during release preparation.

### Priorities

1. Reduce tree-heavy rendering cost through targeted foliage and glow optimizations without removing established shader systems. The 50% tree-overhead reduction is a measurable target, not a guaranteed FPS claim.
2. Reduce nearby haze, rain mist, and distracting weather overlay while preserving distance fog, rain, wet ground, and the existing sky pipeline.
3. Preserve Newb X Legacy Always Reflection on terrain (`NL_GROUND_REFL`), retaining nearby strength while reducing far-field work with profile-specific range caps. Keep water reflection separate: give water a distinct, muted mineral-gray identity inspired by the broad visual direction of Newb X Future without copying its assets or implementation; keep its base sky reflection active and bound extra aurora-reflection work by profile and distance.
4. Reduce rounded-cloud sampling where appropriate and retain optimized nighttime auroras.
5. Confirm vegetation, lantern, water, and underwater waving are disabled through the shared compile-time guard.
6. Preserve the approved saturation and all four current development profiles.

### Acceptance

- [x] Static regression validator passes.
- [x] Duplicate-file audit passes.
- [x] Android build and shader compilation pass; generated manifest and profile order inspected.
- [x] Compiled RenderChunk material binaries are present in the artifact.
- [ ] Compare tree-heavy scenes with B0.3.7 and quantify the performance change.
- [ ] Inspect terrain Always Reflection's nearby visibility and shorter far-field cutoff, plus water, haze, rain, clouds, and auroras in all profiles.
- [ ] Verify runtime waving is absent and Minecraft/MB Loader compatibility in-game.

The runtime performance target, visual acceptance, and device compatibility remain unverified until comparable in-game testing is possible. Keep `main` unchanged until review and explicit merge approval.

## BONES roadmap

- **B-Series:** overall Bare Visuals release progression.
- **O-Series:** Overworld-specific work; prioritize it before Nether and End.
- **N-Series:** Nether-specific work.
- **E-Series:** End-specific work.
- **S-Series:** The Sift, only if it becomes available and testable.

Dimension counters are independent from each other and from B-Series. The historical O-Series mapping and detailed naming rules live in [Important.md](Important.md).
