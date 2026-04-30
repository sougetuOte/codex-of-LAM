# 旧 docs 資産 採掘メモ

Status: Raw harvest
Date: 2026-04-30

## 目的

このメモは、旧 Claude 版 `docs/specs/`、`docs/adr/`、`docs/design/` から
Codex LAM へ再利用できそうな設計知見を、軽量モデルで先に採掘した一次メモである。

ここでは最終判断をしない。
次の判断ステップで、`docs/migration/codex-reusable-legacy-docs.md`、ADR、design、tasks へ
反映するかを決める。

## 採掘方針

- そのまま移植できる実装ではなく、Codex-native に再表現できる判断原理を拾う。
- Claude Code 固有の hook、slash command、settings、subagent 実装は直移植しない。
- 採用候補、後で判断、Claude-only 寄り、不採用候補に粗分類する。
- 詳細な採否は 5.5 または 5.4 の判断ステップで行う。

## ADR 由来

### 採用候補

- `docs/adr/0001-model-routing-strategy.md`
  - 低コスト層で粗分類し、重い判断を上位モデルへ残す三層分離は、Codex のモデル運用ガイドに使える。
- `docs/adr/0002-stop-hook-implementation.md`
  - 状態ファイル、反復回数上限、test/lint による Green State 確認は、Codex の phase/gate 設計へ転用できる。
- `docs/adr/0003-context7-vs-webfetch.md`
  - 一次ソース優先とフォールバックの優先順位付けは、Codex の公式情報確認ルールへ使える。
- `docs/adr/0004-bash-read-commands-allow-list.md`
  - read-only 操作は広く許容し、破壊的操作だけ別ガードで止める分離は、Codex の権限運用にも有効。

### 後で判断

- `docs/adr/0001-model-routing-strategy.md`
  - 計画と実行でモデルを切り替える発想は有用だが、Codex の現行モデル構成に合わせた再評価が必要。
- `docs/adr/0002-stop-hook-implementation.md`
  - 最新メッセージや実行状態を直接読む設計は、Codex 側で安定して取得できる情報に置き換える必要がある。
- `docs/adr/0004-bash-read-commands-allow-list.md`
  - `Bash(cat *)` のような許可粒度は Claude 書式なので、Codex の権限モデルに合わせて再設計する。

### Claude-only 寄り

- `docs/adr/0001-model-routing-strategy.md`
  - hooks / subagents / haiku-sonnet-opus 前提の具体ルーティングは Claude Code 固有。
- `docs/adr/0002-stop-hook-implementation.md`
  - Ralph Wiggum や Stop hook 実装は Claude plugin / hook 前提。
- `docs/adr/0003-context7-vs-webfetch.md`
  - context7 MCP と code.claude.com の組み合わせは Claude Code 文脈が強い。
- `docs/adr/0004-bash-read-commands-allow-list.md`
  - `settings.json` の `permissions.allow` 書式は Claude harness 前提。

### 不採用候補

- `.claude/` を単純に `.codex/` へリネームする移植。
  - `docs/adr/0005-codex-native-harness.md` の Codex-native 方針と衝突する。
- WebFetch の無応答を前提にした自動フロー。
  - Codex ではタイムアウト、公式情報確認、ユーザー判断への復帰を別途設計する。

## Design 由来

### 採用候補

- `docs/design/scalable-code-review-design.md`
  - review stage、状態永続化、スケール判定、chunking、依存グラフは大規模レビューに有用。
- `docs/design/lam-orchestrate-design.md`
  - タスク分解、担当割当、Wave 単位の並列実行は Codex の多ファイル作業に使える。
- `docs/design/gitleaks-integration-design.md`
  - 外部バイナリを薄いラッパーで issue 化し、未導入、失敗、明示 opt-out を分ける設計は security gate に使える。
- `docs/design/cross-module-blame-design.md`
  - 契約カードがある場合だけ帰責ヒントを注入する設計は、モジュール境界レビューの補助として有用。

### 後で判断

- `docs/design/codex-lam-replacement-design.md`
  - 段階移行、棚卸し、非破壊 cleanup は有用だが、Wave や manifest の切り方は現行 Codex 仕様に合わせて再調整する。
- `docs/design/hooks-python-migration-design.md`
  - subprocess / importlib / sys.path の 3 層テストは有用だが、Claude hook event と起動形式は直移植しない。

### Claude-only 寄り

- `docs/design/v4.0.0-immune-system-design.md`
  - PreToolUse / PostToolUse / Stop / PreCompact と permission-level / Green State loop は Claude 実行系に強く依存。
- `docs/design/lam-orchestrate-design.md`
  - Task tool、Subagent 制約、Agent Teams 実験機能は Claude 固有の操作面が強い。

### 不採用候補

- `docs/design/v4.0.0-immune-system-design.md`
  - `decision: block` や `stop_hook_active` による停止阻止ループは、Codex に同型の hook がなく移植しにくい。
- `docs/design/lam-orchestrate-design.md`
  - `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` や `~/.claude/tasks/` 共有キュー前提の拡張。

## Specs 由来: Green State / KPI / Loop Log / TDD

### 採用候補

- `docs/specs/loop-log-schema.md`
  - `convergence_reason`、`issues`、`classification`、`deferred_items` を JSON schema で構造化する発想は、監査ログと KPI 集計に使える。
- `docs/specs/evaluation-kpi.md`
  - K1-K5 をログから定量化し、ベースラインを先に取る方針は運用評価の土台になる。
- `docs/specs/green-state-definition.md`
  - Green State を「スキャンして issue がゼロ」と明確化し、段階的に拡張する考え方は収束条件の標準化に使える。

### 後で判断

- `docs/specs/green-state-definition.md`
  - G3/G4 のような完全実装前提の条件は、Codex LAM の権限設計や仕様同期機構が固まってから判断する。
- `docs/specs/evaluation-kpi.md`
  - `/quick-save` や `/project-status` への埋め込みは、Codex 側の定常出力フローに置き換える。
- `docs/specs/loop-log-schema.md`
  - `changed_files` や詳細な `deferred_items` は便利だが、最初から常時取得すると重い。

### Claude-only 寄り

- `docs/specs/tdd-introspection-v2.md`
  - `/retro` 統合、PostToolUse / Stop hook、`systemMessage` 通知は Claude Code 運用前提。
- `docs/specs/tdd-introspection-v2.md`
  - JUnit XML 利用は汎用だが、`.claude/test-results.xml` などのパス設計はそのまま採らない。

### 不採用候補

- `docs/specs/tdd-introspection-v2.md`
  - `exitCode` 非依存の回避策は環境固有の不具合対処であり、Codex LAM の設計原則には直接載せにくい。
- `docs/specs/green-state-definition.md`
  - テストフレームワーク自動検出順序の具体列挙は、Codex 環境差分を踏まえて再設計する。

## Specs 由来: Scalable Review / Cross-module Blame

### 採用候補

- `docs/specs/scalable-code-review-spec.md`
  - 依存グラフで影響範囲を出し、`SESSION_STATE.md` や外部 JSON/MD へ状態を永続化する考え方は、セッション継続に使える。
- `docs/specs/scalable-code-review.md`
  - 静的事前分析、LLM review、統合という分業は、モデルコスト削減とレビュー精度の両方に効く。
- `docs/specs/scalable-code-review.md`
  - tree-sitter / ast で構造を先に取り、LLM の context を絞る方針は Codex でも有用。
- `docs/specs/scalable-code-review-phase5-spec.md`
  - 静的解析、chunking、依存追跡、再レビューを束ねる pipeline は、複数 workflow 統合の候補。

### 後で判断

- `docs/specs/scalable-code-review-spec.md`
  - topological sort や SCC 縮約まで含めた依存順 review は強力だが、最初から必要かは未確定。
- `docs/specs/scalable-code-review-phase5-spec.md`
  - 影響 chunk のみ再レビューする案は効率的だが、整合性維持コストと天秤。
- `docs/specs/cross-module-blame-spec.md`
  - 帰責ヒントを prompt に埋める設計は使えそうだが、標準出力に混ぜるかは要検討。

### Claude-only 寄り

- `docs/specs/cross-module-blame-spec.md`
  - `.claude/hooks/analyzers/` や `.claude/agents/*.md` 前提の hook 体系。
- `docs/specs/scalable-code-review.md`
  - `.claude/review-state/` など Claude 固有の永続化 path。
- `docs/specs/scalable-code-review-spec.md`
  - `.claude/commands/full-review.md` の Phase 0-5 前提の導入手順。

### 不採用候補

- `docs/specs/cross-module-blame-spec.md`
  - structured metadata を増やさず agent output marker だけで帰責を表す方針。
- `docs/specs/cross-module-blame-spec.md`
  - `parse_blame_hint()` のような Claude hook 解析関数の直移植。
- `docs/specs/scalable-code-review-phase5-spec.md`
  - 5 段階 full integration の丸ごと再現。まず部分採用が現実的。

## Specs 由来: Immune System / Security / Release / SSOT

### 採用候補

- `docs/specs/v4.0.0-immune-system-requirements.md`
  - 収束条件を先に定義してから loop や自動修正を回す設計は、暴走防止とコスト制御の土台になる。
- `docs/specs/v4.0.0-immune-system-requirements.md`
  - PG / SE / PM の権限等級で変更を段階分けする発想は、人間承認の粒度整理に使える。
- `docs/specs/gitleaks-integration-spec.md`
  - secret 検出を推奨ではなく pipeline gate にする考え方は、auditing gate へ再利用できる。
- `docs/specs/release-ops-revision.md`
  - プロジェクト種別に依存しない汎用 release flow への正規化は、framework 中立性を保ちやすい。
- `docs/specs/v3.9.0-improvement-adoption.md`
  - SSOT 3 層アーキテクチャは、`docs/internal/` と実行層の関係整理に使える。

### 後で判断

- `docs/specs/v4.0.0-immune-system-requirements.md`
  - MAGI / Three Agents / AoT を強く制度化する案は、便利だが運用負荷が高くなりうる。
- `docs/specs/v4.0.0-immune-system-requirements.md`
  - TDD 内省からルールを自動生成する案は魅力的だが、誤学習とルール肥大化の制御が必要。
- `docs/specs/v4.0.0-immune-system-requirements.md`
  - document auto-follow は有用だが、承認疲れ対策を先に検討する。
- `docs/specs/gitleaks-integration-spec.md`
  - `full-review` と `/ship` で異なる失敗扱いにする運用は、Codex の quality gate 設計と合わせて判断する。
- `docs/specs/release-ops-revision.md`
  - PATCH 定義拡張は、versioning rule 全体との整合確認が必要。

### Claude-only 寄り

- `docs/specs/v4.0.0-immune-system-requirements.md`
  - Stop hook や PreCompact 依存の収束制御。
- `docs/specs/v4.0.0-immune-system-requirements.md`
  - `settings.json` allow/deny と hook の二段構成。
- `docs/specs/magi-skill-spec.md`
  - `/magi` 起動や SKILL.md 参照前提の運用。
- `docs/specs/v3.9.0-improvement-adoption.md`
  - `.claude/commands/`、`.claude/rules/`、`.claude/agents/`、`.claude/skills/` 前提の配置。

### 不採用候補

- `docs/specs/v4.0.0-immune-system-requirements.md`
  - Agent Teams 常用や常時 multi-agent 通信。コストと複雑性が大きい。
- `docs/specs/magi-skill-spec.md`
  - MELCHIOR / BALTHASAR / CASPAR などの命名変更部分。設計知見というより branding 寄り。
- `docs/specs/gitleaks-integration-spec.md`
  - `review-config.json` による secret scan opt-out は gate 弱体化につながるため優先度低。
- `docs/specs/release-ops-revision.md`
  - Web service 前提の旧 release flow そのもの。

## 次の判断ステップ候補

この一次メモを読む判断エージェントまたは 5.5 reviewer は、次の観点で絞る。

1. Codex LAM に今すぐ入れるべき baseline。
2. Wave 2C の inventory で個別判断する項目。
3. Wave 3 以降または別 ADR に送る項目。
4. Claude-only として archive / deprecated に寄せる項目。
5. model cost を抑えるため、軽量モデルや CLI / static analysis に委譲できる項目。

