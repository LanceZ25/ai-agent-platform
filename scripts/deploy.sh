#!/bin/bash
set -e

ENV=$1  # dev / test / prod

echo "Deploying agents for environment: $ENV"

# Set resource names
RG="rg-ai-core"
STORAGE="carioaistoragedev"
KEYVAULT="cario-ai-vault-dev"
FOUNDRY="cario-aifoundry-dev"
APPCONFIG="cario-appconfig-dev"
INSIGHTS="cario-ai-insights-dev"

# Example: upload agent files to Storage
az storage blob upload-batch \
    --account-name $STORAGE \
    --destination "agents/$ENV" \
    --source agents/ \
    --overwrite

# Example: log deployment
echo "✅ Agents deployed to $ENV environment in $RG"


