#!/bin/bash
set -e

ENV=$1  # dev / test / prod

if [[ -z "$ENV" ]]; then
    echo "Usage: $0 <environment>"
    exit 1
fi

echo "🔹 Deploying agents for environment: $ENV"

# Resource names
STORAGE="carioaistoragedev"
AGENTS_DIR="./agents"

# Step 1: Upload agent folders to Blob storage
for agent in "$AGENTS_DIR"/*/; do
    agent_name=$(basename "$agent")
    # Skip non-agent folders
    if [[ "$agent_name" == "dev" || "$agent_name" == "test" || "$agent_name" == "prod" ]]; then
        continue
    fi
    echo "📤 Uploading $agent_name..."
    az storage blob upload-batch \
        --account-name "$STORAGE" \
        --destination "agents/$ENV/$agent_name" \
        --source "$agent" \
        --auth-mode login \
        --overwrite
done

echo "✅ Files uploaded to Blob storage."

# Step 2: Register agents in Foundry
python scripts/register-agent.py "$ENV"

echo "🎉 Agents deployed and registered in '$ENV' environment."




