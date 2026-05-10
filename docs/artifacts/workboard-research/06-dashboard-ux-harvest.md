# Dashboard UX Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`docs/project/index.html` や generated SVG が、人間の認知負荷を本当に下げるようにする
ため、dashboard / card / board UX の基本原則を集める。

## Harvest Policy

- 「見た目の豪華さ」ではなく、判断速度、scan しやすさ、blocker 発見を重視する。
- Static HTML で実装できる原則を優先する。
- LAM の quick-load / gate review / release review に合う情報密度を探す。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| GitHub Projects layouts | https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view | table / board / roadmap の使い分け。 |
| GitHub Projects quickstart | https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects | fields, grouping, board, roadmap, charts。 |
| Atlassian Kanban boards | https://www.atlassian.com/agile/kanban/boards | visual signals, columns, WIP limits, blockers。 |
| Carbon Dashboards | https://v10.carbondesignsystem.com/data-visualization/dashboards/ | presentation dashboard / exploration dashboard の区別、hierarchy、metric 制限。 |
| IBM Data Visualization Overview | https://www.ibm.com/design/language/data-visualization/overview/ | understandable, essential, impactful, consistent, contextual。 |
| IBM Data Visualization Basics | https://www.ibm.com/design/language/data-visualization/design/basics | overview first, zoom/filter, details on demand。 |
| Microsoft Viva dashboard cards | https://learn.microsoft.com/en-us/sharepoint/dev/spfx/viva/design/designing-card | card anatomy, title/header/body/footer, card interaction。 |
| Baymard dashboard cards | https://baymard.com/blog/cards-dashboard-layout | dashboard cards は一貫性がないと scan しにくい、という usability finding。 |

## Findings

### GitHub Projects view model

- Table は高密度、Board は workflow、Roadmap は time / milestone という使い分けが明確。
- LAM generated dashboard も一画面に全部詰めるより、view を分ける方がよい。
- Static HTML では tabs / sections で近い体験を作れる。

Classification: `adopt_candidate`

### Atlassian Kanban UX

- card, columns, WIP limits, blockers が board の基本。
- WIP limits は bottleneck と overload を見つける視覚 signal。
- LAM の dashboard でも `Doing > 1` や `Blocked exists` は強調表示する価値がある。

Classification: `adopt_candidate`

### Carbon dashboards

- Presentation dashboard と Exploration dashboard を分ける視点が有効。
- Presentation: current status / big picture / most important data。
- Exploration: search, sort, filter, drill-down。
- 初期 LAM は Presentation dashboard を優先し、探索は link navigation で十分。

Classification: `adopt_candidate`

### IBM data visualization

- data visualization は understandable, essential, impactful, consistent, contextual であるべき。
- LAM dashboard では「重要でない情報を削る」「一貫した色」「文脈に合う粒度」が重要。
- 方向性として、グラフを派手にするより判断に必要な relation を明確にする。

Classification: `adopt_candidate`

### IBM overview first / details on demand

- 重要情報を隠さず、必要に応じて詳細を見られる構造がよい。
- LAM の HTML は以下の順序が自然。
  1. overall status
  2. blockers / active card
  3. workstream matrix
  4. dependency graph
  5. detail links

Classification: `adopt_candidate`

### Microsoft dashboard card anatomy

- card は title / heading / body / footer の役割を分ける。
- card は link / information / direct action の entry point。
- LAM card では heading に `next action` または `current state` を置くとよい。
- 複雑な action UI は不要。Static HTML では link 중심。

Classification: `adopt_candidate`

### Baymard card consistency

- dashboard card は、layout / styling / header / content の一貫性が scan 性を左右する。
- card 内 text を詰めすぎると、視覚化した意味が薄れる。
- LAM の generated card は同じ field order と同じ visual treatment にする。

Classification: `adopt_candidate`

## Dashboard Information Architecture Candidate

### Top Band

- North Star
- Current phase
- Active card
- Next gate
- Blocked count
- Last verification

### Workstream Matrix

- rows: workstreams
- columns: gate / status / active card / blocker / evidence

### Board View

- columns: Backlog / Ready / Doing / Review / Done / Blocked
- WIP limit warning

### Graph View

- active card local dependency graph first
- global dependency graph second

### Detail Index

- specs
- ADRs
- tasks
- artifacts
- generated source info

## Combination Ideas

### C1: Presentation First, Exploration Later

初期 `index.html` は status dashboard に集中する。

- JS search / filtering は入れない。
- navigation は anchor links と file links で十分。
- graph は static SVG。

### C2: Three View Layout

GitHub Projects の三表示を LAM に転用する。

- Table: full card fields
- Board: status flow
- Roadmap: optional milestone view

### C3: Red Flag Strip

Top band に以下を出す。

- `Blocked`
- `Doing WIP exceeded`
- `Missing evidence`
- `Generated view stale`
- `Gate mismatch`

### C4: Card Microformat

Static HTML card は以下の順序で統一する。

1. ID / title
2. status / gate
3. next action
4. evidence link
5. verification

## Adoption Candidates

- Baseline now:
  - generated dashboard は presentation dashboard として始める。
  - top band + workstream matrix + board + local graph + detail links。
  - card layout は一貫させ、短い text にする。

- Next wave:
  - table / board / graph の複数 HTML view。
  - red flag strip。
  - optional roadmap view。

- Reject for initial pilot:
  - rich SPA。
  - drag-and-drop Kanban。
  - realtime filtering / search。
  - decorative chart-heavy dashboard。

## Open Questions

- `index.html` に board と graph を両方置くか、graph は別ページに分けるか。
- HTML は GitHub Pages 前提の relative links にするか、local file open 前提にするか。
- 色は status / gate / workstream のどれを主軸に割り当てるか。
- SVG は static で十分か、クリック可能リンクを埋め込むか。
