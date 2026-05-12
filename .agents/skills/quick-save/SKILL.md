---
name: quick-save
description: |
  Codex LAM lightweight handoff skill.
  Use when the user says quick-save, asks to save the current project state
  for the next session, or wants to update SESSION_STATE.md without broad
  logging or project rediscovery.
---

# Quick Save

Save a Codex LAM project handoff with the smallest useful update.

## Core Rule

- Treat quick-save as a lightweight resume handoff, not a historical log.
- Update `SESSION_STATE.md` in place; do not rewrite it wholesale unless the existing shape is broken.
- Keep only resume-critical state in `SESSION_STATE.md`.
- Move long notes, rationale, or daily history to `docs/daily/` and leave a short pointer.
- If `WORKBOARD.md` changed, run or intentionally skip `python tools/workboard.py validate` with the reason visible.
- Do not make `python tools/workboard.py render` part of ordinary quick-save unless this is a gate, release, or explicit review handoff.
- On Windows, use `pwsh -NoProfile`; read Japanese Markdown with UTF-8.

## Minimum Confirmation

Run or review only these first:

1. `git status --short --branch`
2. `git log --oneline --decorate -5`
3. Existing `SESSION_STATE.md`

Use this command shape for Japanese Markdown on Windows:

```powershell
Get-Content -Encoding UTF8 -LiteralPath SESSION_STATE.md
```

If `SESSION_STATE.md` does not exist, create a short one only when the user wants a handoff in this repository.

## WORKBOARD Handoff Rule

`WORKBOARD.md` is the project-state board. `SESSION_STATE.md` should point to the
active card and next starting file, not duplicate card details.

When `WORKBOARD.md` changed:

1. Prefer `python tools/workboard.py validate`.
2. Run `python tools/workboard.py render` only for gate, release, or explicit review handoff.
3. Record skipped validation or render only when the next session needs to know why.

## Update Targets

Refresh only fields that changed and matter for the next quick-load:

- `保存時刻`
- `現在フェーズ` or equivalent phase field
- `復元サマリ`
- `今回の重要な更新`
- `現在の未 commit 変更`
- `直近の検証結果`
- `次にやること`
- `重要な環境メモ`
- `関連ファイル`

Prefer pointers over pasted detail. `SESSION_STATE.md` should answer: what happened last session, what remains, and where to start next.

## Do Not Include By Default

- Long chronological logs
- Raw worker transcripts
- TDD raw logs or KPI aggregation
- Claude Code logs or Claude-specific restart instructions
- Full requirements, design, task, or review text

If those details are needed, put them in an appropriate artifact such as `docs/daily/` and reference that file briefly.

## Reporting

Keep the completion report short:

```text
--- quick-save 完了 ---
SESSION_STATE.md: 更新済み
未解決: [あれば / なし]
次回開始: 1. ... 2. ...
---
```

## References

- `.codex/workflows/quick-save.md` is the workflow source of truth.
- `docs/internal/08_QUICK_LOAD_SAVE.md` holds detailed operating policy.
- `.agents/skills/quick-load/SKILL.md` is the paired resume skill.
