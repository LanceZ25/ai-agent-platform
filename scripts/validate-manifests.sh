#!/bin/bash
set -e

echo "🔍 Validating agent manifests..."

for manifest in agents/**/manifest.json; do
  npx ajv validate \
    -s schemas/agent-manifest.schema.json \
    -d "$manifest"
done

echo "✅ All manifests valid"

