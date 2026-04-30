# PLANNING Workflow

## Goal

Turn intent into reviewable artifacts before implementation starts.

## Required Inputs

- User intent and constraints.
- Existing docs and source that may be affected.
- Current phase from `.codex/current-phase.md`.

## Steps

1. Inventory relevant files and legacy Claude assumptions.
2. Draft or update requirements in `docs/specs/`.
3. Record architecture decisions in `docs/adr/`.
4. Draft implementation design in `docs/design/`.
5. Decompose work into small TDD-friendly tasks in `docs/tasks/`.
6. Ask for review or approval before broad implementation.

## Forbidden In This Phase

- Broad production code rewrites.
- Treating `.claude/settings.json` or Claude hooks as Codex runtime controls.
- Skipping approval gates for requirements, design, and tasks.
