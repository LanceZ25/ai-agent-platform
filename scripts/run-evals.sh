#!/usr/bin/env bash
set -e

echo "🔍 Running evals for report-agent..."
python evals/engine/eval-runner.py report-agent

