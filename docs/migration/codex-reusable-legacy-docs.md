# Codex へ再利用する旧 docs 資産メモ

Status: Draft
Date: 2026-04-30

## 目的

Claude Code 版 LAM の旧 `docs/specs/`、`docs/design/`、`docs/internal/` には、Claude runtime に依存する記述と、Codex でも活かせる設計思想が混在している。

このメモは、Codex LAM へ再利用すべき思想・仕様・判断を、Wave 2 の棚卸しで見落とさないための入口である。
requirements はすでに承認済みなので、このメモは requirements を再オープンするものではない。
次に design / tasks / migration notes へ必要分を反映する。

## 再利用候補

### 1. モデル選定・モデルルーティング

参照:

- `docs/adr/0001-model-routing-strategy.md`
- `docs/design/v4.0.0-immune-system-design.md`

Codex へ活かす内容:

- routine 判定では軽いモデルを使い、難しい統合判断だけ強いモデルへ上げる。
- 最上位モデルを hooks / routine 判定で消費しない。
- Codex では自動 subagent routing ではなく、設計・レビュー・task generation 時のモデル選定ガイドとして扱う。
- subagent 使用は、Codex の制約に合わせて、ユーザーが明示的に依頼した場合に限定する。

### 2. Green State / 完了判定

参照:

- `docs/specs/green-state-definition.md`
- `docs/design/v4.0.0-immune-system-design.md`
- `docs/specs/gitleaks-integration-spec.md`
- `docs/design/gitleaks-integration-design.md`

Codex へ活かす内容:

- 完了判定を曖昧な自己申告にしない。
- test、lint、対応可能 issue、仕様差分、security check を組み合わせて building / auditing gate の完了条件にする。
- Claude Stop hook ではなく、Codex の review checklist、pytest helper、CLI、手動 gate へ移す。

### 3. TDD introspection

参照:

- `docs/specs/tdd-introspection-v2.md`
- `docs/design/v4.0.0-immune-system-design.md`

Codex へ活かす内容:

- test result を構造化して残す。
- FAIL から PASS への変化や TDD pattern を retro / docs に反映する。
- Claude `PostToolUse` / Stop hook ではなく、pytest helper、CLI、review checklist、SESSION_STATE の検証項目として扱う。

### 4. Scalable Code Review

参照:

- `docs/specs/scalable-code-review-spec.md`
- `docs/specs/scalable-code-review-phase5-spec.md`
- `docs/design/scalable-code-review-design.md`

Codex へ活かす内容:

- 大きい差分を静的解析、chunking、map-reduce review、階層レビュー、依存グラフで扱う。
- secret scan を review / audit の早い段階へ入れる。
- Codex では `/full-review` や Claude agent 実行ではなく、review procedure、CLI、pytest helper、手動/明示的な multi-agent review として再表現する。

### 5. Security / permission / read-write policy

参照:

- `docs/adr/0004-bash-read-commands-allow-list.md`
- `docs/internal/07_SECURITY_AND_AUTOMATION.md`
- `.claude/rules/security-commands.md`
- `.claude/rules/permission-levels.md`

Codex へ活かす内容:

- read-only 操作は比較的広く許容する。
- destructive 操作、workspace 外 write、権限外操作は明示確認する。
- permission level の考え方は、Claude hook ではなく、Codex の作業運用ルール、review gate、CLI validator として再表現する。

### 6. Upstream-first / MCP / 外部仕様確認

参照:

- `docs/adr/0003-context7-vs-webfetch.md`
- `docs/internal/05_MCP_INTEGRATION.md`
- `.claude/rules/upstream-first.md`

Codex へ活かす内容:

- 仕様確認では一次情報を優先する。
- 自動フローでは外部 fetch を必須にしない。
- 対話中に必要な場合だけ、公式 docs や MCP / web を使う。
- 取得不能な場合は警告し、人間判断へ戻す。

### 7. Requirements / development / quality standards

参照:

- `docs/internal/01_REQUIREMENT_MANAGEMENT.md`
- `docs/internal/02_DEVELOPMENT_FLOW.md`
- `docs/internal/03_QUALITY_STANDARDS.md`
- `docs/internal/99_reference_generic.md`

Codex へ活かす内容:

- Definition of Ready。
- spec / design / tasks / tests の同期。
- Red / Green / Refactor。
- SSOT と living documentation。
- 仕様が薄いまま走らない。
- task は atomic に切る。
- docs は付録ではなく SSOT として扱う。

### 8. Multi-perspective decision making

参照:

- `docs/internal/06_DECISION_MAKING.md`
- `docs/specs/magi-skill-spec.md`
- `.claude/skills/magi/`
- `.claude/skills/lam-orchestrate/`

Codex へ活かす内容:

- 複雑な判断では複数観点でレビューする。
- Codex では自動 skill / subagent 実行ではなく、ユーザーが明示的に依頼したときの軽量 subagent review、または review checklist として扱う。
- AoT / Reflection の考え方は、design review や task decomposition に移す。

### 9. Cross-module blame / dependency-aware review

参照:

- `docs/specs/cross-module-blame-spec.md`
- `docs/design/cross-module-blame-design.md`

Codex へ活かす内容:

- 変更の帰責を単一ファイルだけで判断しない。
- upstream / downstream、契約カード、依存グラフを review の補助情報にする。
- Codex では review procedure や migration notes に落とす。

## 次の扱い

- tasks に旧 docs 資産の棚卸し項目を追加する。
- design review 時に、このメモの内容を Codex LAM design へ反映するか判断する。
- Wave 2C の legacy inventory では、`.claude/` だけでなく旧 `docs/` 資産も対象に含める。
- requirements は承認済みのまま維持し、必要があれば次の revision として扱う。
