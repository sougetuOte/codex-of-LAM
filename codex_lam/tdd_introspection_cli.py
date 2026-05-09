from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


VALID_STATUSES = ("PASS", "FAIL", "UNKNOWN")
DEFAULT_SESSION_RECORD_DIR = Path("docs/artifacts/tdd-introspection/sessions")
DEFAULT_RECORD_PATH = DEFAULT_SESSION_RECORD_DIR / "manual-session.log"
SESSION_ID_ENV_KEYS = ("CODEX_SESSION_ID", "CODEX_THREAD_ID")


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
        "--session-id",
        help="Stable session id used to write one TDD record file per session.",
    )
    record_parser.add_argument(
        "--output",
        help="Workspace-relative path to the append-only record file.",
    )
    record_parser.set_defaults(handler=_handle_record)

    summary_parser = subparsers.add_parser(
        "summary", help="Print a read-only summary of TDD records."
    )
    summary_parser.add_argument(
        "--input",
        help="Workspace-relative path to the append-only record file.",
    )
    summary_parser.add_argument(
        "--session-id",
        help="Stable session id used to read one TDD record file per session.",
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
    session_id: str | None = None,
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

    record_timestamp = timestamp or _utc_now()
    output_path = root / (
        output
        if output != DEFAULT_RECORD_PATH
        else default_session_record_path(session_id=session_id, timestamp=record_timestamp)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    record = TddRecord(
        timestamp=record_timestamp,
        status=status,
        target=target.strip(),
        command=command.strip(),
        notes=_clean_optional(notes),
        sync_reminder=_clean_optional(sync_reminder),
    )
    with output_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(format_record(record) + "\n")
    return output_path


def default_session_record_path(
    *, session_id: str | None = None, timestamp: str | None = None
) -> Path:
    cleaned_session_id = _clean_session_id(session_id or _session_id_from_env())
    if cleaned_session_id:
        filename = f"{cleaned_session_id}.log"
    else:
        filename = f"{_compact_timestamp(timestamp or _utc_now())}.log"
    return DEFAULT_SESSION_RECORD_DIR / filename


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


def latest_session_record_path(root: Path) -> Path:
    session_dir = root / DEFAULT_SESSION_RECORD_DIR
    if not session_dir.is_dir():
        raise TddIntrospectionCliError(f"record directory not found: {session_dir}")
    candidates = sorted(
        (path for path in session_dir.glob("*.log") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise TddIntrospectionCliError(f"record file not found under: {session_dir}")
    return candidates[0].relative_to(root)


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
        output=Path(args.output) if args.output else DEFAULT_RECORD_PATH,
        notes=args.notes,
        sync_reminder=args.sync_reminder,
        session_id=args.session_id,
    )
    return 0


def _handle_summary(args: argparse.Namespace) -> int:
    root = Path.cwd()
    if args.input:
        input_path = Path(args.input)
    elif args.session_id:
        input_path = default_session_record_path(session_id=args.session_id)
    else:
        input_path = latest_session_record_path(root)
    summary = summarize_records(read_records(root, input_path=input_path))
    print(format_summary(summary))
    return 0


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _clean_session_id(value: str | None) -> str | None:
    cleaned = _clean_optional(value)
    if cleaned is None:
        return None
    safe = "".join(char if char.isalnum() or char in "-_" else "-" for char in cleaned)
    safe = safe.strip("-_")
    return safe or None


def _session_id_from_env() -> str | None:
    for key in SESSION_ID_ENV_KEYS:
        value = os.environ.get(key)
        if value:
            return value
    return None


def _compact_timestamp(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    parsed = parsed.astimezone(timezone.utc).replace(microsecond=0)
    return parsed.strftime("%Y%m%dT%H%M%SZ")


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
