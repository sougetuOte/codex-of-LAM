# TDD Introspection Summary Example

Status: Draft  
Date: 2026-04-30

## Summary Output

```text
TDD Introspection Summary
- Total records: 2
- PASS: 1
- FAIL: 1
- UNKNOWN: 0
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
  - UNKNOWN: 0
- FAIL->PASS candidates:
  - tests/test_tdd_introspection_cli.py::test_main_summary_prints_read_only_summary
- Notes:
  - summary 出力の整形を確認し、FAIL -> PASS 候補 1 件を検出できた
```

## メモ

- この例では local log から read-only に `summary` を生成した
- reviewed result は retro 側へ転記し、raw log は Git 管理しない
