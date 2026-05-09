# Contributing

このリポジトリは Codex App 前提の Living Architect Model template / starter kit です。
変更するときは、単にファイルを増やすのではなく、要件、設計、タスク、検証結果が追える状態を保ってください。

## 基本方針

- `AGENTS.md` の truth hierarchy と phase / gate を優先する。
- 変更は review しやすい小さな単位に分ける。
- project-facing documentation は日本語を canonical とし、英語版は追従版として扱う。
- 旧 Claude Code 資料は Codex の主制御面にしない。archive / delete 判断は `docs/migration/` の gate に従う。

## 通常の進め方

1. `SESSION_STATE.md` がある場合は quick-load で現在地を確認する。
2. 要件、設計、タスクのどれを変えるのかを明確にする。
3. BUILDING では、可能な範囲で t-wada style TDD の Red / Green / Refactor を使う。
4. ドキュメントのみの変更では `git diff --check` を最小検証とし、挙動に関わる変更では focused test を選ぶ。
5. commit 前に、残リスクと次にやることを `SESSION_STATE.md` または該当 task に残す。

## 参照先

- `AGENTS.md`
- `.codex/workflows/`
- `docs/internal/02_DEVELOPMENT_FLOW.md`
- `docs/internal/03_QUALITY_STANDARDS.md`
- `docs/internal/08_QUICK_LOAD_SAVE.md`
- `docs/tasks/codex-lam-replacement-tasks.md`
