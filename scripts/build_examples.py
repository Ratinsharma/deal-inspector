"""Build public fictional examples from actual recorded development outputs."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT.parent / "deal-inspector-workspace"
parser = argparse.ArgumentParser()
parser.add_argument("--available-only", action="store_true")
args = parser.parse_args()
dev = json.loads((ROOT / "evals/development.json").read_text(encoding="utf-8"))["cases"]
held = json.loads((ROOT / "evals/heldout.json").read_text(encoding="utf-8"))["cases"]
examples = [
    ("smb-owner-purchase.md", "A simple founder purchase", "development-01", dev[0]["prompt"]),
    ("weak-smb-opportunity.md", "Enthusiasm without buying evidence", "development-02", dev[1]["prompt"]),
    ("complex-purchase.md", "An approval dependency challenges the close date", "development-04", dev[3]["prompt"]),
    ("update-review.md", "A buyer resolves the previous blockers", "development-09", dev[8]["prompt"]),
    ("pipeline-overview.md", "A partial pipeline with incompatible value measures", "heldout-07", held[6]["prompt"]),
]
for filename, title, case_id, prompt in examples:
    path = WORK / "runs" / case_id / "new.md"
    if not path.exists() and args.available_only:
        continue
    output = path.read_text(encoding="utf-8-sig")
    output = re.split(r"\n> ⚡ INSIDER EDGE:|\nSTATUS: (?:DONE|BLOCKED)", output, maxsplit=1)[0].rstrip()
    body = f"""# {title}

**Fictional worked example.** Names, figures and events are invented for testing; this is not a customer success story.

This is a recorded Codex-agent response using the v2 skill on 13–14 October 2026. The source review date is fixed in the input. The report text is unchanged except for omission of any session-wide trailing footer. A different model or run may respond differently. See [evaluation conditions](../docs/EVALUATION.md).

## Input

```text
{prompt}
```

## Recorded output

{output}
"""
    (ROOT / "examples" / filename).write_text(body, encoding="utf-8")
print("Built available recorded examples." if args.available_only else "Built all five recorded examples.")
