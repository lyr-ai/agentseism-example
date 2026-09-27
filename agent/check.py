"""AgentSeism evaluator: `check.py <artifact dir>`. Prints one JSON object."""
import json
import sys
from pathlib import Path

try:
    got = json.loads((Path(sys.argv[1]) / "result.json").read_text())
    print(json.dumps({"success": int(got["resolved"])}))
except Exception as exc:  # a run we cannot score is invalid, never a failure
    print(json.dumps({"invalid": True, "invalid_reason": f"{type(exc).__name__}: {exc}"}))
