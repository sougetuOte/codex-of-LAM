# quick-load/save harvest decision

Status: Draft
Date: 2026-05-09

## Purpose

`docs/artifacts/quick-load-harvest-notes.md` と
`docs/artifacts/quick-save-harvest-notes.md` の一次採掘結果をもとに、
Codex LAM で採用する quick-load / quick-save の最小 shape を固定する。

## Baseline Now

- `.codex/workflows/quick-load.md`
  - Decision: Codex-native な短い resume workflow として維持する。
  - Reason: `SESSION_STATE.md` を軸にしつつ、`.codex/current-phase.md`、
    `git status --short --branch`、`git log --oneline --decorate -3` を
    最小確認に含める形が、この repo の Windows/Codex 運用に合っている。

- `.codex/workflows/quick-save.md`
  - Decision: 新規追加する。
  - Reason: `docs/internal/08_QUICK_LOAD_SAVE.md` には詳細方針があるが、
    日常運用で参照しやすい短い差分更新 workflow がまだ Codex 側にない。

- `docs/internal/08_QUICK_LOAD_SAVE.md`
  - Decision: 背景方針と詳細運用の SSOT として維持する。
  - Reason: quick-load / quick-save の補助コマンド、同期、deepen 条件、
    optional layer、将来の validator 候補は internal docs に残すのが自然。

- `SESSION_STATE.md`
  - Decision: 薄い handoff memo のまま維持する。
  - Reason: quick-save は履歴保全ではなく、次回セッションの最初の 5 分を
    迷わず始めることを優先する。長い履歴や詳細環境情報は必要に応じて
    `docs/daily/` や他 artifact へ逃がす。

## Next Wave Decision

- `docs/internal/08_QUICK_LOAD_SAVE.md` の checklist の厚さ
  - Decision: 今回は全面改稿せず、運用原理のほうを優先して同期する。
  - Reason: `完了済み`、`重要な環境メモ`、`関連ファイル`、`主要コマンド`
    などをどこまで必須にするかは、実運用を見ながら薄くする余地がある。

- `SESSION_STATE.md` 項目名 drift の扱い
  - Decision: workflow 側で exact heading を前提にしすぎない書き方へ寄せる。
  - Reason: 現在の state file と internal docs で `フェーズ` /
    `現在フェーズ` の表記ゆれがあり、resume 手順が見出し名に縛られるのは弱い。

## Archive Runtime-specific

- `.claude/commands/quick-save.md` の Claude 再開導線
  - Decision: `claude -c`、`claude`、`/quick-load`、`/ship` 前提の案内は採用しない。
  - Reason: Codex-native workflow の canonical source ではないため。

- `.claude/logs/loop-*.txt`、`.claude/logs/permission.log`、KPI 集計
  - Decision: Codex quick-save の標準材料にはしない。
  - Reason: いずれも optional / legacy 寄りであり、日常 handoff を重くする。

## Impact On Current Work

- `.codex/workflows/quick-save.md` を追加する。
- `.codex/workflows/quick-load.md` は field-name drift を吸収する方向で軽く調整する。
- `docs/internal/08_QUICK_LOAD_SAVE.md` に quick-save の短い参照導線を足す。
- `docs/design/codex-lam-replacement-design.md` と
  `docs/migration/claude-to-codex-migration-notes.md` を新しい workflow 構成へ同期する。
