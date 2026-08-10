#!/usr/bin/env python3
"""Validate recipe manifests, input hashes, and required files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as error:
    raise SystemExit("Install validation dependencies with: python -m pip install -r requirements-dev.txt") from error


ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
required = {"schemaVersion", "id", "version", "title", "status", "techniques", "question", "inputs", "runtime", "command", "outputs", "validation", "license"}
schema = json.loads((ROOT / "schemas" / "recipe.v0.1.schema.json").read_text(encoding="utf-8"))
schema_validator = Draft202012Validator(schema, format_checker=FormatChecker())

for path in ROOT.rglob("*.json"):
    if ".git" in path.parts or "output" in path.parts:
        continue
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path.relative_to(ROOT)}: {error}")

for path in (ROOT / "recipes").glob("*/recipe.json"):
    recipe = json.loads(path.read_text(encoding="utf-8"))
    for error in sorted(schema_validator.iter_errors(recipe), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path) or "$"
        errors.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")
    missing = required - set(recipe)
    if missing:
        errors.append(f"{path.relative_to(ROOT)}: missing {sorted(missing)}")
    for item in recipe.get("inputs", []):
        source = path.parent / item.get("path", "")
        if not source.is_file():
            errors.append(f"{path.relative_to(ROOT)}: missing input {item.get('path')}")
            continue
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual != item.get("sha256"):
            errors.append(f"{path.relative_to(ROOT)}: hash mismatch for {item.get('path')}: {actual}")
    if recipe.get("status") != "design" and not (path.parent / "run.py").is_file():
        errors.append(f"{path.relative_to(ROOT)}: executable recipe needs run.py")
    if not (path.parent / "README.md").is_file():
        errors.append(f"{path.relative_to(ROOT)}: recipe needs README.md")

if errors:
    print("Validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print("Recipe contracts, full JSON Schema conformance, and input hashes valid.")
