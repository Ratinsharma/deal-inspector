"""Check portable skill packaging, metadata and local documentation links."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
errors = []
def check(condition, message):
    if not condition:
        errors.append(message)

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
check(match is not None, "SKILL.md must start with bounded frontmatter")
if match:
    fields = dict(re.findall(r"^([a-z_-]+): (.+)$", match.group(1), re.M))
    check(fields.get("name") == "deal-inspector", "Preserve the skill name")
    try:
        description = json.loads(fields.get("description", "null"))
        check(isinstance(description, str) and 0 < len(description) <= 1024, "Description must be a quoted string of 1-1024 characters")
    except json.JSONDecodeError:
        check(False, "Description must use a valid simple quoted scalar")
check(len(skill.splitlines()) < 500, "Core skill must remain under 500 lines")
for required in ("## Inspect:", "## Update a review", "## Review a pipeline", "## Coaching boundary"):
    check(required in skill, f"Missing workflow: {required}")
for banned in ("/skill deal-inspector", "13-16", "2-3x", "assume 3-8 weeks"):
    check(banned not in skill, f"Obsolete claim in core: {banned}")
package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
check(package["name"] == "deal-inspector", "Package name changed")
check(package["version"] == "2.0.0", "Expected version 2.0.0")
check(not package.get("dependencies"), "This is a skill, not an application runtime")
check("Copyright (c) 2026 Ratz0007" in (ROOT / "LICENSE").read_text(encoding="utf-8"), "Preserve the original licence notice")
for file in ROOT.rglob("*.md"):
    if ".git" in file.parts:
        continue
    text = file.read_text(encoding="utf-8")
    for link in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
        link = link.strip("<>").split("#")[0]
        if not link or re.match(r"[a-z]+:", link, re.I):
            continue
        check((file.parent / link).exists(), f"Broken relative link: {file.relative_to(ROOT)} -> {link}")
data = json.loads((ROOT / "evals/development.json").read_text(encoding="utf-8"))
check(data.get("fictional") is True, "Evaluation inputs must be labelled fictional")
check(len(data["cases"]) == 12, "Expected twelve development cases")
check(len({c["id"] for c in data["cases"]}) == 12, "Duplicate development case IDs")
check(all(c.get("prompt") and c.get("checks") for c in data["cases"]), "Incomplete development case")
for name in ("smb-owner-purchase.md", "weak-smb-opportunity.md", "update-review.md", "complex-purchase.md"):
    file = ROOT / "examples" / name
    check(file.exists(), f"Missing worked example: {name}")
    if file.exists():
        text = file.read_text(encoding="utf-8")
        check("fictional" in text.lower() and "## Input" in text and "## Recorded output" in text, f"Example needs fictional label, input and recorded output: {name}")
if errors:
    for error in errors:
        print("FAIL:", error)
    sys.exit(1)
print("PASS: skill packaging, metadata, twelve development cases, four worked examples, and relative links")
