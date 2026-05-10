# Project Graph / Knowledge Graph Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`WORKBOARD.md` と関連 Markdown を、単なる task list ではなく、仕様・ADR・タスク・
検証・実装の関係を見える化する project graph として扱うための材料を集める。

## Harvest Policy

- Agentic engineering の project graph と、Markdown knowledge base の graph の両方を見る。
- 採用候補は repo-native Markdown / static HTML / SVG に落とせるものを優先する。
- Graph は「美しい全体像」より「次の判断が速くなる関係」を重視する。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| mymir | https://mymir.dev/ | tasks, decisions, dependencies, execution records を project graph として管理する agentic PM tool。 |
| Obsidian Graph View | https://obsidian.md/help/plugins/graph | note を node、internal link を edge として可視化する。 |
| Obsidian Links | https://obsidian.md/help/link-notes | backlinks / local graph / wikilinks の考え方。 |
| Foam Graph View | https://docs.foamnotes.com/features/graph-view/ | Markdown files / tags を graph node として表示。named views / group filters がある。 |
| Foam Wikilinks | https://docs.foamnotes.com/features/wikilinks | wikilinks, placeholders, section links, Markdown compatibility。 |
| Foam Janitor | https://docs.swo.moe/foam-1/workspace-janitor | Markdown link health を保つ janitor / hook / GitHub Action の発想。 |
| Task Master RPG | https://docs.task-master.dev/capabilities/rpg-method | dependency-aware task graph と topological ordering。 |

## Findings

### mymir context network

- tasks, specs, acceptance criteria, status lifecycle, typed dependency edges,
  decisions, execution records, file paths を graph にする。
- agent には lifecycle stage に応じて compact context block を渡す。
- Structure view と Graph view の二面がある。
- AGPL v3 / Postgres / Bun / self-hosted なので、直接取り込みは重い。

Classification: `adopt_candidate` for concept, `reject_candidate` for direct embedding

### mymir context retrieval

- agent が毎回全体を読むのではなく、task stage に応じた context bundle を受け取る。
- LAM の quick-load と相性がよい。
- `WORKBOARD.md` の card から linked evidence を選んで渡す仕組みの参考になる。

Classification: `adopt_candidate`

### Obsidian graph / local graph

- note 間 link を graph として見せる。
- global graph は全体理解、local graph は現在 note 周辺の理解に向く。
- LAM では global graph より、active card 周辺の local dependency graph が有効。
- 方向や typed edge は Obsidian 標準 link だけでは弱い。

Classification: `adopt_candidate` for local graph idea

### Foam graph / named views

- files, tags, placeholders を node にし、links を edge にする。
- group / color / named views で graph を用途別に切り替えられる。
- LAM でも `view=gate`, `view=workstream`, `view=active-card` のような生成 view が有効。

Classification: `adopt_candidate`

### Foam wikilinks / placeholders

- 存在しない note への link を placeholder として扱える。
- LAM では未作成 spec / task / ADR を "planned artifact" として graph に出せる可能性がある。
- 標準 Markdown compatibility を保つため、wikilink は慎重。

Classification: `decide_later`

### Foam janitor

- Markdown graph は link health を保つ補助ツールが必要。
- LAM でも `tools/workboard.py validate` は card ID だけでなく、linked files の存在、
  orphaned card、missing evidence を検査するべき。

Classification: `adopt_candidate`

### Task Master RPG

- dependency graph と topological ordering を PRD / task decomposition に組み込む。
- LAM の graph は自然言語 link graph だけでなく、explicit edge table を持つべき。

Classification: `adopt_candidate`

## Edge Types Candidate

`WORKBOARD.md` で最初から edge type を持つと、あとで graph / next-card が強くなる。

| Edge | Meaning |
| --- | --- |
| `depends_on` | この card の開始に必要 |
| `blocks` | この card が終わるまで止まるもの |
| `relates_to` | 判断時に参照するが順序制約ではない |
| `supersedes` | 古い判断・card を置き換える |
| `evidenced_by` | 検証・調査・artifact への根拠 link |
| `implements` | spec / ADR を実装する |
| `verifies` | test / review が requirement を検証する |

## Combination Ideas

### C1: Explicit Edge Table + Markdown Links

Markdown links だけに頼らず、`WORKBOARD.md` に edge table を持つ。

- typed edge: graph / next-card / validation 用
- normal links: human navigation 用

### C2: Global + Local Graph

generated SVG / HTML では二種類の graph を作る。

- Global: workstream / gate / active cards の全体像
- Local: active card 周辺の depends_on / blocks / evidence

### C3: Planned Artifact Nodes

まだ存在しない spec / task / ADR を planned node として表示する。

- 良い点: 欠落が見える。
- リスク: phantom docs が増える。

初期 pilot では `missing linked file` warning に留めるのが無難。

### C4: Context Bundle Export

`tools/workboard.py context CARD-ID` で、active card に必要な compact context を出す。

材料:

- card
- upstream decisions
- evidence files
- related specs / ADR / tasks
- known blockers

## Adoption Candidates

- Baseline now:
  - `WORKBOARD.md` に explicit dependency / evidence links を持つ。
  - generated graph は active card 周辺を重視する。
  - validator は missing link / missing evidence / orphaned active card を見る。

- Next wave:
  - `tools/workboard.py context CARD-ID`。
  - typed edge table。
  - global / local graph の二種類生成。

- Reject for initial pilot:
  - graph database。
  - wikilink 前提。
  - mymir の直接取り込み。

## Open Questions

- edge table は card table 内に持つか、別セクションに切るか。
- Markdown standard link と wikilink のどちらを採用するか。
- `evidenced_by` を card field にするか、edge type にするか。
- graph SVG は階層レイアウトで足りるか、force-directed view が必要か。
