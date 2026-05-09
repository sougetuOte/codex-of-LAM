# LAM Quick Start Guide

> New to LAM? Start with the [concept slides](docs/slides/index-en.html) for a visual overview.

## Prerequisites

- Codex App
- Git
- A GitHub account
- Python 3.8+ when using helper CLI or verification tooling

## Step 1: Create a Repository from the Template

Click "Use this template" on GitHub to create a new repository.

[Create from template](https://github.com/sougetuOte/codex-of-LAM/generate)

Or clone manually:

```bash
git clone https://github.com/sougetuOte/codex-of-LAM.git my-project
cd my-project
rm -rf .git && git init
```

## Step 2: Open it in Codex App

Open the repository in Codex App. In the first session, tell the AI:

```text
Read AGENTS.md and SESSION_STATE.md, then quick-load.
If SESSION_STATE.md does not exist, treat this as a new project.
```

In a fresh repository created from the template, `SESSION_STATE.md` usually does not exist yet.
In that case, start from `AGENTS.md`, `.codex/current-phase.md`, and `.codex/workflows/`, then begin in PLANNING.

The Codex LAM entry points are `AGENTS.md`, `.codex/current-phase.md`, `.codex/workflows/`, and the needed `.agents/skills/`.
Legacy Claude Code material is not the primary Codex App control surface. See `docs/migration/` when archive or deletion decisions matter.

## Step 3: Start in PLANNING

For a new project, begin in PLANNING and describe your idea:

```text
Start in PLANNING phase.
"I want to build a web app that manages ..."
```

The AI will brainstorm with you and move through each approval gate:

```text
1. Describe your idea in natural language
2. Refine requirements with the AI
3. Requirements spec (docs/specs/) is generated -> approve
4. ADR and design docs are generated -> approve
5. Task breakdown (docs/tasks/) is generated -> approve
```

Only after all approval gates are passed should the project move to BUILDING.

## Step 4: Adapt LAM to Your Project

Once requirements are defined, tell the AI:

```text
Requirements are complete. Review all LAM files and adapt the necessary parts to this project.
```

### Files to adapt

| File | What to change |
|------|---------------|
| `AGENTS.md` | Update the Identity section with your project name and description |
| `README.md` / `README_en.md` | Rewrite with your project description |
| `CHANGELOG.md` | Start fresh |
| `docs/specs/` | Remove LAM-specific specs |
| `docs/adr/` | Remove LAM-specific ADRs |
| `QUICKSTART.md` etc. | LAM onboarding guides; delete if unnecessary |

### Files to keep as-is

| Directory | Why |
|-----------|-----|
| `.codex/workflows/` | Codex-native phase, review, and quick-load/save procedures |
| `.agents/skills/` | Candidate project skills for Codex App |
| `docs/internal/` | Development process SSOT |
| `docs/artifacts/knowledge/` | Project knowledge accumulation |
| `CHEATSHEET.md` | Operational reference |

## Step 5: Your First BUILDING Session

Once accepted tasks exist, switch to BUILDING and start TDD implementation:

```text
Move to BUILDING phase.
Start from the smallest accepted task and use Red-Green-Refactor.
```

After implementation, move to AUDITING and make the Green State, verification results, and residual risks explicit.

## FAQ

### Q: What if my session disconnects?

A: Use `quick-load` to resume. `SESSION_STATE.md` is the short handoff memo.

### Q: How do I save session state?

A: Use `quick-save` to update `SESSION_STATE.md`. Put longer notes in `docs/daily/`, and keep git commits as a separate operation.


## Next Steps

1. Review the [new project slides](docs/slides/story-newproject-en.html)
2. Start your first PLANNING session in Codex App
3. Keep [CHEATSHEET_en.md](CHEATSHEET_en.md) handy for daily reference
4. Explore [docs/internal/](docs/internal/) for the process SSOT deep dive
