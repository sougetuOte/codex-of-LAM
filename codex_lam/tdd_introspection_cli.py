from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


VALID_STATUSES = ("PASS", "FAIL", "UNKNOWN")
DEFAULT_RECORD_PATH = Path("docs/artifacts/tdd-introspection-records.log")


class TddIntrospectionCliError(ValueError):
    """Raised when CLI inputs are invalid."""


@dataclass(frozen=True)
class TddRecord:
    timestamp: str
    status: str
    target: str
    command: str
    notes: str | None = None
    sync_reminder: str | None = None


@dataclass(frozen=True)
class TddSummary:
    total: int
    by_status: dict[str, int]
    fail_to_pass_targets: tuple[str, ...]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codex-tdd-introspection")
    subparsers = parser.add_subparsers(dest="command_name", required=True)

    record_parser = subparsers.add_parser("record", help="Append a TDD record.")
    record_parser.add_argument("--status", required=True, choices=VALID_STATUSES)
    record_parser.add_argument("--target", required=True)
    record_parser.add_argument("--command", required=True)
    record_parser.add_argument("--notes")
    record_parser.add_argument("--sync-reminder")
    record_parser.add_argument(
        "--output",
        default=str(DEFAULT_RECORD_PATH),
        help="Workspace-relative path to the append-only record file.",
    )
    record_parser.set_defaults(handler=_handle_record)

    summary_parser = subparsers.add_parser(
        "summary", help="Print a read-only summary of TDD records."
    )
    summary_parser.add_argument(
        "--input",
        default=str(DEFAULT_RECORD_PATH),
        help="Workspace-relative path to the append-only record file.",
    )
    summary_parser.set_defaults(handler=_handle_summary)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.error("no subcommand selected")
    return handler(args)


def append_record(
    root: Path,
    *,
    status: str,
    target: str,
    command: str,
    output: Path = DEFAULT_RECORD_PATH,
    notes: str | None = None,
    sync_reminder: str | None = None,
    timestamp: str | None = None,
) -> Path:
    if status not in VALID_STATUSES:
        raise TddIntrospectionCliError(
            f"status must be one of {VALID_STATUSES}, got: {status}"
        )
    if not target.strip():
        raise TddIntrospectionCliError("target must not be empty")
    if not command.strip():
        raise TddIntrospectionCliError("command must not be empty")

    output_path = root / output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    record = TddRecord(
        timestamp=timestamp or _utc_now(),
        status=status,
        target=target.strip(),
        command=command.strip(),
        notes=_clean_optional(notes),
        sync_reminder=_clean_optional(sync_reminder),
    )
    with output_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(format_record(record) + "\n")
    return output_path


def format_record(record: TddRecord) -> str:
    parts = [
        f"timestamp={record.timestamp}",
        f"status={record.status}",
        f"target={_quote_value(record.target)}",
        f"command={_quote_value(record.command)}",
    ]
    if record.notes:
        parts.append(f"notes={_quote_value(record.notes)}")
    if record.sync_reminder:
        parts.append(f"sync_reminder={_quote_value(record.sync_reminder)}")
    return " ".join(parts)


def read_records(root: Path, *, input_path: Path = DEFAULT_RECORD_PATH) -> list[TddRecord]:
    path = root / input_path
    if not path.is_file():
        raise TddIntrospectionCliError(f"record file not found: {path}")

    records: list[TddRecord] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.strip():
            records.append(parse_record(raw_line))
    return records


def parse_record(line: str) -> TddRecord:
    values = {
        key: value
        for key, value in (
            _split_token(token) for token in _tokenize_record(line)
        )
    }
    try:
        return TddRecord(
            timestamp=values["timestamp"],
            status=values["status"],
            target=values["target"],
            command=values["command"],
            notes=values.get("notes"),
            sync_reminder=values.get("sync_reminder"),
        )
    except KeyError as exc:
        raise TddIntrospectionCliError(f"record is missing field: {exc.args[0]}") from exc


def summarize_records(records: Sequence[TddRecord]) -> TddSummary:
    by_status = {status: 0 for status in VALID_STATUSES}
    fail_to_pass_targets: list[str] = []
    last_status_by_target: dict[str, str] = {}

    for record in records:
        if record.status not in VALID_STATUSES:
            raise TddIntrospectionCliError(
                f"record contains invalid status: {record.status}"
            )
        by_status[record.status] += 1
        previous = last_status_by_target.get(record.target)
        if previous == "FAIL" and record.status == "PASS":
            fail_to_pass_targets.append(record.target)
        last_status_by_target[record.target] = record.status

    return TddSummary(
        total=len(records),
        by_status=by_status,
        fail_to_pass_targets=tuple(fail_to_pass_targets),
    )


def format_summary(summary: TddSummary) -> str:
    lines = [
        "TDD Introspection Summary",
        f"- Total records: {summary.total}",
        f"- PASS: {summary.by_status['PASS']}",
        f"- FAIL: {summary.by_status['FAIL']}",
        f"- UNKNOWN: {summary.by_status['UNKNOWN']}",
        f"- FAIL->PASS candidates: {len(summary.fail_to_pass_targets)}",
    ]
    if summary.fail_to_pass_targets:
        lines.append("Candidates:")
        for target in summary.fail_to_pass_targets:
            lines.append(f"- {target}")
    else:
        lines.append("Candidates:")
        lines.append("- none")
    return "\n".join(lines)


def _handle_record(args: argparse.Namespace) -> int:
    append_record(
        Path.cwd(),
        status=args.status,
        target=args.target,
        command=args.command,
        output=Path(args.output),
        notes=args.notes,
        sync_reminder=args.sync_reminder,
    )
    return 0


def _handle_summary(args: argparse.Namespace) -> int:
    summary = summarize_records(read_records(Path.cwd(), input_path=Path(args.input)))
    print(format_summary(summary))
    return 0


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _quote_value(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _tokenize_record(line: str) -> list[str]:
    tokens: list[str] = []
    current: list[str] = []
    in_quotes = False
    escape = False

    for char in line:
        if escape:
            current.append(char)
            escape = False
            continue
        if char == "\\" and in_quotes:
            escape = True
            continue
        if char == '"':
            in_quotes = not in_quotes
            current.append(char)
            continue
        if char == " " and not in_quotes:
            if current:
                tokens.append("".join(current))
                current = []
            continue
        current.append(char)

    if current:
        tokens.append("".join(current))
    return tokens


def _split_token(token: str) -> tuple[str, str]:
    if "=" not in token:
        raise TddIntrospectionCliError(f"invalid token: {token}")
    key, value = token.split("=", 1)
    return key, _unquote_value(value)


def _unquote_value(value: str) -> str:
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        inner = value[1:-1]
        return inner.replace('\\"', '"').replace("\\\\", "\\")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
