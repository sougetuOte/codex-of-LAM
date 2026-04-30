from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest

from codex_lam.manifest import (
    CodexLamManifest,
    ManifestValidationError,
    validate_manifest_file,
)


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_PHASES = ("PLANNING", "BUILDING", "AUDITING")
EXPECTED_APPROVAL_GATES = ("requirements", "design", "tasks", "building", "auditing")
EXPECTED_WORKFLOWS = (
    ".codex/workflows/planning.md",
    ".codex/workflows/building.md",
    ".codex/workflows/auditing.md",
)
REQUIRED_DOCS = (
    "AGENTS.md",
    ".codex/constitution.md",
    ".codex/workflows/planning.md",
    ".codex/workflows/building.md",
    ".codex/workflows/auditing.md",
    "docs/specs/codex-lam-replacement-requirements.md",
    "docs/adr/0005-codex-native-harness.md",
    "docs/design/codex-lam-replacement-design.md",
    "docs/tasks/codex-lam-replacement-tasks.md",
)


def test_codex_manifest_is_valid() -> None:
    manifest = validate_manifest_file(ROOT / ".codex" / "manifest.json", ROOT)

    assert manifest.name == "Codex Living Architect Model"
    assert manifest.runtime == "codex"
    assert manifest.phases == EXPECTED_PHASES
    assert manifest.approval_gates == EXPECTED_APPROVAL_GATES


@pytest.mark.parametrize(
    "path",
    [
        *REQUIRED_DOCS,
    ],
)
def test_codex_replacement_artifacts_exist(path: str) -> None:
    assert (ROOT / path).is_file()


def _write_minimal_codex_contract(
    root: Path,
    *,
    runtime: str = "codex",
    source_harness: str = ".codex",
    phases: tuple[str, ...] = EXPECTED_PHASES,
    approval_gates: tuple[str, ...] = EXPECTED_APPROVAL_GATES,
    documents: tuple[str, ...] = REQUIRED_DOCS,
) -> Path:
    for rel_path in REQUIRED_DOCS:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{rel_path}\n", encoding="utf-8")

    manifest_path = root / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "name": "Codex Living Architect Model",
                "runtime": runtime,
                "phases": list(phases),
                "approval_gates": list(approval_gates),
                "documents": list(documents),
                "source_harness": source_harness,
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def _expect_manifest_error(match: str, **overrides: object) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_root = Path(temp_dir)
        manifest_path = _write_minimal_codex_contract(tmp_root, **overrides)

        with pytest.raises(ManifestValidationError, match=match):
            validate_manifest_file(manifest_path, tmp_root)


def test_manifest_rejects_claude_runtime() -> None:
    _expect_manifest_error("runtime", runtime="claude", source_harness=".claude")


def test_manifest_rejects_non_codex_source_harness() -> None:
    _expect_manifest_error("source_harness", source_harness=".claude")


@pytest.mark.parametrize(
    ("phases", "label"),
    [
        (("PLANNING", "BUILDING"), "missing"),
        (("PLANNING", "BUILDING", "BUILDING", "AUDITING"), "duplicate"),
        (("BUILDING", "PLANNING", "AUDITING"), "wrong_order"),
        (("planning", "BUILDING", "AUDITING"), "wrong_case"),
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_manifest_rejects_invalid_phase_lists(phases: tuple[str, ...], label: str) -> None:
    del label
    _expect_manifest_error("phases", phases=phases)


@pytest.mark.parametrize(
    ("approval_gates", "label"),
    [
        (("requirements", "design", "tasks", "building"), "missing"),
        (
            ("requirements", "design", "tasks", "building", "building", "auditing"),
            "duplicate",
        ),
        (("design", "requirements", "tasks", "building", "auditing"), "wrong_order"),
        (("Requirements", "design", "tasks", "building", "auditing"), "wrong_case"),
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_manifest_rejects_invalid_approval_gate_lists(
    approval_gates: tuple[str, ...], label: str
) -> None:
    del label
    _expect_manifest_error("approval_gates", approval_gates=approval_gates)


def test_manifest_rejects_missing_required_document() -> None:
    _expect_manifest_error(
        "documents are missing",
        documents=REQUIRED_DOCS + ("docs/migration/missing-note.md",),
    )


def test_manifest_rejects_missing_required_workflow() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_root = Path(temp_dir)
        manifest_path = _write_minimal_codex_contract(
            tmp_root,
            documents=tuple(path for path in REQUIRED_DOCS if not path.startswith(".codex/workflows/")),
        )
        (tmp_root / EXPECTED_WORKFLOWS[1]).unlink()

        with pytest.raises(ManifestValidationError, match="required workflows are missing"):
            validate_manifest_file(manifest_path, tmp_root)


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
