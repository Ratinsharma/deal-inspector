# Deal Inspector

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![ECC Skill](https://img.shields.io/badge/ECC-Skill-purple)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#)

**Forensic B2B deal inspection for AI agents.** A skeptical VP of Sales in your terminal — interrogates deals instead of validating them. MEDDPICC scoring, silent killer detection, pipeline forensics.

Paste raw deal notes, call summaries, email threads, or a CRM export. Get an evidence-backed verdict (Commit / Best Case / Omit), a drafted next action, and the trap-door question that reveals whether the deal is real.

---

## Quick Install

### Claude Code / ECC

```bash
# Clone the repo
git clone https://github.com/Ratz0007/deal-inspector.git
cd deal-inspector

# Run the install script (auto-detects your skills directory)
./install.sh          # macOS / Linux
.\install.ps1         # Windows PowerShell
```

Then in Claude Code:

```
/skill deal-inspector
```

### Manual Install

Copy `SKILL.md` to your ECC or Claude skills directory:

| Platform | Directory |
|----------|-----------|
| ECC | `~/.claude/skills/` |
| Claude Code | `~/.claude/skills/` |
| OpenCode | `~/.config/opencode/skills/` |

---

## Usage

Paste any deal information and Deal Inspector will:

1. **Ingest** — extract what you know and what's missing
2. **Score** — forensic MEDDPICC (0-2 per element, /16 total)
3. **Detect** — silent killers (single-threading, phantom EB, untested champion, etc.)
4. **Verdict** — Commit / Best Case / Omit with evidence-backed close date
5. **Act** — the single highest-leverage gap, drafted message, and trap-door question
6. **Portfolio** — across multiple deals, finds systemic pipeline leaks

### Example

```
Deal: Starlight Software — $450k ACV
Stage: Negotiation
Champion: Maria Chen (VP Eng) — loves the product
EB: Unknown — "they'll be involved at signature"
Competition: None
Timeline: Q3 close
```

Deal Inspector will flag **Phantom Economic Buyer**, **Unquantified Pain**, and **Paper Process Not Started** — and give you the exact message to open the EB conversation.

---

## Scoring Rubric (MEDDPICC)

| Element | 0 — Absent | 1 — Claimed | 2 — Evidenced |
|---------|-----------|-------------|---------------|
| **M**etrics | No economic quantification | Pain acknowledged, unquantified | Buyer stated specific figure in writing |
| **E**conomic Buyer | Unnamed / assumed | Named but never met | Named, direct contact made |
| **D**ecision Criteria | Unknown / guessing | Described verbally, not shaped | Documented, seller influenced them |
| **D**ecision Process | "End of quarter" | Rough sequence, no owners | Each step, owner, date known |
| **P**aper Process | Never discussed | Acknowledged, not timed | Mapped with confirmed durations |
| **I**dentified Pain | Interest without pain | Real but tolerable | Consequential, urgent, cost of inaction |
| **C**hampion | Coach only | Friendly, helpful, untested | Power, personal win, internal action |
| **C**ompetition | Unknown | Known, no differentiation | Known, differentiation established |

**Verdicts:** COMMIT (13-16), BEST CASE (9-12), OMIT (0-8)

---

## Silent Killers

| Killer | Description |
|--------|-------------|
| Single-threaded | One contact carries the deal |
| Untested champion | Friendly, never taken internal risk |
| Phantom economic buyer | Named, never met |
| Seller-generated urgency | Deadlines trace to seller's quarter |
| Unquantified pain | No number = no business case |
| Paper process not started | Legal/security untouched inside 30 days |
| Happy ears | Enthusiasm without commitments |
| Ghosted momentum | Reply latency increasing |
| Stage inflation | CRM stage ahead of evidence |

---

## Why Not Just Ask ChatGPT?

Because sales reps are systematically optimistic about their own deals. Deal Inspector is built to counterweight that bias with evidence. It doesn't validate — it interrogates.

Every score requires a name, a date, a document, or an observed behaviour. Sentiment is scored as absent.

---

## Contributing

PRs welcome! If you have ideas for new silent killers, scoring improvements, or better trap-door questions, open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-idea`)
3. Commit your changes (`git commit -am 'Add my idea'`)
4. Push (`git push origin feature/my-idea`)
5. Open a Pull Request

---

## License

[MIT](LICENSE) © Ratz0007
