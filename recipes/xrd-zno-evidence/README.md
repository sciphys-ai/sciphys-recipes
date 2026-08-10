# ZnO XRD peak list to auditable evidence

This executable tutorial demonstrates the SciPhys contract from an input hash to phase-candidate output and an Evidence Bundle. The data is a synthetic sparse peak list; it is useful for interface and regression demonstration, not real-world accuracy claims.

Build a local checkout of `sciphys-os` 0.2.x, then run:

```bash
python run.py --sciphys-os /path/to/sciphys-os --output output
```

The runner invokes the SciPhys CLI, checks the declared input hash, verifies the expected ZnO candidate, creates an Evidence Bundle, and calls the runtime validator. It writes `inspection.json`, `evidence-bundle.json`, and `validation.json`.

Scientific boundary: the result states that peaks are consistent with wurtzite ZnO. It does not establish sample purity, quantitative phase fraction, or independent confirmation. Real publication use requires raw-pattern QC, acquisition metadata, licensed reference provenance, complementary evidence where appropriate, and expert review.
