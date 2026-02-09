# tests/run_agents_demo.py
"""
Demo runner to test BioMechanismAgent and LiteratureAgent together.

This script ensures the project root is on sys.path so imports like `agents.*` work
regardless of how you run the script from VS Code / PowerShell. It also imports the
actual file name `biomechanism.py` (not `biom.py`) as visible in your project.

Run from project root:
    python tests/run_agents_demo.py
"""

import sys
import os
import json
import time
from pathlib import Path

# ---------------------------
# Ensure project root is on sys.path
# ---------------------------
# Calculate project root (one level up from tests/)
THIS_FILE = Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[1]  # parent of tests/ directory
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Now safe to import project modules
try:
    # NOTE: your file in agents/ appears to be named `biomechanism.py` (see your screenshot).
    # import using that exact module name
    from agents.biomechanism import BioMechanismAgent
except Exception as e:
    print("Failed to import BioMechanismAgent from agents.biomechanism:", e)
    raise

try:
    from agents.literature import LiteratureAgent
except Exception as e:
    print("Failed to import LiteratureAgent from agents.literature:", e)
    raise

# ---------------------------
# Demo logic
# ---------------------------
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def pretty_print(title, obj):
    print("\n" + "="*60)
    print(title)
    print("-"*60)
    print(json.dumps(obj, indent=2))
    print("="*60 + "\n")

def run_demo(drug_name="Montelukast"):
    print("=== AstraMorph Agents Demo ===")
    print("Project root:", PROJECT_ROOT)
    print("Working dir:", Path(".").resolve())
    print("Using drug:", drug_name)
    # instantiate agents (they will detect GEMINI_API_KEY or run mock mode)
    bio_agent = BioMechanismAgent()
    lit_agent = LiteratureAgent()

    # run BioMechanism
    print("Running BioMechanismAgent...")
    try:
        mech_out = bio_agent.run(drug_name)
    except Exception as e:
        mech_out = {"error": str(e)}
    pretty_print("BioMechanismAgent Output", mech_out)

    # run LiteratureAgent (no abstracts provided for demo)
    print("Running LiteratureAgent...")
    try:
        lit_out = lit_agent.run(drug_name, abstracts=None)
    except Exception as e:
        lit_out = {"error": str(e)}
    pretty_print("LiteratureAgent Output", lit_out)

    # compile combined report
    report = {
        "drug": drug_name,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mechanism": mech_out,
        "literature": lit_out,
        "mode": {
            "GEMINI_API_KEY_present": bool(os.environ.get("GEMINI_API_KEY")),
        }
    }

    # write report
    filename = RESULTS_DIR / f"demo_report_{drug_name}_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"Saved combined report -> {filename}")

    return report

if __name__ == "__main__":
    run_demo()
