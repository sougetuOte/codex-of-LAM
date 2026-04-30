# Codex LAM Replacement Tasks

Status: Draft for review
Date: 2026-04-30

## Wave 1: Codex Contract Scaffold

- [x] Add failing manifest tests for the Codex replacement contract.
- [x] Add `codex_lam/manifest.py` with manifest validation.
- [x] Add `AGENTS.md` as the Codex entry point.
- [x] Add `.codex/manifest.json`.
- [x] Add `.codex/workflows/planning.md`.
- [x] Add `.codex/workflows/building.md`.
- [x] Add `.codex/workflows/auditing.md`.
- [x] Add requirements, ADR, design, and task docs for review.
- [x] Run focused tests and record results.

## Wave 2: Harness Behavior Migration

- [ ] Classify Claude hooks into portable logic, Codex-native workflow, and
  deprecated runtime glue.
- [ ] Port permission-level classification into a standalone validator if it is
  still useful outside Claude Code.
- [ ] Port TDD introspection into a CLI or pytest helper that does not depend on
  Claude PostToolUse payloads.
- [ ] Add tests for phase transitions and approval-gate state.
- [ ] Add migration notes for projects that already copied `.claude/`.

## Wave 3: Legacy Cleanup

- [ ] Mark `.claude/` as legacy in top-level docs after reviewer approval.
- [ ] Decide whether to keep English docs only or repair Japanese mojibake.
- [ ] Remove or archive Claude-only docs once Codex parity is accepted.
- [ ] Update quickstart and cheatsheet for Codex.

## Review Gates

- Requirements review before expanding behavior.
- ADR review before deleting or archiving Claude assets.
- Design review before implementing portable validators.
- Task review before each build wave.
