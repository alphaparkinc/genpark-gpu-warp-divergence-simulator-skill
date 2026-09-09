import sys
import json
from client import GPUWarpDivergence

gpu = GPUWarpDivergence()

def handle_call(name, arguments):
    if name == "vote":
        preds = arguments["predicates"]
        active = arguments.get("active_mask", gpu.full_mask)
        return {
            "ballot": hex(gpu.ballot_sync(active, preds)),
            "all_sync": gpu.all_sync(active, preds),
            "any_sync": gpu.any_sync(active, preds)
        }
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_call(req.get("name"), req.get("arguments", {}))
            print(json.dumps({"id": req.get("id"), "result": res}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
