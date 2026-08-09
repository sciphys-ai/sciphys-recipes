# SciPhys Recipes

[![Validate recipes](https://github.com/sciphys-ai/sciphys-recipes/actions/workflows/validate.yml/badge.svg)](https://github.com/sciphys-ai/sciphys-recipes/actions/workflows/validate.yml)

Executable, evidence-producing workflows for experimental science.

A SciPhys recipe is more than a notebook or prompt. It pins inputs and tool versions, declares a command, produces machine-readable artifacts, and connects every scientific claim back to data through an Evidence Bundle.

## Recipe maturity

- `design`: scientific workflow and failure modes are documented; not yet executable.
- `executable`: runs locally from declared public inputs.
- `reproduced`: an independent contributor reproduced the declared outputs.
- `reviewed`: a domain expert reviewed the scientific interpretation and limitations.

## Current recipes

| Recipe | Technique | Status | Output |
|---|---|---|---|
| [`xrd-zno-evidence`](recipes/xrd-zno-evidence/README.md) | XRD | executable | inspection, Evidence Bundle, validation report |
| [`battery-health-screening.md`](recipes/battery-health-screening.md) | electrochemistry | design | proposed health evidence workflow |

## Recipe contract

Each recipe directory contains `recipe.json`, redistributable input or immutable input references, a runnable entry point, expected assertions, and documentation. The manifest follows [`schemas/recipe.v0.1.schema.json`](schemas/recipe.v0.1.schema.json).

Required outputs normally include normalized data, QC findings, analysis results, reproducible figure bundle where relevant, claim ledger, Evidence Bundle, and validation report. A recipe must surface missing capabilities and scientific limitations rather than silently skipping them.

Validate repository contracts:

```bash
python scripts/validate.py
```

## Ecosystem

- [sciphys-os](https://github.com/sciphys-ai/sciphys-os) provides runtime tools and Skills.
- [sciphys-formats](https://github.com/sciphys-ai/sciphys-formats) defines portable measurement and evidence contracts.
- [sciphys-bench](https://github.com/sciphys-ai/sciphys-bench) evaluates recipe correctness, reproducibility, and claim integrity.

Code is Apache-2.0. Every recipe input must declare its own license and provenance.
