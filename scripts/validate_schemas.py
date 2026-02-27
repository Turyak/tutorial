#!/usr/bin/env python3
"""Validate example JSON payloads against project JSON schemas."""

from pathlib import Path
import json
import sys

try:
    import jsonschema
except ImportError:
    print("ERROR: Missing dependency 'jsonschema'. Install with: pip install jsonschema")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "docs" / "schemas"
EXAMPLES_DIR = ROOT / "docs" / "examples"

PAIRS = [
    ("user_profile.schema.json", "user_profile.example.json"),
    ("daily_plan.schema.json", "daily_plan.example.json"),
    ("daily_log.schema.json", "daily_log.example.json"),
    ("evidence_source.schema.json", "evidence_source.example.json"),
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    ok = True
    for schema_name, example_name in PAIRS:
        schema_path = SCHEMAS_DIR / schema_name
        example_path = EXAMPLES_DIR / example_name

        if not schema_path.exists() or not example_path.exists():
            print(f"[FAIL] Missing files: {schema_path} or {example_path}")
            ok = False
            continue

        schema = load_json(schema_path)
        instance = load_json(example_path)

        validator = jsonschema.Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
        if errors:
            print(f"[FAIL] {example_name} against {schema_name}")
            for err in errors:
                path = ".".join(str(p) for p in err.path) or "<root>"
                print(f"  - {path}: {err.message}")
            ok = False
        else:
            print(f"[OK]   {example_name} validates against {schema_name}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
