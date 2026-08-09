# Contributing to SciPhys Recipes

A contribution can start as a `design` recipe, but only `executable` and higher recipes appear as runnable examples.

Every executable recipe needs a `recipe.json`, licensed and hashed inputs or immutable references, runnable code, expected assertions, declared outputs, limitations, and validation instructions. Pin tool and contract versions. Keep raw data unchanged. Do not embed private lab information or rely on private hosted services for the core workflow.

Run `python -m pip install -r requirements-dev.txt` and then
`python scripts/validate.py`. Promotion to `reproduced` requires an independent
reproduction record; promotion to `reviewed` requires named domain review with
limitations retained.
