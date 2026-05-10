# 機能仕様書: WORKBOARD 初期 pilot

## メタ情報
| 項目 | 内容 |
|------|------|
| ステータス | Approved |
| 作成日 | 2026-05-10 |
| 更新日 | 2026-05-10 |
| 関連ADR | [ADR-0006](../adr/0006-workboard-markdown-ssot.md) |
| 関連Design | [workboard-initial-pilot-design.md](../design/workboard-initial-pilot-design.md) |
| 関連Tasks | [workboard-initial-pilot-tasks.md](../tasks/workboard-initial-pilot-tasks.md) |

## 1. 概要

### 1.1 目的

`WORKBOARD.md` を project state の軽量 SSOT とし、quick-load を重くせずに、gate 前の可視化、依存確認、Green State の根拠確認へつなげる。

この pilot は workflow infrastructure の初期導入であり、rich Kanban や自動 task selection ではない。

### 1.2 ユーザーストーリー

```text
As a Codex LAM user,
I want a small repo-native WORKBOARD that links cards, gates, dependencies, evidence, and verification,
So that I can resume quickly and review project state without rereading the whole repository.
```

### 1.3 スコープ

**含む:**
- root `WORKBOARD.md` の初期 template
- card table と short card detail の Markdown microformat
- `tools/workboard.py validate`
- `tools/workboard.py render`
- generated view としての `docs/project/index.html`
- generated graph としての `docs/project/graph.svg`
- quick-load / gate / release 前の運用契約

**含まない:**
- rich SPA または drag-and-drop Kanban
- `tools/workboard.py next`
- `tools/workboard.py context CARD-ID`
- card 別 HTML
- CI drift check
- GitHub Pages deploy
- external tool adapter
- Vibe Kanban / Task Master / mymir / seite の直接依存

## 2. 機能要求

### FR-001: `WORKBOARD.md` を state SSOT として扱う
- **説明**: board の正本は root `WORKBOARD.md` とし、HTML / SVG は generated view として扱う。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] root `WORKBOARD.md` が存在する
  - [ ] `WORKBOARD.md` に dashboard、workstreams、gate matrix、card table、card detail、dependency map がある
  - [ ] generated HTML / SVG を手編集する必要がない
  - [ ] `SESSION_STATE.md` には board の詳細を重複保存しない

### FR-002: Card ID と Markdown microformat を固定する
- **説明**: 初期 pilot では human-readable で grep しやすい `WB-001` 形式を採用する。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] card ID は `WB-001` のような `WB-` + 3 桁連番である
  - [ ] card table は最小 card fields を持つ
  - [ ] card detail は `### WB-001: Title` の heading で始まる
  - [ ] parser は table row と detail heading の不一致を warning できる

### FR-003: Quick-load を軽く保つ
- **説明**: quick-load は render せず、`SESSION_STATE.md` と `WORKBOARD.md` 冒頭 dashboard までで現在状態を把握できる。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] `WORKBOARD.md` 冒頭 dashboard に active card、blocked、gate、verification summary がある
  - [ ] quick-load の通常手順に `tools/workboard.py render` を含めない
  - [ ] 詳細が必要な時だけ card detail または evidence links へ降りる

### FR-004: 初期 validator warning set を提供する
- **説明**: `tools/workboard.py validate` は、初期 pilot に必要な構造不整合だけを検出する。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] duplicate card ID を error として出す
  - [ ] active card missing next action を warning として出す
  - [ ] blocked card missing blocker reason を warning として出す
  - [ ] dependency target missing を warning として出す
  - [ ] evidence file missing を warning として出す
  - [ ] `Done` / `Released` card missing verification を warning として出す

### FR-005: 初期 render output を提供する
- **説明**: `tools/workboard.py render` は presentation dashboard と dependency overview を生成する。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] `docs/project/index.html` を生成できる
  - [ ] `docs/project/graph.svg` を生成できる
  - [ ] HTML は top band、workstream matrix、card board、detail links を含む
  - [ ] SVG は workstream / active card 周辺の dependency overview を含む
  - [ ] 出力は local file としてレビューできる

### FR-006: Generated artifact policy を明示する
- **説明**: generated files には source path と generated marker を入れ、truth ではないことを示す。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] HTML / SVG に `Generated from WORKBOARD.md by tools/workboard.py` 相当の marker がある
  - [ ] source hash は初期 pilot では任意または非スコープである
  - [ ] generated files を commit 対象にするかは render deterministic 性を見て判断する

### FR-007: Gate / release 前の確認契約を定義する
- **説明**: gate 前と release 前は validate + render を行い、人間が dashboard / graph を見る。
- **優先度**: Should
- **受け入れ条件**:
  - [ ] gate 前の checklist に validate + render が含まれる
  - [ ] release 前の checklist に generated artifacts の diff 確認が含まれる
  - [ ] docs-only change では pytest を省略できるが、workboard parser / renderer 変更時は focused test を選ぶ

## 3. 非機能要求

### NFR-001: 低コンテキスト負荷
- quick-load で全文再読や render を要求しない
- card detail と evidence links で progressive drill-down できる

### NFR-002: Reviewability
- truth は Markdown と Python standard library で読める範囲に置く
- generated HTML / SVG は review surface であり、手編集対象にしない

### NFR-003: Dependency-minimal
- 初期 pilot は Python standard library を優先する
- Mermaid CLI、MkDocs、Docusaurus、GitHub Pages、external Kanban を必須依存にしない

### NFR-004: Deterministic output
- 同じ `WORKBOARD.md` から同じ出力が得られることを目指す
- source hash / CI drift check は後続 wave 候補とする

### NFR-005: Language portability
- 人間が読む本文、card title、context、evidence 説明は project primary language を使ってよい
- 初期 pilot では parser / renderer が読む heading、field name、status value、detail label は安定した英語 token とする
- localized parser labels や多言語切替 UI は初期 pilot の非スコープとする

## 4. データモデル

### 4.1 Card table fields

| Field | 必須 | 説明 |
|------|------|------|
| `ID` | Yes | `WB-001` 形式の card ID |
| `Title` | Yes | card の短い名前 |
| `Status` | Yes | `Todo`, `Active`, `Blocked`, `Done`, `Released` |
| `Gate` | Yes | `requirements`, `design`, `tasks`, `building`, `auditing` など |
| `Workstream` | Yes | 作業のまとまり |
| `Next action` | Active では Yes | 次に実行する最小行動 |
| `Depends on` | No | `WB-001` 形式の依存先。複数は comma 区切り |
| `Evidence` | Done / Released では Yes | docs / tests / artifacts への path。複数は comma 区切り |
| `Verification` | Done / Released では Yes | 実行した確認または未実行理由 |
| `Blocker` | Blocked では Yes | blocking reason |

### 4.2 Card detail fields

各 card detail は次の順序を基本にする。

```markdown
### WB-001: Title

- Goal:
- Context:
- Definition of Done:
- Verification:
- Evidence:
- Next action:
- Blockers:
```

長い実行計画、議論ログ、検証ログは `docs/tasks/` または `docs/artifacts/` へ逃がす。

## 5. インターフェース

### CLI

```text
python tools/workboard.py validate
python tools/workboard.py render
```

初期 pilot では `WORKBOARD.md` を default input とし、output は以下へ固定する。

- `docs/project/index.html`
- `docs/project/graph.svg`

## 6. 権限と安全性

| 変更対象 | 権限等級 | 理由 |
|---------|---------|------|
| `WORKBOARD.md` template | SE | project state SSOT に関わる |
| validator warning set | SE | gate 前の見落とし防止に関わる |
| generated HTML / SVG | PG | generated view であり truth ではない |
| source hash / CI drift check | SE | release contract と CI に関わるため後続判断 |
| external adapter | PM | workflow と dependency surface を広げるため非スコープ |

## 7. 制約事項

- `SESSION_STATE.md` は quick-load 用に薄く保つ
- `WORKBOARD.md` は長い議論ログを抱え込まない
- generated artifacts は truth ではない
- `.claude/` や Claude Code hook を primary control surface にしない
- 初期 pilot では pre-commit hook を必須にしない
- template 利用者の本文言語は固定しない。ただし `ID`, `Status`, `Goal`, `Todo`, `Active` など parser が読む token は初期 pilot では英語固定とする

## 8. 依存関係

- [WORKBOARD Visualization Synthesis Decision](../artifacts/workboard-research/09-synthesis-options.md)
- [WORKBOARD Review Reinforcement](../artifacts/workboard-research/10-review-reinforcement.md)
- [quick-load skill](../../.agents/skills/quick-load/SKILL.md)
- [quick-save skill](../../.agents/skills/quick-save/SKILL.md)
- [Quick Load / Save policy](../internal/08_QUICK_LOAD_SAVE.md)

## 9. テスト観点

- duplicate card ID を検出できる
- missing dependency target を検出できる
- missing evidence file を検出できる
- Active / Blocked / Done / Released の必須 field 不足を検出できる
- sample `WORKBOARD.md` から deterministic な HTML / SVG を生成できる
- generated marker が HTML / SVG に入る
- quick-load 手順が render を要求しない

## 10. 未決定事項

- [ ] generated HTML / SVG を初回から commit 対象にするか
- [ ] source hash を後続 wave で入れるか
- [ ] `tools/workboard.py context CARD-ID` をいつ追加するか
- [ ] `tools/workboard.py next` をいつ追加するか

## 11. 変更履歴
| 日付 | 変更者 | 内容 |
|------|--------|------|
| 2026-05-10 | Codex | 初版作成 |
