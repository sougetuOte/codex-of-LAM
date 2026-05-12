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


def test_validate_reports_missing_card_table_as_error() -> None:
    workboard = load_workboard_module()
    text = """# WORKBOARD

## Dashboard

- Active card: WB-001

## Cards

No table yet.

## Card Details
"""

    result = workboard.validate_workboard_text(text)

    assert any(
        "Cards section must contain a card table" in issue.message
        for issue in result.errors
    )


def test_validate_warns_when_dashboard_active_card_is_missing() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "| WB-002 | Different active | Active | building | Workboard | Add validator | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
        detail("WB-002", "Different active"),
    )

    result = workboard.validate_workboard_text(text)

    assert any(
        "dashboard active card missing from Cards: WB-001" in issue.message
        for issue in result.warnings
    )


def test_render_html_contains_marker_source_and_dashboard_sections() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "| WB-001 | Render dashboard | Active | building | Workboard | Add render command | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
        detail("WB-001", "Render dashboard"),
    )

    html, _svg = workboard.render_workboard_text(text, source_path=Path("WORKBOARD.md"))

    assert "Generated from WORKBOARD.md by tools/workboard.py" in html
    assert "Source: WORKBOARD.md" in html
    assert "Top Band" in html
    assert "Workstream Matrix" in html
    assert "Card Board" in html
    assert 'href="#WB-001"' in html
    assert '<html lang="en">' in html


def test_render_html_uses_japanese_lang_when_board_contains_japanese() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "| WB-001 | 日本語のカード | Active | building | Workboard | 確認する | | docs/tasks/workboard-initial-pilot-tasks.md | 未実行 | |",
        detail("WB-001", "日本語のカード"),
    )

    html, _svg = workboard.render_workboard_text(text, source_path=Path("WORKBOARD.md"))

    assert '<html lang="ja">' in html


def test_render_svg_contains_marker_source_and_dependency_overview() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "\n".join(
            [
                "| WB-001 | Render dashboard | Active | building | Workboard | Add render command | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
                "| WB-002 | Follow-up | Todo | building | Workboard | | WB-001 | docs/tasks/workboard-initial-pilot-tasks.md | Not run: waiting | |",
            ]
        ),
        "\n".join(
            [
                detail("WB-001", "Render dashboard"),
                detail("WB-002", "Follow-up"),
            ]
        ),
    )

    _html, svg = workboard.render_workboard_text(text, source_path=Path("WORKBOARD.md"))

    assert "Generated from WORKBOARD.md by tools/workboard.py" in svg
    assert "Source: WORKBOARD.md" in svg
    assert "Dependency Overview" in svg
    assert "WB-002 -> WB-001" in svg


def test_render_output_is_deterministic() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "| WB-001 | Render dashboard | Active | building | Workboard | Add render command | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
        detail("WB-001", "Render dashboard"),
    )

    first = workboard.render_workboard_text(text, source_path=Path("WORKBOARD.md"))
    second = workboard.render_workboard_text(text, source_path=Path("WORKBOARD.md"))

    assert first == second


def test_render_rejects_validation_errors() -> None:
    workboard = load_workboard_module()
    text = sample_board(
        "\n".join(
            [
                "| WB-001 | First | Active | building | Workboard | Add render command | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
                "| WB-001 | Duplicate | Todo | building | Workboard | | | docs/tasks/workboard-initial-pilot-tasks.md | | |",
            ]
        ),
        detail("WB-001", "First"),
    )

    try:
        workboard.render_workboard_text(text, source_path=Path("WORKBOARD.md"))
    except workboard.WorkboardRenderError as exc:
        assert any("duplicate card ID: WB-001" in issue.message for issue in exc.result.errors)
    else:
        raise AssertionError("render should reject validation errors")


def test_render_files_does_not_write_outputs_when_validation_fails(tmp_path: Path) -> None:
    workboard = load_workboard_module()
    board_path = tmp_path / "WORKBOARD.md"
    html_path = tmp_path / "docs" / "project" / "index.html"
    svg_path = tmp_path / "docs" / "project" / "graph.svg"
    board_path.write_text(
        sample_board(
            "\n".join(
                [
                    "| WB-001 | First | Active | building | Workboard | Add render command | | docs/tasks/workboard-initial-pilot-tasks.md | Not run: red first | |",
                    "| WB-001 | Duplicate | Todo | building | Workboard | | | docs/tasks/workboard-initial-pilot-tasks.md | | |",
                ]
            ),
            detail("WB-001", "First"),
        ),
        encoding="utf-8",
    )

    try:
        workboard.render_workboard_files(board_path, html_path, svg_path)
    except workboard.WorkboardRenderError:
        pass
    else:
        raise AssertionError("render should reject validation errors")

    assert not html_path.exists()
    assert not svg_path.exists()
