# The Living Architect Model

**"AI as a Partner, Not Just a Tool."**

This repository defines the **"Living Architect Model"**, a protocol set designed to enable Large Language Models, centered on Codex App, to act as an autonomous "Architect" and "Gatekeeper" for medium-to-large scale software development projects.

By placing these definition files in your project root, you transform a standard coding assistant into a proactive guardian of project consistency and health.

## Getting Started

| Step | Resource | Time |
|------|----------|------|
| 1. Understand concepts | [Slides](docs/slides/index-en.html) | 5 min |
| 2. Set up your project | [Quick Start](QUICKSTART_en.md) | 10 min |
| 3. Daily reference | [Cheatsheet](CHEATSHEET_en.md) | Reference |

## Core Concepts

- **Active Retrieval**: The AI must actively search and load context, rather than relying on passive memory.
- **Gatekeeper Role**: The AI blocks low-quality code and ambiguous specs before they enter the codebase.
- **Zero-Regression**: Strict impact analysis and TDD cycles to prevent regressions.
- **Multi-Perspective Decisions**: Use the MAGI System (MELCHIOR, BALTHASAR, CASPAR) + Reflection for robust structured decision-making.
- **Command Safety**: Strict Allow/Deny lists for terminal commands to prevent accidental damage.
- **Living Documentation**: Documentation is treated as code, updated dynamically in every cycle.
- **Phase Control**: Explicit switching between PLANNING/BUILDING/AUDITING phases to prevent "accidental implementation".
- **Approval Gates**: Explicit approvals between sub-phases prevent rushing ahead with incomplete deliverables.

## Contents

### Constitution & Quick Reference

| File | Description |
|------|-------------|
| `AGENTS.md` | Codex constitution. Defines the AI's identity, core principles, and authority |
| `CHEATSHEET.md` / `CHEATSHEET_en.md` | Quick reference. Commands and agents list |

### Operational Protocols (`docs/internal/`)

| File | Description |
|------|-------------|
| `00_PROJECT_STRUCTURE.md` | Physical layout and naming conventions |
| `01_REQUIREMENT_MANAGEMENT.md` | From idea to spec (Definition of Ready) |
| `02_DEVELOPMENT_FLOW.md` | Impact analysis, TDD, and review cycles |
| `03_QUALITY_STANDARDS.md` | Coding standards and quality gates |
| `04_RELEASE_OPS.md` | Deployment and emergency protocols |
| `05_MCP_INTEGRATION.md` | MCP server integration & MEMORY.md policy (optional) |
| `06_DECISION_MAKING.md` | Multi-Perspective Decision Making Protocol (MAGI System + AoT + Reflection) |
| `07_SECURITY_AND_AUTOMATION.md` | Command Safety Protocols (Allow/Deny Lists) |
| `99_reference_generic.md` | General advice and best practices (Non-SSOT) |

### Codex App / Legacy Extensions

| Directory | Description |
|-----------|-------------|
| `.codex/workflows/` | Codex-native phase workflows, quick-load/save, and review procedures |
| `.agents/skills/` | Candidate project skills for Codex App |
| `.claude/` | Legacy Claude Code compatibility material; useful as migration source, not the primary control surface |

## How to Use

### Option A: Use as a Template (Recommended)

On GitHub, click the **"Use this template"** button at the top of this repository page to create a new repository with this structure pre-configured.

**Reference Documentation:**
- [Creating a repository from a template - GitHub Docs (English)](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
- [テンプレートからリポジトリを作成する - GitHub Docs (日本語)](https://docs.github.com/ja/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

### Option B: git clone

```bash
git clone https://github.com/sougetuOte/codex-of-LAM.git my-project
cd my-project
rm -rf .git && git init
```

LAM components (`AGENTS.md`, `.codex/workflows/`, `docs/internal/`) work together as a system. We recommend using the full set rather than copying individual files. Treat `.claude/` as legacy compatibility material.

### Option C: Adopt into an Existing Project

To introduce LAM into a project already in development:

1. Create a working directory inside your project and extract the LAM ZIP there

```bash
mkdir _lam_source
cd _lam_source
# Download and extract the ZIP here
```

2. Open the target project in Codex App and instruct it:

```
Place the Living Architect Model from _lam_source/ into this project for Codex App usage.
```

3. If you have existing requirements or specs, have the AI reference them for adaptation:

```
Reference <your-requirements-file> and review all LAM files to adapt the necessary parts.
```

If no existing requirements exist, just start using LAM as-is. You can adapt after defining requirements in PLANNING.

## Phases

| Phase | Purpose | Prohibited |
|---------|---------|------------|
| PLANNING | Requirements, design, task decomposition | Code generation |
| BUILDING | TDD implementation | Implementation without specs |
| AUDITING | Review, audit, refactoring | PM-level fixes prohibited (PG/SE allowed) |

### Approval Gates

```
requirements → [approval] → design → [approval] → tasks → [approval] → BUILDING → [approval] → AUDITING
```

User approval is required at the completion of each sub-phase. Proceeding without approval is prohibited.

## You Don't Need to Memorize Commands

The tables below list the main operating surfaces, but you don't need to memorize them. Ask the AI: "What workflow or skill should I use here?" Start with PLANNING and go from there.

## Work Split

| Role | Purpose | Recommended Phase |
|-------|---------|-------------------|
| Gatekeeper | Judgment, integration, approval gates | ALL |
| Worker | Disjoint implementation or documentation updates | BUILDING |
| Explorer | Read-only research and diff orientation | PLANNING / AUDITING |
| Reviewer | Findings, residual risk, verification results | AUDITING |

## Session Management Commands

| Command | Purpose |
|---------|---------|
| `quick-save` | Save (SESSION_STATE.md + docs/daily when needed; no git operations) |
| `quick-load` | Load (SESSION_STATE.md + minimal confirmation bundle) |

## Workflows

| Operation | Purpose |
|---------|---------|
| ship | Logical commit / push grouping |
| review | Diff inspection, findings, verification summary |
| release | CHANGELOG, tag, GitHub Release |
| wave planning | Select tasks and execution order for the next Wave |
| retro | Learning cycle at Wave/Phase completion |

## Recommended Models

| Phase | Recommended Model |
|-------|-------------------|
| **PLANNING** | GPT-5.4, with context-harvest when useful |
| **BUILDING** | GPT-5.4; use 5.3-class models for simple read-only/classification work |
| **AUDITING** | GPT-5.4; reserve GPT-5.5 for irreversible or high-risk judgments |

## Requirements

| Requirement | Purpose | Required |
|-------------|---------|----------|
| Codex App | AI assistant runtime | Required |
| Python 3.8+ | Helper CLI and verification tooling | Recommended |
| Git | Version control | Required |
| [gitleaks](https://github.com/gitleaks/gitleaks) | Secret scanning (`/full-review` G5 check) | Recommended |

If gitleaks is not installed, `/full-review` will fail at Green State G5. Set `"gitleaks_enabled": false` in `review-config.json` to disable if not needed.

## License

MIT License
