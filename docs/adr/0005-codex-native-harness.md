# ADR-0005: Codex-native harness への置き換え

Date: 2026-04-30
Status: Accepted

## Context

Living Architect Model は Claude Code を前提に作られている。
リポジトリには `.claude/settings.json`、hook scripts、slash commands、subagent prompts など、Claude Code 固有の資産が含まれている。

Codex は Claude Code と異なる協働モデル、権限モデル、ツール実行モデルを持つ。
そのため、`.claude/` を名前だけ変えて Codex の実行面として扱うと、実際には存在しない hook、slash command、subagent の挙動を前提にした、誤解を招くハーネスになる。

一方で、`.claude/` 配下には捨てるべきでない運用知識も含まれている。
rules、commands、hooks、agents/subagents、settings、guides、checklists のうち、Codex で安全かつ自然に対応できるものは、Codex-native な形へ移す必要がある。

## Decision

Codex LAM は、Claude Code の runtime 互換ではなく、Codex-native な file-driven harness として構成する。

- `AGENTS.md` を Codex の主要な instruction surface とする。
- `.codex/manifest.json` で有効な harness contract を宣言する。
- `.codex/workflows/` で `PLANNING`、`BUILDING`、`AUDITING` を定義する。
- `docs/specs/`、`docs/adr/`、`docs/design/`、`docs/tasks/` をレビュー可能な planning surface とする。
- Python tests で manifest、required artifacts、phase/gate contract を検証する。
- `SESSION_STATE.md` を手動 quick-load/save の最短復元メモとして使う。

`.claude/` 配下の資産は legacy input として扱う。
Codex の実行時ソースにはしないが、Wave 2 以降で棚卸しし、Codex で対応可能なものは最大限移設または再実装する。

特に `.claude/agents/` や subagent 定義は、原則として Codex の役割別レビュー観点、作業手順、workflow、または task generation guidance として文書化する。
ただし一律変換はしない。design または tasks を作る時点で、各 agent/subagent ごとに Codex での扱いを個別確認する。

## Alternatives Considered

### A. `.claude/` をそのまま `.codex/` にリネームする

却下。
ファイル名だけを変えても、hook semantics、slash commands、subagent assumptions は Claude Code 固有のまま残る。
これは Codex harness として誤解を招く。

### B. Claude harness を残し、Codex 用の補足だけを追加する

却下。
どちらの runtime が権威を持つのか曖昧になり、`.claude/` と `.codex/` の二重管理を生む。

### C. Codex-native file contract を採用する

採用。
現在の Codex の協働モデルに合わせやすく、レビュー可能で、テスト可能で、ユーザー承認ゲートとも相性がよい。

### D. Claude assets を全面削除してゼロから作る

却下。
`.claude/` には移行すべき運用知識が含まれている。
最初の wave で破壊的に削除すると、移設すべきルールや検証観点を失うリスクがある。

## Consequences

- Wave 1 は置き換え scaffold を作る。legacy file の全面削除はしない。
- Wave 2 は `.claude/` 配下の rules、commands、hooks、agents/subagents、settings、guides、checklists、運用メモを棚卸しする。
- Wave 2 では旧 `docs/specs/`、`docs/adr/`、`docs/design/`、`docs/internal/` に残る設計知見も棚卸しし、Codex-native に再表現できるものだけを採用候補にする。
- 棚卸しした項目は、Codex ハーネスへ移設、Codex-native workflow/CLI/pytest/review procedure として再実装、legacy 参考資料として維持、Claude-only runtime glue として非推奨化、のいずれかに分類する。
- quick-load/save は、当面 `SESSION_STATE.md` を手動共有する運用で扱う。
- Codex harness は opaque runtime hooks ではなく、人間に見える workflow discipline と executable checks に依存する。
- 既存 Claude assets と Codex documents が矛盾する場合、Codex 側を優先する。
