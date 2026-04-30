# Codex LAM 置き換え要件

Status: 承認済み
Date: 2026-04-30

## 問題

現在の Living Architect Model は Claude Code 向けに設計されている。
制御面は `.claude/settings.json`、hooks、slash commands、custom subagents に依存している。

Codex ではそれらの仕組みをそのまま実行面として扱えない。したがって、Claude Code 固有の仕組みが存在するかのように振る舞うのではなく、Codex で読めて、レビューできて、テストできる形に置き換える必要がある。

## 目的

- `AGENTS.md` を Codex の主要な入口として置く。
- 実行中のハーネス定義を `.codex/` に移す。
- `PLANNING`、`BUILDING`、`AUDITING` の3フェーズを維持する。
- requirements、design、tasks、building、auditing の承認ゲートを維持する。
- requirements、ADR、design、tasks、実行可能テストで置き換え内容をレビュー可能にする。
- 実装時は可能な限り t-wada style TDD を使う。
- `.claude/` は移行元資料として扱い、Codex の実行時ソースにはしない。
- Codex の quick-load で、短い状態ファイルから作業文脈を復元できるようにする。
- `.claude/` にある rules、commands、hooks、agents/subagents、設定、運用知識のうち、Codex で安全かつ自然に対応できるものは最大限 Codex ハーネスへ移設する。

## 非目的

- 最初の wave で `.claude/` 配下をすべて削除すること。
- Claude Code hooks を Codex 内でエミュレートすること。
- Codex の権限モデルを迂回する隠し自動化層を作ること。
- 明示的な移行タスクなしに、既存の歴史的ドキュメントを書き換えること。

## 用語

- Codex ハーネス: `AGENTS.md`、`.codex/manifest.json`、`.codex/constitution.md`、`.codex/workflows/`、関連する `docs/` 成果物で構成される、Codex 向けの作業契約。
- 承認ゲート: 次の作業段階へ進む前に、ユーザーまたはレビュー担当者が明示的に受け入れる必要がある確認点。
- quick-load: 新しい Codex セッションで `SESSION_STATE.md` を読めば、直前の作業状態、次の行動、主要ファイル、既知の注意点を復元できる状態。
- legacy Claude material: `.claude/` 配下の既存資料。設計の参考にはできるが、Codex 実行時の権威ある設定としては扱わない。
- portable legacy behavior: `.claude/` 配下にあるルール、コマンド、hook、agent/subagent、設定、運用知識のうち、Claude Code 固有の runtime に依存せず、Codex の文書、workflow、CLI、pytest、レビュー手順として再表現できるもの。

## 権威順位

移行期間中に文書が衝突した場合、以下の順で扱う。

1. ユーザーの明示的な指示。
2. `AGENTS.md`。
3. `.codex/constitution.md` と `.codex/workflows/`。
4. requirements、ADR、design、tasks。
5. 既存コードとテスト。
6. `.claude/` 配下の legacy Claude material。

`.claude/` は、Codex ハーネスと矛盾する場合には Codex 側を優先する。

## 承認ゲート

承認ゲートは、フェーズ遷移または大きな作業開始の前に確認する。

| ゲート | 位置づけ | 承認条件 |
| --- | --- | --- |
| requirements | PLANNING 中 | 問題、目的、非目的、受け入れ条件がレビュー済みであること |
| design | BUILDING 開始前 | ADR と design が requirements と矛盾しないこと |
| tasks | BUILDING 開始前 | tasks が小さく、TDD で進められる単位に分かれていること |
| building | AUDITING 開始前 | 実装とテストが tasks と同期していること |
| auditing | 完了前 | レビュー結果、残リスク、検証結果が記録されていること |

Codex は承認がないまま次フェーズへ進まない。ユーザーが明示的にリスクを受け入れた場合のみ、この制約を上書きできる。

## 機能要件

### FR-1 Codex 入口

リポジトリは `AGENTS.md` を Codex の主要な instruction file として持たなければならない。

`AGENTS.md` は少なくとも以下を定義する。

- Codex LAM における役割。
- 権威順位。
- `PLANNING`、`BUILDING`、`AUDITING` のフェーズ。
- 承認ゲート。
- レビューとテストの基本方針。
- `.claude/` を legacy として扱う境界。

### FR-2 Codex ハーネスマニフェスト

リポジトリは `.codex/manifest.json` を持たなければならない。

manifest は少なくとも以下のフィールドを持つ。

- `name`
- `runtime`
- `source_harness`
- `phases`
- `approval_gates`
- `documents`

manifest は以下を満たさなければならない。

- `runtime` は `codex` である。
- `source_harness` は `.codex` である。
- `phases` は `PLANNING`, `BUILDING`, `AUDITING` の順である。
- `approval_gates` は `requirements`, `design`, `tasks`, `building`, `auditing` の順である。
- `documents` に列挙されたファイルは存在する。
- Claude 実行時を指す値を、Codex の実行契約として宣言しない。

### FR-3 Phase workflows

リポジトリは `.codex/workflows/` 配下に以下の workflow ファイルを持たなければならない。

- `.codex/workflows/planning.md`
- `.codex/workflows/building.md`
- `.codex/workflows/auditing.md`

各 workflow は少なくとも以下を説明する。

- フェーズの目的。
- 必要な入力。
- 主な手順。
- そのフェーズで禁止または注意すべきこと。
- 次の承認ゲートとの関係。

### FR-4 レビュー可能な planning artifacts

置き換え作業は以下の成果物でレビュー可能にする。

- requirements: `docs/specs/codex-lam-replacement-requirements.md`
- ADR: `docs/adr/0005-codex-native-harness.md`
- design: `docs/design/codex-lam-replacement-design.md`
- tasks: `docs/tasks/codex-lam-replacement-tasks.md`

### FR-5 実行可能な検証

置き換え作業は pytest で検証できなければならない。

少なくとも以下の失敗ケースをテストする。

- manifest の `runtime` が `codex` ではない。
- manifest の `source_harness` が `.codex` ではない。
- phase 一覧が不足、重複、順序違い、または大文字小文字違いになっている。
- approval gate 一覧が不足、重複、順序違い、または大文字小文字違いになっている。
- manifest が列挙する required document が存在しない。
- required workflow が存在しない。

### FR-6 quick-load 状態復元

リポジトリは手動 quick-load のために `SESSION_STATE.md` を使える状態にする。

`SESSION_STATE.md` は少なくとも以下を含む。

- 保存時刻。
- 現在フェーズ。
- ブランチと remote。
- 完了済み作業。
- 進行中の作業。
- 次の手順。
- 主要ファイル。
- 既知の環境注意点。

新しい Codex セッションでは、`SESSION_STATE.md` を読むことで、次に読むべきファイルと次に実行すべき確認を判断できる必要がある。

### FR-7 Legacy behavior の最大移設

Codex LAM は `.claude/` 配下の既存資産を単に無視してはならない。

Wave 2 以降で、少なくとも以下を棚卸しする。

- `.claude/commands/` の slash command。
- `.claude/hooks/` の hook script。
- `.claude/agents/` または subagent 定義。
- `.claude/settings.json` などの設定。
- `.claude/` 配下にある rules、guides、checklists、運用メモ。

棚卸しした項目は、以下のいずれかに分類する。

- Codex ハーネスへ移設する。
- Codex-native workflow、CLI、pytest helper、レビュー手順として再実装する。
- legacy 参考資料として残す。
- Claude Code 専用の runtime glue として非推奨化または削除候補にする。

Codex で安全かつ自然に対応できるものは、原則として移設または再実装する。
移設しない場合は、理由を tasks、design、migration notes のいずれかに記録する。

`.claude/agents/` や subagent 定義は、基本方針として Codex の役割別レビュー観点、作業手順、workflow、または task generation guidance として文書化する。
ただし、すべてを同じ形に変換できるとは限らないため、design または tasks を作る時点で、各 agent/subagent ごとに Codex での扱いを個別確認する。

## 非機能要件

- NFR-1: 各ドキュメントは単独レビューできる大きさに保つ。
- NFR-2: 依存関係インストール後、テストはネットワークなしで実行できる。
- NFR-3: 最初の wave では legacy ファイルを破壊的に削除しない。
- NFR-4: Claude Code の内部仕様を知らなくても、Codex ハーネスを理解できる。
- NFR-5: 日本語で書ける project-facing documentation は日本語を基本にする。コード識別子、ファイル名、コマンド、API 名は英語のままでよい。

## 受け入れ条件

- `python -m pytest tests/test_codex_manifest.py` が通る。
- `AGENTS.md` が存在し、Codex の入口、権威順位、フェーズ、承認ゲート、legacy Claude boundary を説明している。
- `.codex/manifest.json` が存在し、FR-2 の schema と値を満たす。
- `.codex/workflows/planning.md`、`.codex/workflows/building.md`、`.codex/workflows/auditing.md` が存在し、FR-3 の最小内容を満たす。
- manifest の `documents` に列挙された required document がすべて存在する。
- requirements、ADR、design、tasks が互いに矛盾しない。
- ADR が、Claude runtime controls ではなく Codex-native file-driven harness を使う理由を記録している。
- `SESSION_STATE.md` を読めば、quick-load 後に次の作業と注意点を復元できる。
- `.claude/` 配下のファイルを Codex 実行時の権威ある設定として扱っていない。
- `.claude/` 配下の rules、commands、hooks、agents/subagents、設定、運用知識が棚卸し対象として明記され、Codex へ移設するか、再実装するか、legacy として残すか、非推奨化するかを判断する作業が tasks に含まれている。
