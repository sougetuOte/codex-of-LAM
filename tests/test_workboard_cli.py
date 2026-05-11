from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_workboard_module():
    module_path = Path(__file__).resolve().parents[1] / "tools" / "workboard.py"
    spec = importlib.util.spec_from_file_location("workboard_tool", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sample_board(card_rows: str, details: str = "") -> str:
    return f"""# WORKBOARD

## Dashboard

- Active card: WB-001
- Blocked: none
- Gate: building
- Verification summary: focused tests pending

## Workstreams

| Workstream | Focus | Status |
|------------|-------|--------|
| Workboard | Pilot | Active |

## Gate Matrix

| Gate | State | Evidence |
|------|-------|----------|
| building | Active | docs/tasks/workboard-initial-pilot-tasks.md |

## Cards

| ID | Title | Status | Gate | Workstream | Next action | Depends on | Evidence | Verification | Blocker |
|----|-------|--------|------|------------|-------------|------------|----------|--------------|---------|
{card_rows}

## Card Details

{details}

## Dependency Map

- WB-001 -> none
"""


def detail(card_id: str, title: str) -> str:
    return f"""### {card_id}: {title}

- Goal: keep project state visible
- Context: WORKBOARD pilot
- Definition of Done: validator can read the card
- Verification: focused pytest
- Evidence: docs/tasks/workboard-initial-pilot-tasks.md
- Next action: implement validator
- Blockers: none
"""


def test_parse_workboard_reads_card_table_and_details() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "| WB-001 | Template validator | Active | building | Workboard | Add validator | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
        detail("WB-001", "Template validator"),
    )

    board = workboard.parse_workboard(text)

    assert [card.card_id for card in board.cards] == ["WB-001"]
    assert board.cards[0].title == "Template validator"
    assert board.cards[0].status == "Active"
    assert board.detail_ids == {"WB-001"}


def test_validate_reports_duplicate_card_id_as_error(tmp_path: Path) -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "\n".join(
            [
                "| WB-001 | First | Active | building | Workboard | Add validator | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
                "| WB-001 | Duplicate | Todo | building | Workboard | | | docs/tasks/workboard-initial-pilot-tasks.md | | |",
            ]
        ),
        detail("WB-001", "First"),
    )

    result = workboard.validate_workboard_text(text, root=tmp_path)

    assert any("duplicate card ID: WB-001" in issue.message for issue in result.errors)


def test_validate_warns_for_required_fields_by_status(tmp_path: Path) -> None:
    workboard = load_workboard_module()
    existing = tmp_path / "docs" / "tasks" / "workboard-initial-pilot-tasks.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("# tasks\n", encoding="utf-8")
    text = sample_board(
        "\n".join(
            [
                "| WB-001 | Active missing next | Active | building | Workboard | | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
                "| WB-002 | Blocked missing blocker | Blocked | building | Workboard | Wait | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: blocked | |",
                "| WB-003 | Done missing verification | Done | building | Workboard | | | docs/tasks/workboard-initial-pilot-tasks.md | | |",
            ]
        ),
        "\n".join(
            [
                detail("WB-001", "Active missing next"),
                detail("WB-002", "Blocked missing blocker"),
                detail("WB-003", "Done missing verification"),
            ]
        ),
    )

    result = workboard.validate_workboard_text(text, root=tmp_path)

    warning_messages = [issue.message for issue in result.warnings]
    assert "WB-001 active card missing next action" in warning_messages
    assert "WB-002 blocked card missing blocker reason" in warning_messages
    assert "WB-003 done card missing verification" in warning_messages


def test_validate_warns_for_missing_dependency_and_evidence(tmp_path: Path) -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "| WB-001 | Missing links | Active | building | Workboard | Add validator | WB-999 | docs/missing.md | Not run: red first | |",
        detail("WB-001", "Missing links"),
    )

    result = workboard.validate_workboard_text(text, root=tmp_path)

    warning_messages = [issue.message for issue in result.warnings]
    assert "WB-001 dependency target missing: WB-999" in warning_messages
    assert "WB-001 evidence file missing: docs/missing.md" in warning_messages
