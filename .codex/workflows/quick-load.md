# QUICK-LOAD Workflow

## Goal

Resume work from `SESSION_STATE.md` with the smallest possible context cost.

## Core Rule

- Treat quick-load as resume, not re-reading the whole project.
- Start with minimum confirmation only.
- Read more files only when the next action is blocked by missing detail.
- Do not render `WORKBOARD.md` during quick-load.
- Use `pwsh -NoProfile` for the first shell checks on Windows.

## Minimum Confirmation

1. Read `.codex/current-phase.md`.
2. Run `git status --short --branch`.
3. Run `git log --oneline --decorate -3`.
4. Read only the equivalent resume fields from `SESSION_STATE.md`:
   - `保存時刻`
   - phase field such as `フェーズ` or `現在フェーズ`
   - `復元サマリ`
   - `現在の未 commit 変更`
   - `次にやること`
   - `関連ファイル`

If `SESSION_STATE.md` does not exist, report that the session will start as a new
session and stop there.

## WORKBOARD Dashboard Check

If the minimum confirmation points to `WORKBOARD.md`, read only the top
`## Dashboard` block and, if needed, the active card row from `## Cards`.

Do not run `python tools/workboard.py render` in quick-load. Rendering belongs to
gate, release, or explicit review workflows.

## Deepen Only If Needed

Read more only when one of these is true.

- `次にやること` cannot be executed from the summary alone.
- `git status` shows dirty changes that need interpretation.
- `.codex/current-phase.md` and `SESSION_STATE.md` disagree.
- The `WORKBOARD.md` dashboard and `SESSION_STATE.md` disagree.
- The user asked for review, implementation, or deeper analysis.

## Expansion Order

When deeper reading is necessary, expand in this order.

1. `AGENTS.md`
2. Needed sections of `SESSION_STATE.md`
3. The relevant part of the current task document
4. The required requirement, ADR, or design section
5. The touched code or tests

## Reporting Format

Use a short resume summary such as:

```text
--- quick-load 完了 ---
前回: YYYY-MM-DD | Phase: [Phase]

完了: [要約]
未完了: [あれば/なし]
次: 1. ... 2. ...
参照予定: [ファイルパス]
---
```

## Reference

Detailed operating policy lives in `docs/internal/08_QUICK_LOAD_SAVE.md`.
