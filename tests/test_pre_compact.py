"""
Retirement guard for the old Claude pre-compact hook tests.

The hook runtime is no longer a Codex control surface. This test keeps the
retirement decision reviewable without importing legacy hook code.
"""
from __future__ import annotations

from pathlib import Path


def test_pre_compact_hook_retirement_is_documented() -> None:
    gate = Path("docs/migration/claude-archive-delete-gate.md").read_text(
        encoding="utf-8"
    )

    assert "pre-compact" in gate
    assert "archive / delete" in gate
    assert "LivingArchitectModel-legacy-v4.6.1-reference" in gate
    assert "Restore Procedure" in gate
