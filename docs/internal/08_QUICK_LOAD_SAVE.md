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
- Codex App on Windows では、日常の quick-load / quick-save 補助コマンドも
  `pwsh -NoProfile` を標準にする。
- Git Bash は手動ローカル作業で使えても、Codex 実行時の標準前提にはしない。

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

設計 / review 向けの追加原則:

- context compaction の危険域に入る前に `quick-save` する
- 長い session を無理に延命しない
- 再開時に必要な判断根拠、非採用案、未決事項を優先して残す

記録粒度の目安:

- 1 回の変更で終わったことは「完了済み」へ移す
- 途中で止めた変更は「現在の未 commit 変更」と「次にやること」の両方へ残す
- 長い背景説明は `docs/daily/` に寄せ、`SESSION_STATE.md` には要約だけ残す

quick-save 前の推奨確認は以下で十分。

```powershell
git status --short --branch
git log --oneline --decorate -5
```

TDD introspection CLI を使っている場合は、必要に応じて以下も追加してよい。

```powershell
python -m codex_lam.tdd_introspection_cli summary
```

FAIL -> PASS 候補を retro 前に見返したい場合は、
`docs/artifacts/tdd-introspection-summary-usage.md` を参照する。

追加の広い state exploration は、context compaction や state drift が疑われるときだけ行う。

特に設計 / review では、以下を感じたら続行前に quick-save を優先する。

- 判断根拠が薄くなってきた
- 非採用案や却下理由を思い出しにくい
- 同じ file を繰り返し読み直している
- 会話上は進んでいるが、未決事項が artifact に固定されていない

## 4. quick-load で最初に行うこと

新しい Codex セッションでは、**最小確認** と **必要時だけ深掘り** を分ける。

### 4.1 最小確認

まずは以下だけで開始してよい。

1. `.codex/current-phase.md` を読む
2. `git status --short --branch` を実行する
3. `git log --oneline --decorate -3` を実行する
4. `SESSION_STATE.md` から以下だけ読む
   - `保存時刻`
   - `フェーズ`
   - `復元サマリ`
   - `現在の未 commit 変更`
   - `次にやること`
   - `関連ファイル`

この時点では、requirements / ADR / design / tasks や code / tests を**まだ読まない**。

### 4.2 深掘り条件

以下のいずれかに当てはまるときだけ、追加の文書やコードを読む。

- `SESSION_STATE.md` の `次にやること` を実行するのに詳細が足りない
- `git status` が dirty で、未 commit 変更の理解が必要
- phase と `SESSION_STATE.md` の内容が食い違う
- 直近 commit だけでは次の判断点が見えない
- ユーザーが review / implementation / deep analysis を明示的に求めている

### 4.3 深掘りの順番

深掘りが必要な場合も、以下の順で最小限に広げる。

1. `AGENTS.md`
2. `SESSION_STATE.md` の必要セクションだけ追読
3. 現在 wave に対応する tasks の該当箇所
4. 必要になった requirements / ADR / design の該当箇所
5. 直近で触った code / tests

`SESSION_STATE.md` 全文読みは、要約だけでは不足すると確認できた場合に限る。

PowerShell で日本語 Markdown を読む場合は、以下を使う。

```powershell
Get-Content -Encoding UTF8 -LiteralPath SESSION_STATE.md
```

見出し位置を絞って読む場合は、`rg -n` などで対象セクションを先に特定する。
PowerShell を使う場合も、profile 付き起動で不要なノイズを出さないことを優先する。

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
