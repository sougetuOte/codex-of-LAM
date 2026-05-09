---
name: quick-load
description: |
  Codex LAM project resume skill.
  Use when the user says quick-load, asks to resume a Codex LAM repo,
  asks what the next task is after reopening a session, or wants a
  low-context re-entry into a project that uses SESSION_STATE.md.
---

# Quick Load

Resume a Codex LAM project with the smallest useful context.

## Core Rule

- Treat quick-load as resume, not project rediscovery.
- Start with the minimum confirmation bundle.
- Read more files only when the next action is blocked.
- On Windows, use `pwsh -NoProfile` for the first shell checks.

## Minimum Confirmation

Run or read only these first:

1. `.codex/current-phase.md`
2. `git status --short --branch`
3. `git log --oneline --decorate -3`
4. `SESSION_STATE.md` resume fields:
   - `保存時刻`
   - `フェーズ` or `現在フェーズ`
   - `復元サマリ`
   - `現在の未 commit 変更`
   - `次にやること`
   - `関連ファイル`

If `SESSION_STATE.md` does not exist, report that this is a new session and stop.

## Deepen Only If Needed

Read additional context only when one of these is true:

- `次にやること` cannot be executed from the summary alone.
- `git status` shows dirty changes that need interpretation.
- `.codex/current-phase.md` and `SESSION_STATE.md` disagree.
- The user asked for review, implementation, or deeper analysis.

When deepening, expand in this order:

1. `AGENTS.md`
2. Needed sections of `SESSION_STATE.md`
3. The current task document
4. Required requirement, ADR, or design sections
5. Touched code or tests

## Reporting

Keep the result short:

```text
--- quick-load 完了 ---
前回: YYYY-MM-DD | Phase: [Phase]

完了: [要約]
未完了: [あれば/なし]
次: 1. ... 2. ...
参照予定: [ファイルパス]
---
```

## References

- `.codex/workflows/quick-load.md` is the workflow source of truth.
- `docs/internal/08_QUICK_LOAD_SAVE.md` holds detailed operating policy.
