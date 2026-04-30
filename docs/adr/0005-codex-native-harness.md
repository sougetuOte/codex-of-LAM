# ADR-0005: Codex-Native Harness Replacement

Date: 2026-04-30
Status: Proposed

## Context

LAM currently uses Claude Code as its target runtime. The repo contains
Claude-specific assets such as `.claude/settings.json`, hook scripts, slash
commands, and subagent prompts. Codex has a different collaboration and tool
model, so directly porting those files would create a misleading harness.

## Decision

Use a Codex-native, file-driven harness:

- `AGENTS.md` is the primary Codex instruction surface.
- `.codex/manifest.json` declares the active harness contract.
- `.codex/workflows/` defines PLANNING, BUILDING, and AUDITING.
- `docs/specs/`, `docs/adr/`, `docs/design/`, and `docs/tasks/` remain the
  reviewable planning surface.
- Python tests validate the manifest and required replacement artifacts.

Claude assets remain as legacy input for now and are not treated as the active
Codex runtime.

## Alternatives Considered

### A. Rename `.claude/` to `.codex/`

Rejected. The file names would change, but hook semantics, slash commands, and
subagent assumptions would still be Claude-specific.

### B. Keep Claude Harness and Add Codex Notes

Rejected. This would preserve ambiguity about which runtime is authoritative.

### C. Codex-Native File Contract

Accepted. It is explicit, reviewable, testable, and aligned with Codex's current
project instruction and local tooling model.

## Consequences

- The first wave is a replacement scaffold, not a full deletion of legacy files.
- Future tasks can migrate useful hook logic into Codex-compatible scripts or
  tests.
- Reviewers can validate the new contract without running Claude Code.
- The harness relies on human-visible workflow discipline plus executable
  checks, rather than opaque runtime hooks.
