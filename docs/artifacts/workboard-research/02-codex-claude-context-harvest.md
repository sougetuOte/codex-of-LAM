# Codex / Claude Context Management Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

Codex App / Claude Code 系の context 管理、agent-facing docs、worktree / skill /
memory 運用から、`WORKBOARD.md` と静的 dashboard の設計に使える要素を拾う。

## Harvest Policy

- OpenAI / Anthropic の公式 docs を優先する。
- Codex LAM の quick-load 軽量化方針と矛盾しないものだけ候補にする。
- Claude Code 固有機能は、そのまま移植せず、Codex-native な概念へ変換する。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| Codex AGENTS.md | https://developers.openai.com/codex/guides/agents-md | repo-level instructions の公式 guidance。 |
| Codex Prompting | https://developers.openai.com/codex/prompting | Codex に明示 context / done / verification を与える guidance。 |
| Codex Workflows | https://developers.openai.com/codex/workflows | worktree, issue, PR, handoff などの workflow examples。 |
| Codex Skills | https://developers.openai.com/codex/skills | progressive disclosure で必要な instructions だけ読む設計。 |
| Codex Memories | https://developers.openai.com/codex/memories | local memory と checked-in instructions の使い分け。 |
| Codex Worktrees | https://developers.openai.com/codex/app/worktrees | isolated tasks / branches の使い方。 |
| Claude Code Best Practices | https://www.anthropic.com/engineering/claude-code-best-practices | context 管理、plan / explore / code / commit の実例。 |
| Claude Code Memory | https://docs.anthropic.com/en/docs/claude-code/memory | `CLAUDE.md` と memory import の公式 guidance。 |
| Claude Code Common Workflows | https://docs.anthropic.com/en/docs/claude-code/common-workflows | plan, research, parallel sessions, git worktrees の workflow。 |
| Claude Cowork live artifacts | https://support.claude.com/en/articles/14729249-use-live-artifacts-in-claude-cowork | persistent HTML dashboard 的な live artifact の説明。 |

## Findings

### Codex AGENTS.md

- Codex は repo instruction として `AGENTS.md` を使う。
- 大きな instruction は分割し、必要な場所に近い instructions を置く考え方がある。
- `WORKBOARD.md` は `AGENTS.md` の代わりではなく、状態 SSOT として分けるのがよい。

Classification: `adopt_candidate`

### Codex prompting / workflows

- Codex には task goal、context、definition of done、verification expectation を明示する方がよい。
- Workflows は issue / PR / worktree / handoff の単位で進む。
- `WORKBOARD.md` の card に `Goal`, `Context`, `DoD`, `Verification` を持たせると、
  Codex への依頼精度が上がる。

Classification: `adopt_candidate`

### Codex skills

- Skills は progressive disclosure を前提にしており、必要なときだけ詳細 instructions を読む。
- `WORKBOARD.md` も同じ発想にできる。
  - 冒頭 dashboard: quick-load 用
  - card detail: task 開始時
  - linked docs: gate / review 時

Classification: `adopt_candidate`

### Codex memories

- memory は便利だが、repo の canonical truth ではない。
- 複数 PC や template 利用を考えると、永続状態は checked-in docs を中心にする方がよい。
- `WORKBOARD.md` は memory ではなく repo artifact として置く。

Classification: `adopt_candidate`

### Codex worktrees

- 複数タスクを独立 branch / worktree で進める発想は board card と相性がよい。
- `card id -> branch/worktree/pr` の対応を持てると、状態の追跡がかなり楽になる。
- ただし initial pilot では branch automation まで入れない。

Classification: `decide_later`

### Claude Code best practices / memory

- Claude Code 側も、探索、計画、実装、commit を分け、context を管理する実例がある。
- `CLAUDE.md` は長くしすぎず、必要に応じて import や topic split を使う思想がある。
- Codex LAM では `AGENTS.md` / `.codex/workflows` / `WORKBOARD.md` を分担させるのが自然。

Classification: `adopt_candidate`

### Claude Code common workflows

- research を別 context に逃がす、plan mode で方針を固める、worktree で並行作業する、
  という運用が出てくる。
- 今回の context-harvest 方針と整合している。
- `WORKBOARD.md` は main context に残す薄い coordination surface として機能できる。

Classification: `adopt_candidate`

### Claude Cowork live artifacts

- persistent interactive HTML dashboard の発想は、`docs/project/index.html` に近い。
- ただし Claude Cowork の live artifact は product-specific で、repo-native SSOT ではない。
- 参考にするのは「人間が見る状態 surface は HTML でよい」という点。

Classification: `decide_later`

## Combination Ideas

### C1: Progressive Disclosure Workboard

`WORKBOARD.md` を三段構成にする。

1. Quick dashboard: quick-load が読む。
2. Card table: active task selection に使う。
3. Links: specs / tasks / ADR / artifacts に飛ぶ。

### C2: Agent-Ready Card Contract

各 card に Codex prompting と同じ要素を持たせる。

- Goal
- Context
- Definition of Done
- Verification
- Evidence
- Next action

これにより、card をそのまま Codex 依頼文の材料にできる。

### C3: Worktree Link Later

初期 pilot では入れないが、将来は card に以下を持たせる。

- branch
- worktree
- PR
- owner / agent

Codex App の worktree と board を接続できる。

### C4: Live Artifact Without Product Lock-in

Claude Cowork の live artifact 的な体験を、repo-native generated HTML として再現する。

- Product artifact ではなく checked-in static HTML。
- Source は `WORKBOARD.md`。
- Rendering は local / CI / GitHub Pages のどれでも可能にする。

## Adoption Candidates

- Baseline now:
  - `WORKBOARD.md` は `AGENTS.md` と `SESSION_STATE.md` の間に置く状態 SSOT。
  - quick-load は冒頭 dashboard のみ読む。
  - card には Goal / DoD / Verification を入れる。

- Next wave:
  - card id と branch/worktree/PR の optional mapping。
  - generated HTML を live artifact 風の dashboard にする。

- Reject for initial pilot:
  - Claude Code hooks / slash command 前提の移植。
  - memory を canonical project state とすること。

## Open Questions

- `WORKBOARD.md` の冒頭 dashboard は何行以内に制限するか。
- card の fields は Markdown table で扱えるか、YAML block が必要か。
- Codex App worktree と連携する場合、repo template として optional にできるか。
