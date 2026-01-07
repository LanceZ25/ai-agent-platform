
#!/usr/bin/env bash
set -euo pipefail

echo "==> Validating agent manifests"

SCHEMA="schemas/agent-manifest.schema.json"
DEV_GLOB="agents/dev/**/manifest.json"
TEST_GLOB="agents/test/**/manifest.json"
PROD_GLOB="agents/prod/**/manifest.json"

run_ajv() {
  echo "-> Using AJV via npx"
  npx --yes ajv-cli@5.0.0 validate -s "$SCHEMA" -d "$DEV_GLOB"
  npx --yes ajv-cli@5.0.0 validate -s "$SCHEMA" -d "$TEST_GLOB"
  npx --yes ajv-cli@5.0.0 validate -s "$SCHEMA" -d "$PROD_GLOB"
}

run_jsonschema() {
  echo "-> AJV not available; falling back to Python jsonschema"
  python - <<'PY'
import json, glob, pathlib, sys
from jsonschema import validate, Draft202012Validator

schema_path = pathlib.Path("schemas/agent-manifest.schema.json")
schema = json.loads(schema_path.read_text())
Draft202012Validator.check_schema(schema)

failures = 0
for env in ["agents/dev", "agents/test", "agents/prod"]:
    for mf in glob.glob(f"{env}/**/manifest.json", recursive=True):
        try:
            data = json.loads(pathlib.Path(mf).read_text())
            validate(instance=data, schema=schema)
            print(f"[OK] {mf}")
        except Exception as e:
            failures += 1
            print(f"[FAIL] {mf}: {e}")

sys.exit(1 if failures else 0)
PY
}

# Try AJV via npx. If it fails, fall back to jsonschema.
if command -v npx >/dev/null 2>&1; then
  if run_ajv; then
    echo "All manifests valid (AJV)."
    exit 0
  else
    echo "AJV validation failed to run—falling back to Python."
    run_jsonschema
    echo "All manifests valid (jsonschema)."
    exit 0
  fi
else
  run_jsonschema
  echo "All manifests valid (jsonschema)."
fi



