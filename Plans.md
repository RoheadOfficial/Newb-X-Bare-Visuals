# Plans

## Current milestone: B0.3.7

**Focus:** polish and performance, not another full visual redesign.

### Known issues
- Frame-rate drops remain noticeable around trees and dense terrain.
- Fog/haze is too visible at close range as well as across distance.
- The cause of each issue still needs to be isolated through source inspection and comparable in-game tests.

### Priorities
1. Investigate nearby haze separately from distance fog and rain-driven fog.
2. Inspect tree-heavy terrain rendering for avoidable shader cost.
3. Check visual clutter across sky, terrain lighting, clouds, water, and weather as a combined scene.
4. Preserve the saturation and overall look accepted in B0.3.6 unless testing identifies a specific regression.
5. Check compatibility with the next Minecraft release and MB Loader independently.
6. Keep Default, Pootaytoe, and Bare Visuals distinct and in their established order.

### Test scenes
Use comparable conditions when comparing builds:
- Dense forest, forest edge, and distant terrain
- Mountains and open plains
- Water and wet ground
- Clouds, rain, and thunderstorms
- Night sky and aurora

Record the Minecraft version, MB Loader version, selected profile, observed stutter/FPS, and visible differences. Separate shader-rendering cost from chunk-loading or world-generation stutter. A target of 50–60+ FPS is aspirational, not a claim or guarantee.

### Completion checks
- [ ] Inspect the current fog/mist and tree-heavy terrain paths before changing them.
- [ ] Make only targeted changes with a clear reason and a review of visual risk.
- [ ] Run the current-source validator and Android build.
- [ ] Inspect the generated pack, manifest, profile order, and artifact name.
- [ ] Test all three profiles on the target Android setup.
- [ ] Compare against B0.3.6 in equivalent scenes and record observations.
- [ ] Verify Minecraft and MB Loader compatibility separately.
- [ ] Review duplicate-audit findings manually; delete only files confirmed redundant and unneeded.
- [ ] Update the changelog to match verified results, not planned work.

## BONES dimension roadmap

Work proceeds in this order:

1. **O-Series — Overworld:** performance and visual polish first.
2. **N-Series — Nether:** begin dedicated work after the Overworld reaches an acceptable baseline.
3. **E-Series — End:** follow the Nether.
4. **S-Series — The Sift:** conditional on the dimension being available and testable.

Each dimension has its own version counter. A dimension update does not automatically change the B-Series version. The B-Series changes only when the overall project's update scope warrants it.

## Future direction

Newb X Future is the primary inspiration for ideas to investigate. The source foundation remains Newb X Legacy / Newb X MCBE, and the pack remains Newb X Bare Visuals. Inspiration does not imply a codebase switch or permission to reuse assets.

Larger visual additions wait until the current performance and fog issues are understood. The first full release is planned as **B1**, after release criteria are met; the timing and exact release scope are not yet fixed.

## Historical plans

Earlier B0.3.2 and B0.2.9 plans are retained in the repository history and changelog where relevant. This file tracks the active roadmap rather than duplicating old implementation checklists.