#!/usr/bin/env bash
set -e

echo "🔍 Running evals for all agents..."

for agent in agents/*; do
    agent_name=$(basename $agent)
    echo "Running evals for $agent_name..."
    python3 evals/engine/eval-runner.py $agent_name
done


