# Quick Load / Save Workflow

Codex LAM における `SESSION_STATE.md` ベースの手動 quick-load / quick-save 運用を定義する。

## 1. 方針

- `SESSION_STATE.md` は短いセッション復元メモとして扱う。
- `SESSION_STATE.md` は `.gitignore` 対象のまま維持する。
- 別PCや別環境へ引き継ぐ場合は、共有フォルダなどで手動同期する。
- `docs/daily/` は長めの日次ログ用であり、quick-load の必須入力にはしない。
- quick-load / quick-save は、当面 CLI 自動化ではなく review 可能な手動 workflow として運用する。
- quick-save は **差分更新を標準** とし、毎回 full rewrite しない。
- loop log / daily / KPI は、必要な session だけ追加する optional layer として扱う。

## 2. `SESSION_STATE.md` 必須項目 checklist

quick-save 時点の `SESSION_STATE.md` は、少なくとも以下を含む。

- 保存時刻
- プロジェクト名
- 現在フェーズ
- ブランチ
- Remote
- 現在の作業パス
- 復元サマリ
- 完了済み
- 今回の重要な更新
- 現在の未 commit 変更
- 次にやること
- 重要な環境メモ
- 関連ファイル

以下は強く推奨する。

- 直近の検証結果
- 実行した主要コマンド
- sandbox / 権限 / OS 由来の既知問題
- 次回の開始点になる wave / task 名

## 3. quick-save で記録する項目

quick-save では、次回セッションが「迷わず最初の 5 分を過ごせる」ことを目標に記録する。

最低限、以下を書く。

- 今どこまで終わったか
- 何が未完了か
- 次に何から始めるか
- どのファイルを先に読むべきか
- 直近の test / manual verification の結果
- 続行時に踏みやすい罠

軽量運用の原則:

- 既存 `SESSION_STATE.md` をベースに差分だけ更新する
- 基本更新対象は `保存時刻`、`今回の重要な更新`、`現在の未 commit 変更`、`次にやること`
- `完了済み` の長い履歴は、大きなマイルストーンがない限り触らない
- 背景説明を増やしすぎず、「次の 5 分で困らない情報」を優先する

記録粒度の目安:

- 1 回の変更で終わったことは「完了済み」へ移す
- 途中で止めた変更は「現在の未 commit 変更」と「次にやること」の両方へ残す
- 長い背景説明は `docs/daily/` に寄せ、`SESSION_STATE.md` には要約だけ残す

quick-save 前の推奨確認は以下で十分。

```powershell
git status --short --branch
git log --oneline --decorate -5
```

追加の広い state exploration は、context compaction や state drift が疑われるときだけ行う。

## 4. quick-load で最初に行うこと

新しい Codex セッションでは、以下の順で確認する。

1. `SESSION_STATE.md` を読む
2. `git status --short --branch` を実行する
3. `git log --oneline --decorate -5` を実行する
4. `AGENTS.md` を読む
5. `.codex/manifest.json` を読む
6. `.codex/current-phase.md` を読む
7. 現在 wave に対応する requirements / ADR / design / tasks を読む
8. 必要なら直近で触った code / tests を開く

PowerShell で日本語 Markdown を読む場合は、以下を使う。

```powershell
Get-Content -Encoding UTF8 -LiteralPath SESSION_STATE.md
```

## 5. 共有と同期

- `SESSION_STATE.md` は GitHub へ通常 push しない
- quick-load が必要な環境間では、共有フォルダ、クラウドストレージ、または手動コピーで同期する
- `docs/daily/` は共有してもよいが、quick-load の前提にはしない

## 6. `docs/daily/` の扱い

- `docs/daily/` は長めの日次ログ、振り返り、補助メモ用
- quick-load の必須入力ではない
- `SESSION_STATE.md` に入りきらない履歴や背景を置く場所として使う
- `SESSION_STATE.md` から参照リンクを張るのはよい
- 毎回の quick-save で更新する必要はない

## 7. 将来の自動検証

必要になった時点で、以下のどちらかを追加検討する。

- `SESSION_STATE.md` の見出し存在を検証する CLI
- `SESSION_STATE.md` の必須項目を検証する pytest helper

ただし BUILDING 初期段階では、まず文書運用を固める。
自動検証は、項目や書式が安定してから導入する。
