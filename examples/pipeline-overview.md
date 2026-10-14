# A partial pipeline with incompatible value measures

**Fictional worked example.** Names, figures and events are invented for testing; this is not a customer success story.

This is a recorded Codex-agent response using the v2 skill on 13–14 October 2026. The source review date is fixed in the input. The report text is unchanged except for omission of any session-wide trailing footer. A different model or run may respond differently. See [evaluation conditions](../docs/EVALUATION.md).

## Input

```text
Today is 13 October 2026. Can you sanity-check my October forecast from this paste? This is fictional. The screenshot footer says 12 open opportunities and EUR 72,000 in the dashboard, but I pasted only three rows. I do not know how that dashboard handles currency or ACV versus total contract value. Do not assume the missing nine deals are like these.

P-11 Birch Tools: EUR 8,000 ACV, CRM Commit, close 23 October. Owner agreed scope and price in an 8 October email; contract review and signature steps have not been discussed.
P-12 Canal Data: USD 15,000 total contract value over two years, CRM Best Case, close 30 October. Decision is budget-dependent; budget meeting on 21 October is buyer-confirmed. Annual contract value was not recorded and no exchange rate is provided.
P-13 Dune Works: EUR 10,000 ACV, CRM Pipeline, close 31 October. Buyer expects to reconsider in January 2027 and has made no October buying commitment.

I need a brief manager view I can use without overstating this snapshot.
```

## Recorded output

# October forecast sanity check

**Manager view, 13 October 2026:** This is a risk-only review of three pasted open opportunities, not the full October forecast. The screenshot reports 12 open opportunities and EUR 72,000, but its currency conversion and ACV/TCV basis are unknown. The missing nine deals cannot be assessed from these rows. Team category definitions were not supplied, so no category changes or expected-amount forecast are justified.

| Deal | Recorded amount and posture | Evidence concern | Next action |
|---|---|---|---|
| P-11 Birch Tools | EUR 8,000 ACV; Commit; close 23 October | Owner agreed scope and price in an 8 October email, a positive buying signal. Authority to complete the purchase and contract review/signature steps are not established. The October date remains unconfirmed. | Ask the owner who must review and approve the agreement, who signs, and whether those steps can finish by 23 October. |
| P-12 Canal Data | USD 15,000 TCV over two years; Best Case; close 30 October | Decision depends on budget. A buyer-confirmed meeting on 21 October establishes a decision checkpoint, not funding approval or completion timing. ACV is unrecorded. | Confirm the budget outcome after 21 October and, if approved, the remaining decision and signing steps needed for 30 October. |
| P-13 Dune Works | EUR 10,000 ACV; Pipeline; close 31 October | Buyer expects to reconsider in January 2027 and has made no October buying commitment. October timing is unsupported by supplied buyer evidence. | Nurture toward the January reconsideration; ask what buying condition and review date would make that useful. Reconcile the CRM date with the buyer’s timing. |

**Amount boundary:** The two EUR ACV rows total **EUR 18,000 of recorded open pipeline**, not an expected October close amount. Keep Canal’s USD 15,000 TCV separate. Do not combine these with EUR 72,000 or infer a share of the dashboard total.

**Suggested priority:** Resolve Birch’s completion path first because its recorded close date is nearest and scope/price are agreed. Progress means a buyer-confirmed approval/signature path with owners and dates. If the owner cannot confirm it, flag the close date as unresolved. Preserve the recorded fields while checking them. Product capability fit cannot be assessed from this paste.
