# Living Architect Model Cheatsheet

## Getting Started

> Start with the [concept slides](docs/slides/index-en.html), then use the [quickstart](QUICKSTART_en.md) for setup.

1. Open the repository in Codex App
2. Read `AGENTS.md` and `SESSION_STATE.md`, then quick-load
3. Follow the phase in `.codex/current-phase.md`

```text
Typical flow:
  PLANNING -> Requirements -> [Approval] -> Design -> [Approval] -> Tasks -> [Approval]
  BUILDING -> TDD implementation (Red -> Green -> Refactor) -> [Approval]
  AUDITING -> Quality audit -> [Approval] -> Done
```

## Directory Structure

```text
AGENTS.md                  # Codex constitution
.codex/
├── current-phase.md       # Current phase
└── workflows/             # Codex-native workflows

.agents/skills/            # Candidate Codex App project skills
docs/internal/             # Process SSOT
docs/specs/                # Specifications
docs/adr/                  # Architecture Decision Records
docs/tasks/                # Tasks
SESSION_STATE.md           # Local handoff, not tracked by Git

.claude/                   # Legacy compatibility material, not primary control surface
```

## Phases

| Phase | Purpose | Main output |
|------|---------|-------------|
| PLANNING | Requirements, ADRs, design, tasks | Markdown artifacts |
| BUILDING | t-wada style TDD implementation | tests / production code |
| AUDITING | Review, audit, regression checks | findings / fixes |

Approval gates:

```text
requirements -> design -> tasks -> building -> auditing
```

## Session Management

| Operation | Purpose | Entry |
|-----------|---------|-------|
| quick-load | Minimal resume | `.agents/skills/quick-load/SKILL.md` |
| quick-save | Short handoff save | `.agents/skills/quick-save/SKILL.md` |
| commit / push | Distribution and sharing | Normal Git operations |

quick-save keeps `SESSION_STATE.md` short. Move long history, environment notes, and research logs to `docs/daily/` or `docs/artifacts/`.

## Codex App Work Units

| Feature | Use |
|---------|-----|
| commentary updates | Short progress updates while working |
| plans | Multi-step progress management |
| subagents | Parallel read-only research or disjoint write tasks |
| review pane | Diff review, findings, and fix decisions |
| in-app browser | localhost, slides, and UI checks |
| automations | Follow-ups, reminders, and monitors |

## Model Use

| Use | Model policy |
|-----|--------------|
| Routine judgment and implementation | GPT-5.4 |
| Read-only harvest and simple classification | 5.3-class models |
| Large corpora | Preprocess with context-harvest |
| Irreversible or high-risk decisions | GPT-5.5 |

The Gatekeeper keeps judgment. Workers receive evidence gathering, mechanical updates, and disjoint implementation tasks.

## Skills

| Skill | Purpose |
|-------|---------|
| `quick-load` | Low-context resume |
| `quick-save` | Lightweight handoff update |
| `context-harvest` | Read-only harvest for large corpora |
| `lam-orchestrate` | Decompose and parallelize multi-file work |
| `magi` | Complex decision-making |
| `clarify` | Ambiguity, contradiction, and gap checks |
| `spec-template` | Spec creation |
| `adr-template` | ADR creation |

## Reference Documents

| File | Description |
|------|-------------|
| `docs/internal/00_PROJECT_STRUCTURE.md` | Structure, naming, state management |
| `docs/internal/01_REQUIREMENT_MANAGEMENT.md` | Requirements process |
| `docs/internal/02_DEVELOPMENT_FLOW.md` | Development flow and TDD |
| `docs/internal/03_QUALITY_STANDARDS.md` | Quality standards |
| `docs/internal/04_RELEASE_OPS.md` | Release and incident response |
| `docs/internal/05_MCP_INTEGRATION.md` | MCP / MEMORY usage |
| `docs/internal/06_DECISION_MAKING.md` | MAGI / AoT / Reflection |
| `docs/internal/07_SECURITY_AND_AUTOMATION.md` | Command safety |
| `docs/internal/08_QUICK_LOAD_SAVE.md` | quick-load/save |
| `docs/internal/09_MODEL_AND_CONTEXT_POLICY.md` | Model and context policy |
| `docs/internal/10_DISTRIBUTION_MODEL.md` | Distribution model |

## Quick Reference

**Need to resume?**
Use `quick-load`. Start with `SESSION_STATE.md` and the minimal confirmation bundle.

**Need to pause?**
Use `quick-save`. Keep `SESSION_STATE.md` short and move long notes elsewhere.

**Need to implement?**
Use BUILDING. Start from the smallest accepted task and use Red-Green-Refactor.

**Need to review?**
Use AUDITING. Lead with findings, verification, and residual risk.

**Unsure what is true?**
Check phase, requirements, design, tasks, then code/tests in truth hierarchy order.
