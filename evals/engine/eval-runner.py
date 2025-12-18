import json
import sys
from pathlib import Path

def call_agent(agent_name, payload):
    if agent_name == "customer-service-agent":
        req = payload.get("customer_request", "")
        return {"draft_email": f"Draft email generated for: {req}"}
    elif agent_name == "tnt-onboarding-agent":
        req = payload.get("carrier_request", "")
        return {"onboarding_steps": f"TNT config steps generated for: {req}"}
    else:
        return {"error": "Unknown agent"}

def run_eval(agent_name, eval_file):
    with open(eval_file) as f:
        data = json.load(f)
    response = call_agent(agent_name, data["input"])
    output_text = json.dumps(response).lower()
    for assertion in data["assertions"]:
        if assertion["type"] == "contains":
            expected = assertion["value"].lower()
            if expected not in output_text:
                print(f"❌ FAIL: {eval_file}")
                print(f"Expected to contain: {expected}")
                return False
    print(f"✅ PASS: {eval_file}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python eval-runner.py <agent-name>")
        sys.exit(1)
    agent_name = sys.argv[1]
    eval_dir = Path(f"agents/{agent_name}/evals")
    failed = False
    for eval_file in eval_dir.glob("*.json"):
        if not run_eval(agent_name, eval_file):
            failed = True
    if failed:
        print("❌ Eval failures detected")
        sys.exit(1)
    print("✅ All evals passed")

if __name__ == "__main__":
    main()
