import sys
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

def main(env):
    # Map environment to Foundry endpoint and project
    endpoints = {
        "dev": {
            "endpoint": "https://cario-aifoundry-dev.services.ai.azure.com/api/projects/proj-default",
            "project": "proj-default"
        },
        # Add test/prod later if needed
    }

    if env not in endpoints:
        print(f"❌ Environment '{env}' not configured")
        sys.exit(1)

    cfg = endpoints[env]

    # Use DefaultAzureCredential (will pick up SP, CLI login, or environment vars)
    client = AIProjectClient(
        endpoint=cfg["endpoint"],
        credential=DefaultAzureCredential(),
        project_name=cfg["project"]
    )

    print(f"\n🔹 Registered Agents in '{env}' ({cfg['project']})\n")
    agents = client.agents.list()

    found = False
    for a in agents:
        found = True
        print(f" - Name: {a.name}")
        print(f"   ID:   {a.id}")
        print(f"   Description: {getattr(a, 'description', 'N/A')}\n")

    if not found:
        print("⚠️ No agents found!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python list-agents.py <environment>")
        sys.exit(1)

    env = sys.argv[1]
    main(env)

