# AUDITING Workflow

## Goal

Review behavior, quality, security, and documentation consistency after or
between implementation waves.

## Steps

1. Review the changed files first.
2. Check requirement, ADR, design, task, and code consistency.
3. Run focused tests, then broader tests when shared behavior changed.
4. If `WORKBOARD.md` exists and the review is a gate or release readiness check,
   run `python tools/workboard.py validate` and `python tools/workboard.py render`,
   then inspect the generated artifact diff as a review surface.
5. Report findings by severity with file and line references.
6. Apply only low-risk fixes unless the user approves larger corrections.

## Codex App Optional Path

- Use the Codex App review pane for diff inspection, inline comments, staging
  checks, commit, push, and PR preparation when available.
- Use in-app browser inspection for local HTML slides, README image previews,
  frontend surfaces, and generated visual artifacts.
- Use Worktree mode for independent audit passes that should not disturb active
  implementation work.
- Keep automations as optional audit helpers, such as recent-commit summaries or
  scheduled drift checks. Do not make them required gates until they are reliable
  manually.

Do not treat "probably fine" as Green State. The gate should be able to see what
was verified, what remains open, and whether any unresolved issue blocks closure.

## Role Guidance

- `code-reviewer` 由来:
  - 品質、保守性、セキュリティ、文書整合性を分けて見る。
  - 指摘は好みではなく、具体的なリスクと改善案に結び付ける。
- `quality-auditor` 由来:
  - 仕様ドリフト、構造整合性、依存境界、既知の運用ルール逸脱を確認する。
  - 複数モジュールにまたがる不整合は、upstream/downstream の帰責判断を補助情報として添える。

## Severity And Scope

- Critical / Warning / Info を使い、Issue がない場合もその旨を明示する。
- `PG/SE/PM` は Claude runtime metadata ではなく、修正判断の補助ラベルとしてのみ参照する。
- scalable review の原理は使ってよいが、Claude hook loop や analyzer pipeline は前提にしない。

## Findings

Use review findings for defects, regressions, missing tests, or security risks.
Keep summaries secondary to concrete issues.
