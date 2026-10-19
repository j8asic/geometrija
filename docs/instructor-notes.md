# Instructor notes

## Intended delivery

Exercise 1: approximately 90 minutes (setup/interface 15, navigation/selection 15, coordinate construction 25, Gumball/snaps/layers 20, independent check and saving 15). Demonstrate one short action, let students repeat it, and ask for the checkpoint before moving on. The first model is deliberately a pontoon, not a fair hull. No prior CAD or programming experience is assumed.

Exercise 2: approximately two 90-minute sessions. Stop the first session once the five section curves have correct longitudinal positions. Use the second for rails, Sweep2/Loft comparison, mirroring and checking. The built-in drawing is a synthetic open-ended hull segment: closure is optional, not an acceptance requirement. A lecturer-supplied real lines plan can replace it, but must include known dimensions and station positions.

Exercise 3: approximately 90 minutes of Rhino work, plus 20–30 minutes for the source research (profile import and curve 20, fin scaling and Loft 25, bulb and BooleanUnion 30, checks and reflection 15). Assign the research worksheet before class if the modelling session must stay within 90 minutes. It assumes the Exercise 1 coordinate convention. Exercise 2 is useful context but is not required. The deliverable is an isolated keel component, not a hull attachment or a naval-architecture design recommendation.

Exercise 4 transfers the Rhino hull surface from Exercise 2 into Maxsurf Modeler. Students need Maxsurf Modeler and should read the linked Maxsurf introduction first. The course convention maps to Maxsurf as bow +X, starboard −Y and up +Z; remind students to match the Rhino export units during IGES import.

Exercise 5: about 60 minutes. Students use the completed Exercise 2 hull to create station, waterline and buttock contours, arrange Right, Front and Top detail views on an A3 layout, and export a one-page PDF. The starter hull is open at its ends; closure is not part of this drawing exercise.

Before teaching, walk through the exercises on the classroom Rhino installation. The text targets Rhino 8 on Windows, with command-name fallbacks and a Mac note. Rhino was not executable in the authoring environment; HTML/data validation is not a substitute for this classroom smoke test. Video URLs are supplied by the lecturer; no unverified video titles, chapters, durations or timestamps are asserted.

## Corrections and extensions to the supplied TeX

- One explicit right-handed convention throughout: X forward, Y to port, Z upward. Right is the body-plan YZ view; Front is the XZ profile view; Top is XY. All numeric point examples use the `w` world-coordinate prefix.
- Toolbar positions are useful landmarks, not a rule that only the left creates and only the top modifies. Panels/workspaces can change.
- Scaling now distinguishes base point, reference length and scale factor. Independent horizontal and vertical checks are required.
- Picture opacity is adjusted for readability, not prescribed as 70–80% transparency. Background colour masking is optional and image-format/version dependent.
- Non-uniform stretching or moving picture-surface control points is not presented as trustworthy scan rectification. Students preserve the original and verify known dimensions; perspective-distorted scans should be rectified before tracing.
- Centreline correction affects only the relevant endpoint control points, uses world Y, and does not flatten every curve to Y=0. PointsOff, not merely Esc, is the explicit way to hide control points.
- Station positions are numeric, not judged from a perspective view. Rail snapping explicitly disables Osnap Project so 3D points are not flattened to the active CPlane.
- The formerly unfinished surface stage now includes Sweep2 using keel and sheer rails, a Loft alternative, hard-chine guidance, symmetry, naked-edge inspection, normal direction and fairness checks.
- Mirroring and Join do not guarantee tangency or a watertight solid. Cap is only applicable to planar openings. No hydrostatic claim is made for an open surface.

## Practice geometry

`downloads/practice-stations.csv` is the editable source. Each station is an analytic quarter-ellipse in its YZ plane: y = b sin(theta), z = keel + (sheer - keel)(1 - cos(theta)), 0 <= theta <= pi/2. The drawing overlays all five sections at X=0 for the tracing exercise. The generated offsets CSV contains their actual world X coordinates. Seven reference points per section are sampled at 15-degree intervals; the displayed curves use a denser sampling.

S0 and S4 have nonzero breadth by design. Students are modelling the portion between two finite sections, not a pointed bow or completed stern. They should not shrink a terminal section to zero to make the model look closed.

## Keel fin and bulb practice geometry

Exercise 3 uses X forward, Y to port, and Z upward. Students first compare real hull and keel dimensions from web sources, then choose ratios for their own model. The lesson distinguishes published boat draft and overall keel depth from fin span, and asks students to identify datums and label estimates. The NACA 0012 root profile lies in XY at Z = 0. `downloads/keel-naca-0012-unit-chord-points.csv` contains 41 headerless XYZ rows normalized to a unit chord; Rhino's point-file importer requires no heading row and the exercise asks for individual point objects rather than a point cloud.

The source `CurveThroughPt` step in the original article refers to a `Close=Yes` option. Rhino's command has no such option, so the converted lesson joins a short line between the finite trailing-edge endpoints and checks that the resulting curve is closed before lofting. The bulb is a closed profile revolved about an X-parallel axis. A small overlap, set as five percent of the chosen bulb diameter, places the bulb top above the fin-tip plane to create a clear Boolean intersection. The component remains closed at its root and is not presented as an installed keel or a performance-validated design. The starter sources include the Star class specifications, which define several keel-specific dimensions, and manufacturer pages that provide hull dimensions but not every keel dimension.

## Review emphasis

Prioritise correct units, recoverable/layered construction, calibrated images and measured station positions over a polished screenshot. Ask students to distinguish an input tracing error from a surface-generation error. A plausible-looking surface is not evidence of dimensional accuracy, fairness or a valid closed volume. For the keel exercise, a successful union only establishes that Rhino created a joined result; it does not establish hydrodynamic performance or suitability for a vessel.
