# Codex LAM 置き換えタスク

Status: Draft for review
Date: 2026-04-30

## Wave 1: Codex contract scaffold

- [x] Codex 置き換え contract のための最初の manifest test を追加する。
- [x] manifest validation 用の `codex_lam/manifest.py` を追加する。
- [x] Codex 入口として `AGENTS.md` を追加する。
- [x] `.codex/manifest.json` を追加する。
- [x] `.codex/workflows/planning.md` を追加する。
- [x] `.codex/workflows/building.md` を追加する。
- [x] `.codex/workflows/auditing.md` を追加する。
- [x] requirements、ADR、design、tasks を review 可能な形で追加する。
- [x] focused test を実行し、結果を記録する。

## Wave 1 Review Sync: 承認前の文書同期

- [x] requirements review の指摘を反映する。
- [x] requirements を日本語化し、承認ゲート、quick-load、legacy behavior 最大移設を明記する。
- [x] ADR を requirements の FR-6/FR-7 に同期する。
- [x] design を requirements の FR-6/FR-7 と FR-5 test matrix に同期する。
- [x] tasks を requirements、ADR、design に同期する。
- [x] requirements の最終軽量レビューを行う。
- [x] requirements の承認を得る。
- [ ] ADR のレビューと承認を得る。
- [ ] design のレビューと承認を得る。
- [ ] tasks のレビューと承認を得る。

## Wave 2A: Manifest validation hardening

requirements FR-5 と design の TDD Strategy に合わせて、manifest validation を強化する。

- [ ] `source_harness` が `.codex` ではない場合に失敗する test を追加する。
- [ ] phase list の不足で失敗する test を追加する。
- [ ] phase list の重複で失敗する test を追加する。
- [ ] phase list の順序違いで失敗する test を追加する。
- [ ] phase list の大文字小文字違いで失敗する test を追加する。
- [ ] approval gate list の不足で失敗する test を追加する。
- [ ] approval gate list の重複で失敗する test を追加する。
- [ ] approval gate list の順序違いで失敗する test を追加する。
- [ ] approval gate list の大文字小文字違いで失敗する test を追加する。
- [ ] manifest が列挙する required document が存在しない場合に失敗する test を追加する。
- [ ] required workflow が存在しない場合に失敗する test を追加する。
- [ ] 上記の Red test を通すために `codex_lam/manifest.py` を更新する。
- [ ] focused test を実行し、Windows ACL 問題が出た場合は権限外実行または手動 cleanup を記録する。

## Wave 2B: quick-load/save workflow

requirements FR-6 と design の `SESSION_STATE.md` 方針に合わせて、手動 quick-load/save を運用できる形にする。

- [ ] `SESSION_STATE.md` の必須項目を checklist として明文化する。
- [ ] quick-save 時に記録する項目を定義する。
- [ ] quick-load 時に最初に読むファイルと確認コマンドを定義する。
- [ ] `SESSION_STATE.md` は `.gitignore` 対象のまま、共有フォルダで手動同期する運用を明記する。
- [ ] `docs/daily/` は長めの日次ログであり、quick-load の必須入力ではないことを明記する。
- [ ] 必要になった時点で、`SESSION_STATE.md` の必須項目を検証する CLI または pytest helper を検討する。

## Wave 2C: Legacy behavior inventory and migration

requirements FR-7 と ADR/design の方針に合わせて、`.claude/` 配下の資産と旧 `docs/` 資産を棚卸しし、Codex で扱える形へ移す。

- [ ] `.claude/commands/` の slash command を棚卸しする。
- [ ] `.claude/hooks/` の hook script を棚卸しする。
- [ ] `.claude/agents/` または subagent 定義を棚卸しする。
- [ ] `.claude/settings.json` などの設定を棚卸しする。
- [ ] `.claude/` 配下の rules、guides、checklists、運用メモを棚卸しする。
- [ ] 旧 `docs/specs/`、`docs/design/`、`docs/internal/` の Codex へ再利用できる資産を棚卸しする。
- [ ] `docs/migration/codex-reusable-legacy-docs.md` を入口として、model routing、Green State、scalable review、TDD introspection、security/permission、upstream-first、development flow、multi-perspective decision、cross-module blame を分類する。
- [ ] 棚卸し結果を `docs/migration/claude-legacy-inventory.md` などの review 可能な文書へまとめる。
- [ ] 各 legacy item を、Codex ハーネスへ移設、Codex-native workflow/CLI/pytest/review procedure として再実装、legacy 参考資料として維持、Claude-only runtime glue として非推奨化、のいずれかに分類する。
- [ ] 旧 docs 由来の reusable idea を、Codex LAM design、workflow、CLI、pytest helper、review checklist、migration notes のどれへ反映するか判断する。
- [ ] 移設しない legacy item について、理由を design、tasks、または migration notes に記録する。
- [ ] `.claude/agents/` や subagent 定義は、原則として役割別レビュー観点、作業手順、workflow、task generation guidance として文書化する。
- [ ] ただし agent/subagent は一律変換せず、design または tasks を作る時点で各項目ごとに Codex での扱いを個別確認する。
- [ ] permission-level classification が Claude 外でも有用なら、standalone validator へ移す。
- [ ] TDD introspection が有用なら、Claude `PostToolUse` payload に依存しない CLI または pytest helper へ移す。
- [ ] `.claude/` をコピー済みの既存プロジェクト向け migration notes を追加する。

## Wave 3: Legacy cleanup

Codex parity がレビューされ、移設対象と非推奨対象が明確になったあとで実施する。

- [ ] reviewer approval 後、top-level docs で `.claude/` を legacy として明記する。
- [ ] 日本語 mojibake の既存 docs を修復するか、英語のみを維持するか、bilingual docs として再生成するかを決める。
- [ ] Codex parity が受け入れられたあと、Claude-only docs を archive または削除する。
- [ ] quickstart を Codex 前提へ更新する。
- [ ] cheatsheet を Codex 前提へ更新する。

## Review Gates

- requirements review: behavior migration を拡張する前に実施する。
- ADR review: Claude assets の削除または archive 前に実施する。
- design review: portable validator や migration helper を実装する前に実施する。
- tasks review: 各 build wave の前に実施する。
- building review: implementation と tests が tasks と同期しているか確認する。
- auditing review: findings、残リスク、検証結果を確認する。
