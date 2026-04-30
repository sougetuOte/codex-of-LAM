# Codex LAM Replacement Requirements

Status: Draft for review
Date: 2026-04-30

## Problem

The current Living Architect Model is designed around Claude Code. Its control
surface relies on `.claude/settings.json`, hooks, slash commands, and custom
subagent files. Codex needs a replacement that preserves the architectural
discipline without pretending those Claude-specific mechanisms exist.

## Goals

- Provide a Codex-native constitution through `AGENTS.md`.
- Move the active harness definition to `.codex/`.
- Preserve PLANNING, BUILDING, and AUDITING phases.
- Preserve approval gates for requirements, design, tasks, building, and
  auditing.
- Make the replacement reviewable through requirements, ADR, design, tasks, and
  executable tests.
- Encourage t-wada style TDD during implementation.
- Treat `.claude/` as legacy source material, not the Codex runtime.

## Non-Goals

- Remove every `.claude/` file in the first wave.
- Emulate Claude Code hooks inside Codex.
- Build a hidden automation layer that overrides Codex permissions.
- Change the existing historical docs except where a task explicitly targets
  migration cleanup.

## Functional Requirements

### FR-1 Codex Entry Point

The repository must include `AGENTS.md` as the primary Codex instruction file.
It must define identity, truth hierarchy, phases, guardrails, and review
protocol.

### FR-2 Codex Harness Manifest

The repository must include `.codex/manifest.json`. The manifest must declare:

- runtime `codex`
- source harness `.codex`
- phases `PLANNING`, `BUILDING`, `AUDITING`
- approval gates `requirements`, `design`, `tasks`, `building`, `auditing`
- key documents that make up the Codex replacement

### FR-3 Phase Workflows

The repository must include phase workflows under `.codex/workflows/`.

### FR-4 Reviewable Planning Artifacts

The replacement must include this requirements document, an ADR, a design
document, and a task plan.

### FR-5 Executable Validation

The replacement must include tests that fail when:

- the manifest targets Claude instead of Codex
- approval gates are incomplete
- required replacement artifacts are missing

## Non-Functional Requirements

- NFR-1: Documents must be small enough to review independently.
- NFR-2: Tests must run without network access after dependencies are installed.
- NFR-3: The first replacement wave must avoid destructive deletion of legacy
  files.
- NFR-4: The harness must be understandable without knowing Claude Code internals.

## Acceptance Criteria

- `python -m pytest tests/test_codex_manifest.py` passes.
- `AGENTS.md` and `.codex/manifest.json` exist.
- Required docs and workflows listed in the manifest exist.
- The ADR records why Codex uses a file-driven harness instead of Claude hooks.
