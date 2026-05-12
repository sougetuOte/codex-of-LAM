# QUICK-SAVE Workflow

## Goal

Update `SESSION_STATE.md` in place so the next session can resume in the first
five minutes without broad re-discovery.

## Core Rule

- Treat quick-save as a lightweight handoff, not a historical log.
- Update only the sections that changed.
- Keep `SESSION_STATE.md` short and move long background to other artifacts when
  needed.
- If `WORKBOARD.md` changed, prefer `python tools/workboard.py validate`.
- Keep `python tools/workboard.py render` for gate, release, or explicit review
  handoffs rather than ordinary quick-save.
- Use `pwsh -NoProfile` for the first shell checks on Windows.

## Minimum Confirmation

1. Run `git status --short --branch`.
2. Run `git log --oneline --decorate -5`.
3. Review the current `SESSION_STATE.md` before editing it.

## Update In Place

Prioritize these fields.

- `保存時刻`
- `今回の重要な更新`
- `現在の未 commit 変更`
- `次にやること`

Add or refresh these only when they help the next resume.

- current phase or equivalent phase field
- short verification result
- key related files
- unresolved issue or caution

If a long explanation is needed, move it to `docs/daily/` or another artifact
and leave only a short pointer in `SESSION_STATE.md`.

## WORKBOARD Handoff

`SESSION_STATE.md` should point to the active WORKBOARD card and next starting
file. Do not paste card details into the handoff.

When `WORKBOARD.md` changed:

1. Run `python tools/workboard.py validate`, or record why validation was skipped.
2. Render only for gate, release, or explicit review handoff.
3. If generated files changed, leave the next session enough context to inspect
   the diff without re-reading the full board.

## Do Not Pull In By Default

- Claude Code loop logs
- Claude Code permission logs
- KPI aggregation
- Claude-specific restart instructions

These are optional or legacy concerns, not part of the default Codex handoff.

## Codex App Optional Path

- Thread automations can remind or resume a long-running thread, but they do not
  replace `SESSION_STATE.md`.
- Project or standalone automations should be introduced only after the manual
  quick-save flow is stable and reviewable.
- If an automation produces a useful summary, copy only the reviewed summary into
  `SESSION_STATE.md`; keep raw automation output outside the quick-load path.

## Reporting Format

Use a short completion summary such as:

```text
--- quick-save 完了 ---
SESSION_STATE.md: 更新済み
未解決: [あれば / なし]
次回開始: 1. ... 2. ...
---
```

## Reference

Detailed operating policy lives in `docs/internal/08_QUICK_LOAD_SAVE.md`.
