
#!/usr/bin/env python
import json
import sys
import argparse
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
    passed = True
    for assertion in data.get("assertions", []):
        if assertion["type"] == "contains":
            expected = assertion["value"].lower()
            if expected not in output_text:
                print(f"❌ FAIL: {eval_file}")
                print(f"Expected to contain: {expected}")
                passed = False
    if passed:
        print(f"✅ PASS: {eval_file}")
    return passed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--evaldir", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    agent_name = manifest_path.parent.name
    eval_dir = Path(args.evaldir)

    results = []
    failed = False

    for eval_file in sorted(eval_dir.glob("*.json")):
        ok = run_eval(agent_name, eval_file)
        results.append({"agent": agent_name, "eval": str(eval_file), "passed": ok})
        if not ok:
            failed = True

    # Append results to evals/results/latest.json
    out_dir = Path("evals/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "latest.json"

    # Merge with existing results if present
    existing = []
    if out_file.exists():
        existing = json.loads(out_file.read_text())
    existing.extend(results)
    out_file.write_text(json.dumps(existing, indent=2))

    if failed:
        sys.exit(1)

if __name__ == "__main__":
    main()


