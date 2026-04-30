# BUILDING Workflow

## Goal

Implement approved tasks with t-wada style TDD wherever practical.

## Cycle

1. Red: write or update a focused failing test that expresses the requirement.
2. Green: add the smallest production change that passes the test.
3. Refactor: improve structure while keeping tests green.
4. Sync docs and tasks with the actual result.
5. Report changed files and verification results.

Green State is explicit: the current task is only green when the focused check
has passed, or when a blocker is recorded with a concrete reason and next step.

## Role Guidance

- `tdd-developer` 由来:
  - 変更前に仕様、既存コード、既存テストを読む。
  - Red で要求を固定し、Green では最小実装にとどめる。
  - Refactor でのみ構造改善を行い、機能追加は混ぜない。
- `test-runner` 由来:
  - focused test を最初に回し、失敗時は原因を要約してから次手を決める。
  - docs-only change では pytest を省略できるが、省略理由を報告する。

## Reporting Expectations

- Red / Green / Refactor のどこまで進んだかを明示する。
- 実行した focused check、結果、既知 blocker を残す。
- TDD introspection は将来の optional helper 候補とし、この workflow の必須 gate にはしない。

## Guardrails

- If a requirement is ambiguous, return to PLANNING.
- If a change crosses module boundaries, expand the test scope.
- If a test cannot be written first, document why in the task file.
