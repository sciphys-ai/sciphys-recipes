#!/usr/bin/env python3
"""Run the ZnO evidence recipe against a local SciPhys OS checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run_json(command: list[str]) -> dict:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sciphys-os", required=True, type=Path)
    parser.add_argument("--output", default=HERE / "output", type=Path)
    args = parser.parse_args()

    manifest = json.loads((HERE / "recipe.json").read_text(encoding="utf-8"))
    expected = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
    source = HERE / manifest["inputs"][0]["path"]
    actual_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual_hash != manifest["inputs"][0]["sha256"]:
        raise SystemExit(f"Input hash mismatch: {actual_hash}")

    cli = args.sciphys_os.resolve() / "dist" / "scripts" / "sciphys.js"
    if not cli.is_file():
        raise SystemExit(f"Missing built SciPhys CLI at {cli}; run pnpm build in sciphys-os")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    inspection = run_json(["node", str(cli), "xrd", "inspect", str(source), "ZnO"])
    candidates = {candidate["phase"]["id"]: candidate for candidate in inspection.get("candidates", [])}
    for candidate_id in expected["requiredCandidateIds"]:
        if candidate_id not in candidates:
            raise SystemExit(f"Missing expected candidate {candidate_id}")
        if candidates[candidate_id]["matchedPeaks"] < expected["minimumMatchedPeaks"]:
            raise SystemExit(f"Insufficient matched peaks for {candidate_id}")
    if expected["requiredWarning"] and not inspection.get("warning"):
        raise SystemExit("Inspection must include a limitation warning")

    created_at = datetime.fromtimestamp(int(os.environ.get("SOURCE_DATE_EPOCH", "1786320000")), timezone.utc).isoformat().replace("+00:00", "Z")
    bundle = {
        "schemaVersion": "sciphys.evidence-bundle.v0.1",
        "id": "recipe:xrd-zno-evidence",
        "createdAt": created_at,
        "nodes": [
            {"id": "raw:zno.xy", "type": "raw-data", "label": "Synthetic ZnO peak list", "contentHash": actual_hash, "uri": source.as_uri(), "mediaType": "text/plain"},
            {"id": "process:sciphys-xrd-inspect", "type": "process", "label": "SciPhys XRD inspection", "metadata": {"implementation": "sciphys-os", "recipeVersion": manifest["version"]}},
            {"id": "result:inspection", "type": "result", "label": "XRD phase candidate inspection", "uri": "./inspection.json", "mediaType": "application/json"}
        ],
        "edges": [
            {"from": "raw:zno.xy", "to": "process:sciphys-xrd-inspect", "relation": "used"},
            {"from": "process:sciphys-xrd-inspect", "to": "result:inspection", "relation": "generated"}
        ],
        "claims": [
            {"id": "claim:consistent-wurtzite-zno", "text": "The supplied peak positions are consistent with wurtzite ZnO.", "kind": "interpretation", "evidenceRefs": ["result:inspection"], "status": "draft"}
        ],
        "reviews": []
    }

    inspection_path = output / "inspection.json"
    bundle_path = output / "evidence-bundle.json"
    inspection_path.write_text(json.dumps(inspection, indent=2) + "\n", encoding="utf-8")
    bundle_path.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    validation = run_json(["node", str(cli), "evidence", "validate", str(bundle_path)])
    (output / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    if not validation.get("valid") or validation.get("metrics", {}).get("evidenceCoverage") != expected["evidenceCoverage"]:
        raise SystemExit("Evidence Bundle validation failed")
    print(f"Recipe completed: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
