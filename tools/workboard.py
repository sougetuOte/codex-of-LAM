from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


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


def parse_workboard(text: str) -> Workboard:
    cards = _parse_cards(_extract_section(text, "Cards"))
    details = _parse_details(_extract_section(text, "Card Details"))
    return Workboard(cards=tuple(cards), details=details)


def validate_workboard_text(text: str, root: Path | None = None) -> ValidationResult:
    board = parse_workboard(text)
    root = root or Path.cwd()
    errors: list[Issue] = []
    warnings: list[Issue] = []

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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate WORKBOARD.md.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate root WORKBOARD.md.")

    args = parser.parse_args(argv)
    if args.command == "validate":
        result = validate_workboard_file(Path.cwd() / "WORKBOARD.md")
        print(format_validation_result(result))
        return 0 if result.ok else 1

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
    table_lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 2:
        return []

    header = _split_table_row(table_lines[0])
    if header != list(CARD_FIELDS):
        return []

    cards: list[Card] = []
    for line in table_lines[2:]:
        cells = _split_table_row(line)
        if not cells or _is_separator_row(cells):
            continue
        padded = cells + [""] * (len(CARD_FIELDS) - len(cells))
        values = dict(zip(CARD_FIELDS, padded[: len(CARD_FIELDS)]))
        cards.append(Card(values=values))
    return cards


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


if __name__ == "__main__":
    raise SystemExit(main())
