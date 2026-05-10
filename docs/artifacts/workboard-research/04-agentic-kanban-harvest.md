# Agentic Kanban / Task Board Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`WORKBOARD.md` の card / status / workstream / next action 設計に使える
AI coding agent 向け Kanban / task board 事例を集める。

## Harvest Policy

- 公式 docs / product page を優先する。
- 外部 tool をそのまま採用するのではなく、LAM に取り込める情報設計を拾う。
- 複数 agent / worktree / review を支える最小 card contract を探す。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| Vibe Kanban | https://www.vibekanban.com/ | AI coding agents を Kanban / worktree / review で運用する tool。sunsetting 予定の表示あり。 |
| Vibe Kanban docs | https://www.vibekanban.com/docs/index | isolated git worktree, multi-agent, visual review の説明。 |
| Vibe Kanban workspaces | https://vibekanban.com/docs/workspaces/ | task ごとに git worktree を切る workspace model。 |
| Task Master PRD parsing | https://docs.task-master.dev/getting-started/quick-start/prd-quick | PRD から tasks.json、dependencies、priorities、test strategies を生成する workflow。 |
| Task Master task structure | https://docs.task-master.dev/capabilities/task-structure | next task, metadata, dependency validation, status update など。 |
| Task Master RPG method | https://docs.task-master.dev/capabilities/rpg-method | Repository Planning Graph による依存-aware PRD / task generation。 |
| GitHub Projects views | https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view | table / board / roadmap の view model。 |
| GitHub Projects quickstart | https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects | fields, views, automation, charts の基本。 |
| Atlassian Kanban board | https://www.atlassian.com/agile/kanban/boards | card / columns / WIP limits / commitment point / delivery point の整理。 |

## Findings

### Vibe Kanban

- AI coding agent の bottleneck は coding そのものより、人間の plan / review に移るという前提がある。
- task ごとに isolated git worktree を使い、parallel agent execution を安全にする。
- Kanban board, prompt, review diff, built-in browser / QA などを一つの UI に集める。
- ただし product 自体は sunsetting 表示があり、直接依存は危険。

Classification: `adopt_candidate` for concept, `reject_candidate` for direct dependency

### Vibe Kanban workspace model

- 1 task = 1 isolated workspace / worktree という対応は非常に分かりやすい。
- worktree があると agent 同士の衝突を避けやすい。
- `WORKBOARD.md` には初期から `branch/worktree/pr` 欄を必須にせず、optional field として
  置けるようにするのがよい。

Classification: `decide_later`

### Task Master

- PRD から task list, dependencies, priorities, test strategies を生成する流れは
  LAM の requirements -> tasks gate と近い。
- `next` は dependencies を満たした pending / in-progress task を選ぶ。
- dependency validation、complexity analysis、task expansion は `WORKBOARD.md` の
  validator / next-card logic の参考になる。
- ただし `.taskmaster/` と `tasks.json` が別 SSOT になりやすい。

Classification: `adopt_candidate` for method, `reject_candidate` as primary SSOT

### Task Master RPG

- Repository Planning Graph は、機能分解、構造分解、明示依存、topological ordering を
  PRD 段階から持つ。
- LAM の `WORKBOARD.md` に `depends_on`, `blocks`, `phase/gate`, `entry/exit criteria`
  を入れる根拠になる。
- 特に "next work" を選ぶには dependency graph が必要。

Classification: `adopt_candidate`

### GitHub Projects

- 同じ project items を table / board / roadmap の複数 view で見る設計が参考になる。
- Table は高密度・多フィールド、Board は status flow、Roadmap は time / milestone。
- LAM でも `WORKBOARD.md` から同じ source を複数 view に render するのがよい。
- GitHub Projects 自体を SSOT にすると offline / template / multi-PC の摩擦が増える。

Classification: `adopt_candidate` for view model, `decide_later` for integration

### Atlassian Kanban

- Kanban の重要要素は visual signals, columns, WIP limits, commitment point, delivery point。
- WIP limit は Codex App で複数作業を抱えすぎないために有効。
- blocker / dependency の即時可視化が board の価値。
- Gantt より continuous flow の方が今回の LAM には合う。

Classification: `adopt_candidate`

## Combination Ideas

### C1: LAM Workboard Card Contract

各 card は以下を持つ。

- ID
- title
- status
- workstream
- gate
- goal
- next action
- definition of done
- verification
- depends_on
- blocks
- evidence files
- optional branch / worktree / PR

### C2: Views From One Source

GitHub Projects の発想を借り、同じ `WORKBOARD.md` から複数 view を生成する。

- Table view: all cards + fields
- Board view: status columns
- Roadmap view: milestones / target dates がある場合のみ
- Graph view: dependency / blocks

### C3: Next Card Recommendation

Task Master の `next` を参考に、validator / exporter が次の候補を出せるようにする。

条件:

- status が `Ready` または `Backlog`
- depends_on が `Done` / `Released`
- gate が現在 phase と矛盾しない
- blocker がない
- priority / user-selected focus を考慮

### C4: WIP Limit As Context Guard

Kanban の WIP limit を Codex context guard に転用する。

- `Doing` は原則 1。
- parallel work は明示的に worker / worktree / card を分ける。
- `Doing` が増えたら quick-save / board update を促す。

## Adoption Candidates

- Baseline now:
  - `WORKBOARD.md` は card + status + dependency を持つ。
  - `Doing` WIP limit を明示する。
  - card に `next action`, `DoD`, `verification`, `evidence` を持たせる。

- Next wave:
  - `tools/workboard.py next` 相当の候補抽出。
  - optional branch / worktree / PR field。
  - generated board view / table view。

- Reject for initial pilot:
  - Vibe Kanban 依存。
  - Task Master を primary SSOT にする。
  - GitHub Projects を canonical state にする。

## Open Questions

- `Doing` の WIP limit は 1 固定か、ユーザー承認で 2 以上にできるか。
- `status` と `gate` は別 field にするか、統合するか。
- `priority` を持たせるか、今は `next action` と `blocked` だけで十分か。
- future worktree integration のために card ID 形式をどうするか。
