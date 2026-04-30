# `.claude/` コピー済み project 向け migration notes

Status: Draft
Date: 2026-04-30

## 目的

既存 project に `.claude/` 一式が残っている場合、Codex へ切り替えるときの
最小移行方針をまとめる。

この文書は「何をそのまま使わないか」と「何を Codex 側へ読み替えるか」を
素早く判断するためのメモであり、Claude compatibility layer を作るための
仕様ではない。

## 最初に確認すること

1. `AGENTS.md` が存在し、Codex の入口として使えるか確認する。
2. `.codex/current-phase.md` が現在の作業フェーズを示しているか確認する。
3. `.claude/` を runtime source ではなく legacy reference として扱う前提を共有する。
4. `SESSION_STATE.md` を用意し、quick-load / quick-save を Codex 手動運用へ切り替える。

## 読み替え表

| Claude 側資産 | Codex 側の読み替え先 | 備考 |
| --- | --- | --- |
| `.claude/commands/planning.md`, `building.md`, `auditing.md` | `.codex/workflows/` | slash command としては使わず、workflow 文書として扱う |
| `.claude/commands/quick-load.md`, `quick-save.md` | `SESSION_STATE.md`, `docs/internal/08_QUICK_LOAD_SAVE.md` | state file 中心の手動運用へ切り替える |
| `.claude/agents/*.md` | `.codex/workflows/` の role guidance | frontmatter は持ち込まず、観点と手順だけ移す |
| `.claude/rules/*` | `AGENTS.md`, `.codex/constitution.md`, internal docs | rule file をそのまま canonical にしない |
| `.claude/hooks/*` | 原則なし。必要なら CLI / pytest helper を別設計する | event-driven automation は直移植しない |
| `.claude/settings.json` | Codex の実際の権限モデル + `AGENTS.md` の運用ルール | allow/ask/deny 書式は読み替え対象 |
| `.claude/current-phase.md` | `.codex/current-phase.md` | phase signal を一本化する |

## 残してよいもの

- 旧 spec / ADR / design / internal docs
- `.claude/commands/quick-save.md` のような運用メモ
- `.claude/agents/*.md` の review 観点、作業手順、DoR / TDD discipline
- `.claude/rules/permission-levels.md` や `security-commands.md` の判断原理

## そのまま使わないもの

- `.claude/settings.json` の `permissions.allow/deny/ask` 書式
- hook registration
- slash command frontmatter
- subagent frontmatter の `model`, `tools`, `permission-level`
- Stop / PostToolUse / PreCompact 前提の自動 loop

## Codex での実務上の扱い

- `PG/SE/PM` は runtime metadata ではなく、修正やレビューの重さを説明する補助ラベルとしてのみ扱う。
- TDD introspection は optional helper 候補として残し、常時自動記録にはしない。
- scalable review と cross-module blame は audit の観点としてのみ残し、自動 pipeline 化は急がない。
- `.claude/` が残っていても、canonical source は `.codex/` と `docs/` と既存 tracked files に置く。

## 既存 project を移行するときの順序

1. `AGENTS.md` と `.codex/` を追加または更新する。
2. requirements / ADR / design / tasks を Codex 前提で同期する。
3. `SESSION_STATE.md` と quick-load/save 運用を用意する。
4. `.claude/` 資産を inventory し、移設 / 再表現 / legacy 参考 / archive を分類する。
5. 反映先が決まった項目だけを workflow、internal docs、helper 候補へ移す。

## Deferred items

- permission-level classification の standalone validator 化判断
- TDD introspection helper の実装判断
- scalable review helper の自動化
- quickstart / cheatsheet の Codex 前提更新
