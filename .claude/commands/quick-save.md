---
description: セッション状態のセーブ（SESSION_STATE.md + ループログ + Daily記録）
---

# クイックセーブ

プロジェクトルートの `SESSION_STATE.md` を軽量更新する。
git commit は行わない（コミットは `/ship` を使用）。
Codex では **差分更新をデフォルト** とし、毎回フル再要約しない。

## 0. 軽量化ルール

- 既存 `SESSION_STATE.md` を土台にし、**全面書き換えしない**。
- 基本は以下だけを更新する。
  - `保存時刻`
  - `今回の重要な更新`
  - `現在の未 commit 変更`
  - `次にやること`
  - 必要なら `直近の BUILDING 更新` または同等の直近作業欄
- `完了済み` や長い履歴は、重要な節目がない限り追記しない。
- `git status --short --branch` と `git log --oneline --decorate -5` を優先し、広い再探索はしない。
- context compaction や state drift が疑われる場合のみ、quick-load 側に「軽い state exploration」を勧める一文を残す。

## 1. プロジェクトルートの SESSION_STATE.md を書き出す

以下の内容を **必要な箇所だけ** 簡潔に更新する。

### 最優先で更新する項目

- 保存時刻
- 今回の重要な更新（1〜5 bullet 程度）
- 進行中タスク / 次にやること
- 変更ファイル一覧
- 未解決の問題

### 完了タスク
- 大きな節目があった場合のみ箇条書き
- すでに書いてある長い履歴は無理に整形し直さない

### 進行中タスク
- 作業途中のものとその現在の状態
- 次に何をすべきか

### 次のステップ
- 次セッションで最初にやるべきこと（優先順位付き）

### 変更ファイル一覧
- 今回変更したファイルのパス一覧

### 未解決の問題
- 残っている課題、確認事項（なければ「なし」）

### コンテキスト情報
- 現在のフェーズ (PLANNING / BUILDING / AUDITING)
- 現在のgitブランチ
- 関連するSPEC/ADR/設計書ファイル名

## 2. ループログ保存

Codex では **デフォルトでは省略可**。

- `.claude/logs/loop-*.txt` が存在しても、通常の quick-save では必須にしない。
- loop log を使う wave / task、またはユーザーが明示した場合だけ扱う。
- 詳細: `docs/specs/loop-log-schema.md`

## 3. Daily 記録

Codex では **デフォルトでは省略可**。

- `docs/daily/YYYY-MM-DD.md` は長めの振り返りが必要な時だけ更新する。
- quick-load のための必須作業にはしない。
- 必要時のみ以下を記録:

### 本日完了
- 完了したタスク（1〜3項目）

### 明日の最優先
- 次にやるべきこと（1項目）

### 課題・気づき
- あれば最大1つ

### KPI 集計

ベースライン確立後（Wave 2 完了後）、KPI を集計・表示する。
詳細定義: `docs/specs/evaluation-kpi.md`

集計手順:
1. `.claude/logs/loop-*.txt` を走査し、K1〜K5 を計算
2. `.claude/logs/permission.log` を走査し、等級分布（PG/SE/PM）を集計
3. テンプレートは `docs/specs/evaluation-kpi.md` Section 6 を参照

## 4. 完了報告

以下を表示:

```
--- quick-save 完了 ---
SESSION_STATE.md: 更新済み
Daily: 必要時のみ更新

再開方法:
  claude -c  （直前セッション続行）
  claude     （新規セッション）

再開後: /quick-load
git commit が必要なら: /ship
---
```
