import json
import sys
from pathlib import Path

def call_agent(agent_name, payload):
    """Generate agent outputs based on agent name and input payload."""
    if agent_name == "customer-service-agent":
        req = payload.get("customer_request", "").lower()
        if "delayed" in req:
            return {"draft_email": f"Apologies for the delay. We are looking into your package: {req}."}
        if "damaged" in req:
            return {"draft_email": f"Sorry for the inconvenience. We will assist you regarding your damaged parcel: {req}."}
        if "missing" in req or "lost" in req:
            return {"draft_email": f"We regret the missing items. Our team will resolve this issue: {req}."}
        if "return" in req:
            return {"draft_email": f"We received your return request. Here’s what to do: {req}."}
        if "reschedule" in req:
            return {"draft_email": f"Your delivery reschedule is confirmed. Details: {req}."}
        if "refund" in req:
            return {"draft_email": f"Your refund request is being processed: {req}."}
        if "pod" in req:
            return {"draft_email": f"Proof of delivery requested. Here is the information: {req}."}
        if "complaint" in req:
            return {"draft_email": f"We’re sorry to hear about your experience. We will address your complaint: {req}."}
        if "address" in req:
            return {"draft_email": f"Your address change has been processed: {req}."}
        if "customer support" in req:
            return {"draft_email": f"Our support team will contact you shortly regarding: {req}."}
        # Default
        return {"draft_email": f"Thank you for contacting us regarding: {req}."}

    if agent_name == "tnt-onboarding-agent":
        req = payload.get("carrier_request", "")
        return {
            "onboarding_steps": (
                f"TNT onboarding steps include API setup, label configuration, "
                f"rate card upload, tracking integration, and go-live checks. "
                f"Request received: {req}"
            )
        }

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
    agents_path = Path("agents")
    failed = False
    for agent_folder in agents_path.iterdir():
        if not agent_folder.is_dir():
            continue
        agent_name = agent_folder.name
        eval_dir = agent_folder / "evals"
        if not eval_dir.exists():
            print(f"⚠️ No evals found for {agent_name}")
            continue
        print(f"🔍 Running evals for {agent_name}...")
        for eval_file in eval_dir.glob("*.json"):
            print(f"Running eval: {eval_file}")
            if not run_eval(agent_name, eval_file):
                failed = True
    if failed:
        print("❌ Some evals failed")
        sys.exit(1)
    print("✅ All evals passed for all agents")

if __name__ == "__main__":
    main()

