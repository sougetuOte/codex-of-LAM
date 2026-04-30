# 機能仕様書: TDD Introspection Helper

## メタ情報
| 項目 | 内容 |
|------|------|
| ステータス | Draft |
| 作成日 | 2026-04-30 |
| 更新日 | 2026-04-30 |
| 関連ADR | なし |

## 1. 概要

### 1.1 目的

Codex LAM の BUILDING フェーズで、TDD の進行から retro に有用な入力を
軽量に残すための optional helper を定義する。

### 1.2 ユーザーストーリー

```
As a Codex LAM user,
I want a lightweight helper that records focused TDD transitions,
So that I can run retro with concrete FAIL -> PASS evidence without relying on runtime hooks.
```

### 1.3 スコープ

**含む:**
- Codex-native CLI または pytest helper としての最小仕様
- FAIL -> PASS 遷移と focused test 実行結果の記録
- retro 用の入力を残すための出力形式
- 手動 workflow と共存する運用

**含まない:**
- Claude `PostToolUse` / Stop hook の直移植
- 常時自動記録
- ルール自動生成
- Green State の自動判定置き換え

## 2. 機能要求

### FR-001: Optional helper として実行できる
- **説明**: helper は Codex LAM の必須 gate ではなく、必要時のみ明示実行できる。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] BUILDING の必須手順に組み込まれない
  - [ ] CLI または pytest helper のどちらか一方で成立する
  - [ ] helper を使わない通常 BUILDING 手順と矛盾しない

### FR-002: focused test の結果を軽量記録する
- **説明**: helper は focused test 実行の要約を、retro に再利用できる最小粒度で残す。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] 記録対象は test command、timestamp、対象テスト、PASS/FAIL を含む
  - [ ] 結果保存は workspace 内の review 可能なテキスト形式とする
  - [ ] 結果が取れない場合は silent failure せず、記録不能を明示する

### FR-003: FAIL -> PASS 遷移を retro 入力として残せる
- **説明**: helper は連続した実行結果から FAIL -> PASS を後で判定できるようにする。
- **優先度**: Must
- **受け入れ条件**:
  - [ ] 同一対象の複数実行を時系列で追える
  - [ ] retro 実行前に、FAIL -> PASS 候補を人間が読める
  - [ ] helper 自身は rule candidate を自動生成しない

### FR-004: spec / design / tasks / docs 同期の確認を促せる
- **説明**: helper は code changes だけで完結したように見せず、同期確認を促す。
- **優先度**: Should
- **受け入れ条件**:
  - [ ] 出力に sync reminder を含められる
  - [ ] 少なくとも `spec`, `design`, `tasks`, `docs` の確認対象を示せる

## 3. 非機能要求

### NFR-001: 低運用コスト
- 手動 BUILDING を置き換えず、追加負荷が小さいこと
- 長い常駐プロセスや event-driven runtime に依存しないこと

### NFR-002: Reviewability
- 保存先と出力形式は人間がそのまま読めること
- review 時に helper の挙動を説明できること

### NFR-003: Runtime independence
- Claude hook、slash command、frontmatter metadata に依存しないこと

## 4. データ形式

最小の 1 行 1 record 形式を想定する。

```text
timestamp=<iso8601> status=<PASS|FAIL|UNKNOWN> target=<nodeid-or-command> command="<test command>"
```

必要なら次の補助項目を追加できる。

- `notes=<short summary>`
- `sync_reminder=<spec|design|tasks|docs>`

## 5. インターフェース

### CLI 案

```text
codex-tdd-introspection record --status PASS --target tests/test_example.py::test_case --command "pytest tests/test_example.py::test_case"
```

初手の実装は CLI を先行する。
理由は、Codex-native な明示実行として導入しやすく、pytest runtime への結合を後回しにできるため。

### pytest helper 案

- focused test 実行後に明示呼び出しする fixture / helper
- 自動 hook ではなく、利用側が opt-in で呼ぶ
- CLI 先行の運用が安定した後の後続候補として扱う

## 6. 権限と安全性

| 変更対象 | 権限等級 | 理由 |
|---------|---------|------|
| helper の結果ファイル追記 | SE | workspace 内の補助記録だが write を伴う |
| retro 用の集計表示 | PG | read-only の要約表示 |
| rule candidate 自動生成 | PM | 本 spec の対象外。将来判断が必要 |

## 7. 制約事項

- `permission-level classification` の standalone validator 化とは切り分ける
- Green State の自動収束ロジックには接続しない
- 保存先は `.claude/` 直下を canonical にしない
- 初手の正式保存先は `docs/artifacts/tdd-introspection-records.log` とする

## 8. 依存関係

- `docs/internal/02_DEVELOPMENT_FLOW.md`
- `docs/migration/legacy-harvest-decision.md`
- `docs/specs/tdd-introspection-v2.md`（legacy reference）

## 9. テスト観点

- helper 未使用でも BUILDING が成立すること
- PASS / FAIL / UNKNOWN を区別して記録できること
- 同一 target の連続実行を retro が読めること
- 記録不能時に失敗理由を人間が確認できること

## 10. 未決定事項

- [x] 初手の実装は CLI を先行し、pytest helper は後続候補とする
- [x] 記録ファイルの正式保存先は `docs/artifacts/tdd-introspection-records.log` とする
- [x] この wave では read-only な `summary` 表示までを持ち、rule candidate 生成や retro 自動連携は持たない

## 11. 変更履歴
| 日付 | 変更者 | 内容 |
|------|--------|------|
| 2026-04-30 | Codex | 初版作成 |
