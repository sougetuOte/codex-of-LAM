# Codex hooks / full-review Position

Status: Accepted
Date: 2026-05-09

## Purpose

Codex に lifecycle hooks が追加されたため、公開 template の説明から hooks を消し切るべきか、旧 LAM の `full-review` 相当をどう扱うべきかを小判断する。

## AoT Decomposition

| Atom | 判断内容 | 依存 |
|------|----------|------|
| A1 | 現行公開 template に Codex hooks をどう表現するか | なし |
| A2 | `full-review` 相当を今すぐ runtime として戻すか | A1 |
| A3 | 現時点の review 代替運用をどう示すか | A1 |

## MAGI

### A1: Codex hooks の表現

**MELCHIOR**: 公式 docs では `features.codex_hooks = true`、`hooks.json`、`PreToolUse` / `PostToolUse` / `Stop` が存在する。将来性を隠すと template が古く見える。

**BALTHASAR**: hooks は feature flag 配下であり、完全な enforcement boundary ではない。旧 Claude Hooks をそのまま復活させる表現は誤解を招く。

**CASPAR**: Codex hooks は optional advanced path として明記する。常用前提ではなく、trusted project で段階導入する lifecycle extension とする。

### A2: full-review 相当の再導入

**MELCHIOR**: `Stop` hook は追加継続プロンプトを作れるため、旧 `full-review` の「もう一周」挙動に近い。`PostToolUse` も検証結果レビューに使える。

**BALTHASAR**: 現時点で template runtime に入れるには、Windows、sandbox、project trust、hook fail-open/fail-closed の検証が不足している。

**CASPAR**: 今すぐ active runtime として戻さない。将来の Codex-native `full-review` pilot 候補として tasks / docs に位置づける。

### A3: 現時点の review 代替運用

**MELCHIOR**: `context-harvest` で広い evidence を薄く採掘し、`magi` で判断を構造化すれば、かなり近い review loop を実現できる。

**BALTHASAR**: これは自動収束ではなく、人間と Living Architect の gate 判断に依存する。旧 `full-review` と同一視してはいけない。

**CASPAR**: 現行は `context-harvest` + `magi` + review pane + focused verification を推奨運用とする。

## Reflection

致命的な見落としなし。Codex hooks の存在を認めつつ、旧 Claude runtime を戻さない方針と両立する。

## Decision

- Codex hooks は `optional advanced path` として公開文書・slides に戻す。
- 旧 `full-review` command は戻さない。
- Codex-native `full-review` は `Stop` / `PostToolUse` / `PermissionRequest` を使う将来 pilot 候補とする。
- 現時点の代替は `context-harvest` + `magi` + review pane + focused verification と表現する。

## Impact

- README / CHEATSHEET / slides で、hooks を「存在しない」扱いにしない。
- architecture slides は「常駐自動化ではない」から「feature-flagged optional hooks」として再調整する。
