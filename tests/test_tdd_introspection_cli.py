from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from codex_lam.tdd_introspection_cli import (
    DEFAULT_RECORD_PATH,
    TddIntrospectionCliError,
    append_record,
    format_record,
    format_summary,
    main,
    parse_record,
    summarize_records,
)


def test_append_record_writes_minimal_record() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        output_path = append_record(
            root,
            status="PASS",
            target="tests/test_example.py::test_case",
            command="pytest tests/test_example.py::test_case",
            timestamp="2026-04-30T12:00:00+00:00",
        )

        assert output_path == root / DEFAULT_RECORD_PATH
        assert output_path.read_text(encoding="utf-8") == (
            'timestamp=2026-04-30T12:00:00+00:00 '
            'status=PASS '
            'target="tests/test_example.py::test_case" '
            'command="pytest tests/test_example.py::test_case"\n'
        )


def test_append_record_writes_optional_fields() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        output_path = append_record(
            root,
            status="FAIL",
            target="tests/test_example.py::test_case",
            command="pytest tests/test_example.py::test_case",
            notes="missing edge case",
            sync_reminder="spec",
            timestamp="2026-04-30T12:00:00+00:00",
        )

        assert output_path.read_text(encoding="utf-8") == (
            'timestamp=2026-04-30T12:00:00+00:00 '
            'status=FAIL '
            'target="tests/test_example.py::test_case" '
            'command="pytest tests/test_example.py::test_case" '
            'notes="missing edge case" '
            'sync_reminder="spec"\n'
        )


def test_append_record_rejects_invalid_status() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        with pytest.raises(TddIntrospectionCliError, match="status must be one of"):
            append_record(
                root,
                status="BROKEN",
                target="tests/test_example.py::test_case",
                command="pytest tests/test_example.py::test_case",
            )


def test_append_record_rejects_blank_target() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        with pytest.raises(TddIntrospectionCliError, match="target must not be empty"):
            append_record(
                root,
                status="PASS",
                target="   ",
                command="pytest tests/test_example.py::test_case",
            )


def test_format_record_escapes_quotes() -> None:
    rendered = format_record(
        record=type(
            "Record",
            (),
            {
                "timestamp": "2026-04-30T12:00:00+00:00",
                "status": "UNKNOWN",
                "target": 'tests/test_"quoted".py::test_case',
                "command": 'pytest "quoted"',
                "notes": None,
                "sync_reminder": None,
            },
        )()
    )

    assert '\\"quoted\\"' in rendered


def test_main_record_writes_custom_output(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        output = root / "tmp" / "custom.log"
        monkeypatch.chdir(root)

        exit_code = main(
            [
                "record",
                "--status",
                "UNKNOWN",
                "--target",
                "tests/test_example.py::test_case",
                "--command",
                "pytest tests/test_example.py::test_case",
                "--output",
                str(output.relative_to(root)),
            ]
        )

        assert exit_code == 0
        assert output.is_file()
        monkeypatch.chdir(original_cwd)


def test_parse_record_round_trips_optional_fields() -> None:
    record = parse_record(
        'timestamp=2026-04-30T12:00:00+00:00 status=PASS '
        'target="tests/test_example.py::test_case" '
        'command="pytest tests/test_example.py::test_case" '
        'notes="missing edge case" sync_reminder="spec"'
    )

    assert record.status == "PASS"
    assert record.notes == "missing edge case"
    assert record.sync_reminder == "spec"


def test_summarize_records_reports_fail_to_pass_candidates() -> None:
    records = [
        parse_record(
            'timestamp=2026-04-30T12:00:00+00:00 status=FAIL '
            'target="tests/test_example.py::test_case" '
            'command="pytest tests/test_example.py::test_case"'
        ),
        parse_record(
            'timestamp=2026-04-30T12:01:00+00:00 status=PASS '
            'target="tests/test_example.py::test_case" '
            'command="pytest tests/test_example.py::test_case"'
        ),
        parse_record(
            'timestamp=2026-04-30T12:02:00+00:00 status=UNKNOWN '
            'target="tests/test_other.py::test_case" '
            'command="pytest tests/test_other.py::test_case"'
        ),
    ]

    summary = summarize_records(records)

    assert summary.total == 3
    assert summary.by_status == {"PASS": 1, "FAIL": 1, "UNKNOWN": 1}
    assert summary.fail_to_pass_targets == ("tests/test_example.py::test_case",)
    rendered = format_summary(summary)
    assert "TDD Introspection Summary" in rendered
    assert "- FAIL->PASS candidates: 1" in rendered
    assert "- tests/test_example.py::test_case" in rendered


def test_main_summary_prints_read_only_summary(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    original_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        monkeypatch.chdir(root)
        append_record(
            root,
            status="FAIL",
            target="tests/test_example.py::test_case",
            command="pytest tests/test_example.py::test_case",
            timestamp="2026-04-30T12:00:00+00:00",
        )
        append_record(
            root,
            status="PASS",
            target="tests/test_example.py::test_case",
            command="pytest tests/test_example.py::test_case",
            timestamp="2026-04-30T12:01:00+00:00",
        )

        exit_code = main(["summary"])

        assert exit_code == 0
        output = capsys.readouterr().out
        assert "TDD Introspection Summary" in output
        assert "- Total records: 2" in output
        assert "- PASS: 1" in output
        assert "- FAIL: 1" in output
        assert "- FAIL->PASS candidates: 1" in output
        monkeypatch.chdir(original_cwd)
