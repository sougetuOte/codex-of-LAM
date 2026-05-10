# WORKBOARD Review Reinforcement

Status: Draft review and reinforcement notes
Date: 2026-05-10

## Purpose

`09-synthesis-options.md` で固めた A+C 方針を、既存成果物と 01-09 の根拠に照らして
再レビューする。あわせて、判断を補強するための最小限の再調査を行い、不足、
未確定判断、後続 wave に逃がすべき項目を分ける。

このファイルは実装仕様ではない。PLANNING gate 前の補強メモである。

## Reviewed Artifacts

- `docs/artifacts/2026-05-10-magi-project-state-visibility.md`
- `docs/artifacts/2026-05-10-workboard-visualization-seed.md`
- `docs/artifacts/workboard-research/01-md-to-html-harvest.md`
- `docs/artifacts/workboard-research/02-codex-claude-context-harvest.md`
- `docs/artifacts/workboard-research/03-drift-generation-harvest.md`
- `docs/artifacts/workboard-research/04-agentic-kanban-harvest.md`
- `docs/artifacts/workboard-research/05-project-graph-harvest.md`
- `docs/artifacts/workboard-research/06-dashboard-ux-harvest.md`
- `docs/artifacts/workboard-research/07-traceability-harvest.md`
- `docs/artifacts/workboard-research/08-license-dependency-harvest.md`
- `docs/artifacts/workboard-research/09-synthesis-options.md`

## Adopted Direction Under Review

初期 pilot は `Option A: Minimal Native Workboard` を baseline とし、
`Option C: Task Graph Inspired Workboard` から以下だけを取り込む。

- progressive drill-down
- short card detail blocks
- explicit dependency / evidence links
- future `context CARD-ID` に転用できる card detail contract

`next`、`context CARD-ID`、card 別 HTML、CI drift check、external adapter、
traceability matrix は後続 wave 候補とする。

## Local Review Findings

### R1. A+C 方針は 01-08 の baseline と整合している

- 01 は `WORKBOARD.md` SSOT、generated view、Mermaid の補助利用、
  Docusaurus / Mermaid CLI 非必須を支持している。
- 02 は progressive disclosure と card contract を支持している。
- 03 は quick-load で render せず、gate / release 前に render する契約を支持している。
- 04 は card、status、dependency、WIP limit を支持している。
- 05 は dependency / evidence links と将来の `context CARD-ID` を支持している。
- 06 は presentation dashboard、top band、workstream matrix、board、local graph、
  detail links を支持している。
- 07 は evidence / verification を Green State の根拠として扱う方針を支持している。
- 08 は no fork、Ring 0: Markdown + Python standard library、external tool は思想だけ借りる
  方針を支持している。

結論: A+C 方針を止める矛盾は見つからない。

### R2. 09 で固めた範囲は安全側に寄っている

09 は `WORKBOARD.md` root、最小 card fields、short card detail、初期 validator warning、
render timing を明示した。これは seed / MAGI の「薄い board を index として扱う」
結論と整合する。

特に良い点は、C の魅力である graph / context bundle をすぐ実装せず、まず
card microformat を安定させる点である。これは初期 pilot の過負荷を避ける。

### R3. まだ仕様化が必要な箇所は残る

以下は実装 wave に入る前に、`WORKBOARD.md` template または設計メモで固定した方がよい。

- card ID 形式。例: `WB-001`、または workstream prefix 付き。
- Markdown table と detail heading の parser 境界。
- `Evidence` に複数 file links を置く時の区切り形式。
- generated marker の具体形。
- `docs/project/index.html` と `docs/project/graph.svg` の deterministic 性をどこまで保証するか。

## Targeted Re-Research

### Task Master

Source:

- https://docs.task-master.dev/capabilities/task-structure

確認内容:

- task fields に `id`, `title`, `status`, `dependencies`, `priority`, `details`,
  `testStrategy`, `subtasks`, `metadata` がある。
- `next` は依存を満たした pending / in-progress task を選ぶ。
- `show` は task detail を表示する。

Implication:

- `WORKBOARD.md` の `ID`, `Status`, `Depends on`, `Verification`, detail block は妥当。
- ただし `priority`, `next`, `context CARD-ID` は初期必須にしなくてよい。
  Task Master 的な自動選択は後続 wave で十分。

### Vibe Kanban

Sources:

- https://github.com/BloopAI/vibe-kanban
- https://www.vibekanban.com/

確認内容:

- GitHub repo は Apache-2.0 license 表示。
- Vibe Kanban は sunsetting と表示され、open source / community maintained に寄っている。
- planning board、agent workspace、diff review、browser preview、複数 coding agents 連携が中核。
- 開発には Rust、Node.js、pnpm などの runtime surface がある。

Implication:

- plan / review / workspace という情報設計は参考になる。
- 直接依存、fork、primary SSOT 化は初期 pilot には不向き。
- 04 / 08 の「concept は採用、dependency は reject」は補強された。

### seite

Sources:

- https://seite.sh/
- https://github.com/seite-sh/seite

確認内容:

- seite は AI-native static site generator として、Markdown から HTML、Markdown copy、
  RSS、sitemap、search index、`llms.txt` などを生成する。
- single Rust binary / no runtime dependencies を掲げ、Windows install も用意している。
- GitHub repo は MIT license 表示。
- ただし `.claude/CLAUDE.md` scaffold、Claude Code agent、MCP など product-specific な面が強い。

Implication:

- generated static view と LLM-friendly artifacts の思想は参考になる。
- Codex LAM 初期 pilot では直接採用しない。
- 後続で public docs layer を考える時に、MkDocs / mdBook と並べて再評価する価値がある。

### GitHub Actions / Pages

Sources:

- https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
- https://docs.github.com/en/enterprise-cloud@latest/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

確認内容:

- workflow artifacts は workflow run 後に build/test output などを保存・共有する用途。
- GitHub Pages custom workflows は static site generator の build/deploy に使える。

Implication:

- CI artifact preview と GitHub Pages deploy は技術的には可能。
- ただし初期 pilot では local render + tracked generated files 候補で十分。
- Pages deploy / artifact upload は後続 wave に留める判断を補強する。

### Mermaid / MkDocs

Sources:

- https://mermaid.ai/docs/mermaid-oss/intro/index.html
- https://www.mkdocs.org/

確認内容:

- Mermaid は text definition から diagram を作る用途に合うが、HTML で render する場合は
  CDN script または package install が必要になる。
- MkDocs は Markdown と YAML config から static HTML site を作る docs generator である。

Implication:

- Mermaid は `WORKBOARD.md` 内の補助 source としては有効。
- Mermaid CLI / Node dependency を初期必須にしない判断は維持する。
- MkDocs は public docs polish 向きで、board / gate / traceability の初期 core ではない。

## Reinforced Decisions

### Baseline Now

- root `WORKBOARD.md` を SSOT にする。
- quick-load は `SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard までに留める。
- `WORKBOARD.md` は card table と short card detail を持つ。
- generated HTML / SVG は view であり truth ではない。
- `tools/workboard.py validate` は初期 warning set に絞る。
- `tools/workboard.py render` は presentation dashboard を生成する。
- external tools は思想だけ借り、直接依存しない。

### Next Wave Decisions

- `tools/workboard.py context CARD-ID`
- `tools/workboard.py next`
- source hash / `check-generated`
- CI drift check
- card 別 HTML
- traceability matrix / gate readiness view
- GitHub Pages / docs site layer
- optional import/export adapter

### Reject For Initial Pilot

- Vibe Kanban dependency / fork
- Task Master primary SSOT
- mymir embed / graph database
- Docusaurus direct adoption
- Mermaid CLI required dependency
- rich SPA / drag-and-drop Kanban
- GitHub Pages deploy
- pre-commit hook mandatory workflow

## Remaining Uncertainties

### U1. Card ID convention

実装前に固定する必要がある。推奨は human-readable で grep しやすい `WB-001` 形式。
workstream prefix は便利だが、stream 移動時に ID が揺れるため初期は避ける。

### U2. Markdown microformat

初期は table + `### CARD-ID: Title` の detail heading で始めるのがよさそうである。
YAML front matter / fenced block は parser が必要になり、初期 wave には重い。

### U3. Generated files を本当に commit するか

09 では commit 対象候補とした。最終判断は render が deterministic か、diff が安定するかを
実装 wave で確認してから行う。

### U4. Source hash scope

初期は generated marker + source path まで。source hash は `WORKBOARD.md` 単体か linked files
も含めるかで運用負荷が変わるため、後続 wave に回す。

### U5. 専用スキル化

今回の作業は `context-harvest` の後段にあたる。

現時点では別スキルを作る必要はない。理由は、`context-harvest` が既に
広い corpus の採掘、raw notes、synthesis、反映判断を含んでいるためである。

ただし、この「synthesis 後のレビュー・補強調査」は再利用価値が高い。今後も複数回発生するなら、
`decision-reinforcement` のような小さな skill に切り出す価値がある。

候補 skill の責務:

1. 既存 synthesis / decision note を固定する。
2. 根拠 artifacts を横断レビューする。
3. stale になり得る外部情報だけを再調査する。
4. `reinforced`, `weakened`, `unresolved`, `deferred` に分類する。
5. 元 decision note に最小反映する。

## Recommendation

09 の A+C 採用判断は維持してよい。

次は実装ではなく、PLANNING gate 用の小さな仕様化に進むのが安全である。
具体的には、`WORKBOARD.md` template、`tools/workboard.py validate/render` の scope、
generated marker、quick-load / gate 前 render 契約を 1 つの spec または task に落とす。
