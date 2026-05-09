# Template Onboarding Harvest Notes

Status: Raw harvest
Date: 2026-05-09

## Purpose

Codex LAM を GitHub template / starter kit として他ユーザーが使う場合に、
初期導線が Codex App 前提で分かりやすいかを確認する。

## Harvest Policy

- 対象は `README*`, `QUICKSTART*`, `CHEATSHEET*`, `docs/slides/*`。
- 判断はまだ確定しない。ここでは evidence と分類だけを残す。
- 観点は fresh repo 利用者、既存 repo 導入者、日英追従、旧 Claude Code 表現の混入。

## Findings

### `README.md` / `README_en.md`

- Classification: adopt_candidate
- Evidence:
  - 入口が `Slides -> QUICKSTART -> CHEATSHEET` の 3 step になっており、初回利用者の導線としては明確。
  - template / git clone / existing project の 3 option があり、配布モデルと整合している。
  - Codex runtime の必須構成は `AGENTS.md`, `.codex/workflows/`, `docs/internal/` と説明されている。
- Concern:
  - gitleaks 説明で `/full-review` という slash-command 風表現が残る。
  - 英語版の `Operational Protocols` に `08_QUICK_LOAD_SAVE.md`, `09_MODEL_AND_CONTEXT_POLICY.md`,
    `10_DISTRIBUTION_MODEL.md` が載っておらず、日本語版と情報量がずれている。

### `QUICKSTART.md` / `QUICKSTART_en.md`

- Classification: adopt_candidate
- Evidence:
  - Step 1-5 の順に、template 作成、Codex App 起動、PLANNING、適応、BUILDING へ進む形になっている。
  - `SESSION_STATE.md` がない場合は新規プロジェクトとして扱う、と明示している。
  - LAM 自体の docs/specs/adr を新規プロジェクトへ適応または削除する指示がある。
- Concern:
  - 「旧 Claude Code 資料はすぐ消さない」とする FAQ は、現 public template で `.claude/` が削除済みの状態と噛み合いにくい。
  - fresh repo 利用者には、まず `SESSION_STATE.md` が存在しないのが通常であることをもう少し強く示した方がよい。

### `CHEATSHEET.md` / `CHEATSHEET_en.md`

- Classification: adopt_candidate
- Evidence:
  - 日常運用向けに phase、session management、model use、skills、truth hierarchy が短くまとまっている。
  - `SESSION_STATE.md` が local handoff で Git 管理外と説明されている。
- Concern:
  - 初回利用時の 2 手目が `AGENTS.md` と `SESSION_STATE.md` を読んで quick-load になっている。
    fresh repo では `SESSION_STATE.md` がない場合が自然なので、存在しなければ新規開始と分かる表現が必要。
  - `subagents` を使える機能として紹介しているが、判断の保持や分離責務は本文中では薄い。

### `docs/slides/*`

- Classification: decide_later
- Evidence:
  - `docs/slides/index*.html`, `intro*.html`, `story-newproject*.html`,
    `story-daily*.html`, `story-evolution*.html`, `architecture*.html` が存在する。
  - README / QUICKSTART から参照される `index*.html` と `story-newproject*.html` は存在する。
  - visual assets `lam-starter-flow.svg` と `quick-load-flow.svg` は存在する。
- Concern:
  - `intro*.html`, `story-daily*.html`, `story-evolution*.html`,
    `story-newproject*.html` に `/full-review`, `/quick-load`, `/quick-save`, `/ship`
    のような slash-command 表現が残る。
  - `story-daily*.html` と `story-evolution*.html` には `.claude/skills/` や
    `.claude/rules/auto-generated/` が残っており、現 Codex template の入口としては危険。
  - slides は数が多く、単純置換だけで直すと文脈崩れが起きやすい。

## Initial Classification

| Area | Classification | Reason |
| --- | --- | --- |
| README / QUICKSTART / CHEATSHEET の入口修正 | baseline_now | 変更範囲が小さく、fresh repo 誤読を直接減らす |
| 英語版 README の protocol 一覧同期 | baseline_now | 日英差分で template 利用者を迷わせるため |
| slides 全体の Codex-native 化 | next_wave_decision | 残存表現が広く、視覚導線として別 gate でレビューした方が安全 |
| `/full-review` 表現の置換 | baseline_now for README, next_wave_decision for slides | README は小修正で済むが slides は複数文脈にまたがる |
| `.claude/` 残存表現の扱い | next_wave_decision | slides の再設計または legacy 分離が必要 |

## Impact On Current Work

- Step 1 の fresh repo / template validation では、まず README / QUICKSTART / CHEATSHEET の
  初期導線を修正する価値が高い。
- Step 2 の public template collateral review では、slides を別 sub-wave として扱うべき。
- `docs/internal/10_DISTRIBUTION_MODEL.md` の Section 8 と 10 は現方針として妥当だが、
  実際の README / slides 側にはまだ古い control-surface 表現が残っている。
