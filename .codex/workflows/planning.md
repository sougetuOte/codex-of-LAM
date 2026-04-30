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

## Role Guidance

- `requirement-analyst` 由来:
  - 曖昧さ、スコープ漏れ、受け入れ条件不足を先に潰す。
  - 実装方法より先に、Who / What / Why と制約を固定する。
- `design-architect` 由来:
  - 要件を満たす最小設計を優先し、過剰な抽象化は避ける。
  - trade-off と ADR 候補を明示する。
- `task-decomposer` 由来:
  - 1 review / 1 PR 相当の粒度を目安にする。
  - 依存順序、並列化可能性、検証方法をタスクに残す。
- `doc-writer` 由来:
  - specs / ADR / design / tasks は SSOT として同期し、曖昧な表現を残さない。

## Forbidden In This Phase

- Broad production code rewrites.
- Treating `.claude/settings.json` or Claude hooks as Codex runtime controls.
- Skipping approval gates for requirements, design, and tasks.
