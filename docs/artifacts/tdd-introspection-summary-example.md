# TDD Introspection Summary Example

Status: Draft  
Date: 2026-04-30

## Summary Output

```text
TDD Introspection Summary
- Total records: 3
- PASS: 1
- FAIL: 1
- UNKNOWN: 1
- FAIL->PASS candidates: 1
Candidates:
- tests/test_tdd_introspection_cli.py::test_main_summary_prints_read_only_summary
```

## retro 転記例

```markdown
### TDD Introspection

- Summary:
  - PASS: 1
  - FAIL: 1
  - UNKNOWN: 1
- FAIL->PASS candidates:
  - tests/test_tdd_introspection_cli.py::test_main_summary_prints_read_only_summary
- Notes:
  - summary 出力の整形を確認し、FAIL -> PASS 候補 1 件を検出できた
  - focused pytest は Windows ACL により tmp_path setup で失敗したため UNKNOWN として扱った
```

## メモ

- この例では local session log から read-only に `summary` を生成した
- reviewed result は retro 側へ転記し、raw log は Git 管理しない
- `SESSION_STATE.md` には raw log ではなく、直近 summary の要点だけ残す
- `UNKNOWN` は環境要因と実装不明点を分けて扱う
