# Slides Codex-native Harvest Notes

Status: Raw harvest
Date: 2026-05-09

## Purpose

public template 利用者が最初に見る `docs/slides/*` を、Codex App 前提の onboarding surface として
使えるか確認する。ここでは判断前の evidence を残す。

## Harvest Policy

- 対象は `docs/slides/*.html` と `docs/slides/assets/*`。
- 主観的な良し悪しより、template 利用者の初期離脱につながる不整合を優先する。
- 分類は `baseline_candidate`, `rewrite_candidate`, `archive_or_hide_candidate`, `needs_visual_qa`。

## Slide Inventory

| File | Current role | Initial classification |
| --- | --- | --- |
| `docs/slides/index.html` / `index-en.html` | slide 目次 | baseline_candidate |
| `docs/slides/intro.html` / `intro-en.html` | 初回概念説明 | rewrite_candidate |
| `docs/slides/story-newproject.html` / `story-newproject-en.html` | template から新規 project を始める物語 | rewrite_candidate |
| `docs/slides/story-daily.html` / `story-daily-en.html` | 日常運用の物語 | archive_or_hide_candidate |
| `docs/slides/story-evolution.html` / `story-evolution-en.html` | framework が育つ物語 | archive_or_hide_candidate |
| `docs/slides/architecture.html` / `architecture-en.html` | 技術深掘り | rewrite_candidate |
| `docs/slides/assets/lam-starter-flow.svg` | README / intro 用 visual | baseline_candidate |
| `docs/slides/assets/quick-load-flow.svg` | README / intro 用 visual | baseline_candidate |

## Findings

### Index

- Evidence:
  - `index*.html` は `intro`, `story-newproject`, `story-daily`, `story-evolution`, `architecture` へ誘導している。
  - `story-daily` の説明は quick-load / ship / quick-save の日常運用を推している。
  - `architecture` の説明は immune system hooks を前面に出している。
- Risk:
  - 古い story deck へそのまま誘導すると、入口で Codex-native 方針と矛盾する。
- Classification: baseline_candidate if card labels are adjusted; otherwise rewrite_candidate.

### Intro

- Evidence:
  - `intro*.html` は `lam-starter-flow.svg` と `quick-load-flow.svg` を使い、README の入口と整合しやすい。
  - Quick Start slide は GitHub template / git clone -> Codex App -> PLANNING -> adapt -> audit の流れを持つ。
  - `intro*.html` に `/full-review` 表現が残る。
- Risk:
  - 初回 deck なので、slash-command 風表現が 1 箇所でも目立つと旧 runtime への誤解を生む。
- Classification: rewrite_candidate, but low-risk targeted rewrite.

### Story New Project

- Evidence:
  - `story-newproject*.html` は template 作成、Codex App 起動、PLANNING、requirements、ADR/design、task、BUILDING、AUDITING まで一連の流れを説明している。
  - `.codex/workflows/`, `.agents/skills/`, `docs/internal/` を template の入口として説明している。
  - AUDITING section に `/full-review src/auth/` が残る。
  - `code-reviewer`, `test-reviewer`, `quality-auditor`, `security-reviewer` など旧 agent 風の表現がある。
- Risk:
  - 新規利用者向けとして価値が高い一方、後半の audit 表現は現在の Codex App workflow / review pane / optional workers と再接続が必要。
- Classification: rewrite_candidate, high-priority.

### Story Daily

- Evidence:
  - `story-daily*.html` は `/quick-load`, `/building`, `/full-review`, `/ship`, `/quick-save`, `/release` を日常操作として扱う。
  - `.claude/skills/` へ skill を置く表現が残る。
  - hooks / PreToolUse / PostToolUse / Stop hook を immune system として説明する。
  - `SESSION_STATE.md` による復帰という中核アイデアは再利用可能。
- Risk:
  - 現在の Codex template では `.claude/` は active runtime ではない。
  - slash-command 日常運用を main story として出すと、README / QUICKSTART の Codex-native 方針と正面衝突する。
- Classification: archive_or_hide_candidate, or substantial rewrite.

### Story Evolution

- Evidence:
  - `story-evolution*.html` は TDD introspection、pattern-review、auto-generated rules、rule lifecycle を説明する。
  - `/pattern-review`, `/quick-save`, `/full-review` 表現が残る。
  - `.claude/rules/auto-generated/` が残る。
- Risk:
  - Codex LAM の思想紹介としては面白いが、public template 初回導線としては古い runtime の印象が強すぎる。
- Classification: archive_or_hide_candidate for first release, later rewrite if needed.

### Architecture

- Evidence:
  - `architecture*.html` は `.codex/workflows`, `.agents/skills`, MAGI, AoT, Green State など現方針と合う部分がある。
  - 同時に PreToolUse / PostToolUse / Stop hook, `hooks/`, `settings.json`, `agent-memory/` など旧 runtime 構造が残る。
  - `/lam-orchestrate` や `/magi` の slash-command 風見出しが残る。
- Risk:
  - 深掘り deck は新規利用者が README から直接行く可能性があり、ここで runtime 構造を誤解させると危険。
- Classification: rewrite_candidate, but first release では index から「advanced / pending refresh」と分離する選択もあり。

## Candidate Gate Options

### Option 1: Targeted Public-onboarding Patch

- Keep all slide files.
- Patch visible entry points and most dangerous terms:
  - `index*` card labels and descriptions
  - `intro*` `/full-review`
  - `story-newproject*` `/full-review` and worker wording
  - `story-daily*` `.claude/skills/`
  - `story-evolution*` `.claude/rules/auto-generated/`
  - `architecture*` file structure map old paths
- Pros: fast, preserves existing collateral.
- Cons: still leaves deeper old story logic.

### Option 2: Curated First-release Slide Set

- Keep `index*`, `intro*`, `story-newproject*`, assets as public first path.
- Hide or clearly mark `story-daily*`, `story-evolution*`, `architecture*` as advanced / pending Codex-native refresh.
- Pros: protects new-user onboarding.
- Cons: smaller slide offering until rewrite wave completes.

### Option 3: Full Slide Rewrite Before Public Use

- Rewrite all five deck pairs to Codex-native terms.
- Pros: highest polish.
- Cons: larger edit, requires browser visual QA and likely multiple review passes.

## Raw Recommendation For MAGI

- Public template onboarding should not expose `story-daily*` and `story-evolution*` as normal next steps until rewritten.
- `intro*` and `story-newproject*` are worth repairing first because they explain the critical first journey.
- `architecture*` should be treated as advanced material and either repaired or de-emphasized in `index*`.
- The safest next implementation slice is:
  1. `index*`: mark stable path vs pending refresh.
  2. `intro*`: remove slash-command style audit wording.
  3. `story-newproject*`: replace `/full-review` story with Codex-native AUDITING / review pane / worker-assisted audit wording.
  4. Defer deep rewrites of `story-daily*`, `story-evolution*`, `architecture*`.
