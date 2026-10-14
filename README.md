# Deal Inspector

**AI-assisted deal reviews for B2B sellers.** Turn supplied deal notes into a clear recommendation, the evidence behind it, and a practical next action.

Deal Inspector helps you separate product fit, whether an opportunity is worth pursuing, and what supports its timing. It starts with simple SMB purchases and adds deeper qualification when a buying process needs it.

It is a reusable Markdown skill for an AI assistant, not a standalone application. It works with the material you supply and does not independently verify buyer claims.

## See the review before you install

A founder may have the authority and money to buy while still being unable to take on a rollout. A friendly contact may love a demo without being able to approve a purchase. The next useful action is different in each case.

The examples below show the complete input and a recorded review. All organisations, people, figures and events in them are **fictional**.

| Example | What it demonstrates |
| --- | --- |
| [A simple founder purchase](examples/smb-owner-purchase.md) | Recognising a straightforward approval path without adding enterprise requirements |
| [Enthusiasm without buying evidence](examples/weak-smb-opportunity.md) | Asking a useful question instead of treating interest as a commitment |
| [A second review of the same deal](examples/update-review.md) | Changing the recommendation when the buyer resolves a blocker |
| [A complex purchase with an approval dependency](examples/complex-purchase.md) | Keeping the recorded forecast separate from the evidence supporting it |

For example, the weak-opportunity review proposes asking:

> “What would need to improve for this to be worth buying, and who would join you in deciding?”

The full review explains why that question matters and what buyer response would count as progress. It does not turn demo enthusiasm into a purchase commitment.

## Try it in an AI chat

1. Open [SKILL.md](SKILL.md), copy its full contents, and paste them into your AI chat.
2. Add anonymised notes or a fictional example.
3. Ask: **“Inspect this deal and recommend the next action.”**

No qualification form is required. Short notes are enough for a limited review. A more detailed review needs better source material, not more confident guesses.

Copy-paste use is a manual prompt route. Results depend on the assistant and model; compatibility with every chat product is not claimed. Your assistant provider's normal terms, data handling and usage costs apply.

## What a review gives you

- **Recommendation:** advance, resolve a blocker, nurture, or disqualify, with a product-fit assessment.
- **Evidence:** decisive buyer statements/actions, recorded fields, assumptions, gaps and contradictions.
- **Next action:** a specific step, proposed wording when useful, the buyer response that would count as progress, and a proportionate fallback.
- **Timing:** a forecast or close-date check when requested or material, with insufficient evidence made visible.

The default review is concise. Ask for a full qualification table, a meeting agenda or a proposed action plan when you need more detail.

A missing field is not proof that the buying fact does not exist. A product requirement is not a confirmed mismatch until supplied capability evidence establishes it. A founder can hold several buying roles when the evidence supports that.

## Three ways to use it

**Inspect a deal**

Paste notes, emails or transcript excerpts for one opportunity. Use a review date when relative dates, overdue commitments or close-period checks matter.

**Update a review**

Paste the previous review or snapshot and the new material. Ask what changed, which blockers were resolved and what to do next. The skill does not promise memory across chats.

**Review a pipeline**

Paste a bounded table or export. Define the scope, period, currency/value basis and your team's category meanings if you want forecast-category recommendations. Without those conventions, the skill gives a risk-only review. It does not invent weights, exchange rates or historical movement.

See [usage and input guidance](docs/USAGE.md) and the [qualification reference](docs/MEDDPICC.md).

## Install in Claude Code

The installer copies the core skill and licence into `<skills-root>/deal-inspector/`. By default, that root is `~/.claude/skills`. Supporting documentation is optional; the core review works from `SKILL.md` alone.

Clone this repository, then run the installer for your system:

```bash
git clone https://github.com/Ratinsharma/deal-inspector.git
cd deal-inspector
bash install.sh
```

Windows PowerShell:

```powershell
.\install.ps1
```

Start a new Claude Code session and invoke:

```text
/deal-inspector Inspect this deal: [your anonymised notes]
```

For a custom skills root, use `bash install.sh --target-dir "/path/with spaces/skills"` or `.\install.ps1 -TargetDir "C:\path with spaces\skills"`.

Reinstallation requires `--force` or `-Force`. Force applies only to an owned Deal Inspector installation; it does not authorise replacing an arbitrary directory. Make a copy of local edits before overwriting them.

For manual installation, place this repository's `SKILL.md` in `~/.claude/skills/deal-inspector/SKILL.md`, and retain `LICENSE` with it. Manual copies are not managed by the uninstaller.

### Uninstall and legacy cleanup

Run `bash uninstall.sh` or `.\uninstall.ps1`. Use the same custom-root flag if applicable. The uninstaller targets one installation, checks ownership and file hashes, and preserves unrelated files.

Removing a locally modified owned file requires explicit force. Removing the old `deal-inspector-SKILL.md` single-file layout is separate: `bash uninstall.sh --legacy --force` or `.\uninstall.ps1 -Legacy -Force`. Review that file first; legacy ownership cannot be established from its filename.

## Validation and compatibility

Version 2.0.0 is a reviewable prototype. [Evaluation and verification](docs/EVALUATION.md) records the actual tests, model conditions, results and limitations.

The evaluation compares the revised skill with the original and a generic deal-review prompt on fictional cases. It measures the quality of those reviews, not forecast accuracy, revenue impact or real-world adoption.

Claude installation checks and live model invocation are reported separately. A correct file layout is not evidence that an authenticated Claude session has successfully run the skill. Other agent platforms are not officially verified.

Run the local checks with Python:

```text
python scripts/check_repo.py
python tests/test_installers.py
```

Routine CI checks documentation and installers; it does not make paid model calls.

## Data and judgment boundaries

Anonymise customer material before sharing it. Remove credentials, unnecessary personal information and commercially sensitive details you are not authorised to submit to your assistant.

Deal Inspector drafts recommendations. It does not send messages, edit CRM fields, independently approve concessions or promise product capabilities. Recorded CRM fields remain distinct from recommended checks or changes.

There is no numerical win probability. Close timing remains unknown when the supplied steps do not support a date. Coaching a seller's behaviour requires an observed transcript moment; incomplete CRM notes alone do not establish poor performance.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for safe reproductions, example standards and validation requirements. Report failures with anonymised inputs and the actual model/version rather than customer data.

## Author and licence

Ratin Sharma · [GitHub](https://github.com/Ratinsharma) · [LinkedIn](https://www.linkedin.com/in/ratin-sharma-ae/)

[MIT licence](LICENSE). Original copyright notice: © 2026 Ratz0007. No endorsement by MEDDICC, an AI provider or a sales practitioner is implied.
