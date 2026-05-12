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
