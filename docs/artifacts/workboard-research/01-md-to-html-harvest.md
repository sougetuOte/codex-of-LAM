# Markdown to HTML/SVG Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`WORKBOARD.md` や関連 Markdown を SSOT にし、HTML / SVG の静的ビューを
生成するための参考事例を集める。ここでは採用決定ではなく、後続の比較材料を
残す。

## Harvest Policy

- 公式 docs または一次情報を優先する。
- 単独採用だけでなく、LAM に取り込める部品や思想を拾う。
- 依存が重いものは、直接採用ではなく参考候補として扱う。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| MkDocs | https://www.mkdocs.org/ | Markdown + YAML config で static site を生成する Python 系 docs generator。 |
| Material for MkDocs | https://squidfunk.github.io/mkdocs-material/ | MkDocs 上の成熟した theme / UX layer。検索、navigation、cards などが強い。 |
| mdBook | https://rust-lang.github.io/mdBook/ | Markdown を book 形式の HTML にする Rust 系 generator。`SUMMARY.md` 中心。 |
| Docusaurus | https://docusaurus.io/docs | Markdown / MDX から React ベースの docs site を作る。機能は強いが依存は重い。 |
| Mermaid | https://mermaid.js.org/ | Markdown 風テキストから diagrams を生成する。Mermaid CLI で SVG 生成可能。 |
| Markmap | https://markmap.js.org/ | Markdown を mind map として表示する。階層把握に向く。 |
| seite | https://seite.sh/ | Claude Code を UI とする AI-native static site generator。Markdown から HTML / RSS / sitemap / search index / `llms.txt` を生成する。 |

## Findings

### MkDocs / Material for MkDocs

- Markdown を中心にした docs-as-code として成熟している。
- Python 系なので、この repo の既存検証環境と相性は比較的よい。
- `mkdocs.yml` で navigation を明示するため、`WORKBOARD.md` からの自動生成とは
  少し発想が違う。
- Material for MkDocs は見た目と検索が強いが、theme 依存が増える。

Classification: `decide_later`

### mdBook

- `SUMMARY.md` で本の章立てを作る方式。
- Rust single binary 的に扱える余地があり、依存は比較的閉じやすい。
- project dashboard より、体系化された manual / internal docs に向く。
- LAM の「動的仕様書」より「読ませる本」寄り。

Classification: `decide_later`

### Docusaurus

- Markdown / MDX / React の組み合わせで表現力が高い。
- plugin ecosystem が強く、docs site としては成熟している。
- Node / React 依存が大きく、この repo の minimal template 方針とは重くなりやすい。
- 最初の pilot には過剰。

Classification: `reject_candidate` for initial pilot, `decide_later` for public docs site

### Mermaid

- Markdown 内に diagram source を残せるので、`WORKBOARD.md` の依存 map に向く。
- CLI で SVG 化できるが、Node 系依存とレンダリング環境の問題が入る。
- 最初は Markdown 内の lightweight view として使い、必須 render path にはしない方がよい。

Classification: `adopt_candidate`

### Markmap

- Markdown の見出し構造を mind map 化できる。
- 仕様や task の階層把握にはよいが、status / gate / dependency の表現は弱い。
- `WORKBOARD.md` の補助 view としては面白い。

Classification: `decide_later`

### seite

- Claude Code を操作 UI とし、Markdown から静的サイトを生成するという発想が今回の
  LAM 可視化に近い。
- `CLAUDE.md`, GitHub Actions, static HTML, search index, `llms.txt` など、
  agent-facing docs と human-facing site を同時に意識している。
- ただし新しめの tool なので、license、安定性、Windows 運用、Codex との距離は
  次回調査が必要。
- 直接採用より、「AI-native docs generator がどのファイルを生成しているか」を
  参考にする価値が高い。

Classification: `decide_later`

## Combination Ideas

### C1: Minimal Native Generator

`WORKBOARD.md` を自前 parser で読み、標準ライブラリ寄りの Python で
`docs/project/index.html` と `graph.svg` を生成する。

- 強み: 依存が最小。template として壊れにくい。
- 弱み: Markdown parser / link resolver を自作しすぎる危険。

### C2: Mermaid Source + Native HTML

`WORKBOARD.md` には Mermaid source を残す。HTML は自前生成し、diagram は最初は
Mermaid source のまま表示する。SVG 生成は後続 wave。

- 強み: 認知負荷を早く下げられる。
- 弱み: GitHub 上では Mermaid は読めるが、生成 HTML 内での扱いは別検討。

### C3: MkDocs / Material Adapter

`WORKBOARD.md` から MkDocs navigation や summary page を生成し、既存 docs を
見やすくする。

- 強み: docs site 品質が高い。
- 弱み: LAM の board / gate 表現は別途作る必要がある。

### C4: seite-inspired LAM Dashboard

seite の「AI が docs site を運用する」発想を、Codex LAM 向けに小さく作り付ける。

- 強み: LAM の名前に合う。
- 弱み: tool の調査不足。取り込み可否は未判断。

## Adoption Candidates

- Baseline now:
  - `WORKBOARD.md` を SSOT にする。
  - Mermaid は Markdown 内の lightweight dependency view として使う。
  - HTML / SVG は generated view として扱い、SSOT にしない。

- Next wave:
  - Python generator の parser 境界を設計する。
  - seite の生成物セットと workflow を詳細調査する。
  - MkDocs / mdBook を public docs layer として別枠評価する。

- Reject for initial pilot:
  - Docusaurus 直採用。
  - Mermaid CLI を必須依存にする。

## Open Questions

- `WORKBOARD.md` の構造は Markdown table で足りるか、front matter / fenced block が必要か。
- generated HTML を commit する場合、source hash をどこに埋めるか。
- GitHub Pages で見せる public docs と、local dashboard を同一にするか分けるか。
