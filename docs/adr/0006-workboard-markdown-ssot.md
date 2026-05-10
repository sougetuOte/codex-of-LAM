# ADR-0006: WORKBOARD Markdown SSOT と generated view の採用

Date: 2026-05-10
Status: Accepted

## Context

Codex LAM は quick-load を軽く保ちつつ、複数 wave、gate、dependencies、evidence、verification を見失わない project state surface を必要としている。

既存の `SESSION_STATE.md` は再開用の短い memo として有効だが、project board、依存関係、gate readiness、Green State の根拠まで持たせると肥大化する。

一方で、external Kanban、rich docs site、graph database、GitHub Pages などを初期導入すると、template starter としての軽さ、Windows / Codex App での扱いやすさ、レビュー容易性を損なう。

## Decision

初期 pilot では root `WORKBOARD.md` を project state の SSOT とし、`tools/workboard.py` で validate / render する。

- `WORKBOARD.md` は dashboard、workstreams、gate matrix、card table、short card detail、dependency map を持つ。
- `docs/project/index.html` と `docs/project/graph.svg` は generated view として扱う。
- generated view は認知負荷を下げる presentation / review surface であり、truth ではない。
- quick-load は render しない。`SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard までを基本にする。
- gate 前と release 前は validate + render を行い、人間が dashboard / graph を見る。
- 初期 pilot は external tool を primary dependency にしない。
- 本文言語は project primary language に委ねるが、parser / renderer が読む field name、status value、detail label は初期 pilot では安定した英語 token とする。

## Alternatives Considered

### A. `SESSION_STATE.md` に board 情報も持たせる

却下。
quick-load 用 memo が肥大化し、ユーザーが求める「前回やったこと / 次にやること」の薄い復元面ではなくなる。

### B. External Kanban または Task Master を primary SSOT にする

却下。
UI や自動化の思想は参考になるが、初期 pilot で dependency surface と setup burden が増える。
Codex LAM の template reuse では、Markdown が残る repo-native な失敗耐性を優先する。

### C. `WORKBOARD.md` を SSOT にし、HTML / SVG を generated view にする

採用。
Markdown は review しやすく、Git diff と相性がよく、quick-load も軽く保てる。
HTML / SVG は人間が全体を見るための presentation として追加できる。

### D. 最初から full project graph system を作る

却下。
将来像としては魅力があるが、初期 pilot では過剰である。
card microformat が安定してから、`context CARD-ID`、traceability matrix、graph system を再判断する。

## 3 Agents Analysis

### Affirmative: 推進者の視点

- `WORKBOARD.md` があると、project state、gate、dependencies、evidence を一箇所から追える。
- generated view によって、review pane やブラウザで全体把握しやすくなる。
- Markdown SSOT は template として別 project に持ち込みやすい。
- `context CARD-ID` や traceability matrix へ拡張する土台になる。

### Critical: 批判者の視点

- microformat を増やしすぎると、手書きがつらくなる。
- generated HTML / SVG を commit すると stale truth に見える危険がある。
- validator が厳しすぎると、軽量 board ではなく別の重い gate になる。
- `WORKBOARD.md` に長い議論や実行ログを入れると、結局 quick-load が重くなる。

### Mediator: 調停者の視点

- 初期 pilot は `WB-001` ID、table、short detail、最小 warning set に留める。
- generated files には source path と generated marker を入れ、truth ではないことを明示する。
- source hash、CI drift check、`next`、`context CARD-ID`、card 別 HTML は後続 wave に送る。
- 長い計画やログは `docs/tasks/` と `docs/artifacts/` へ逃がす。

## Consequences

- `WORKBOARD.md` が project state の新しい primary board になる。
- `SESSION_STATE.md` は quick-load 用の薄い memo として維持する。
- `tools/workboard.py` は planning / gate workflow に関わるため、testable な CLI として扱う。
- generated HTML / SVG の commit 方針は、render deterministic 性を確認してから final decision する。
- public docs layer や GitHub Pages は初期 pilot の後続候補になる。
- 日本語以外の利用者は本文を英語などの主言語で書ける。ただし初期 pilot では machine-readable token の localized alias は提供しない。

## Impact

### Positive

- quick-load と project-wide visibility の責務を分けられる。
- gate 前に Green State の根拠を確認しやすくなる。
- Codex App / Windows / GitHub template reuse に合う軽量 workflow になる。

### Negative

- Markdown microformat と parser の保守が増える。
- generated view の stale 化を防ぐ運用が必要になる。

### Affected components

- `WORKBOARD.md`: 新規 state SSOT
- `tools/workboard.py`: 新規 validator / renderer
- `docs/project/index.html`: generated view
- `docs/project/graph.svg`: generated dependency overview
- `docs/internal/08_QUICK_LOAD_SAVE.md`: 後続で workflow contract 反映候補
- `.agents/skills/quick-load/SKILL.md`: 後続で WORKBOARD dashboard 読みを反映候補
- `.agents/skills/quick-save/SKILL.md`: 後続で validate 判断を反映候補

## Verification

- `tools/workboard.py validate` の focused tests
- `tools/workboard.py render` の focused tests
- `git diff --check`
- docs-only planning package では pytest を省略可
- implementation wave では一意の `--basetemp` を使った focused pytest を選ぶ

## References

- [WORKBOARD 初期 pilot spec](../specs/workboard-initial-pilot.md)
- [WORKBOARD 初期 pilot design](../design/workboard-initial-pilot-design.md)
- [WORKBOARD 初期 pilot tasks](../tasks/workboard-initial-pilot-tasks.md)
- [WORKBOARD Visualization Synthesis Decision](../artifacts/workboard-research/09-synthesis-options.md)
- [WORKBOARD Review Reinforcement](../artifacts/workboard-research/10-review-reinforcement.md)
