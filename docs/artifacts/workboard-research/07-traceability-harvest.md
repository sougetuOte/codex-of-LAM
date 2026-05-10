# Traceability / Requirements Engineering Harvest Notes

Status: Raw harvest
Date: 2026-05-10

## Purpose

`WORKBOARD.md` と generated HTML / SVG を、単なる task board ではなく、
requirements / design / tasks / code / tests / review のつながりを見える化する
traceability surface にするための材料を集める。

## Harvest Policy

- safety-critical / enterprise の重い traceability を、そのまま持ち込まない。
- LAM の gate 判断に必要な最小 trace を拾う。
- 「何が欠けているか」「何が余計に作られているか」を発見できる構造を重視する。

## Sources

| Source | URL | Notes |
| --- | --- | --- |
| NASA SWE-047 Traceability Data | https://swehb.nasa.gov/x/vgH7 | electronic traceability data, review, holes, impact analysis。 |
| NASA SWE-052 Bidirectional Traceability | https://swehb.nasa.gov/x/7QL7 | higher-level requirements と software requirements の bidirectional traceability。 |
| NASA SWE-059 Bidirectional Traceability | https://swehb.nasa.gov/pages/viewpage.action?pageId=16451645 | software requirements と design の traceability。 |
| NASA SWE-064 Design to Code Traceability | https://swehb.nasa.gov/pages/viewpage.action?pageId=38142108 | design と code の traceability。 |
| NASA Software Engineering Handbook | https://standards.nasa.gov/standard/nasa/nasa-hdbk-2203 | NPR 7150.2 実装の guidance。 |
| ISO/IEC/IEEE 29148:2018 | https://www.iso.org/standard/72089.html | requirements engineering の life-cycle process / information items。 |
| IEEE/ISO/IEC 29148-2018 | https://standards.ieee.org/ieee/29148/6937/ | good requirement, attributes, lifecycle requirements process。 |
| Task Master RPG Method | https://docs.task-master.dev/capabilities/rpg-method | capability decomposition, dependency graph, entry/exit criteria, test strategy。 |

## Findings

### NASA SWE-047: Traceability Data

- traceability は requirements が design, implementation, verification に運ばれているかを
  確認するためのもの。
- 欠落した requirements、親 requirement を持たない extra functionality、change impact を
  見つける価値がある。
- unique identifiers が重要。
- electronic access は review コスト削減に効く。

Classification: `adopt_candidate` for principle

### NASA Bidirectional Traceability

- forward trace と backward trace の両方があると、欠落と余計な実装を検出できる。
- LAM では full formal traceability matrix ではなく、card / spec / ADR / test / artifact の
  bidirectional link を最小化して持つのがよい。
- `evidenced_by`, `implements`, `verifies`, `depends_on` の edge type が有効。

Classification: `adopt_candidate`

### ISO/IEC/IEEE 29148

- requirements engineering は lifecycle 全体に関わり、情報項目と process を持つ。
- LAM に全部入れると重すぎるが、requirements の属性、good requirement、process artifact の
  考え方は gate 文書に合う。
- 採用するなら "lightweight traceability" として限定する。

Classification: `decide_later`

### Task Master RPG

- decomposition, explicit dependencies, topological ordering, implementation roadmap,
  test strategy は LAM の `WORKBOARD.md` と相性がよい。
- requirements traceability を task generation 側にも接続できる。

Classification: `adopt_candidate`

## Minimal LAM Trace Model Candidate

Formal requirements traceability matrix ではなく、以下の最小 trace を持つ。

| Source | Target | Edge | Purpose |
| --- | --- | --- | --- |
| North Star | Workstream | `decomposes_to` | 目標からラインへの分解 |
| Workstream | Card | `contains` | 作業ラインの範囲 |
| Spec / Requirement | Card | `implemented_by` | requirement が作業へ落ちているか |
| ADR | Card | `constrains` | 判断理由が実装に反映されるか |
| Card | Test / Review / Artifact | `verified_by` | 完了判断の根拠 |
| Card | Card | `depends_on` / `blocks` | 順序・依存 |
| Card | File path | `touches` | 影響範囲 |
| Card | Commit / PR | `delivered_by` | 実施結果 |

## Potential Dashboard Signals

- Requirement without card: 仕様が作業化されていない。
- Card without requirement / rationale: 何のための作業か不明。
- Done card without verification: Green State が明示されていない。
- Implementation without linked decision: design drift の疑い。
- Blocked card with no blocker reason: 管理不能な停滞。
- Changed spec with downstream cards not reviewed: impact analysis が必要。

## Combination Ideas

### C1: Lightweight Traceability Matrix

`WORKBOARD.md` の generated HTML に matrix を出す。

- rows: specs / ADRs / workstreams
- columns: cards / verification / status

### C2: Trace Warnings In Validator

`tools/workboard.py validate` が以下を警告する。

- missing evidence file
- missing dependency target
- card marked Done without verification
- active card without next action
- spec / ADR referenced but file missing

### C3: Impact Analysis View

将来、ある spec / ADR が変わったとき、影響する cards / tests / artifacts を出す。

### C4: Gate Readiness View

gate 前に必要な trace が揃っているかだけを見る view。

例:

- requirements gate: North Star / workstream / spec があるか。
- design gate: ADR / design constraints が linked されているか。
- building gate: tasks / DoD / verification plan があるか。
- auditing gate: review findings / verification evidence があるか。

## Adoption Candidates

- Baseline now:
  - card ID と evidence links を必須化する。
  - `Done` / `Released` に verification を必須化する。
  - explicit dependency links を持つ。

- Next wave:
  - traceability matrix view。
  - gate readiness warning。
  - impact analysis helper。

- Reject for initial pilot:
  - full enterprise RTM。
  - code element / test case までの完全 bidirectional trace。
  - ISO 29148 の文書体系全体の導入。

## Open Questions

- `spec -> card` trace を `WORKBOARD.md` に持つか、各 `docs/tasks/*.md` に持つか。
- `touches` file path は初期から必須にするか。
- commit / PR trace は local-only project でも必要か。
- generated dashboard の red flag に trace warning をどこまで出すか。
