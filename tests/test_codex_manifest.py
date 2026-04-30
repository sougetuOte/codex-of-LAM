from __future__ import annotations

import json
from pathlib import Path

import pytest

from codex_lam.manifest import (
    CodexLamManifest,
    ManifestValidationError,
    validate_manifest_file,
)


ROOT = Path(__file__).resolve().parent.parent


def test_codex_manifest_is_valid() -> None:
    manifest = validate_manifest_file(ROOT / ".codex" / "manifest.json", ROOT)

    assert manifest.name == "Codex Living Architect Model"
    assert manifest.runtime == "codex"
    assert manifest.phases == ("PLANNING", "BUILDING", "AUDITING")
    assert manifest.approval_gates == ("requirements", "design", "tasks", "building", "auditing")


@pytest.mark.parametrize(
    "path",
    [
        "AGENTS.md",
        ".codex/constitution.md",
        ".codex/workflows/planning.md",
        ".codex/workflows/building.md",
        ".codex/workflows/auditing.md",
        "docs/specs/codex-lam-replacement-requirements.md",
        "docs/adr/0005-codex-native-harness.md",
        "docs/design/codex-lam-replacement-design.md",
        "docs/tasks/codex-lam-replacement-tasks.md",
    ],
)
def test_codex_replacement_artifacts_exist(path: str) -> None:
    assert (ROOT / path).is_file()


def test_manifest_rejects_claude_runtime(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "name": "Bad",
                "runtime": "claude",
                "phases": ["PLANNING", "BUILDING", "AUDITING"],
                "approval_gates": ["requirements", "design", "tasks", "building", "auditing"],
                "documents": [],
                "source_harness": ".claude",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ManifestValidationError, match="runtime"):
        validate_manifest_file(manifest_path, tmp_path)


def test_manifest_rejects_missing_required_gate(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "name": "Codex Living Architect Model",
                "runtime": "codex",
                "phases": ["PLANNING", "BUILDING", "AUDITING"],
                "approval_gates": ["requirements", "design", "tasks"],
                "documents": [],
                "source_harness": ".codex",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ManifestValidationError, match="approval_gates"):
        validate_manifest_file(manifest_path, tmp_path)


def test_manifest_model_is_immutable() -> None:
    manifest = CodexLamManifest(
        name="Codex Living Architect Model",
        runtime="codex",
        phases=("PLANNING", "BUILDING", "AUDITING"),
        approval_gates=("requirements", "design", "tasks", "building", "auditing"),
        documents=(),
        source_harness=".codex",
    )

    with pytest.raises(AttributeError):
        manifest.runtime = "claude"  # type: ignore[misc]
