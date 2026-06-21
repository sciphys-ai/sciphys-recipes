# Recipe: ZnO XRD Phase Identification

## Scientific Question

Given an XRD pattern, does the strongest evidence support wurtzite ZnO, and are
there unexplained peaks that require impurity or substrate review?

## Inputs

- `.xy`, `.csv`, `.txt`, `.xrdml`, or supported `.raw` XRD pattern.
- Radiation wavelength, ideally Cu K alpha.
- Optional sample context: film, powder, substrate, dopants, annealing condition.

## Workflow

1. Parse the instrument file with `sciphys-os`.
2. Detect peaks and normalize intensities.
3. Match peaks against candidate reference patterns.
4. Report matched peaks, missing strong reference peaks, and unexplained peaks.
5. Ask an expert to accept, reject, or correct the phase evidence.

## Expected Evidence Table

| Peak 2theta | Candidate | hkl | Evidence |
| --- | --- | --- | --- |
| 31.77 | ZnO wurtzite | 100 | matched |
| 34.42 | ZnO wurtzite | 002 | matched |
| 36.25 | ZnO wurtzite | 101 | matched |

## Common Failure Modes

- preferred orientation makes one peak dominate;
- substrate peaks look like impurity phases;
- dopants shift peak positions;
- broad nanoparticle peaks reduce confidence;
- wrong radiation setting shifts all reference comparisons.

## Expert Feedback

Capture feedback as structured labels:

- correct primary phase;
- missed impurity;
- false impurity;
- substrate artifact;
- preferred orientation;
- needs refinement.
