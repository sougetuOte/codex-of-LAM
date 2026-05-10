# WORKBOARD Visualization Synthesis Options

Status: Draft options before final judgment
Date: 2026-05-10

## Purpose

Batch 1-3 の harvest notes をもとに、次セッションで最終考察するための複数案を
まとめる。このファイルは採用決定ではない。

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

## Option A: Minimal Native Workboard

### Shape

- root `WORKBOARD.md`
- `tools/workboard.py validate`
- `tools/workboard.py render`
- `docs/project/index.html`
- `docs/project/graph.svg`

### Data Model

- Markdown table based cards
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

Initial pilot の第一候補。

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

Option A の次段階。最終形候補。

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

Later integration。今は採用しない。

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

## Cross-Cutting Design Decisions To Make Next

1. `WORKBOARD.md` を root に置くか `docs/project/WORKBOARD.md` に置くか。
2. card fields の最小集合。
3. edge type の最小集合。
4. generated HTML / SVG を commit 対象にするか。
5. validator の初期 warning set。
6. render timing contract をどの workflow doc に書くか。
7. `tools/workboard.py context CARD-ID` を初期に含めるか。
8. Mermaid を source として使うか、補助表示に留めるか。

## Lightweight Recommendation Before Final Review

次セッションの最終考察では、Option A を baseline とし、Option C の一部を
初期設計に混ぜるかを重点的に判断する。

最初の実装 wave は以下までに絞るのが安全そうである。

1. `WORKBOARD.md` initial template
2. `tools/workboard.py validate`
3. `tools/workboard.py render`
4. `docs/project/index.html`
5. `docs/project/graph.svg`

`next` / `context` / CI drift check / external adapters は後続 wave 候補。
