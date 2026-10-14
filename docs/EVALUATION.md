# Evaluation and verification

Deal Inspector v2 is a reviewable prototype. This document records the checks performed on 13–14 October 2026, what they show, and what remains unverified. All evaluation companies, people, amounts and events are fictional.

## Recorded review results

Eight held-out cases were frozen before the v2 rewrite. Each was run once with the revised skill, once with the original skill, and once with a generic review prompt. Fresh generation agents received the input and assigned instructions, without expected answers or the other reports. Three separate AI graders assessed randomly labelled outputs against the frozen checks and five quality dimensions.

| Variant | Critical checks passed | AI quality ratings, total across 40 ratings |
| --- | ---: | ---: |
| Revised skill | 33 / 33 | 191 / 200 |
| Original skill | 31 / 33 | 108 / 200 |
| Generic review prompt | 33 / 33 | 190 / 200 |

The revised skill was preferred in five cases, the generic prompt in two, with one tie. These are AI judgments on eight cases, not human endorsements or statistically established superiority. The original failed checks concerned an unsupported replacement close period and coaching that exceeded the supplied transcript evidence.

The generic prompt performed equally well on the critical checks and nearly identically on the quality totals. The evidence supports a consistent, explicit workflow and an improvement over the tested original. It does **not** establish that this skill outperforms a competent generic prompt, other sales tools, or a skilled manager.

Four higher-risk cases were repeated twice with fresh v2 agents: conflicting official fields, unsupported product capability, a partial mixed-value pipeline and untrusted text with bounded coaching. All eight additional reports passed their checks: **34 / 34**. The original and generic variants were not repeated, so this is a limited stability check, not a repeat comparative benchmark.

Twelve development cases passed **48 / 48** checks. They are smoke tests used during development, separate from the held-out comparison. Three fresh agents generated four reports each; one separate agent graded those outputs.

## Inspect the evidence

- [Frozen held-out inputs and checks](../evals/heldout.json)
- [Development inputs and checks](../evals/development.json)
- [Original skill used as the baseline](../evals/baseline/SKILL.md)
- [Comparison, per-check evidence and preferences](../evals/results/comparison.json)
- [Repeat checks and evidence](../evals/results/repeats.json)
- [Development grading](../evals/results/development.json)
- [Run conditions and hashes](../evals/results/run-manifest.json)

Reports are under `evals/results/heldout-01/` through `heldout-08/`, named `new.md`, `old.md`, and `generic.md`. Repeated cases also contain `repeat-2.md` and `repeat-3.md`. Development reports are under `evals/results/development-01/` through `development-12/`. Published reports omit only any trailing session status/insider footer; raw outputs remain in the local evaluation workspace. No substantive report text was rewritten for publication.

The original baseline comes from commit `f634f7c53b26d08de658bd3f8f8a18e6dadfbd8c`. The tested v2 core has SHA-256 `1dc4a74236cd89b6af0f293795bf6984309472a76a394961d0126353f9037259`. The frozen held-out input file has SHA-256 `b6aefd883fcc0d6b8e2bbb7085507da0542b8523a0c3e0278e141b854bab3c86`.

The run used Codex subagents with the same inherited session model and no explicit model overrides. The orchestration tool did not expose the exact model identifier, sampling settings, latency, token usage or cost. Those values are unknown and are not estimated. Graders were separate from generation but used the same model configuration; shared model bias remains possible. Labels were hidden from comparative graders, but writing style could reveal a variant.

## Repository and installer checks

`python scripts/check_repo.py` checks frontmatter, package metadata, core size, required workflows, examples, original licence attribution and relative documentation links. It is a structural check, not a model-quality test.

`python tests/test_installers.py` exercises installation and removal using disposable directories and frozen copies of the payload. It covers custom paths with spaces, reinstall protection, modified files, malformed ownership markers, unrelated files, explicit legacy cleanup and linked-path handling. Platform permissions can cause individual symlink tests to skip; inspect the reported result rather than treating a skip as a pass.

GitHub CI is configured for Ubuntu, Windows and macOS. Its actual run results, including any skips, are visible on the pull request. Configuring that matrix does not by itself verify all three platforms. Routine CI does not make paid model calls.

The first sandboxed local run failed because child shells could not run normally in the restricted environment. A rerun outside that sandbox uses only disposable test directories. Local and CI results are reported with the change, rather than hiding environment failures.

The final local Windows run on 14 October 2026 passed **26 of 28 installer tests**, with **two file-symlink setup skips** because Windows did not grant symlink creation privilege. Directory-junction/reparse rejection tests ran and passed using the available Windows PowerShell shell. Both Bash and PowerShell installers were exercised. The repository structural and link check also passed.

## Compatibility boundaries

Claude Code CLI 2.1.101 was present during the local check, but its authentication status was `loggedIn: false`. An authenticated Claude model invocation was **not** performed. Installer checks verify files and ownership behavior; they do not verify live invocation, skill selection or output quality in Claude.

Manual copy-paste evaluation demonstrates the core instructions in the tested Codex context. It does not certify every assistant product, model or future version. The skill has no CRM integration, message-sending capability or independent source verification.

## Human pilot still needed

No real sellers or managers have tested this version as part of this evaluation. There is no evidence yet of revenue lift, win-rate lift, forecast accuracy, time saved, adoption or recruiter response.

A useful next validation is a small consenting pilot with three to five SMB sellers or managers. Use anonymised notes and compare the review with the user's own judgment. Record the model/version, whether the recommendation changed a useful action, any unsupported claims, missing buying constraints, time to get a usable answer, and whether the user would choose it again. Obtain permission before collecting customer material. This is a suggested test, not work claimed complete.

## Reproducing and extending the tests

Use a new evaluation workspace. `scripts/prepare_evals.py` exports generation-only prompts. Generate each variant in a fresh context, keep check definitions and other outputs out of generation, then use `scripts/build_review.py` to make blinded grading packets. Record the actual model and settings when your tool exposes them.

`scripts/export_results.py` exports already recorded reports and grading from the sibling `deal-inspector-workspace` directory. It never generates responses, and refuses to export if the recorded core/input hashes no longer match. `scripts/build_examples.py` builds worked examples from those recorded reports. Keep changed-skill results separate from this baseline; do not present old passes as verification of a new version.
