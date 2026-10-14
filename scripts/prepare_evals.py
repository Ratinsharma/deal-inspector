"""Prepare generation-only inputs; keep held-out expectations separate."""
from pathlib import Path
import json

root = Path(__file__).resolve().parent.parent
workspace = root.parent / "deal-inspector-workspace"
inputs = workspace / "inputs"
inputs.mkdir(parents=True, exist_ok=True)
for suite, path in (
    ("development", root / "evals/development.json"),
    ("heldout", root / "evals/heldout.json"),
):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    for index, case in enumerate(data["cases"], 1):
        name = f"{suite}-{index:02}"
        (inputs / f"{name}.txt").write_text(case["prompt"] + "\n", encoding="utf-8")
print("Prepared 12 development and 8 held-out prompt files.")
