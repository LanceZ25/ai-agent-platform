#!/usr/bin/env python3
import sys
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# -----------------------------
# Config
# -----------------------------
ENV = sys.argv[1] if len(sys.argv) > 1 else "dev"

FOUNDRY_ENDPOINT = "https://carioaifoundry-dev-01.services.ai.azure.com/"
STORAGE_ACCOUNT = "carioaistoragedev"

AGENTS_DIR = Path(__file__).parent.parent / "agents"

credential = DefaultAzureCredential()
client = AIProjectClient(endpoint=FOUNDRY_ENDPOINT, credential=credential)

# -----------------------------
# Find all agent folders (skip dev/test/prod root folders)
# -----------------------------
agents_to_register = [
    folder for folder in AGENTS_DIR.iterdir()
    if folder.is_dir() and folder.name not in {"dev", "test", "prod"}
]

print(f"🔹 Agents found: {[a.name for a in agents_to_register]}")

# -----------------------------
# Register or update agents
# -----------------------------
for agent_folder in agents_to_register:
    agent_name = agent_folder.name
    manifest_url = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/agents/{ENV}/{agent_name}/manifest.json"
    print(f"🔹 Registering/updating {agent_name} from {manifest_url}...")
    try:
        agent = client.agents.create_or_update(
            agent_name=agent_name,
            manifest_url=manifest_url
        )
        print(f"✅ Agent {agent_name} registered/updated successfully")
    except Exception as e:
        print(f"❌ SDK method error: {e}")

print(f"🎉 All agents for environment '{ENV}' processed.")
