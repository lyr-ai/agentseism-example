"""AgentSeism runner: `run.py --task <task file> --out <artifact dir>`.

Runs the agent once and writes what happened. It scores nothing; the
evaluator does that.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from support_agent import run  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--task", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
task = json.loads(Path(a.task).read_text())["task"]
# AgentSeism names each run's directory trial_<k>; the simulated agent uses k
# as its run number.
trial = int(Path(a.out).name.rsplit("_", 1)[1])
out = Path(a.out)
out.mkdir(parents=True, exist_ok=True)
(out / "result.json").write_text(json.dumps({"task": task, "resolved": run(task, trial)}))
