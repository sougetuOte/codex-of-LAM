from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from html import escape as html_escape
from pathlib import Path
from typing import Sequence


GENERATED_MARKER = "Generated from WORKBOARD.md by tools/workboard.py. Do not edit by hand."
CARD_FIELDS = (
    "ID",
    "Title",
    "Status",
    "Gate",
    "Workstream",
    "Next action",
    "Depends on",
    "Evidence",
    "Verification",
    "Blocker",
)
DETAIL_LABELS = (
    "Goal",
    "Context",
    "Definition of Done",
    "Verification",
    "Evidence",
    "Next action",
    "Blockers",
)
VALID_STATUSES = {"Todo", "Active", "Blocked", "Done", "Released"}
STATUS_ORDER = ("Active", "Blocked", "Todo", "Done", "Released")
CARD_ID_PATTERN = re.compile(r"^WB-\d{3}$")
DETAIL_HEADING_PATTERN = re.compile(r"^###\s+(WB-\d{3}):\s+(.+?)\s*$")


@dataclass(frozen=True)
class Card:
    values: dict[str, str]

    @property
    def card_id(self) -> str:
        return self.values.get("ID", "")

    @property
    def title(self) -> str:
        return self.values.get("Title", "")

    @property
    def status(self) -> str:
        return self.values.get("Status", "")

    def field(self, name: str) -> str:
        return self.values.get(name, "")


@dataclass(frozen=True)
class CardDetail:
    card_id: str
    title: str
    labels: frozenset[str]


@dataclass(frozen=True)
class Workboard:
    cards: tuple[Card, ...]
    details: dict[str, CardDetail]
    dashboard: dict[str, str]
    workstreams: tuple[dict[str, str], ...]
    gate_matrix: tuple[dict[str, str], ...]

    @property
    def detail_ids(self) -> set[str]:
        return set(self.details)


@dataclass(frozen=True)
class Issue:
    severity: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[Issue, ...]
    warnings: tuple[Issue, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


class WorkboardRenderError(RuntimeError):
    def __init__(self, result: ValidationResult) -> None:
        super().__init__("WORKBOARD validation failed; render aborted")
        self.result = result


def parse_workboard(text: str) -> Workboard:
    return Workboard(
        cards=tuple(_parse_cards(_extract_section(text, "Cards"))),
        details=_parse_details(_extract_section(text, "Card Details")),
        dashboard=_parse_dashboard(_extract_section(text, "Dashboard")),
        workstreams=tuple(_parse_table(_extract_section(text, "Workstreams"))),
        gate_matrix=tuple(_parse_table(_extract_section(text, "Gate Matrix"))),
    )


def validate_workboard_text(text: str, root: Path | None = None) -> ValidationResult:
    board = parse_workboard(text)
    root = root or Path.cwd()
    errors: list[Issue] = []
    warnings: list[Issue] = []
    cards_section = _extract_section(text, "Cards")
    card_table_header = _table_header(cards_section)

    if card_table_header is None:
        errors.append(Issue("error", "Cards section must contain a card table"))
    elif card_table_header != list(CARD_FIELDS):
        errors.append(
            Issue(
                "error",
                "Cards table header must be: " + ", ".join(CARD_FIELDS),
            )
        )
    elif not board.cards:
        errors.append(Issue("error", "Cards table must contain at least one card"))

    seen: set[str] = set()
    duplicate_reported: set[str] = set()
    for card in board.cards:
        if not CARD_ID_PATTERN.match(card.card_id):
            errors.append(Issue("error", f"invalid card ID: {card.card_id}"))
            continue
        if card.card_id in seen and card.card_id not in duplicate_reported:
            errors.append(Issue("error", f"duplicate card ID: {card.card_id}"))
            duplicate_reported.add(card.card_id)
        seen.add(card.card_id)

    card_ids = {card.card_id for card in board.cards}
    for card in board.cards:
        _validate_status_fields(card, warnings)
        _validate_dependencies(card, card_ids, warnings)
        _validate_evidence(card, root, warnings)
        _validate_detail_consistency(card, board.details, warnings)

    for detail_id in sorted(set(board.details) - card_ids):
        warnings.append(Issue("warning", f"{detail_id} detail has no table row"))

    active_card = board.dashboard.get("Active card")
    if active_card and active_card.lower() not in {"none", "n/a", "-"}:
        for card_id in _split_list_field(active_card):
            if card_id not in card_ids:
                warnings.append(
                    Issue("warning", f"dashboard active card missing from Cards: {card_id}")
                )

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings))


def validate_workboard_file(path: Path) -> ValidationResult:
    if not path.is_file():
        return ValidationResult(
            errors=(Issue("error", f"WORKBOARD not found: {path}"),),
            warnings=(),
        )
    return validate_workboard_text(path.read_text(encoding="utf-8"), root=path.parent)


def format_validation_result(result: ValidationResult) -> str:
    lines: list[str] = []
    for issue in result.errors:
        lines.append(f"ERROR: {issue.message}")
    for issue in result.warnings:
        lines.append(f"WARNING: {issue.message}")
    lines.append(
        f"Validation complete: {len(result.errors)} error(s), "
        f"{len(result.warnings)} warning(s)"
    )
    return "\n".join(lines)


def render_workboard_text(text: str, source_path: Path | str = "WORKBOARD.md") -> tuple[str, str]:
    result = validate_workboard_text(text, root=_validation_root(source_path))
    if result.errors:
        raise WorkboardRenderError(result)
    board = parse_workboard(text)
    source = _display_path(source_path)
    return _render_html(board, source, lang=_document_language(text)), _render_svg(board, source)


def render_workboard_files(
    input_path: Path,
    html_output_path: Path,
    svg_output_path: Path,
) -> tuple[Path, Path]:
    text = input_path.read_text(encoding="utf-8")
    html, svg = render_workboard_text(text, source_path=_source_path_for_display(input_path))

    html_output_path.parent.mkdir(parents=True, exist_ok=True)
    svg_output_path.parent.mkdir(parents=True, exist_ok=True)
    html_output_path.write_text(html, encoding="utf-8", newline="\n")
    svg_output_path.write_text(svg, encoding="utf-8", newline="\n")
    return html_output_path, svg_output_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate or render WORKBOARD.md.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate root WORKBOARD.md.")
    subparsers.add_parser("render", help="Render root WORKBOARD.md to docs/project/.")

    args = parser.parse_args(argv)
    if args.command == "validate":
        result = validate_workboard_file(Path.cwd() / "WORKBOARD.md")
        print(format_validation_result(result))
        return 0 if result.ok else 1
    if args.command == "render":
        try:
            html_path, svg_path = render_workboard_files(
                Path.cwd() / "WORKBOARD.md",
                Path.cwd() / "docs" / "project" / "index.html",
                Path.cwd() / "docs" / "project" / "graph.svg",
            )
        except WorkboardRenderError as exc:
            print(format_validation_result(exc.result), file=sys.stderr)
            return 1
        print(f"Rendered {html_path.relative_to(Path.cwd())}")
        print(f"Rendered {svg_path.relative_to(Path.cwd())}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


def _extract_section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start_marker = f"## {heading}"
    start_index: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == start_marker:
            start_index = index + 1
            break
    if start_index is None:
        return ""

    section_lines: list[str] = []
    for line in lines[start_index:]:
        if line.startswith("## "):
            break
        section_lines.append(line)
    return "\n".join(section_lines)


def _parse_cards(section: str) -> list[Card]:
    rows = _parse_table(section)
    return [Card(values={field: row.get(field, "") for field in CARD_FIELDS}) for row in rows]


def _parse_table(section: str) -> list[dict[str, str]]:
    table_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return []

    header = _split_table_row(table_lines[0])
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = _split_table_row(line)
        if not cells or _is_separator_row(cells):
            continue
        padded = cells + [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, padded[: len(header)])))
    return rows


def _table_header(section: str) -> list[str] | None:
    table_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return None
    return _split_table_row(table_lines[0])


def _parse_dashboard(section: str) -> dict[str, str]:
    dashboard: dict[str, str] = {}
    for line in section.splitlines():
        match = re.match(r"^-\s+([^:]+):\s*(.+?)\s*$", line.strip())
        if match:
            dashboard[match.group(1).strip()] = match.group(2).strip()
    return dashboard


def _parse_details(section: str) -> dict[str, CardDetail]:
    details: dict[str, CardDetail] = {}
    current_id: str | None = None
    current_title = ""
    current_labels: set[str] = set()

    def store_current() -> None:
        if current_id is not None:
            details[current_id] = CardDetail(
                card_id=current_id,
                title=current_title,
                labels=frozenset(current_labels),
            )

    for line in section.splitlines():
        heading_match = DETAIL_HEADING_PATTERN.match(line.strip())
        if heading_match:
            store_current()
            current_id = heading_match.group(1)
            current_title = heading_match.group(2).strip()
            current_labels = set()
            continue

        if current_id is None:
            continue
        label_match = re.match(r"^-\s+([^:]+):", line.strip())
        if label_match:
            current_labels.add(label_match.group(1).strip())

    store_current()
    return details


def _split_table_row(row: str) -> list[str]:
    stripped = row.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator_row(cells: Sequence[str]) -> bool:
    return all(set(cell.replace(" ", "")) <= {"-", ":"} for cell in cells)


def _validate_status_fields(card: Card, warnings: list[Issue]) -> None:
    if card.status and card.status not in VALID_STATUSES:
        warnings.append(Issue("warning", f"{card.card_id} unknown status: {card.status}"))

    if card.status == "Active" and not card.field("Next action"):
        warnings.append(Issue("warning", f"{card.card_id} active card missing next action"))

    if card.status == "Blocked" and not card.field("Blocker"):
        warnings.append(Issue("warning", f"{card.card_id} blocked card missing blocker reason"))

    if card.status in {"Done", "Released"}:
        status_name = card.status.lower()
        if not card.field("Verification"):
            warnings.append(Issue("warning", f"{card.card_id} {status_name} card missing verification"))
        if not card.field("Evidence"):
            warnings.append(Issue("warning", f"{card.card_id} {status_name} card missing evidence"))


def _validate_dependencies(
    card: Card,
    card_ids: set[str],
    warnings: list[Issue],
) -> None:
    for dependency in _split_list_field(card.field("Depends on")):
        if dependency not in card_ids:
            warnings.append(
                Issue("warning", f"{card.card_id} dependency target missing: {dependency}")
            )


def _validate_evidence(card: Card, root: Path, warnings: list[Issue]) -> None:
    for evidence in _split_list_field(card.field("Evidence")):
        if _is_external_reference(evidence):
            continue
        if not (root / evidence).is_file():
            warnings.append(Issue("warning", f"{card.card_id} evidence file missing: {evidence}"))


def _validate_detail_consistency(
    card: Card,
    details: dict[str, CardDetail],
    warnings: list[Issue],
) -> None:
    detail = details.get(card.card_id)
    if detail is None:
        warnings.append(Issue("warning", f"{card.card_id} detail heading missing"))
        return

    if detail.title != card.title:
        warnings.append(Issue("warning", f"{card.card_id} detail title differs from table title"))

    missing_labels = [label for label in DETAIL_LABELS if label not in detail.labels]
    if missing_labels:
        warnings.append(
            Issue(
                "warning",
                f"{card.card_id} detail missing labels: {', '.join(missing_labels)}",
            )
        )


def _split_list_field(value: str) -> list[str]:
    if not value:
        return []
    items: list[str] = []
    for raw_item in value.split(","):
        item = raw_item.strip().strip("`")
        if not item or item.lower() in {"none", "n/a", "-"}:
            continue
        items.append(item)
    return items


def _is_external_reference(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def _document_language(text: str) -> str:
    if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", text):
        return "ja"
    return "en"


def _render_html(board: Workboard, source: str, lang: str) -> str:
    return "\n".join(
        [
            "<!doctype html>",
            f"<html lang=\"{lang}\">",
            "<head>",
            "  <meta charset=\"utf-8\">",
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
            "  <title>WORKBOARD Dashboard</title>",
            "  <style>",
            "    body { font-family: system-ui, sans-serif; margin: 24px; color: #1f2937; }",
            "    table { border-collapse: collapse; width: 100%; margin: 12px 0 24px; }",
            "    th, td { border: 1px solid #cbd5e1; padding: 8px; text-align: left; vertical-align: top; }",
            "    th { background: #f1f5f9; }",
            "    .top-band { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px; }",
            "    .metric, .lane { border: 1px solid #cbd5e1; padding: 10px; }",
            "    .board { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }",
            "    .card { border: 1px solid #cbd5e1; padding: 8px; margin: 8px 0; }",
            "    .muted { color: #64748b; font-size: 0.92rem; }",
            "  </style>",
            "</head>",
            "<body>",
            f"<!-- {GENERATED_MARKER} -->",
            "  <header>",
            "    <h1>WORKBOARD Dashboard</h1>",
            f"    <p class=\"muted\">Source: {html_escape(source)}</p>",
            "  </header>",
            "  <section>",
            "    <h2>Top Band</h2>",
            _render_html_top_band(board.dashboard),
            "  </section>",
            "  <section>",
            "    <h2>Workstream Matrix</h2>",
            _render_html_table(board.workstreams),
            "  </section>",
            "  <section>",
            "    <h2>Card Board</h2>",
            _render_html_card_board(board.cards),
            "  </section>",
            "  <section>",
            "    <h2>Card Details</h2>",
            _render_html_detail_links(board.cards),
            "  </section>",
            "</body>",
            "</html>",
            "",
        ]
    )


def _render_html_top_band(dashboard: dict[str, str]) -> str:
    if not dashboard:
        return "    <p class=\"muted\">No dashboard entries found.</p>"
    metrics = [
        "    <div class=\"top-band\">",
    ]
    for label, value in dashboard.items():
        metrics.extend(
            [
                "      <div class=\"metric\">",
                f"        <strong>{html_escape(label)}</strong>",
                f"        <div>{html_escape(value)}</div>",
                "      </div>",
            ]
        )
    metrics.append("    </div>")
    return "\n".join(metrics)


def _render_html_table(rows: Sequence[dict[str, str]]) -> str:
    if not rows:
        return "    <p class=\"muted\">No rows found.</p>"
    headers = tuple(rows[0])
    lines = ["    <table>", "      <thead>", "        <tr>"]
    lines.extend(f"          <th>{html_escape(header)}</th>" for header in headers)
    lines.extend(["        </tr>", "      </thead>", "      <tbody>"])
    for row in rows:
        lines.append("        <tr>")
        lines.extend(
            f"          <td>{html_escape(row.get(header, ''))}</td>" for header in headers
        )
        lines.append("        </tr>")
    lines.extend(["      </tbody>", "    </table>"])
    return "\n".join(lines)


def _render_html_card_board(cards: Sequence[Card]) -> str:
    lines = ["    <div class=\"board\">"]
    for status in STATUS_ORDER:
        status_cards = [card for card in cards if card.status == status]
        lines.extend(
            [
                "      <section class=\"lane\">",
                f"        <h3>{html_escape(status)}</h3>",
            ]
        )
        if not status_cards:
            lines.append("        <p class=\"muted\">No cards</p>")
        for card in status_cards:
            lines.extend(
                [
                    f"        <article class=\"card\" id=\"{html_escape(card.card_id)}\">",
                    f"          <strong>{html_escape(card.card_id)}: {html_escape(card.title)}</strong>",
                    f"          <div>Gate: {html_escape(card.field('Gate'))}</div>",
                    f"          <div>Workstream: {html_escape(card.field('Workstream'))}</div>",
                    f"          <div>Next: {html_escape(card.field('Next action') or 'none')}</div>",
                    "        </article>",
                ]
            )
        lines.append("      </section>")
    lines.append("    </div>")
    return "\n".join(lines)


def _render_html_detail_links(cards: Sequence[Card]) -> str:
    lines = ["    <ul>"]
    for card in cards:
        lines.append(
            f"      <li><a href=\"#{html_escape(card.card_id)}\">"
            f"{html_escape(card.card_id)}: {html_escape(card.title)}</a></li>"
        )
    lines.append("    </ul>")
    return "\n".join(lines)


def _render_svg(board: Workboard, source: str) -> str:
    positions = {card.card_id: (80, 100 + index * 72) for index, card in enumerate(board.cards)}
    dependencies = [
        (card.card_id, dependency)
        for card in board.cards
        for dependency in _split_list_field(card.field("Depends on"))
    ]
    width = 900
    height = max(260, 140 + len(board.cards) * 72)
    lines = [
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"{width}\" height=\"{height}\" viewBox=\"0 0 {width} {height}\">",
        f"  <!-- {GENERATED_MARKER} -->",
    ]
    for card_id, dependency in dependencies:
        lines.append(f"  <!-- {card_id} -> {dependency} -->")
    lines.extend(
        [
            "  <style>",
            "    text { font-family: system-ui, sans-serif; fill: #1f2937; }",
            "    .muted { fill: #64748b; font-size: 13px; }",
            "    .node { fill: #f8fafc; stroke: #334155; stroke-width: 1.5; }",
            "    .active { fill: #dcfce7; }",
            "    .blocked { fill: #fee2e2; }",
            "    .done { fill: #e0f2fe; }",
            "    .edge { stroke: #64748b; stroke-width: 1.4; marker-end: url(#arrow); }",
            "  </style>",
            "  <defs>",
            "    <marker id=\"arrow\" viewBox=\"0 0 10 10\" refX=\"9\" refY=\"5\" markerWidth=\"6\" markerHeight=\"6\" orient=\"auto-start-reverse\">",
            "      <path d=\"M 0 0 L 10 5 L 0 10 z\" fill=\"#64748b\" />",
            "    </marker>",
            "  </defs>",
            "  <text x=\"32\" y=\"36\" font-size=\"24\" font-weight=\"700\">Dependency Overview</text>",
            f"  <text x=\"32\" y=\"62\" class=\"muted\">Source: {_svg_escape(source)}</text>",
        ]
    )

    for card in board.cards:
        x, y = positions[card.card_id]
        class_name = _svg_card_class(card.status)
        lines.extend(
            [
                f"  <rect class=\"node {class_name}\" x=\"{x}\" y=\"{y}\" width=\"270\" height=\"48\" rx=\"6\" />",
                f"  <text x=\"{x + 14}\" y=\"{y + 21}\" font-size=\"14\" font-weight=\"700\">{_svg_escape(card.card_id)}: {_svg_escape(card.title)}</text>",
                f"  <text x=\"{x + 14}\" y=\"{y + 39}\" class=\"muted\">{_svg_escape(card.status)} / {_svg_escape(card.field('Workstream'))}</text>",
            ]
        )

    for card_id, dependency in dependencies:
        if card_id not in positions or dependency not in positions:
            continue
        from_x, from_y = positions[card_id]
        to_x, to_y = positions[dependency]
        lines.append(
            f"  <line class=\"edge\" x1=\"{from_x}\" y1=\"{from_y + 24}\" x2=\"{to_x + 270}\" y2=\"{to_y + 24}\" />"
        )

    lines.extend(["</svg>", ""])
    return "\n".join(lines)


def _svg_card_class(status: str) -> str:
    if status == "Active":
        return "active"
    if status == "Blocked":
        return "blocked"
    if status in {"Done", "Released"}:
        return "done"
    return ""


def _display_path(path: Path | str) -> str:
    if isinstance(path, Path):
        return path.as_posix()
    return str(path).replace("\\", "/")


def _source_path_for_display(path: Path) -> Path:
    try:
        return path.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return path


def _validation_root(path: Path | str) -> Path:
    if isinstance(path, Path):
        if path.suffix:
            return path.parent
        return path
    return Path.cwd()


def _svg_escape(value: str) -> str:
    return html_escape(value, quote=True)


if __name__ == "__main__":
    raise SystemExit(main())
