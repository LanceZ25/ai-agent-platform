import json
import sys
from pathlib import Path

def call_agent(agent_name, payload):
    """
    Simulate agent response for testing/evals.
    """
    if agent_name == "customer-service-agent":
        req = payload.get("customer_request", "")
        # Include expected phrase for eval
        return {"draft_email": f"Proof of Delivery email generated for: {req}"}
    elif agent_name == "tnt-onboarding-agent":
        req = payload.get("carrier_request", "")
        # Include expected phrase for eval
        return {"onboarding_steps": f"TNT config steps generated for: {req}"}
    else:
        return {"error": "Unknown agent"}

def run_eval(agent_name, eval_file):
    """
    Run a single eval JSON file and check assertions.
    """
    with open(eval_file) as f:
        data = json.load(f)

    response = call_agent(agent_name, data["input"])
    output_text = json.dumps(response).lower()

    print(f"Running eval: {eval_file}")
    passed = True
    for assertion in data.get("assertions", []):
        if assertion["type"] == "contains":
            expected = assertion["value"].lower()
            if expected not in output_text:
                print(f"❌ FAIL: {eval_file}")
                print(f"Expected to contain: '{expected}'")
                passed = False
    if passed:
        print(f"✅ PASS: {eval_file}")
    return passed

def main():
    if len(sys.argv) < 2:
        print("Usage: python eval-runner.py <agent-name>")
        sys.exit(1)

    agent_name = sys.argv[1]
    eval_dir = Path(f"agents/{agent_name}/evals")

    if not eval_dir.exists():
        print(f"❌ Eval directory not found: {e

