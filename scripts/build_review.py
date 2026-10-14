"""Build label-blinded review packets from already recorded fictional outputs."""
from pathlib import Path
import hashlib
import json
import random
import re

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT.parent / "deal-inspector-workspace"
suite = json.loads((ROOT / "evals/heldout.json").read_text(encoding="utf-8"))
blind = WORK / "blind"
blind.mkdir(parents=True, exist_ok=True)
mapping = {}
for index, case in enumerate(suite["cases"], 1):
    key = f"heldout-{index:02}"
    variants = ["new", "old", "generic"]
    random.Random(20261013 + index).shuffle(variants)
    mapping[key] = dict(zip(["A", "B", "C"], variants))
    parts = [
        "Judge only these fictional inputs and outputs. Variant identities are withheld.",
        "Do not reward headings, verbosity, or numerical precision. Score evidence-grounded judgment, actionable next steps, proportionality, provenance and concision from 1 (poor) to 5 (strong).",
        "Assess every invariant per output. Cite a short exact excerpt or explain the omission. A missing or contradicted critical requirement fails. Preference is secondary to critical correctness.",
        "INPUT\n" + case["prompt"],
        "CHECKS\n" + json.dumps(case["invariants"], indent=2),
    ]
    for label, variant in mapping[key].items():
        path = WORK / "runs" / key / f"{variant}.md"
        text = path.read_text(encoding="utf-8-sig")
        # Remove only a session-wide trailing footer, never report content.
        text = re.split(r"\n> ⚡ INSIDER EDGE:|\nSTATUS: (?:DONE|BLOCKED)", text, maxsplit=1)[0].rstrip()
        parts.append(f"OUTPUT {label}\n{text}")
    (blind / f"{key}.txt").write_text("\n\n---\n\n".join(parts) + "\n", encoding="utf-8")
(WORK / "blind-mapping.json").write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
(WORK / "run-manifest.json").write_text(json.dumps({
    "evaluation_dates": ["2026-10-13", "2026-10-14"],
    "fictional": True,
    "original_commit": "f634f7c53b26d08de658bd3f8f8a18e6dadfbd8c",
    "skill_sha256": hashlib.sha256((ROOT / "SKILL.md").read_bytes()).hexdigest(),
    "heldout_sha256": hashlib.sha256((ROOT / "evals/heldout.json").read_bytes()).hexdigest(),
    "execution": "Fresh Codex subagents per held-out case and variant; same inherited session model, no explicit model overrides.",
    "model_id": None,
    "settings": "Exact model identifier, sampling parameters, timing and token telemetry were not exposed by the orchestration tool.",
    "generic_prompt": "Review the B2B deal or pipeline and recommend a useful next action based only on supplied evidence.",
    "normalization": "Session-wide trailing status/insider footer omitted from blind packets and examples; raw outputs retained.",
    "limitations": ["AI-generated grading; no human seller pilot", "Variant labels hidden, but content style may reveal a variant", "One inherited model family/session configuration; no cross-model claim"]
}, indent=2) + "\n", encoding="utf-8")
print("Prepared eight blind packets and a private label mapping.")
