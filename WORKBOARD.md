# WORKBOARD

## Dashboard

- Active card: WB-001
- Blocked: none
- Gate: building
- Verification summary: R1 focused and `tests/` regression passed; root collection is blocked by known `pytesttmp-wave2a` ACL residue.

## Workstreams

| Workstream | Focus | Status |
|------------|-------|--------|
| Workboard | Template and validator pilot | Active |

## Gate Matrix

| Gate | State | Evidence |
|------|-------|----------|
| requirements | Approved | docs/specs/workboard-initial-pilot.md |
| design | Approved | docs/design/workboard-initial-pilot-design.md |
| tasks | Approved | docs/tasks/workboard-initial-pilot-tasks.md |
| building | Active | docs/tasks/workboard-initial-pilot-tasks.md |
| auditing | Not started | docs/tasks/workboard-initial-pilot-tasks.md |

## Cards

| ID | Title | Status | Gate | Workstream | Next action | Depends on | Evidence | Verification | Blocker |
|----|-------|--------|------|------------|-------------|------------|----------|--------------|---------|
| WB-001 | Implement WORKBOARD R1 | Active | building | Workboard | Review R1 green result before R2 | | tools/workboard.py, tests/test_workboard_cli.py, WORKBOARD.md, docs/tasks/workboard-initial-pilot-tasks.md | `tests/test_workboard_cli.py`: 4 passed; `tests/`: 41 passed; `validate`: 0 errors / 0 warnings | |
| WB-002 | Render WORKBOARD views | Todo | building | Workboard | | WB-001 | docs/design/workboard-initial-pilot-design.md | Not run: R2 deferred | |
| WB-003 | Sync workflow contract | Todo | building | Workboard | | WB-001, WB-002 | docs/tasks/workboard-initial-pilot-tasks.md | Not run: R3 deferred | |

## Card Details

### WB-001: Implement WORKBOARD R1

- Goal: `WORKBOARD.md` template and `tools/workboard.py validate` are usable.
- Context: R1 is the first BUILDING slice after the accepted planning package.
- Definition of Done: duplicate card IDs are errors, required field gaps are warnings, and the initial board validates without errors.
- Verification: `tests/test_workboard_cli.py`: 4 passed; `tests/`: 41 passed; `python tools/workboard.py validate`: 0 errors / 0 warnings.
- Evidence: `tools/workboard.py`, `tests/test_workboard_cli.py`, `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md`
- Next action: review R1 result and decide whether to start R2.
- Blockers: none

### WB-002: Render WORKBOARD views

- Goal: generate local HTML and SVG review surfaces from the Markdown SSOT.
- Context: R2 starts only after R1 is green and reviewed.
- Definition of Done: generated outputs include source path and generated markers.
- Verification: not run; R2 deferred.
- Evidence: `docs/design/workboard-initial-pilot-design.md`
- Next action: wait for R1 review.
- Blockers: R1 must be green first.

### WB-003: Sync workflow contract

- Goal: connect WORKBOARD validation and dashboard reading to quick-load, quick-save, gate, and release workflows.
- Context: R3 starts only after the template, validator, and render surface are stable enough to document.
- Definition of Done: workflow docs and skills either reflect the contract or record why they do not.
- Verification: not run; R3 deferred.
- Evidence: `docs/tasks/workboard-initial-pilot-tasks.md`
- Next action: wait for R1 and R2 review.
- Blockers: R1 and R2 must be green first.

## Dependency Map

- WB-001 -> none
- WB-002 -> WB-001
- WB-003 -> WB-001, WB-002
