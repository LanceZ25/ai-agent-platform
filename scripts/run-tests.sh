
#!/usr/bin/env bash
set -euo pipefail

echo "==> Running unit tests"
if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt || true
fi

if command -v pytest >/dev/null 2>&1; then
  pytest -q
else
  echo "pytest not installed; skipping unit tests."
fi
