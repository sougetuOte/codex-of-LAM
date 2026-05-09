# Security Policy

このリポジトリは Codex LAM の運用ルール、workflow、template 資産を扱います。
秘密情報、認証情報、承認境界、外部 tool contract の drift は、コード変更と同じくらい慎重に扱います。

## 報告と扱い

- secret、token、private key、認証情報を commit しない。
- 認証情報が混入した疑いがある場合は、まず該当 secret を無効化または rotate し、履歴対応を検討する。
- security issue は通常の機能改善と混ぜず、影響範囲、再現条件、暫定回避策を分けて記録する。
- 外部 API、Codex App、GitHub、MCP、plugin / skill の仕様が関わる場合は、現在の一次情報またはローカル実環境で確認する。

## Codex 実行時の注意

- 破壊的操作、外部通信、権限昇格、credential access は明示承認の対象にする。
- sandbox や approval の制限を回避するための迂回策を採らない。
- Windows の credential manager、temporary directory、ACL の問題は、環境依存の可能性を明記する。
- `.claude/` 配下の legacy automation は参考資料であり、Codex の canonical enforcement として扱わない。

## 参照先

- `AGENTS.md`
- `docs/internal/07_SECURITY_AND_AUTOMATION.md`
- `docs/internal/09_MODEL_AND_CONTEXT_POLICY.md`
- `docs/internal/10_DISTRIBUTION_MODEL.md`
