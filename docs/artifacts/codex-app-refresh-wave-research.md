# Codex App Refresh Wave Research

Status: Draft
Date: 2026-05-09

このメモは、Codex App の新機能を `codex-of-LAM` の template / bootstrap / skill-plugin 配布モデルへどう反映するかを判断するための調査メモである。

`docs/internal/10_DISTRIBUTION_MODEL.md` は現時点で十分整理されているため、この refresh wave では直接大きく書き換えず、まず本メモで採用候補、保留事項、外部評価を分離する。

## 1. 調査範囲

公式情報:

- [Codex app overview](https://developers.openai.com/codex/app)
- [Codex app features](https://developers.openai.com/codex/app/features)
- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [Codex config reference](https://developers.openai.com/codex/config-reference)
- [Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)

外部評価:

- [Simon Willison: Introducing the Codex app](https://simonwillison.net/2026/Feb/2/introducing-the-codex-app/)
- [Awesome Agents: OpenAI Codex App Review](https://awesomeagents.ai/reviews/review-openai-codex-app/)
- [Hacker News: The Codex App](https://news.ycombinator.com/item?id=46859054)
- [Reddit: Meet the Codex app](https://www.reddit.com/r/OpenAI/comments/1qu2vuo/meet_the_codex_app/)
- [TechRadar: critical Codex flaw report](https://www.techradar.com/pro/security/not-just-development-tools-security-experts-discover-critical-flaw-in-openais-codex-which-could-compromise-entire-enterprise-organizations)
- [Windows Central: Chronicle privacy concerns](https://www.windowscentral.com/artificial-intelligence/openai-chronicle-codex-just-like-windows-recall)

外部評価は一次情報ではなく、採用判断の補助材料として扱う。特に review site や Reddit / Hacker News は観測範囲が偏るため、LAM の仕様根拠にはしない。

## 2. 公式情報から見える変化

| 新機能 / 変化 | LAM への影響 | 反映候補 |
| --- | --- | --- |
| Codex App は app / CLI / IDE extension 間で skills や config を共有する | `quick-load` などを自然文運用だけに置く理由が弱くなった | Layer 3 を `skill first, plugin later` として明確化 |
| shared team skills は repo 内 `.agents/skills` に置ける | これまで local mirror 扱いだった `.agents/` の位置づけを再評価する必要がある | `.agents/skills` を template 配布候補に昇格するか判断 |
| Automations と thread automations | stable な繰り返し作業を schedule 化できる | quick-save reminder, friction review, recent commits summary などを候補化 |
| Worktree mode | 並列作業や refresh wave の隔離に向く | 高リスク変更、比較実験、automation は worktree 優先と明記 |
| built-in Git review / stage / commit / push / PR | ship 手順を CLI 前提だけにしなくてよい | review / ship workflow に Codex App review pane を追加 |
| in-app browser / browser-use | frontend や file-backed artifact の確認が Codex App 内で閉じやすくなった | UI / docs artifact 検証手順へ optional に追加 |
| image generation / document / spreadsheet / presentation artifacts | LAM が code 以外の成果物も扱いやすくなった | template core には入れず、artifact workflow として候補化 |
| memories | 個人の安定した好みや落とし穴の再利用に向く | truth source ではなく advisory layer として境界を書く |
| project `.codex/config.toml` | repo 側で推奨設定を持てるが、trusted project 前提 | minimal config template を作るか検討 |
| granular approvals / `approvals_reviewer = auto_review` | 権限運用を細かく設計できる | Windows / Git / pytest の承認ルールを config 化するか検討 |
| native Windows sandbox | Windows 前提の repo 運用と相性がよいが、ACL や temp 問題は残る | 既存の Windows pytest temp policy を維持し、config 側の採用は別判断 |
| computer use / Chronicle | 強力だが OS / plan / privacy の制約がある | Windows 中心の LAM core には入れない。必要時の外部機能扱い |

## 3. 外部評価から見える採用リスク

### Positive signals

- 複数 thread、worktree、automations、skills を一つの UI で扱える点は、従来の single chat / terminal agent より運用モデルとして評価されている。
- Simon Willison は、Codex App を CLI の上にある良い UI とし、特に Skills と Automations を新機能として注目している。
- 公式発表と外部記事の両方で、Codex は coding agent に留まらず、technical / knowledge work の agent harness として見られている。

### Caution signals

- review site や Hacker News では、Electron / resource usage / platform support / rate limits への不満が目立つ。これは template 内容そのものより、ユーザー環境依存リスクとして扱う。
- 外部 review は、Codex が曖昧で大きすぎる task に弱く、明確に scope された task で強いという評価が多い。LAM の小さな gate / wave / TDD 方針とは整合する。
- TechRadar が報じた Codex 系の command injection / token exposure 事例は修正済みとされるが、agent は credentials と live execution environment を扱うため、権限と入力境界を workflow に残す価値がある。
- Chronicle のような画面記憶系機能は便利さと privacy trade-off が大きい。LAM core には採用せず、必要時に明示許可する外部機能として扱うのが安全。

## 4. `10_DISTRIBUTION_MODEL.md` への影響

現時点で `10_DISTRIBUTION_MODEL.md` の基本構造は維持する。

変更候補は以下に限定する。

1. Layer 3 を `Skill / plugin distribution` から、`Project skills / user skills / plugin distribution` へ少し細分化する。
2. `.agents/skills` は公式に shared team skills の置き場所として扱えるため、`project-local skill mirror` ではなく `template candidate` として再評価する。
3. `.codex/config.toml` は template に含める前に、trusted project、approval policy、Windows sandbox、web search、skills.config の最小安全セットを検討する。
4. Automations は template 本体に直入れせず、`stable skill` ができた後の app-local setup とする。

## 5. Refresh Wave 案

### R0: evidence freeze

- 本メモを調査 snapshot として保存する。
- 公式情報と外部評価のリンクを残し、あとで drift したときに再確認できるようにする。

### R1: distribution model amendment

- `10_DISTRIBUTION_MODEL.md` に本メモへのリンクを追加する。
- `.agents/skills`、`~/.codex/skills`、plugin の責務境界を追記する。
- `.codex/config.toml` を template に入れるかどうかは、R2 まで判断を保留する。

### R2: project config pilot

- sample `.codex/config.toml` の候補を設計する。
- まず `docs/internal/10_DISTRIBUTION_MODEL.md` 上の docs-only sample に留め、
  実ファイル化は安全性と portability を確認してからにする。
- 候補項目は `approval_policy`, `approvals_reviewer`, `web_search`, `skills.config`, `features.memories`, `features.multi_agent`, Windows sandbox 周辺に限定する。

### R3: skillization pilot

- `quick-load` を最初の project skill として `.agents/skills/quick-load/SKILL.md` に追加する。
- `quick-save` は session writeback と Git / memory / daily log の境界が絡むため、`quick-load` より後にする。
- skill が安定したら user-level skill または plugin 化を検討する。

### R4: app workflow update

- worktree mode、review pane、in-app browser、automations を `.codex/workflows/`
  の optional path として追加する。
- automations は template 同梱ではなく、安定した workflow を Codex App 側で任意設定する operation として扱う。
- 既存の CLI / PowerShell 前提を消さず、Codex App で使える時の短い分岐を足す。

### R5: fresh repo validation

- GitHub template 相当の新規 repo を想定し、最小ファイル集合で quick-load できるか確認する。
- 既存 repo への bootstrap / sync では、上書き禁止、diff / report 優先を維持する。
- 検証観点は `docs/internal/10_DISTRIBUTION_MODEL.md` の
  `Fresh repo / bootstrap validation` に固定する。

### R6: distribution collateral refresh

- `README.md`, `README_en.md`, `QUICKSTART.md`, `CHEATSHEET.md`, `CHEATSHEET_en.md`, `CHANGELOG.md` の役割とリンクを Codex App 前提へ更新する。
- 既存リンクを維持するため `QUICKSTART_en.md` は必須追加候補として扱う。
- `CONTRIBUTING.md`, `SECURITY.md` は必要性を判断する。
- `docs/slides/*.html` を visual onboarding として再設計する。
- 画像付きの説明を積極的に使い、template / starter kit としての使い方、quick-load、worktree、review / ship、fresh repo bootstrap を直感的に見せる。
- 日本語を canonical、英語を追従版として扱う。

## 6. 推奨判断

採用する:

- `skill first, plugin later`
- `.agents/skills` の template candidate 化
- worktree-first な refresh / automation 方針
- app review pane / in-app browser の optional workflow 化
- memories は advisory layer として明記
- distribution collateral は画像付きの README / HTML slides を重視し、日本語と英語の 2 言語に絞る

保留する:

- `.codex/config.toml` の実ファイル配布。R2 では docs-only sample に留める。
- automations の template 同梱
- `quick-save` の skill 化
- Chronicle / computer use の core 採用

採用しない:

- Codex App 新機能を理由に `AGENTS.md` / docs / tasks の truth hierarchy を弱めること
- 外部評価だけを根拠に LAM の必須 workflow を増やすこと
- slash command 相当の UX を `.codex/workflows/*.md` だけで実現できると扱うこと

## 7. 次の編集候補

- `docs/internal/10_DISTRIBUTION_MODEL.md` の `次に決めること` に本メモへのリンクを追加する。
- `docs/tasks/codex-lam-replacement-tasks.md` の Refresh Wave task を R0-R6 に分解する。
- R1 で `.agents/skills` と user-level skills の境界を本文へ反映する。
- R3 で `.agents/skills/quick-load/SKILL.md` を追加し、quick-load を project skill として試す。
- R4 で `.codex/workflows/` に Codex App optional path を追加する。
- R5 で fresh repo / existing repo bootstrap の最小検証観点を固定する。
- R6 で README / QUICKSTART / CHEATSHEET / slides を Codex App 前提の配布物として更新する。
