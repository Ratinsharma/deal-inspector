# Contributing

Improve seller decisions, evidence handling, or next actions. Prefer a small change backed by a reproducible case to a longer checklist.

## Evidence and privacy

- Use fictional or thoroughly anonymised inputs. No real transcripts, contact information, credentials, customer identifiers, or confidential terms.
- Separate supplied evidence, interpretation, and uncertainty. Unknown is not failure; unsupported requirements differ from unknown capabilities.
- Do not add score-to-probability rules, universal buying-process assumptions, unsupported statistics, or revenue-impact claims.
- Keep simple founder purchases simple. Preserve optional depth and a concise initial review.

## Propose and verify a change

1. Branch from the default branch. Read the current implementation and evaluation cases first.
2. Explain the seller problem or concrete failure and make the smallest coherent change.
3. For behavioural changes, provide a fictional input and before/after outputs with model identifier, date, available settings, skill version or commit, and judging criteria. Separate expected facts and acceptable decisions from exact wording.
4. Add a case that catches the actual failure. Check factual grounding, buying-process adaptation, commercial judgment, and actionability, not just formatting.
5. Run the relevant documented checks. Installer changes require fresh install, reinstall/overwrite, custom-path, and uninstall checks in an isolated directory containing an unrelated neighbouring skill.
6. Open a PR with results and limitations. Distinguish checks run from checks pending.

Model evaluation stays outside routine CI unless its cost and credentials are approved. Retain failed cases; report tradeoffs. One appealing output is not proof of superiority.

## Documentation and ownership

Keep SKILL.md self-contained for default workflows. References clarify the method without becoming hidden runtime dependencies. Public examples must be labelled fictional and outputs honestly labelled according to how they were produced.

Preserve the MIT licence and existing copyright notice. Ratin Sharma remains the package author; the licence notice must not be silently rewritten.

Use issue templates for safe reproductions. If the original case cannot be shared safely, supply a fictional equivalent.
