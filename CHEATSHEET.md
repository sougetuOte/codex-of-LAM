# Living Architect Model チートシート

## はじめに

> まず [概念説明スライド](docs/slides/index.html) で全体像を掴み、[クイックスタート](QUICKSTART.md) で最初の導入を行う。

1. Codex App で repo を開く
2. `AGENTS.md` と、存在する場合は `SESSION_STATE.md` を読んで quick-load
3. `.codex/current-phase.md` の phase に従って進める

fresh repo では `SESSION_STATE.md` がまだないのが通常。ない場合は新規プロジェクトとして PLANNING から始める。

```text
典型的な流れ:
  PLANNING -> 要件定義 -> [承認] -> 設計 -> [承認] -> タスク分解 -> [承認]
  BUILDING -> TDD実装（Red -> Green -> Refactor）-> [承認]
  AUDITING -> 品質監査 -> [承認] -> 完了
```

## ディレクトリ構造

```text
AGENTS.md                  # Codex 用の憲法
.codex/
├── current-phase.md       # 現在のフェーズ
└── workflows/             # Codex-native workflow

.agents/skills/            # Codex App project skill 候補
docs/internal/             # プロセス SSOT
docs/specs/                # 仕様書
docs/adr/                  # ADR
docs/tasks/                # タスク
SESSION_STATE.md           # local handoff（Git 管理外。quick-save 後に作成）
docs/migration/            # legacy 資料の扱いと archive / delete gate
```

## フェーズ

| Phase | 用途 | 主な成果物 |
|------|------|-----------|
| PLANNING | 要件、ADR、設計、タスク | Markdown artifacts |
| BUILDING | t-wada style TDD 実装 | tests / production code |
| AUDITING | レビュー、監査、回帰確認 | findings / fixes |

承認ゲート:

```text
requirements -> design -> tasks -> building -> auditing
```

## セッション管理

| 操作 | 用途 | 入口 |
|------|------|------|
| quick-load | 最小復帰 | `.agents/skills/quick-load/SKILL.md` |
| quick-save | 短い引き継ぎ保存 | `.agents/skills/quick-save/SKILL.md` |
| commit / push | 配布・共有 | 通常の Git 操作 |

quick-save は `SESSION_STATE.md` を短く保つ。長い履歴、環境メモ、調査ログは `docs/daily/` や `docs/artifacts/` に逃がす。

## Codex App での作業単位

| 機能 | 使いどころ |
|------|------------|
| commentary updates | 作業中の短い進捗共有 |
| plans | 複数 step の進行管理 |
| subagents | 並列可能な read-only 調査や disjoint write 作業 |
| review pane | 差分確認、指摘、修正判断 |
| in-app browser | localhost / slides / UI の確認 |
| automations | 継続監視や後続リマインド |

## モデル運用

| 用途 | モデル方針 |
|------|------------|
| 通常判断・実装 | GPT-5.4 |
| read-only 採掘、単純分類 | 5.3 系 |
| 大きな corpus | context-harvest で前処理 |
| 不可逆・高リスク判断 | GPT-5.5 |
| 大きめのレビュー | context-harvest + magi + review pane + focused verification |

判断は Gatekeeper が保持する。worker には証拠収集、機械的更新、disjoint な実装を渡す。

## スキル

| スキル | 用途 |
|--------|------|
| `quick-load` | 省コンテキスト復帰 |
| `quick-save` | 軽量 handoff 更新 |
| `context-harvest` | 大 corpus の read-only 採掘 |
| `lam-orchestrate` | 複数ファイル作業の分解と並列化 |
| `magi` | 複雑な意思決定 |
| `clarify` | 文書の曖昧さ・矛盾・欠落確認 |
| `spec-template` | 仕様書作成 |
| `adr-template` | ADR 作成 |

Codex hooks は optional advanced path。旧 `full-review` は戻さず、将来の Codex-native pilot 候補として扱う。

## 参照ドキュメント

| ファイル | 内容 |
|---------|------|
| `docs/internal/00_PROJECT_STRUCTURE.md` | 構成・命名・状態管理 |
| `docs/internal/01_REQUIREMENT_MANAGEMENT.md` | 要件定義 |
| `docs/internal/02_DEVELOPMENT_FLOW.md` | 開発フロー・TDD |
| `docs/internal/03_QUALITY_STANDARDS.md` | 品質基準 |
| `docs/internal/04_RELEASE_OPS.md` | リリース・緊急対応 |
| `docs/internal/05_MCP_INTEGRATION.md` | MCP / MEMORY 運用 |
| `docs/internal/06_DECISION_MAKING.md` | MAGI / AoT / Reflection |
| `docs/internal/07_SECURITY_AND_AUTOMATION.md` | コマンド安全基準 |
| `docs/internal/08_QUICK_LOAD_SAVE.md` | quick-load/save |
| `docs/internal/09_MODEL_AND_CONTEXT_POLICY.md` | モデル・文脈運用 |
| `docs/internal/10_DISTRIBUTION_MODEL.md` | 配布モデル |

## クイックリファレンス

**再開したい**
`quick-load`。`SESSION_STATE.md` があれば最小確認 bundle、なければ新規プロジェクトとして開始。

**中断したい**
`quick-save`。`SESSION_STATE.md` は短く、長文は別ファイル。

**実装したい**
BUILDING。承認済み task を最小単位で Red-Green-Refactor。

**レビューしたい**
AUDITING。findings を先頭に、検証結果と残リスクを明示。

**迷った**
phase、requirements、design、tasks、code/tests の順で truth hierarchy を確認。
