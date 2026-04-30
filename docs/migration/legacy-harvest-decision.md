# 旧 docs 資産 採掘判断メモ

Status: Draft
Date: 2026-04-30

## 目的

`docs/migration/legacy-harvest-notes.md` の一次採掘結果を、
Codex LAM の計画へどう反映するかを判断する。

## 今すぐ baseline に入れる

- Green State / 完了判定の明確化
  - source: `docs/migration/codex-reusable-legacy-docs.md`, `docs/specs/green-state-definition.md`, `docs/specs/gitleaks-integration-spec.md`
  - 理由: Codex 側でも hook 依存なしで gate 条件へ直結でき、ADR-0005 の workflow discipline と executable checks に合う。
- read/write 権限の基本方針
  - source: `docs/adr/0004-bash-read-commands-allow-list.md`
  - 理由: read-only を広く許容し、破壊的操作だけ明示確認する方針は Codex-native harness の運用基盤として即効性が高い。
- upstream-first / 一次情報優先
  - source: `docs/adr/0003-context7-vs-webfetch.md`
  - 理由: 実装詳細ではなく判断原理なので、Codex の確認ルールへ落としやすい。
- spec / design / tasks / tests 同期と TDD の基本規律
  - source: `docs/internal/01_REQUIREMENT_MANAGEMENT.md`, `docs/internal/02_DEVELOPMENT_FLOW.md`, `docs/internal/03_QUALITY_STANDARDS.md`
  - 理由: すでに Codex LAM の planning / building discipline と整合しており、baseline 化の費用が低い。

## Wave 2C で個別判断

- 旧 docs 資産を棚卸し対象に含めること自体
  - source: `docs/migration/codex-reusable-legacy-docs.md`
  - 理由: 何を design / tasks / workflow に落とすかは項目別の選別が必要。
- Scalable Code Review の chunking / 依存グラフ / map-reduce review
  - source: `docs/migration/legacy-harvest-notes.md`
  - 理由: 有用性は高いが、最初から全部入れると過剰。
- TDD introspection の構造化ログ化
  - source: `docs/migration/legacy-harvest-notes.md`
  - 理由: 発想は再利用できるが、常時取得の重さと Codex での保存面を先に詰める。
- cross-module blame / dependency-aware review
  - source: `docs/migration/legacy-harvest-notes.md`
  - 理由: 補助情報としては強いが、標準レビュー手順に入れるかは運用コスト次第。
- multi-perspective decision making の運用形
  - source: `docs/specs/magi-skill-spec.md`
  - 理由: 観点分解は有用だが、routine 化するか任意 review に留めるかを分けて判断する。

## Wave 2C 後半の判断結果

### scalable review

- 結論: `codex_reexpress`
- 扱い: Claude `/full-review` の自動 loop / hook / analyzer pipeline は直移植しない。
- 今回反映する最小単位:
  - Codex-native の `AUDITING` で使える review 原理として整理する
  - 全体再レビュー原則、規模に応じた review 深度切り替え、Green State 明示を残す
- 後続 wave へ送るもの:
  - AST chunking
  - map-reduce review
  - dependency graph 駆動 review
  - impact analysis

### TDD introspection

- 結論: `codex_reexpress`
- 扱い: BUILDING の必須 gate にはせず、Claude `PostToolUse` 非依存の optional helper candidate として扱う。
- 今回反映する最小単位:
  - Red / Green / Refactor と focused test を報告する規律を維持する
  - retro 用の入力を集める補助としての価値を記録する
- Wave 2C の追加判断:
  - `docs/specs/feat-tdd-introspection-helper.md` を最小 spec として追加する
- 後続 wave へ送るもの:
  - CLI / pytest helper の実装
  - 構造化ログ収集
  - 自動評価ループ

### permission / security

- 結論: `codex_reexpress`
- 扱い: read/write 権限方針と PG/SE/PM の判断原理は採用するが、
  Wave 2C では standalone validator 化しない。
- 今回反映する最小単位:
  - `AGENTS.md` と internal docs へ運用ルールとして残す
  - migration notes に defer を明記する
- 後続 wave へ送るもの:
  - validator 実装の要否判断

### cross-module blame

- 結論: `codex_reexpress`
- 扱い: 自動修正機構にはせず、`AUDITING` での帰責判断支援に限定する。
- 今回反映する最小単位:
  - `spec ambiguity`
  - `upstream/downstream`
  - 契約違反の判断原理
- 後続 wave へ送るもの:
  - blame marker
  - parser
  - report integration
  - contract card

### multi-perspective decision

- 結論:
  - MAGI は `codex_reexpress`
  - `lam-orchestrate` は `codex_reexpress`
  - Claude runtime glue は `archive_runtime_specific`
- 扱い:
  - MAGI は trigger-based decision protocol として残す
  - `lam-orchestrate` は自動 multi-agent 常用ではなく、多ファイル作業の decomposition guidance として再表現する
- 今回反映する最小単位:
  - `docs/internal/06_DECISION_MAKING.md` を SSOT とみなす
  - routine 化しない方針を migration notes と tasks に残す
- 後続 wave へ送るもの:
  - anchor file の常時生成
  - runtime state 連携
  - 自動 orchestration

## Wave 3 以降または別 ADR へ送る

- モデル選定・モデルルーティングの詳細制度化
  - source: `docs/adr/0001-model-routing-strategy.md`
  - 理由: 原理はよいが、現行 Codex のモデル事情に依存しやすく、別 ADR で寿命管理したほうが安全。
- KPI / loop-log schema / 定量評価基盤
  - source: `docs/specs/evaluation-kpi.md`, `docs/specs/loop-log-schema.md`
  - 理由: baseline 前に入れるには重く、まず harness を安定させてから測定系を設計する。
- immune-system 系の高度な自動収束制御
  - source: `docs/specs/v4.0.0-immune-system-requirements.md`
  - 理由: 収束条件の思想は使えるが、自動ルール生成や高度制度化は別 ADR レベルの論点。
- release flow の汎用化詳細
  - source: `docs/specs/release-ops-revision.md`
  - 理由: 今回の Codex-native harness 置換より後段の運用設計。

## Claude-only / archive 寄り

- hook / slash command / subagent runtime 前提の具体実装
  - source: `docs/migration/legacy-harvest-notes.md`
  - 理由: 直移植しない方針と ADR-0005 の決定に一致する。
- `.claude/settings.json` や `permissions.allow` 書式そのもの
  - source: `docs/adr/0004-bash-read-commands-allow-list.md`
  - 理由: 方針は再利用できるが、書式と enforcement は Claude harness 固有。
- Stop / PreToolUse / PostToolUse / PreCompact 依存の制御
  - source: `docs/design/v4.0.0-immune-system-design.md`
  - 理由: Codex に同型 runtime がなく、実装単位では archive 側へ寄せる。
- Agent Teams 常用や Claude 実験機能前提
  - source: `docs/design/lam-orchestrate-design.md`
  - 理由: 設計知見より runtime glue の比重が大きい。

## ADR-0005 への影響

ADR-0005 の承認前に大きな追記は不要。

ADR-0005 はすでに `.claude/` を legacy input として扱い、Wave 2 で棚卸しし、各 agent / subagent を個別確認する方針を示している。
今回の軽量採掘結果は、その決定を補強する材料であり、決定本体を変えるものではない。

ただし、Wave 2 の棚卸し対象に旧 `docs/` 資産も含めることは ADR に一文足す価値がある。
詳細分類は ADR ではなく、migration notes、design、tasks 側へ置く。
