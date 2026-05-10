# License / Dependency / Fork Feasibility Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`WORKBOARD.md` / static dashboard / graph tooling を作る際に、外部 tool を fork して
取り込むべきか、思想だけ借りるべきか、依存を追加すべきかを判断する材料を集める。

## Harvest Policy

- 法的助言ではなく、設計判断のための risk notes として扱う。
- license / dependency / runtime / Windows / template 再利用性を重視する。
- 初期 pilot は dependency-minimal を優先する。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| GitHub Licensing a repository | https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository | public repo と license の基本。 |
| GitHub Licenses API | https://docs.github.com/rest/licenses/licenses | Licensee / SPDX detection の説明。 |
| Open Source Initiative licenses | https://opensource.org/licenses | OSI-approved license list。 |
| GNU AGPL v3 | https://www.gnu.org/licenses/agpl-3.0.html.en | network server software 向け copyleft license。 |
| Apache License 2.0 | https://www.apache.org/licenses/ | Apache Software Foundation license info。 |
| Vibe Kanban GitHub | https://github.com/BloopAI/vibe-kanban | Apache-2.0, Rust + Node/pnpm, sunsetting notice。 |
| Vibe Kanban security | https://vibekanban.com/security | local-first, Apache 2.0 license の説明。 |
| mymir | https://mymir.dev/ | AGPL v3, Postgres, Bun, MCP native, self-hosted。 |
| Task Master npm | https://www.npmjs.com/package/task-master-ai | MIT with Commons Clause, Node, API/model key requirements。 |
| Task Master requirements | https://docs.task-master.dev/getting-started/quick-start/requirements | Node.js と model API key requirements。 |
| Coddo Product Hunt | https://www.producthunt.com/products/coddo | task-first Kanban, Codex CLI support, desktop app。 |

## Findings

### General licensing

- GitHub は license file の追加を推奨している。license がないと再利用権限が不明確になる。
- GitHub license detection は license file matching が中心で、依存 license は別問題。
- OSI license は reuse の共通基盤だが、copyleft / permissive / source-available variants の差は大きい。

Classification: `adopt_candidate` for caution

### AGPL

- GNU AGPL は network server software における community cooperation を意図した copyleft license。
- mymir のような AGPL tool を fork / embed すると、この repo の template / public reuse 方針に
  強い制約や判断コストを持ち込む可能性がある。
- 思想を参考にするだけなら問題は小さいが、コード取り込みは避けるのが無難。

Classification: `reject_candidate` for code embedding

### Apache-2.0 / Vibe Kanban

- Vibe Kanban は GitHub 上で Apache-2.0 license と表示されている。
- ただし Rust + Node.js + pnpm + multi-package 構成で、LAM starter に直接取り込むには重い。
- product は sunsetting 表示があり、依存先としては不安定。
- 概念としては、task-first Kanban, isolated worktree, review diff, local-first が参考になる。

Classification: `adopt_candidate` for concept, `reject_candidate` for fork

### Task Master

- npm package は MIT with Commons Clause と表示されている。
- Commons Clause は commercial/service competition 制限を含むため、通常の permissive MIT と同じ扱いにしない。
- Node.js と model API key / CLI integration が要求される。
- primary SSOT として入れると `.taskmaster/` と `WORKBOARD.md` の二重管理になる。

Classification: `adopt_candidate` for method, `reject_candidate` for embedded dependency

### mymir

- AGPL v3, Postgres, Bun, MCP native, web UI という構成。
- project graph / context retrieval の思想は非常に近い。
- ただし dependency surface が大きく、個人 template / multi-PC / Codex App on Windows の
  初期導入には重い。

Classification: `adopt_candidate` for architecture ideas, `reject_candidate` for direct adoption

### Coddo

- task-first Kanban, auto Git branches, skills, Codex CLI support の思想は近い。
- license / internal data format / self-hosting / export について確認が必要。
- desktop app であるため、repo-native SSOT の代わりにはしない。

Classification: `decide_later`

## Dependency Risk Matrix

| Candidate | License Risk | Runtime Risk | SSOT Risk | Initial Pilot Fit |
| --- | --- | --- | --- | --- |
| Native Python generator | Low | Low | Low | High |
| Mermaid source only | Low | Low | Low | High |
| Mermaid CLI required | Low | Medium | Low | Medium |
| MkDocs / Material | Low | Medium | Medium | Medium |
| mdBook | Low | Medium | Medium | Medium |
| Docusaurus | Low | High | Medium | Low |
| Vibe Kanban fork | Medium | High | High | Low |
| Task Master dependency | Medium | Medium | High | Low |
| mymir fork/embed | High | High | High | Low |
| Coddo integration | Unknown | Medium | Medium | Unknown |

## Combination Ideas

### C1: No Fork Baseline

初期 pilot は外部 tool を fork しない。

- `WORKBOARD.md`
- `tools/workboard.py`
- generated static HTML / SVG

### C2: Dependency Rings

依存を ring で管理する。

1. Ring 0: Markdown + Python standard library
2. Ring 1: small Python package or Mermaid source
3. Ring 2: docs generator / Mermaid CLI / GitHub Pages
4. Ring 3: external app / DB / MCP / fork

初期 pilot は Ring 0-1 に留める。

### C3: Import/Export Adapters Later

外部 tool は primary state ではなく import/export 先にする。

- Task Master tasks.json export
- GitHub Projects CSV / issue mapping
- mymir-like graph JSON export
- Mermaid / SVG render export

### C4: License Gate

外部コードを取り込む前に、以下を必ず確認する。

- license
- dependency license
- runtime requirements
- Windows support
- data export
- whether it becomes SSOT
- template user burden

## Adoption Candidates

- Baseline now:
  - fork しない。
  - external tools は思想と data model だけ借りる。
  - Python standard library 寄りで generator を始める。

- Next wave:
  - Mermaid CLI / MkDocs / mdBook を optional adapter として比較する。
  - GitHub Projects export/import を後で検討する。
  - Coddo / seite は license と exportability を追加調査する。

- Reject for initial pilot:
  - mymir embed / fork。
  - Vibe Kanban fork。
  - Task Master primary SSOT。
  - Docusaurus 直採用。

## Open Questions

- generated HTML / SVG を repo に commit する場合、license header や generated marker は必要か。
- `tools/workboard.py` を MIT / Apache-2.0 repo の一部として公開する前提で問題ないか。
- Coddo / seite の license と export format を次に確認するか。
- GitHub Projects 連携は optional integration として価値があるか。
