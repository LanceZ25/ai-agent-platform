import json
import sys
from pathlib import Path

def call_agent(agent_name, payload):
    request_type = payload.get("request_type", "").upper()
    ref = payload.get("reference_id", "N/A")

    if request_type == "POD":
        return {
            "report": f"Proof of Delivery report for {ref}"
        }

    if request_type == "DELIVERY_STATUS":
        return {
            "report": f"The delivery for {ref} is currently in transit."
        }

    return {
        "report": "Unable to generate report for the given request."
    }


def run_eval(agent_name, eval_path):
    data = json.loads(Path(eval_path).read_text())
    response = call_agent(agent_name, data["input"])
    output = json.dumps(response).lower()

    for assertion in data["assertions"]:
        if assertion["type"] == "contains":
            expected = assertion["value"].lower()
            if expected not in output:
                print(f"❌ FAIL: {eval_path}")
                return False

    print(f"✅ PASS: {eval_path}")
    return True


def main():
    agent = sys.argv[1]
    eval_dir = Path(f"agents/{agent}/evals")

    failed = False
    for eval_file in eval_dir.glob("*.json"):
        if not run_eval(agent, eval_file):
            failed = True

    if failed:
        print("❌ Eval regressions detected")
        sys.exit(1)

    print("✅ All evals passed")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eval-runner.py <agent-name>")
        sys.exit(1)

    main()
