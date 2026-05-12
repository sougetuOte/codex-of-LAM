# WORKBOARD 初期 pilot タスク

Status: Accepted
Date: 2026-05-10

## Purpose

`WORKBOARD.md` を project state SSOT として導入するための、最小実装 wave を R1/R2/R3 に分ける。

この tasks は BUILDING に戻る前の planning gate 用であり、review 後に実装へ進む。

## Inputs

- [WORKBOARD 初期 pilot spec](../specs/workboard-initial-pilot.md)
- [ADR-0006](../adr/0006-workboard-markdown-ssot.md)
- [WORKBOARD 初期 pilot design](../design/workboard-initial-pilot-design.md)
- [WORKBOARD Visualization Synthesis Decision](../artifacts/workboard-research/09-synthesis-options.md)
- [WORKBOARD Review Reinforcement](../artifacts/workboard-research/10-review-reinforcement.md)

## R0: Planning package review

- [x] spec を作成する
- [x] ADR を作成する
- [x] design を作成する
- [x] tasks を作成する
- [x] user review を受ける
- [x] 必要な修正を反映する
  - 2026-05-10: duplicate card ID を error に固定し、workflow sync の非反映時記録を必須化した
  - 2026-05-10: template 利用先の本文言語は固定せず、parser が読む token は英語固定とする language boundary を追加した
- [x] `.codex/current-phase.md` を BUILDING へ戻すか判断する

## R1: WORKBOARD template + validator

Goal: `WORKBOARD.md` の初期 template と `validate` の最小 warning set を TDD で作る。

- [x] Red: sample board parse の focused test を追加する
- [x] Red: duplicate card ID の focused test を追加する
- [x] Red: Active / Blocked / Done card の必須 field 不足 warning test を追加する
- [x] Green: root `WORKBOARD.md` initial template を追加する
- [x] Green: `tools/workboard.py validate` を追加する
- [x] Green: table row と detail heading の basic consistency を確認する
- [x] Refactor: parser 対象を `## Cards` と `## Card Details` に限定する
- [x] Verification: focused pytest を実行する

2026-05-11: R1 focused test / implementation / validation は green。R2 render へ進む前に R1 review を行う。

Acceptance:

- `python tools/workboard.py validate` が実行できる
- duplicate card ID は error になる
- missing next action / blocker / dependency / evidence / verification は warning になる
- valid initial `WORKBOARD.md` は error なしで通る

## R2: Render HTML / SVG

Goal: generated dashboard と dependency overview を local review できる形で出す。

- [x] Red: HTML generated marker test を追加する
- [x] Red: SVG generated marker test を追加する
- [x] Red: deterministic output test を追加する
- [x] Green: `tools/workboard.py render` を追加する
- [x] Green: `docs/project/index.html` を生成する
- [x] Green: `docs/project/graph.svg` を生成する
- [x] Refactor: output order を deterministic にする
- [x] Verification: focused pytest と `python tools/workboard.py render`

2026-05-11: R2 focused render tests と実生成は green。generated files は今回の R2 diff として review / commit 対象にできる。
2026-05-11: R1/R2 接合レビューで、render 前 validation error gate、Cards table 欠落 error、dashboard active-card 不一致 warning を追加した。

Acceptance:

- HTML に source path と generated marker が入る
- SVG に source path と generated marker が入る
- top band、workstream matrix、card board、detail links が HTML に出る
- dependency overview が SVG に出る
- generated files を commit 対象にするか判断できるだけの diff が得られる

## R3: Workflow sync + gate readiness

Goal: quick-load / quick-save / gate 前の運用に WORKBOARD pilot を接続する。

- [x] `.agents/skills/quick-load/SKILL.md` に `WORKBOARD.md` dashboard 読みを反映する。反映しない場合は、非反映理由と代替の authoritative doc を記録する
- [x] `.agents/skills/quick-save/SKILL.md` に `validate` 判断を反映する。反映しない場合は、非反映理由と代替の authoritative doc を記録する
- [x] `docs/internal/08_QUICK_LOAD_SAVE.md` に workflow contract を反映する。反映しない場合は、非反映理由と代替の authoritative doc を記録する
- [x] `SESSION_STATE.md` には詳細を重複させない方針を確認する
- [x] gate 前 checklist と release 前 checklist の文言を同期する
- [x] `git diff --check`
- [x] docs-only なら pytest 省略理由を記録する

2026-05-12: R3 workflow sync を `.agents/skills/quick-load/SKILL.md`,
`.agents/skills/quick-save/SKILL.md`, `.codex/workflows/quick-load.md`,
`.codex/workflows/quick-save.md`, `docs/internal/08_QUICK_LOAD_SAVE.md` に反映した。
`SESSION_STATE.md` には WORKBOARD 詳細を重複させず、active card と次の開始点だけを
残す方針を維持する。

2026-05-12: R1-R3 通しレビューで、generated HTML が日本語本文でも `lang="en"` のまま
になる軽微なアクセシビリティ不整合を修正した。renderer code を変更したため focused
pytest と full tests を実行し、`validate` / `render` / `git diff --check` も通した。

Acceptance:

- quick-load が render を要求しない
- gate 前は validate + render を行う契約が見える
- release 前は generated artifacts diff を確認する契約が見える
- `SESSION_STATE.md` と `WORKBOARD.md` の責務が分離されている

## WB-004: Public docs impact triage

Goal: WORKBOARD / quick-load / quick-save / gate / release contract 更新が public template 利用者向け文書へ与える影響を分類する。

- [x] 5.3 read-only inventory で README / QUICKSTART / CHEATSHEET / CHANGELOG / slides / docs/project を横断検索する
- [x] 5.4 fresh-template-user review で public first path への影響を確認する
- [x] `README*`, `QUICKSTART*`, `CHEATSHEET*`, `docs/slides/index*.html` は、quick-load / quick-save / gate / release の既存説明で足りるため本文更新を見送る
- [x] `WORKBOARD.md` と `docs/project/*` は fresh template user の front door に出さず、maintainer / project-state surface として扱う
- [x] `CHANGELOG.md` の `Unreleased` を、v1.0.0 後の WORKBOARD pilot 実態に合わせて更新する

Classification:

- 今すぐ更新する: `CHANGELOG.md`, `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md`
- リンクや一文だけ足す: なし。WORKBOARD を reusable public feature として出す場合は、将来 `CHEATSHEET*` または architecture slide に限定して追加する
- 後続 task に回す: `story-daily*` の Codex-native refresh、WORKBOARD を公開 feature にするかどうかの別 design review
- 古くなっているので別 review 対象にする: `CHANGELOG.md` の pre-Codex / Claude-era historical noise は別 audit 対象。今回は現行 `Unreleased` だけを修正する

2026-05-12: WB-004 は green。`python tools/workboard.py validate` は 0 errors / 0 warnings、`python tools/workboard.py render` は PASS、focused pytest は sandbox ACL 失敗後に権限外で再実行して 12 passed。次は user approval を得て AUDITING に進むか、追加 BUILDING card を切るか判断する。

## AUDITING: Workboard initial pilot audit

Goal: WORKBOARD initial pilot の R1-R4 成果物を監査し、Green State か残リスク付き継続かを判断できる状態にする。

- [x] user approval を得て AUDITING gate に進む
- [x] changed files を確認する
- [x] spec / ADR / design / tasks / implementation / generated artifacts の整合性を確認する
- [x] `python tools/workboard.py validate` を実行する
- [x] `python tools/workboard.py render` を実行し、generated artifact diff を確認する
- [x] focused tests と必要な broader tests を実行する
- [x] findings、残リスク、次の gate 判断を記録する

Findings:

- Blocking findings: なし。
- Verification: `python tools/workboard.py validate` は 0 errors / 0 warnings。`python tools/workboard.py render` は PASS。focused pytest は 12 passed。broader `tests/` は 49 passed。`gitleaks detect --no-git --source . --redact --verbose` は no leaks found。
- Residual risk: `gitleaks` は local `.pytest_cache` を permission denied で skip した。Git 管理対象ではなく、今回の WORKBOARD pilot 成果物起因の blocker ではない。
- Next gate: 2026-05-12 に audit result と residual risk への user approval を受け、pilot closure と release boundary prep へ進む判断を確定した。

## Pilot Closure

2026-05-12: WORKBOARD initial pilot を closure 承認済みとする。R1 template / validator、R2 render、R3 workflow sync、WB-004 public docs impact triage、WB-006 audit はすべて green。以後は release boundary prep に進む。

Release boundary prep では、`docs/internal/04_RELEASE_OPS.md` の deployment criteria に沿って以下を整理する:

- All Tests Green
- No Critical Bugs
- Quality Gate Passed
- Documentation Updated
- WORKBOARD Updated
- Retrospective Done

実際の tag、release asset、GitHub Release は別途 explicit release approval を得てから実施する。

## Release Boundary Prep

2026-05-12: `docs/internal/04_RELEASE_OPS.md` と `docs/internal/10_DISTRIBUTION_MODEL.md` を基準に release boundary を整理した。

Checklist:

- All Tests Green: PASS。WB-006 audit で focused pytest 12 passed、broader `tests/` 49 passed。
- No Critical Bugs: PASS。blocking findings なし。
- Quality Gate Passed: PASS。WB-006 audit green。
- Documentation Updated: PASS。`CHANGELOG.md`, `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md` を更新済み。
- WORKBOARD Updated: PASS。`python tools/workboard.py validate` と `render` を release boundary prep 中に再実行する。
- Retrospective Done: 未実施。release 実行前に必要。

Release execution approval:

- 未承認。tag、ZIP asset、checksum、GitHub Release はまだ作成しない。
- 次は retrospective を行い、version / tag / ZIP asset / checksum / GitHub Release の scope を明示して user approval を得る。

## Out of Scope

- `tools/workboard.py next`
- `tools/workboard.py context CARD-ID`
- source hash / CI drift check
- card 別 HTML
- GitHub Pages deploy
- external adapter
- rich SPA / drag-and-drop Kanban
- localized parser aliases / multilingual UI

## Review Gate Checklist

- [x] spec / ADR / design / tasks の scope が一致している
- [x] 初期 pilot が quick-load を重くしていない
- [x] R1/R2/R3 が review 可能な大きさに分かれている
- [x] validator warning set が過剰になっていない
- [x] generated view が truth ではないことが明記されている
- [x] 本文言語と parser token の境界が明記されている
- [x] BUILDING に戻る前に user approval を得ている
