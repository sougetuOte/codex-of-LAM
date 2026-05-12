# WORKBOARD 初期 pilot 設計

Status: Accepted
Date: 2026-05-10

## Overview

WORKBOARD 初期 pilot は、root `WORKBOARD.md` を project state SSOT とし、`tools/workboard.py` で validate / render する。

目的は、quick-load を重くせずに、gate 前の project state、card、dependency、evidence、verification を見える状態にすることである。

## Components

### `WORKBOARD.md`

手編集する primary artifact。

初期 template は以下の section を持つ。

1. Dashboard
2. Workstreams
3. Gate Matrix
4. Cards
5. Card Details
6. Dependency Map

Dashboard は quick-load で読む冒頭 surface とする。
Card Details は progressive drill-down 用であり、長い実行計画や検証ログを抱え込まない。

### `tools/workboard.py`

Python standard library ベースの CLI。

初期 command は以下のみ。

```text
python tools/workboard.py validate
python tools/workboard.py render
```

初期 pilot では input / output path を固定する。

- input: `WORKBOARD.md`
- HTML output: `docs/project/index.html`
- SVG output: `docs/project/graph.svg`

### `docs/project/index.html`

Generated presentation dashboard。

初期表示は以下を含む。

- generated marker
- source path
- top band: active / blocked / gate / verification summary
- workstream matrix
- card board
- detail anchors

### `docs/project/graph.svg`

Generated dependency overview。

初期表示は、workstream と active card 周辺の dependency overview に絞る。
Graph layout は deterministic な簡易配置を優先し、rich interaction は持たない。

## Markdown Microformat

### Card table

Cards section には Markdown table を置く。

```markdown
## Cards

| ID | Title | Status | Gate | Workstream | Next action | Depends on | Evidence | Verification | Blocker |
|----|-------|--------|------|------------|-------------|------------|----------|--------------|---------|
| WB-001 | Define pilot spec | Active | design | Workboard | Review planning package | | docs/specs/workboard-initial-pilot.md | Not run: planning | |
```

### Card detail

Card detail heading は `### WB-001: Title` とする。

```markdown
### WB-001: Define pilot spec

- Goal: WORKBOARD 初期 pilot の planning package を固定する
- Context: 実装前に spec / ADR / design / tasks を同期する
- Definition of Done: planning docs が review 可能で、R1/R2/R3 に分割されている
- Verification: `git diff --check`
- Evidence: `docs/specs/workboard-initial-pilot.md`
- Next action: user review
- Blockers: none
```

## Parser Boundary

初期 parser は Markdown 全体を完全には解釈しない。
次の範囲だけを対象にする。

- `## Cards` 直下の table
- `## Card Details` 配下の `### WB-001: Title` headings
- card detail 内の bullet labels

Parser は unknown section を許容する。
これにより `WORKBOARD.md` を人間が自然に編集できる余地を残す。

## Language Boundary

本文、card title、context、evidence 説明は project primary language を使ってよい。
この repo では日本語を基本にするが、template 利用先が英語や他言語で本文を書くことは妨げない。

一方で、初期 parser / renderer が読む token は英語固定とする。

- section heading: `## Cards`, `## Card Details`
- table fields: `ID`, `Title`, `Status`, `Gate`, `Workstream`, `Next action`, `Depends on`, `Evidence`, `Verification`, `Blocker`
- status values: `Todo`, `Active`, `Blocked`, `Done`, `Released`
- detail labels: `Goal`, `Context`, `Definition of Done`, `Verification`, `Evidence`, `Next action`, `Blockers`

localized aliases や多言語 UI は後続 wave 候補とし、初期 pilot では扱わない。

## Validation Rules

初期 warning set は spec の FR-004 に限定する。

| Rule | Severity | 備考 |
|------|----------|------|
| duplicate card ID | error | 同一 ID は graph / detail link を壊す |
| active card missing next action | warning | quick-load で次行動が失われる |
| blocked card missing blocker reason | warning | review 不能になる |
| dependency target missing | warning | dependency graph が壊れる |
| evidence file missing | warning | Green State の根拠が失われる |
| Done / Released card missing verification | warning | 完了状態が暗黙になる |

初期 pilot では spec -> card trace、touches file path、commit / PR trace、impact analysis は扱わない。

## Render Design

### HTML

HTML は static single file とする。
外部 CDN や Node build を要求しない。
`lang` attribute は board 本文に日本語文字が含まれる場合 `ja`、それ以外は `en` とする。

Generated marker の例:

```html
<!-- Generated from WORKBOARD.md by tools/workboard.py. Do not edit by hand. -->
```

CSS は inline または同一ファイル内に置く。
初期 pilot では public docs の polish より、gate 前の視認性を優先する。

### SVG

SVG は Python から直接文字列生成する。
ノードは deterministic order で並べる。
初期 layout は workstream lane と dependency lines の簡易表現にする。

Generated marker の例:

```xml
<!-- Generated from WORKBOARD.md by tools/workboard.py. Do not edit by hand. -->
```

## Workflow Contract

### Quick-load

- `tools/workboard.py render` は実行しない
- `SESSION_STATE.md` と `WORKBOARD.md` dashboard まで読む
- 詳細が必要な場合だけ active card detail と evidence links へ降りる

### Quick-save

- `WORKBOARD.md` が変わった場合は `validate` を検討する
- 重い render は必須にしない

### Gate 前

- `python tools/workboard.py validate`
- `python tools/workboard.py render`
- dashboard / graph を確認する

### Release 前

- `python tools/workboard.py validate`
- `python tools/workboard.py render`
- generated artifacts の diff を確認する

## Test Strategy

### R1 focused tests

- valid card table を parse できる
- duplicate card ID を error にできる
- Active / Blocked / Done card の必須 field 不足を warning にできる

### R2 focused tests

- HTML に generated marker と source path が入る
- SVG に generated marker と source path が入る
- 同じ sample input から同じ output が生成される

### R3 verification

- workflow docs または skills の反映範囲を確認する
- `git diff --check`
- docs-only change なら pytest 省略可

## Deferred Design

- `tools/workboard.py context CARD-ID`
- `tools/workboard.py next`
- source hash
- CI drift check
- card 別 HTML
- traceability matrix
- GitHub Pages deploy
- external tool adapter

## Risks

- `WORKBOARD.md` が長くなりすぎる
  - 緩和: long plan / logs は `docs/tasks/` と `docs/artifacts/` へ逃がす
- generated artifacts が truth に見える
  - 緩和: generated marker と source path を必須にする
- parser が brittle になる
  - 緩和: parser 対象 section を限定し、unknown section を許容する
- validator が重い gate になる
  - 緩和: 初期 warning set を限定し、error は duplicate ID から始める

## Related Documents

- [WORKBOARD 初期 pilot spec](../specs/workboard-initial-pilot.md)
- [ADR-0006](../adr/0006-workboard-markdown-ssot.md)
- [WORKBOARD 初期 pilot tasks](../tasks/workboard-initial-pilot-tasks.md)
- [WORKBOARD Visualization Synthesis Decision](../artifacts/workboard-research/09-synthesis-options.md)
- [WORKBOARD Review Reinforcement](../artifacts/workboard-research/10-review-reinforcement.md)
