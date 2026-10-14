# Using Deal Inspector

Deal Inspector reviews supplied evidence and proposes a practical next action. You remain responsible for the customer relationship and commercial decisions. It cannot independently verify notes, know unshared product capabilities, or guarantee a sale.

## Before sharing notes

Use fictional names or aliases. Remove personal contact details, account numbers, credentials, confidential terms, and identifying customer information. Check your organisation's policy and the AI provider's data settings before sharing material. Do not upload real transcripts or customer data to public GitHub issues.

The skill introduces no telemetry or automatic storage. Your assistant or platform may store chat history under its own settings. Deal Inspector is not a secure customer-data vault.

## Copy-paste use

1. Open [the root skill](../SKILL.md).
2. Paste the entire SKILL.md into your AI chat, then add anonymised notes and your request. Supporting references are not required for the core workflows.
3. Start with a concise review; request detailed qualification only when helpful.

Portable chat use is best-effort: assistants can follow instructions differently or truncate long input. An attractive example is not platform certification. See the published evaluation and compatibility notes for what was actually tested.

## Claude Code use

Follow [the README installation instructions](../README.md). The intended layout is a named directory containing `deal-inspector/SKILL.md`, not a loose Markdown file. Invoke `/deal-inspector` followed by your request and anonymised notes.

Claude discovery and invocation must be tested separately from portable-chat behaviour. An installer check does not prove the model's sales judgment. Consult [Claude's skill documentation](https://code.claude.com/docs/en/skills) if your installed version behaves differently.

## Three workflows

### Inspect one deal

Use the information you have; completing a form is not a prerequisite. A minimal deal anchor can support a low-confidence review. Without any identifiable opportunity, the assistant should ask for a short description instead of inventing one.

```text
Inspect this deal. Keep the review concise.
Account: Fictional owner-led logistics business.
Solution: Scheduling software.
Context: The owner says manual schedule changes delay dispatch.
Notes: They requested a demo next week. Price and approval path are unknown.
Requested close date: None.
```

When known, supply the amount, currency, value basis such as ACV or total contract value, note dates, stakeholder roles, buyer statements, commitments, and next meeting. Include product constraints relevant to fit. Do not fill gaps with guesses.

Expect decisive evidence, material uncertainty, up to three useful questions, and a next action with an observable progress signal. A short buyer-facing draft is included when useful. Ask for full qualification, a meeting agenda, or an action plan only when useful. Proposed dates, owners, and steps must remain labelled as proposals.

### Update a previous review

Paste a previous review or its compact snapshot plus new notes. The skill has no independent memory across sessions.

```text
Update this review using the new notes.
Previous review: [paste anonymised review or snapshot]
New notes, with dates: [paste new evidence]
Show what changed, whether it represents commercial progress, and the next action.
```

The result should distinguish resolved blockers from increased activity and preserve unresolved contradictions. Ask for a copyable snapshot to continue later.

### Review a pipeline

Provide separately labelled opportunities. State the period, seller constraints, and priorities if you want action prioritisation.

```text
Review this pipeline for this week's work.
I have four hours for follow-up. Prioritise actions that can resolve a material blocker.
Team forecast definitions: [supply definitions or say none]
Deal A: [anonymised notes]
Deal B: [anonymised notes]
Deal C: [anonymised notes]
```

Expect a compact per-deal pursuit recommendation, blocker, and next action. Without stated constraints, ranking is provisional action priority, not an objective account-value ranking. A qualitative category is not a win probability.

Mixed currencies, ACV and total contract value, periods, and possible duplicates must not be combined into misleading totals. If the input is too large, use a smaller batch and preserve which deals were reviewed.

## Check the result before using it

- Does each consequential conclusion follow from the notes or a labelled uncertainty?
- Has something unmentioned been mistaken for something absent?
- Is an unknown product capability treated as a question, not a proven mismatch?
- Does the action target the buyer's blocker and say what response counts as progress?
- Does the draft avoid fabricated urgency, promises, and unauthorised concessions?

Correct interpretations before sending a message or changing a forecast. Deal Inspector drafts advice; it does not send messages, update CRM, or commit terms for you.
