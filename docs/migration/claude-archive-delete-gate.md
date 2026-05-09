# Claude archive / delete gate

Status: Gate proposal
Date: 2026-05-09

## Purpose

Wave 3 legacy cleanup leaves one high-risk action: deciding whether tracked `.claude/`
material should be archived, deleted, or kept as legacy reference.

This gate exists so that Codex parity does not silently turn into destructive cleanup.
No file movement or deletion is approved by this document alone.

## Current evidence

- `git ls-files .claude` reports 104 tracked files.
- Top-level docs already describe `.claude/` as legacy compatibility material, not the Codex primary control surface.
- `docs/migration/claude-legacy-inventory.md` classifies `.claude/` families by `codex_adopted`, `codex_reexpress`, `decide_later`, and `archive_runtime_specific`.
- Wave 3 non-destructive cleanup confirmed no mojibake hits in the checked docs and no remaining quickstart / cheatsheet rewrite need.

## Keep As Legacy Reference

Keep these unless a later gate proves they are fully superseded:

- `.claude/commands/quick-load.md`, `.claude/commands/quick-save.md`
  - Reason: useful migration reference for handoff semantics.
- `.claude/agents/*.md`
  - Reason: role guidance has been reexpressed, but the original review perspectives remain useful as reference.
- `.claude/rules/*.md`
  - Reason: permission, quality, decision, and phase rules are useful source material when auditing Codex docs.
- `.claude/skills/*`
  - Reason: several skills have Codex mirrors or project skill descendants; originals remain useful comparison material.

## Archive Candidates

Candidate archive group for a future gate:

- `.claude/hooks/`
  - Reason: Claude event-driven hook runtime is not Codex canonical control surface.
  - Risk: analyzers and tests may still be useful as source material for future scalable review work.
- `.claude/states/`
  - Reason: runtime state snapshots are historical, not active Codex state.
- `.claude/agent-memory/`
  - Reason: Claude subagent memory is historical context, not active handoff state.
- `.claude/settings.json`
  - Reason: Claude permission contract is not Codex permission contract.
- `.claude/current-phase.md`
  - Reason: `.codex/current-phase.md` is the active phase signal.
- `.claude/lam-loop-state.json.bak`
  - Reason: runtime residue.

## Delete Candidates

No direct delete candidates are approved yet.

If deletion is later approved, prefer archive-first in the same repo history before deletion:

1. Move candidate groups to an explicit archive path, or keep them tracked with stronger legacy labels.
2. Verify Codex docs and tests.
3. Only then consider deletion in a separate commit.

## Required Gate Before Archive / Delete

Before any file movement or deletion:

1. Confirm the exact file list with `git ls-files .claude`.
2. Decide archive path or delete path.
3. Document restore procedure.
4. Run `git diff --check`.
5. Run focused tests if code, hooks, scripts, or importable Python files are moved or deleted.
6. Get explicit user approval for the destructive or history-shaping operation.

## Recommendation

Do not delete `.claude/` in the current wave.

The safer next action is to keep `.claude/` as tracked legacy reference and only archive
runtime-specific subtrees after a separate approval gate.
