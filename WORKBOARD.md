# WORKBOARD

## Dashboard

- Active card: WB-004
- Blocked: なし
- Gate: building
- Verification summary: R1-R3 は shipped。次は public docs / onboarding impact triage。

## Workstreams

| Workstream | Focus | Status |
|------------|-------|--------|
| Workboard | template / validator / render と運用接続の pilot | Active |

## Gate Matrix

| Gate | State | Evidence |
|------|-------|----------|
| requirements | 承認済み | docs/specs/workboard-initial-pilot.md |
| design | 承認済み | docs/design/workboard-initial-pilot-design.md |
| tasks | 承認済み | docs/tasks/workboard-initial-pilot-tasks.md |
| building | 実行中 | docs/tasks/workboard-initial-pilot-tasks.md |
| auditing | 未着手 | docs/tasks/workboard-initial-pilot-tasks.md |

## Cards

| ID | Title | Status | Gate | Workstream | Next action | Depends on | Evidence | Verification | Blocker |
|----|-------|--------|------|------------|-------------|------------|----------|--------------|---------|
| WB-001 | WORKBOARD R1 を実装する | Done | building | Workboard | | | tools/workboard.py, tests/test_workboard_cli.py, WORKBOARD.md, docs/tasks/workboard-initial-pilot-tasks.md | `tests/test_workboard_cli.py`: 4 passed; `tests/`: 41 passed; `validate`: 0 errors / 0 warnings | |
| WB-002 | WORKBOARD view を render する | Done | building | Workboard | | WB-001 | tools/workboard.py, tests/test_workboard_cli.py, docs/project/index.html, docs/project/graph.svg | `tests/test_workboard_cli.py`: 11 passed; `tests/`: 48 passed; `render`: HTML/SVG generated | |
| WB-003 | workflow contract を同期する | Done | building | Workboard | | WB-001, WB-002 | docs/tasks/workboard-initial-pilot-tasks.md, .agents/skills/quick-load/SKILL.md, .agents/skills/quick-save/SKILL.md, .codex/workflows/quick-load.md, .codex/workflows/quick-save.md, docs/internal/08_QUICK_LOAD_SAVE.md, .codex/workflows/auditing.md, docs/internal/04_RELEASE_OPS.md, tools/workboard.py, tests/test_workboard_cli.py, docs/project/index.html, docs/project/graph.svg | `tests/test_workboard_cli.py`: 12 passed; `tests/`: 49 passed; `validate`: 0 errors / 0 warnings; `render`: HTML/SVG regenerated; `git diff --check`: PASS; commit `6b780f1` pushed | |
| WB-004 | public docs impact を triage する | Active | building | Workboard | README / QUICKSTART / CHEATSHEET / CHANGELOG / slides への影響を分類する | WB-003 | SESSION_STATE.md, README.md, README_en.md, QUICKSTART.md, QUICKSTART_en.md, CHEATSHEET.md, CHEATSHEET_en.md, CHANGELOG.md, docs/slides/index.html | Not run: next session start | |

## Card Details

### WB-001: WORKBOARD R1 を実装する

- Goal: `WORKBOARD.md` template と `tools/workboard.py validate` を利用可能にする。
- Context: R1 は、承認済み planning package の後に行う最初の BUILDING slice。
- Definition of Done: duplicate card ID は error、必須 field 不足は warning になり、初期 board が error なしで validate できる。
- Verification: `tests/test_workboard_cli.py`: 4 passed; `tests/`: 41 passed; `python tools/workboard.py validate`: 0 errors / 0 warnings.
- Evidence: `tools/workboard.py`, `tests/test_workboard_cli.py`, `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md`
- Next action: なし。
- Blockers: なし

### WB-002: WORKBOARD view を render する

- Goal: Markdown SSOT から、local review 用の HTML / SVG view を生成する。
- Context: R2 は R1 が green かつ review 済みになった後だけ開始する。
- Definition of Done: generated output に source path と generated marker が含まれる。
- Verification: `tests/test_workboard_cli.py`: 11 passed; `tests/`: 48 passed; `python tools/workboard.py render`: HTML/SVG generated.
- Evidence: `tools/workboard.py`, `tests/test_workboard_cli.py`, `docs/project/index.html`, `docs/project/graph.svg`
- Next action: なし。
- Blockers: なし

### WB-003: workflow contract を同期する

- Goal: WORKBOARD の dashboard 読み、validate、render timing を quick-load、quick-save、gate、release workflow へ接続する。
- Context: R3 は template、validator、render surface、R1/R2 review fix が shipped した後に開始する。
- Definition of Done: workflow docs と skill が contract を反映する。反映しない場合は理由と代替 authoritative doc を記録する。
- Verification: `python -m pytest tests/test_workboard_cli.py -q -p no:cacheprovider --basetemp ...`: 12 passed; `python -m pytest tests -q -p no:cacheprovider --basetemp ...`: 49 passed; `python tools/workboard.py validate`: 0 errors / 0 warnings; `python tools/workboard.py render`: HTML/SVG regenerated; `git diff --check`: PASS.
- Evidence: `docs/tasks/workboard-initial-pilot-tasks.md`, `.agents/skills/quick-load/SKILL.md`, `.agents/skills/quick-save/SKILL.md`, `.codex/workflows/quick-load.md`, `.codex/workflows/quick-save.md`, `docs/internal/08_QUICK_LOAD_SAVE.md`, `.codex/workflows/auditing.md`, `docs/internal/04_RELEASE_OPS.md`, `tools/workboard.py`, `tests/test_workboard_cli.py`, `docs/project/index.html`, `docs/project/graph.svg`
- Next action: なし。
- Blockers: なし

### WB-004: public docs impact を triage する

- Goal: WORKBOARD / quick-load / quick-save / gate / release contract 更新が public template 利用者向け文書へ与える影響を分類する。
- Context: R1-R3 は commit `6b780f1` として shipped。次は README、QUICKSTART、CHEATSHEET、CHANGELOG、slides などの onboarding surface へ反映すべき差分を判断する。
- Definition of Done: 対象文書を「今すぐ更新する」「リンクや一文だけ足す」「後続 task に回す」「古くなっているので別 review 対象にする」に分類し、更新計画を作る。
- Verification: 未実行。次セッション開始時に実施する。
- Evidence: `SESSION_STATE.md`, `README.md`, `README_en.md`, `QUICKSTART.md`, `QUICKSTART_en.md`, `CHEATSHEET.md`, `CHEATSHEET_en.md`, `CHANGELOG.md`, `docs/slides/index.html`
- Next action: docs impact triage の対象一覧を作り、fresh template user の first path と public onboarding slides を優先して分類する。
- Blockers: なし

## Dependency Map

- WB-001 -> none
- WB-002 -> WB-001
- WB-003 -> WB-001, WB-002
- WB-004 -> WB-003
