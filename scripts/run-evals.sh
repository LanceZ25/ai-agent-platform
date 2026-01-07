
#!/usr/bin/env bash
set -euo pipefail

echo "==> Running agent evals for all environments"
mkdir -p evals/results

# Install Python deps if needed
if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt || true
fi

failed=0

for ENV in dev test prod; do
  echo "Checking evals in $ENV environment..."
  for AGENT_DIR in agents/$ENV/*; do
    AGENT_NAME="$(basename "$AGENT_DIR")"
    EVAL_DIR="$AGENT_DIR/evals"
    MANIFEST="$AGENT_DIR/manifest.json"

    if [ -f "$MANIFEST" ] && [ -d "$EVAL_DIR" ] && ls "$EVAL_DIR"/*.json >/dev/null 2>&1; then
      echo "Running evals for $AGENT_NAME in $ENV"
      if ! python evals/engine/eval-runner.py \
        --manifest "$MANIFEST" \
        --evaldir "$EVAL_DIR"; then
        failed=1
      fi
    else
      echo "⚠️ No eval cases found for $AGENT_NAME in $ENV"
    fi
  done
done

if [ -f evals/results/latest.json ]; then
  echo "Evals summary written: evals/results/latest.json"
else
  echo "No eval results found."
fi

if [ "$failed" -ne 0 ]; then
  echo "❌ Regressions detected in agent evals."
  exit 1
fi

echo "✅ All agent evals passed."

