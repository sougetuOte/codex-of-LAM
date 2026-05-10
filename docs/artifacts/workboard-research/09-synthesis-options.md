# WORKBOARD Visualization Synthesis Decision

Status: Draft adoption judgment before implementation planning
Date: 2026-05-10

## Purpose

Batch 1-3 の harvest notes をもとに、`WORKBOARD.md` と generated dashboard の
初期 pilot 方針を固める。このファイルは実装仕様ではなく、PLANNING gate に進むための
採用判断メモである。

## Inputs

- `01-md-to-html-harvest.md`
- `02-codex-claude-context-harvest.md`
- `03-drift-generation-harvest.md`
- `04-agentic-kanban-harvest.md`
- `05-project-graph-harvest.md`
- `06-dashboard-ux-harvest.md`
- `07-traceability-harvest.md`
- `08-license-dependency-harvest.md`
- `2026-05-10-workboard-visualization-seed.md`
- `2026-05-10-magi-project-state-visibility.md`

## Stable Findings

### F1. `WORKBOARD.md` should be the state SSOT

`SESSION_STATE.md` は quick-load 用に薄く保つ。`WORKBOARD.md` は goal, workstreams,
cards, gates, dependencies, evidence を持つ project board とする。

### F2. Generated HTML / SVG should be views, not truth

HTML / SVG は認知負荷を下げるための presentation / review surface であり、
手編集しない。

### F3. Quick-load must stay light

quick-load は render しない。読むのは `SESSION_STATE.md` と `WORKBOARD.md` の
冒頭 dashboard まで。

### F4. Gate / release should force visibility

gate 前と release 前は validate + render を行い、人間が dashboard / graph を見る。

### F5. External tools are inspiration, not dependencies

Vibe Kanban, Task Master, mymir, Coddo, seite は参考になるが、初期 pilot では
primary dependency / SSOT にしない。

### F6. Workboard should support progressive drill-down

全体把握は dashboard / generated view で行い、詳細確認は `CARD-ID` または
workstream を明示してから行う。曖昧な「もっと詳しく」は全文再読ではなく、
関連 card detail と evidence links の提示に留める。

想定する深掘り順序は以下とする。

1. `SESSION_STATE.md`: 復帰用。次にやることだけを見る。
2. `WORKBOARD.md` 冒頭 dashboard: active card、blocked、gate、検証状態を見る。
3. `WORKBOARD.md` card table / workstream: 詳細を見る作業単位を選ぶ。
4. `WORKBOARD.md` card detail: `Goal`, `Context`, `DoD`, `Verification`,
   `Evidence`, `Next action` を読む。
5. linked docs: spec、ADR、tasks、artifacts は gate / review / 判断時だけ読む。

## Final Judgment

初期 pilot は **Option A: Minimal Native Workboard** を baseline とし、
**Option C: Task Graph Inspired Workboard** から以下だけを取り込む。

- progressive drill-down
- short card detail blocks
- explicit dependency / evidence links
- future `context CARD-ID` に転用できる card detail contract

採用する理由は、A が quick-load の軽さ、Windows / Codex App / template reuse、
Git 管理された Markdown SSOT を守りやすく、C の一部が「全体から必要な細部へ降りる」
体験を最小コストで補えるためである。

初期 pilot では、C の graph system / next-card automation / context bundle export までは
実装しない。これらは card microformat が安定してから後続 wave で判断する。

## Initial Pilot Baseline

### Files

- root `WORKBOARD.md`
- `tools/workboard.py`
- `docs/project/index.html`
- `docs/project/graph.svg`

### `WORKBOARD.md` Structure

1. Dashboard
2. Workstreams
3. Gate Matrix
4. Kanban / card table
5. Short card detail blocks
6. Dependency map

### Minimum Card Fields

Card table は一覧性を優先し、以下を最小 field とする。

- `ID`
- `Title`
- `Status`
- `Gate`
- `Workstream`
- `Next action`
- `Depends on`
- `Evidence`
- `Verification`
- `Blocker`

Card detail は、後で `tools/workboard.py context CARD-ID` に転用できるように、
以下の順序に揃える。

1. `Goal`
2. `Context`
3. `Definition of Done`
4. `Verification`
5. `Evidence`
6. `Next action`
7. `Blockers`

長い実行計画、議論ログ、検証ログは `WORKBOARD.md` に抱え込まず、
`docs/tasks/` または `docs/artifacts/` へ逃がす。

### Initial Validator Scope

`tools/workboard.py validate` の初期 warning set は以下までに絞る。

- duplicate card ID
- active card missing next action
- blocked card missing blocker reason
- dependency target missing
- evidence file missing
- `Done` / `Released` card missing verification

`spec -> card` trace、`touches` file path、commit / PR trace、impact analysis は後続 wave に回す。

### Initial Render Scope

`tools/workboard.py render` は、最初は presentation dashboard として扱う。

- `docs/project/index.html`: top band、workstream matrix、card board、detail links
- `docs/project/graph.svg`: workstream / active card 周辺の dependency overview

初期 pilot では rich SPA、drag-and-drop Kanban、interactive filtering、card 別 HTML、
GitHub Pages deploy は含めない。

### Generated Artifact Policy

初期 pilot では `docs/project/index.html` と `docs/project/graph.svg` を commit 対象候補とする。
ただし、stale truth 化を防ぐため、生成物には source path と generated marker を入れる。
source hash と CI drift check は後続 wave の判断対象にする。

### Workflow Contract

- quick-load: render しない。`SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard まで読む。
- quick-save: `WORKBOARD.md` が変わった場合は validate を検討する。重い render は必須にしない。
- gate 前: validate + render を行い、dashboard / graph を見る。
- release 前: validate + render を行い、tracked generated artifacts の diff を確認する。
- on-demand: ユーザーが全体把握を求めた時だけ render する。

## Option A: Minimal Native Workboard

### Shape

- root `WORKBOARD.md`
- `tools/workboard.py validate`
- `tools/workboard.py render`
- `docs/project/index.html`
- `docs/project/graph.svg`

### Data Model

- Markdown table based cards
- short card detail blocks for active / ready cards
- explicit dependency fields
- evidence file links
- no external parser unless needed

### Pros

- dependency-minimal
- Windows / Codex App / template reuse に強い
- quick-load が軽い
- 失敗しても Markdown が残る

### Cons

- parser / renderer を自作しすぎる危険
- rich docs site にはならない
- 初期 UX は控えめ

### Fit

Initial pilot の baseline として採用する。

## Option B: Markdown SSOT + MkDocs / mdBook View

### Shape

- `WORKBOARD.md`
- docs generator config
- generated site or Pages deployment
- graph / board は custom extension または pre-generated HTML/SVG

### Pros

- docs site として見やすい
- search / navigation が手に入る
- public template の見栄えが良い

### Cons

- tool config と build lifecycle が増える
- board / gate / traceability は結局 custom が必要
- quick-load とは別系統になる

### Fit

Public docs polish / later wave 向き。

## Option C: Task Graph Inspired Workboard

### Shape

- `WORKBOARD.md` の card + typed edge を強める
- `tools/workboard.py next CARD?`
- `tools/workboard.py context CARD-ID`
- local graph / traceability matrix を生成

### Pros

- mymir / Task Master RPG の強みを repo-native に取り込める
- Codex に渡す context bundle が作れる
- LAM の "Living" 感が強い

### Cons

- 初期仕様が重くなりやすい
- edge type を増やしすぎると手書き負担が上がる
- final design judgment が必要

### Fit

一部だけ初期 pilot に取り込む。`next` / `context` / traceability matrix は後続 wave 候補。

## Option D: External Tool Adapter

### Shape

- `WORKBOARD.md` は SSOT
- import/export adapter で Task Master / GitHub Projects / mymir-like JSON に出す
- Coddo / external Kanban は optional view

### Pros

- 外部 UI / automation を必要時だけ使える
- lock-in を避けやすい
- 将来の ecosystem 変化に対応しやすい

### Cons

- adapter maintenance cost
- data mapping の曖昧さ
- 初期 pilot には不要

### Fit

Later integration。初期 pilot では採用しない。

## Option E: Full Project Graph System

### Shape

- graph database または mymir-like server
- MCP tools
- browser UI
- task lifecycle agents

### Pros

- もっとも強力
- multi-agent / multi-session context retrieval に強い
- LAM の未来像としては魅力的

### Cons

- 依存が重い
- license / runtime / setup burden が大きい
- template starter から離れる
- Codex App on Windows の軽さと衝突する

### Fit

Research only。現時点では採用しない。

## Drill-Down Contract

初期 pilot では、`WORKBOARD.md` を「全体を見る board」だけでなく、
細部へ降りるための index として扱う。

### Initial Behavior

- quick-load: `SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard だけ読む。
- 全体把握: generated `docs/project/index.html` と `docs/project/graph.svg` を見る。
- もう少し詳しく: active `CARD-ID` があれば、その card detail を読む。
- active card が曖昧な場合: 候補 card を 2-3 個提示してから詳細へ降りる。
- gate / review / 高リスク判断: card detail の evidence links から linked docs を読む。

### Initial Card Detail Contract

各 card detail は、後で `tools/workboard.py context CARD-ID` に流用できるように、
以下の順序を基本にする。

1. `Goal`
2. `Context`
3. `Definition of Done`
4. `Verification`
5. `Evidence`
6. `Next action`
7. `Blockers`

長い実行計画、議論ログ、検証ログは card detail に抱え込まず、
`docs/tasks/` または `docs/artifacts/` へ逃がす。

### Deferred Tooling

`tools/workboard.py context CARD-ID`、card 別 HTML、interactive filtering は
初期 pilot には含めない。ただし、card detail の microformat は将来の
context bundle export を妨げない形にする。

## Cross-Cutting Design Decisions To Make Next

1. `WORKBOARD.md` は root に置く。
2. card fields の最小集合は `Initial Pilot Baseline` の `Minimum Card Fields` とする。
3. card detail は `WORKBOARD.md` 内に短く置き、長い実行計画は `docs/tasks/` へ逃がす。
4. edge type は初期には `depends_on` と evidence links に留める。
5. generated HTML / SVG は commit 対象候補とし、最終判断は実装 wave で deterministic 性を見て行う。
6. validator の初期 warning set は `Initial Validator Scope` とする。
7. render timing contract は `docs/internal/08_QUICK_LOAD_SAVE.md` または関連 workflow に反映する。
8. `tools/workboard.py context CARD-ID` は初期に含めない。
9. Mermaid は Markdown 内の補助表示に留め、Mermaid CLI は初期必須依存にしない。

## Implementation Wave Recommendation

最終考察の結論として、Option A を baseline とし、Option C の一部を
初期設計に混ぜる。

現時点では、Option C から初期に取り込むのは progressive drill-down と
card detail contract までに留めるのが安全そうである。`next` / `context` の
CLI 化は、card microformat が安定してから後続 wave で扱う。

最初の実装 wave は以下までに絞るのが安全そうである。

1. `WORKBOARD.md` initial template
   - dashboard
   - workstreams
   - card table
   - short card detail blocks
2. `tools/workboard.py validate`
3. `tools/workboard.py render`
4. `docs/project/index.html`
5. `docs/project/graph.svg`

`next` / `context` / card 別 HTML / CI drift check / external adapters は後続 wave 候補。
