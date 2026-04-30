from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_PHASES = ("PLANNING", "BUILDING", "AUDITING")
EXPECTED_APPROVAL_GATES = ("requirements", "design", "tasks", "building", "auditing")
EXPECTED_WORKFLOWS = (
    ".codex/workflows/planning.md",
    ".codex/workflows/building.md",
    ".codex/workflows/auditing.md",
)


class ManifestValidationError(ValueError):
    """Raised when the Codex LAM manifest violates the project contract."""


@dataclass(frozen=True)
class CodexLamManifest:
    name: str
    runtime: str
    phases: tuple[str, ...]
    approval_gates: tuple[str, ...]
    documents: tuple[str, ...]
    source_harness: str


def validate_manifest_file(path: Path, root: Path) -> CodexLamManifest:
    if not path.is_file():
        raise ManifestValidationError(f"manifest not found: {path}")

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ManifestValidationError(f"manifest is invalid JSON: {exc}") from exc

    manifest = _parse_manifest(raw)
    _validate_manifest(manifest, root)
    return manifest


def _parse_manifest(raw: dict[str, Any]) -> CodexLamManifest:
    try:
        return CodexLamManifest(
            name=str(raw["name"]),
            runtime=str(raw["runtime"]),
            phases=tuple(raw["phases"]),
            approval_gates=tuple(raw["approval_gates"]),
            documents=tuple(_document_paths(raw.get("documents", []))),
            source_harness=str(raw["source_harness"]),
        )
    except KeyError as exc:
        raise ManifestValidationError(f"missing manifest field: {exc.args[0]}") from exc
    except TypeError as exc:
        raise ManifestValidationError("manifest field has invalid type") from exc


def _document_paths(documents: list[Any]) -> list[str]:
    paths: list[str] = []
    for item in documents:
        if isinstance(item, str):
            paths.append(item)
            continue
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"])
            continue
        raise ManifestValidationError("documents must contain paths")
    return paths


def _validate_manifest(manifest: CodexLamManifest, root: Path) -> None:
    if manifest.runtime != "codex":
        raise ManifestValidationError("runtime must be codex")

    if manifest.source_harness != ".codex":
        raise ManifestValidationError("source_harness must be .codex")

    if manifest.phases != EXPECTED_PHASES:
        raise ManifestValidationError(f"phases must be {EXPECTED_PHASES}")

    if manifest.approval_gates != EXPECTED_APPROVAL_GATES:
        raise ManifestValidationError(
            f"approval_gates must be {EXPECTED_APPROVAL_GATES}"
        )

    missing = [doc for doc in manifest.documents if not (root / doc).is_file()]
    if missing:
        raise ManifestValidationError(f"manifest documents are missing: {missing}")

    missing_workflows = [path for path in EXPECTED_WORKFLOWS if not (root / path).is_file()]
    if missing_workflows:
        raise ManifestValidationError(f"required workflows are missing: {missing_workflows}")
