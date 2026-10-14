"""Publish recorded fictional outputs and grading; never generate model responses."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT.parent / "deal-inspector-workspace"
DEST = ROOT / "evals/results"
VIEW = WORK / "iteration-1"

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def report(path):
    text = path.read_text(encoding="utf-8-sig")
    return re.split(r"\n> \u26a1 INSIDER EDGE:|\nSTATUS: (?:DONE|BLOCKED)", text, maxsplit=1)[0].rstrip() + "\n"

def export(case, variant, grade, eval_id):
    key = case["id"]
    output = report(WORK / "runs" / key / f"{variant}.md")
    public = DEST / key / f"{variant}.md"
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_text(output, encoding="utf-8")
    run = VIEW / key / variant
    (run / "outputs").mkdir(parents=True, exist_ok=True)
    (run / "outputs/report.md").write_text(output, encoding="utf-8")
    write(run / "eval_metadata.json", {"eval_id": eval_id, "prompt": case["prompt"]})
    checks = grade["expectations"]
    write(run / "grading.json", {**grade, "summary": {
        "passed": sum(c["passed"] for c in checks), "failed": sum(not c["passed"] for c in checks),
        "total": len(checks), "pass_rate": sum(c["passed"] for c in checks) / len(checks)}})

suite = [{**case, "id": f"heldout-{index:02}"} for index, case in enumerate(read(ROOT / "evals/heldout.json")["cases"], 1)]
mapping = read(WORK / "blind-mapping.json")
totals = {v: {"passed": 0, "total": 0, "quality_sum": 0, "quality_ratings": 0} for v in ("new", "old", "generic")}
comparisons = []
for source in ("held-a.json", "held-b.json", "held-c.json"):
    for case in read(WORK / "grading" / source)["cases"]:
        key = case["id"]
        input_case = next(c for c in suite if c["id"] == key)
        decoded = {}
        for label, grade in case["outputs"].items():
            variant = mapping[key][label]
            decoded[variant] = grade
            totals[variant]["passed"] += sum(e["passed"] for e in grade["expectations"])
            totals[variant]["total"] += len(grade["expectations"])
            totals[variant]["quality_sum"] += sum(grade["quality"].values())
            totals[variant]["quality_ratings"] += len(grade["quality"])
            export(input_case, variant, grade, int(key[-2:]))
        comparisons.append({"id": key, "outputs": decoded,
                            "preferred": [mapping[key][label] for label in case["preferred"]], "reason": case["reason"]})

repeats = []
for filename in ("repeats-a.json", "repeats-b.json"):
    for run in read(WORK / "grading" / filename)["runs"]:
        case = next(c for c in suite if c["id"] == run["id"])
        export(case, run["run"], run, int(case["id"][-2:]))
        repeats.append(run)
dev_cases = [{**case, "id": f"development-{index:02}"} for index, case in enumerate(read(ROOT / "evals/development.json")["cases"], 1)]
dev_grades = read(WORK / "grading/development.json")
for index, case in enumerate(dev_cases, 101):
    grade = next(c for c in dev_grades["cases"] if c["id"] == case["id"])
    export(case, "new", grade, index)

write(DEST / "comparison.json", {"fictional": True, "totals": totals, "cases": sorted(comparisons, key=lambda c: c["id"])})
write(DEST / "repeats.json", {"fictional": True, "runs": repeats})
write(DEST / "development.json", dev_grades)
manifest = read(WORK / "run-manifest.json")
manifest["development_execution"] = "Three fresh generation agents, four cases each; one separate AI grader. Development checks are smoke tests, not blind comparisons."
manifest["repeat_execution"] = "Two additional fresh v2 runs each on heldout-03, 06, 07 and 08; separate AI graders; no original/generic repeat comparison."
manifest["raw_outputs_published"] = False
manifest["raw_outputs_note"] = "Original outputs retained in the local evaluation workspace; published reports omit only trailing session status/insider footers."
assert manifest["skill_sha256"] == hashlib.sha256((ROOT / "SKILL.md").read_bytes()).hexdigest(), "Evaluated skill changed"
assert manifest["heldout_sha256"] == hashlib.sha256((ROOT / "evals/heldout.json").read_bytes()).hexdigest(), "Frozen inputs changed"
write(DEST / "run-manifest.json", manifest)
baseline = ROOT / "evals/baseline"
baseline.mkdir(parents=True, exist_ok=True)
shutil.copyfile(WORK / "baseline/SKILL.md", baseline / "SKILL.md")
print(json.dumps({"heldout": totals, "repeat_checks": sum(len(c["expectations"]) for c in repeats),
                  "repeat_passed": sum(e["passed"] for c in repeats for e in c["expectations"]),
                  "development_checks": sum(len(c["expectations"]) for c in dev_grades["cases"])}))
