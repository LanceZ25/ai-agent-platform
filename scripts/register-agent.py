
#!/usr/bin/env python
import argparse, subprocess, sys

def run(cmd):
    print(">", " ".join(cmd))
    res = subprocess.run(cmd)
    if res.returncode != 0:
        sys.exit(res.returncode)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--env", required=True, choices=["dev","test","prod"])
    p.add_argument("--agent", required=True)
    p.add_argument("--storage-account", required=True)
    p.add_argument("--appconfig-name", required=True)
    args = p.parse_args()

    agents_container = f"agents-{args.env}"
    evals_container  = f"eval-results-{args.env}"

    manifest_url = f"https://{args.storage_account}.blob.core.windows.net/{agents_container}/{args.agent}/manifest.json"
    prompt_url   = f"https://{args.storage_account}.blob.core.windows.net/{agents_container}/{args.agent}/prompts/system.txt"
    evals_url    = f"https://{args.storage_account}.blob.core.windows.net/{evals_container}"

    # Keys visible to Foundry/runner
    run(["az", "appconfig", "kv", "set", "--name", args.appconfig_name,
         "--key", f"agents:{args.env}:{args.agent}:manifest", "--value", manifest_url, "--yes"])
    run(["az", "appconfig", "kv", "set", "--name", args.appconfig_name,
         "--key", f"agents:{args.env}:{args.agent}:prompt", "--value", prompt_url, "--yes"])
    run(["az", "appconfig", "kv", "set", "--name", args.appconfig_name,
         "--key", f"agents:{args.env}:{args.agent}:evals", "--value", evals_url, "--yes"])

    print(f"Registered {args.agent} ({args.env}) in App Config: {args.appconfig_name}")

if __name__ == "__main__":
    main()



