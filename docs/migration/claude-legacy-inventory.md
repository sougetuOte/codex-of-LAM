# Claude legacy inventory

Status: Draft
Date: 2026-04-30

## 目的

`.claude/` 配下の legacy Claude material と、旧 `docs/` 資産のうち
Codex へ再利用できるものを棚卸しし、移設方針を review 可能な形で残す。

この文書は「何を残し、何を移し、何を archive 寄りにするか」の地図である。
ここでは family 単位の分類を先に行い、実装や細部の再設計は必要な wave へ送る。

## 分類ラベル

- `codex_adopted`
  - すでに Codex 側へ反映済み、または反映先が明確
- `codex_reexpress`
  - 原理は有用。Codex-native workflow / docs / CLI / pytest helper として再表現する
- `decide_later`
  - 有用性は高いが、導入コストや適用範囲を Wave 2C 後半以降で判断する
- `archive_runtime_specific`
  - Claude runtime や hook / slash command / subagent frontmatter に強く依存し、直移植しない

## `.claude/commands/`

| Family | 代表ファイル | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| phase entry | `.claude/commands/planning.md`, `building.md`, `auditing.md` | `codex_adopted` | `.codex/workflows/` と `AGENTS.md` に役割を移した |
| quick handoff | `.claude/commands/quick-load.md`, `quick-save.md` | `codex_adopted` | `SESSION_STATE.md` と `docs/internal/08_QUICK_LOAD_SAVE.md` に手動 workflow として移した |
| status / planning assist | `.claude/commands/project-status.md`, `wave-plan.md` | `codex_reexpress` | tasks / `SESSION_STATE.md` / commentary updates へ再表現する |
| review / retrospective | `.claude/commands/full-review.md`, `pattern-review.md`, `retro.md` | `decide_later` | scalable review / TDD introspection / audit procedure として分解して判断する |
| release / commit assist | `.claude/commands/ship.md` | `decide_later` | release flow / Git 運用として別途整理する |

### メモ

- `/quick-load` と `/quick-save` の核心はすでに Codex 側へ移した。
- `/full-review` は発想は有用だが、Claude hook と subagent 自動運用への依存が強く、そのままは持ち込まない。

## `.claude/hooks/`

| Family | 代表ファイル | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| permission gate | `.claude/hooks/pre-tool-use.py` | `codex_reexpress` | read/write 権限方針として運用ルールへ残し、必要なら standalone validator を検討する |
| TDD / doc sync / loop logging | `.claude/hooks/post-tool-use.py` | `decide_later` | TDD introspection、doc sync、loop log を個別に分けて判断する |
| stop / pre-compact automation | `.claude/hooks/lam-stop-hook.py`, `pre-compact.py` | `archive_runtime_specific` | Claude event loop 依存が強いため直移植しない |
| analyzers pipeline | `.claude/hooks/analyzers/` | `decide_later` | scalable review、chunking、dependency-aware review の素材として再利用可否を判断する |
| hook test suite | `.claude/hooks/tests/` | `archive_runtime_specific` | Claude hook 契約のテストなので、そのままは持ち込まない |
| shared utils | `.claude/hooks/_hook_utils.py` | `archive_runtime_specific` | hook 入出力前提の utility なので archive 寄り |

### メモ

- hook の「自動介入」自体は archive 寄り。
- ただし permission policy、TDD signal、dependency-aware review は判断原理として価値がある。

## `.claude/agents/`

| Family | 代表ファイル | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| implementation role | `.claude/agents/tdd-developer.md`, `test-runner.md` | `codex_reexpress` | BUILDING workflow、task 粒度、test discipline として文書化する |
| planning role | `.claude/agents/requirement-analyst.md`, `design-architect.md`, `task-decomposer.md`, `doc-writer.md` | `codex_reexpress` | spec / ADR / design / tasks の review 観点と作業手順へ移す |
| review role | `.claude/agents/code-reviewer.md`, `quality-auditor.md` | `codex_reexpress` | AUDITING procedure、review checklist、finding style へ移す |
| frontmatter / model / tool declarations | 全 agent file の metadata | `archive_runtime_specific` | Claude subagent runtime の制御面としては持ち込まない |

### メモ

- agent の人格や起動形式ではなく、役割別の review 観点と手順だけを持ってくる。
- これは requirements / design / tasks で決めた「一律変換しない」方針に一致する。

### Item-by-item confirmation

| Legacy item | 分類 | Codex での反映先 | 理由 |
| --- | --- | --- | --- |
| `.claude/agents/tdd-developer.md` | `codex_reexpress` | `.codex/workflows/building.md` | TDD 手順、pre-flight、Red/Green/Refactor 報告は有用だが、subagent frontmatter は不要 |
| `.claude/agents/test-runner.md` | `codex_reexpress` | `.codex/workflows/building.md` | focused test 実行と失敗要約の手順だけを残せば足りる |
| `.claude/agents/code-reviewer.md` | `codex_reexpress` | `.codex/workflows/auditing.md` | severity-first review、品質/セキュリティ/整合性の観点はそのまま使える |
| `.claude/agents/quality-auditor.md` | `codex_reexpress` | `.codex/workflows/auditing.md` | 仕様ドリフト、構造整合性、帰責判断支援を audit procedure に再表現する |
| `.claude/agents/requirement-analyst.md` | `codex_reexpress` | `.codex/workflows/planning.md` | 曖昧さ解消、受け入れ条件、DoR 観点が planning に有用 |
| `.claude/agents/design-architect.md` | `codex_reexpress` | `.codex/workflows/planning.md` | 最小設計、trade-off、ADR 候補整理を planning guidance に移す |
| `.claude/agents/task-decomposer.md` | `codex_reexpress` | `.codex/workflows/planning.md` | 1 review / 1 PR 粒度、依存整理、検証可能性を task generation guidance に移す |
| `.claude/agents/doc-writer.md` | `codex_reexpress` | `.codex/workflows/planning.md` | spec / ADR / design / tasks の SSOT discipline として使う |
| frontmatter `permission-level`, `model`, `tools` | `archive_runtime_specific` | `docs/migration/claude-to-codex-migration-notes.md` | Claude subagent runtime 制御面なので Codex の canonical contract にはしない |

## `.claude/settings.json`

| Item | 分類 | Codex での扱い |
| --- | --- | --- |
| `permissions.allow/deny/ask` の思想 | `codex_reexpress` | read-only を広く許容し、破壊的操作だけ明示確認する運用ルールへ残す |
| hook registration | `archive_runtime_specific` | Codex に同型 runtime がないため直移植しない |
| Claude permission pattern 文字列 | `archive_runtime_specific` | Codex の実際の権限モデルに読み替える |

### メモ

- 書式は持ち込まない。
- policy だけを Codex 側の review / escalation discipline として残す。

## `.claude/rules/`

| Family | 代表ファイル | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| identity / phase | `core-identity.md`, `phase-rules.md` | `codex_adopted` | `AGENTS.md` と `.codex/workflows/` に移した |
| upstream-first | `upstream-first.md` | `codex_adopted` | すでに Codex 側の作業原則として採用済み |
| permission / security | `permission-levels.md`, `security-commands.md` | `codex_reexpress` | baseline 候補。運用ルールと validator 候補へ分離する |
| planning / quality guideline | `planning-quality-guideline.md`, `code-quality-guideline.md` | `codex_reexpress` | planning / building / auditing の checklist として取り込む |
| decision making | `decision-making.md` | `decide_later` | MAGI / multi-perspective review の扱いを Wave 2C 後半で判断する |
| test result output | `test-result-output.md` | `decide_later` | TDD introspection / report format の一部として判断する |
| auto-generated trust model | `.claude/rules/auto-generated/trust-model.md` | `archive_runtime_specific` | Claude 自動生成ルールとしては持ち込まない |

## `.claude/skills/`

| Family | 代表ファイル | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| templates / clarify | `adr-template`, `spec-template`, `clarify`, `ui-design-guide`, `skill-creator` | `codex_adopted` | repo-local skill / user skill としてすでに同等物がある、または作成済み |
| decision skill | `magi` | `decide_later` | 思考フレームとしては有用。routine 化の強さを後で決める |
| orchestration skill | `lam-orchestrate` | `decide_later` | 多ファイル作業分解の思想は有用だが、自動 multi-agent 常用は避ける |

### メモ

- skill の中でも「文書テンプレート系」は比較的移しやすい。
- 自動 orchestration や Claude runtime 前提の運用は薄めて持つ。

## `.claude/states/` と runtime state files

| Family | 代表ファイル | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| feature state snapshots | `.claude/states/*.json` | `archive_runtime_specific` | 過去 feature の状態記録として参照のみ |
| current phase | `.claude/current-phase.md` | `codex_adopted` | `.codex/current-phase.md` へ移した |
| loop state / test result / logs | `.claude/lam-loop-state.json.bak`, `.claude/test-results.xml`, `.claude/logs/` | `archive_runtime_specific` | Codex 運用で必要なら別形式で再設計する |
| agent memory | `.claude/agent-memory/` | `archive_runtime_specific` | Claude subagent 運用の副産物として参照のみ |

## 旧 `docs/` 資産

| Theme | 入口 | 分類 | Codex での扱い |
| --- | --- | --- | --- |
| baseline now | `docs/migration/legacy-harvest-decision.md` の Green State / read-write / upstream-first / spec-design-tasks-tests sync | `codex_reexpress` | AGENTS / internal docs / workflow / validator 候補へ段階反映する |
| scalable review | `docs/specs/scalable-code-review*.md`, `docs/design/scalable-code-review-design.md` | `decide_later` | review procedure / helper / audit wave 候補 |
| TDD introspection | `docs/specs/tdd-introspection-v2.md` | `decide_later` | CLI / pytest helper / report format 候補 |
| cross-module blame | `docs/specs/cross-module-blame-spec.md`, `docs/design/cross-module-blame-design.md` | `decide_later` | dependency-aware review 補助として検討 |
| model routing / KPI / immune system automation | 関連 ADR / spec / design | `archive_runtime_specific` と `decide_later` の混在 | 原理だけ残し、制度化は別 ADR か後続 wave へ送る |

### Reusable idea mapping

| Reusable idea | 反映先 | 今回の扱い |
| --- | --- | --- |
| Green State / 完了判定 | `.codex/workflows/building.md`, `.codex/workflows/auditing.md`, `AGENTS.md` | 反映済み |
| read/write 権限方針 | `AGENTS.md`, `docs/internal/07_SECURITY_AND_AUTOMATION.md`, migration notes | 原理は採用、Claude settings 書式は不採用 |
| `requirement-analyst` / `design-architect` / `task-decomposer` / `doc-writer` の観点 | `.codex/workflows/planning.md` | 反映済み |
| `tdd-developer` / `test-runner` の観点 | `.codex/workflows/building.md` | 反映済み |
| `code-reviewer` / `quality-auditor` の観点 | `.codex/workflows/auditing.md` | 反映済み |
| TDD introspection | CLI / pytest helper candidate | spec は追加し、実装判断は後続 |
| permission-level classification | migration notes / 将来の validator 候補 | Wave 2C では helper 化せず defer を確定 |
| scalable review / cross-module blame | audit procedure / review checklist | 原理だけ反映、自動 pipeline は不採用 |

## 今回の判断

### すでに Codex 側へ移したもの

- phase workflow
- quick-load / quick-save の手動運用
- `.claude/current-phase.md` の役割
- upstream-first の判断原理

### Wave 2C 後半で判断したもの

- permission-level classification は standalone validator にせず、workflow guidance と migration notes に留める
- TDD introspection は optional helper candidate として spec を追加し、実装タイミングは後続 wave で判断する
- scalable review の review 原理をどの review checklist / auditing procedure へ落とすか
- cross-module blame の判断原理をどの review checklist / auditing procedure へ落とすか
- `lam-orchestrate` の decomposition guidance をどの task generation guidance へ落とすか

### 今回は移設しないものと理由

| Legacy item | 分類 | 理由 |
| --- | --- | --- |
| `.claude/hooks/lam-stop-hook.py`, `pre-compact.py` | `archive_runtime_specific` | Claude event loop 前提で、Codex には同型ランタイムがない |
| `.claude/hooks/post-tool-use.py` の常時自動記録 | `decide_later` | TDD introspection / doc sync の原理は有用だが、保存面とコスト設計が未確定 |
| `.claude/hooks/analyzers/` | `decide_later` | scalable review の素材ではあるが、最初から自動 pipeline にすると過剰 |
| `.claude/settings.json` の `permissions.allow/deny/ask` 書式 | `archive_runtime_specific` | Codex の権限モデルと一致しないため、方針だけ再利用する |
| slash command frontmatter | `archive_runtime_specific` | command loader 契約が Claude 専用 |
| subagent frontmatter | `archive_runtime_specific` | Codex では role guidance へ変換し、runtime metadata は残さない |

### archive 寄りのもの

- hook registration と event-driven automation
- Claude slash command frontmatter
- Claude subagent frontmatter と model/tool declaration
- `.claude/states/`、`agent-memory/`、loop state などの runtime residue

## 4論点の統合結論

### scalable review

- 分類: `codex_reexpress`
- この wave の結論:
  - Codex-native `AUDITING` で使う review 原理として扱う
  - 自動 review pipeline としては実装しない
- archive / defer:
  - hook loop
  - analyzer 連鎖
  - AST chunking
  - map-reduce review
  - dependency graph 駆動 review

### TDD introspection

- 分類: `codex_reexpress`
- この wave の結論:
  - BUILDING の必須 gate にはしない
  - Claude `PostToolUse` 非依存の optional helper candidate として残す
- archive / defer:
  - hook 主導の常時ログ化
  - Claude payload 前提の自動収集
  - rules 自動生成ループ

### cross-module blame

- 分類: `codex_reexpress`
- この wave の結論:
  - `AUDITING` における帰責判断支援として再表現する
  - 修正先の自動決定や専用 feature 化はしない
- archive / defer:
  - blame marker
  - parser
  - contract card
  - report integration

### multi-perspective decision

- 分類:
  - MAGI: `codex_reexpress`
  - `lam-orchestrate`: `codex_reexpress`
  - Claude runtime glue: `archive_runtime_specific`
- この wave の結論:
  - MAGI は trigger-based decision protocol として残す
  - `lam-orchestrate` は多ファイル作業の decomposition guidance として再表現する
  - 常用 routine や runtime state 管理としては持ち込まない

## 次の反映先

- `AGENTS.md`
  - read/write 権限の原則
  - quality / review 観点の baseline
- `docs/internal/`
  - permission / quality / decision-making の Codex-native 運用書
- `docs/tasks/codex-lam-replacement-tasks.md`
  - Wave 2C 後半の個別判断タスク
- 必要なら別 ADR
  - scalable review
  - TDD introspection
  - stronger model routing policy

## baseline 候補の反映先決定

| Candidate | Artifact |
| --- | --- |
| Green State / 完了判定 | `.codex/workflows/building.md`, `.codex/workflows/auditing.md`, `AGENTS.md` |
| read/write 権限の基本方針 | `AGENTS.md` |
| upstream-first / 一次情報優先 | `.codex/constitution.md`, `AGENTS.md` |
| spec / design / tasks / tests 同期 | 既存の `AGENTS.md`, `.codex/constitution.md`, BUILDING/AUDITING workflow を維持 |
