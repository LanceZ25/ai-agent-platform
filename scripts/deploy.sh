
#!/usr/bin/env bash
set -euo pipefail
shopt -s globstar nullglob

ENV="${1:-dev}"  # dev | test | prod

# Map env → storage/appconfig and resource groups
case "$ENV" in
  dev)
    STORAGE_ACCOUNT="${STORAGE_ACCOUNT_DEV:-carioaistoragedev}"
    APPCONFIG_NAME="${APPCONFIG_NAME_DEV:-cario-appconfig-dev}"
    EXPECTED_SUB_NAME="ai-dev-sub"
    EXPECTED_RG="${RESOURCE_GROUP_DEV:-rg-ai-core-dev}"     # adjust if your dev RG differs
    ;;
  test)
    STORAGE_ACCOUNT="${STORAGE_ACCOUNT_TEST:-carioaistoragedev}"
    APPCONFIG_NAME="${APPCONFIG_NAME_TEST:-cario-appconfig-dev}"
    EXPECTED_SUB_NAME="ai-test-sub"
    EXPECTED_RG="${RESOURCE_GROUP_TEST:-rg-ai-core-test}"
    ;;
  prod)
    STORAGE_ACCOUNT="${STORAGE_ACCOUNT_PROD:-carioaistoragedev}"
    APPCONFIG_NAME="${APPCONFIG_NAME_PROD:-cario-appconfig-dev}"
    EXPECTED_SUB_NAME="ai-prod-sub"
    EXPECTED_RG="${RESOURCE_GROUP_PROD:-rg-ai-core-prod}"
    ;;
  *)
    echo "Usage: deploy.sh [dev|test|prod]"; exit 1 ;;
esac

AGENTS_CONTAINER="agents-$ENV"
EVALS_CONTAINER="eval-results-$ENV"

echo "🔹 Deploying agents for environment: $ENV"
echo "   Storage: $STORAGE_ACCOUNT | AppConfig: $APPCONFIG_NAME"

# ---- Guard 1: subscription name must match ----
CURRENT_NAME=$(az account show --query name -o tsv || echo "")
CURRENT_ID=$(az account show --query id -o tsv || echo "")
echo "🔎 Azure context → $CURRENT_NAME ($CURRENT_ID)"
if [ "$CURRENT_NAME" != "$EXPECTED_SUB_NAME" ]; then
  echo "❌ Subscription mismatch. Expected '$EXPECTED_SUB_NAME'. Aborting."
  exit 1
fi

# ---- Guard 2: resource group must exist ----
if ! az group show --name "$EXPECTED_RG" --query name -o tsv >/dev/null 2>&1; then
  echo "❌ Resource group '$EXPECTED_RG' not found in subscription '$CURRENT_NAME'. Aborting."
  exit 1
fi
echo "✅ Resource group '$EXPECTED_RG' is present."

# ---- Agent discovery ----
echo "📂 Listing agents/$ENV:"
ls -la "agents/$ENV" || true

AGENT_DIRS=()
for d in "agents/$ENV"/*; do
  if [[ -d "$d" && -f "$d/manifest.json" ]]; then
    AGENT_DIRS+=("$d")
  fi
done

echo "🔹 Agents found: ${AGENT_DIRS[@]-[]}"
if [[ ${#AGENT_DIRS[@]} -eq 0 ]]; then
  echo "❌ No agents with manifest.json found under agents/$ENV. Aborting."
  exit 1
fi

# ---- Upload artifacts to Storage ----
echo "📤 Uploading agent files to Blob Storage…"
az storage blob upload-batch \
  --account-name "$STORAGE_ACCOUNT" \
  --auth-mode login \
  --destination "$AGENTS_CONTAINER" \
  --source "agents/$ENV"
echo "✅ Files uploaded to Blob storage."

# Upload CI eval results (if present)
if [[ -d "evals/results" ]]; then
  az storage blob upload-batch \
    --account-name "$STORAGE_ACCOUNT" \
    --auth-mode login \
    --destination "$EVALS_CONTAINER" \
    --source "evals/results"
fi

# ---- Register agents in App Configuration ----
echo "📝 Registering agents in App Configuration…"
for AGENT_DIR in "${AGENT_DIRS[@]}"; do
  AGENT_NAME="$(basename "$AGENT_DIR")"
  echo "   • $AGENT_NAME"
  python scripts/register-agent.py \
    --env "$ENV" \
    --agent "$AGENT_NAME" \
    --storage-account "$STORAGE_ACCOUNT" \
    --appconfig-name "$APPCONFIG_NAME"
done

echo "🎉 Agents deployed and registered in '$ENV' environment."

