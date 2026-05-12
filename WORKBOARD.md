# WORKBOARD

## Dashboard

- Active card: WB-009
- Blocked: なし
- Gate: auditing
- Verification summary: WORKBOARD initial pilot は closure 承認済み。release boundary prep 完了。次は retrospective / release 実行承認。

## Workstreams

| Workstream | Focus | Status |
|------------|-------|--------|
| Workboard | template / validator / render と運用接続の pilot | Done |
| Release | WORKBOARD pilot 後の release boundary prep | Active |

## Gate Matrix

| Gate | State | Evidence |
|------|-------|----------|
| requirements | 承認済み | docs/specs/workboard-initial-pilot.md |
| design | 承認済み | docs/design/workboard-initial-pilot-design.md |
| tasks | 承認済み | docs/tasks/workboard-initial-pilot-tasks.md |
| building | 完了 | docs/tasks/workboard-initial-pilot-tasks.md |
| auditing | 実行中 | docs/tasks/workboard-initial-pilot-tasks.md |

## Cards

| ID | Title | Status | Gate | Workstream | Next action | Depends on | Evidence | Verification | Blocker |
|----|-------|--------|------|------------|-------------|------------|----------|--------------|---------|
| WB-001 | WORKBOARD R1 を実装する | Done | building | Workboard | | | tools/workboard.py, tests/test_workboard_cli.py, WORKBOARD.md, docs/tasks/workboard-initial-pilot-tasks.md | `tests/test_workboard_cli.py`: 4 passed; `tests/`: 41 passed; `validate`: 0 errors / 0 warnings | |
| WB-002 | WORKBOARD view を render する | Done | building | Workboard | | WB-001 | tools/workboard.py, tests/test_workboard_cli.py, docs/project/index.html, docs/project/graph.svg | `tests/test_workboard_cli.py`: 11 passed; `tests/`: 48 passed; `render`: HTML/SVG generated | |
| WB-003 | workflow contract を同期する | Done | building | Workboard | | WB-001, WB-002 | docs/tasks/workboard-initial-pilot-tasks.md, .agents/skills/quick-load/SKILL.md, .agents/skills/quick-save/SKILL.md, .codex/workflows/quick-load.md, .codex/workflows/quick-save.md, docs/internal/08_QUICK_LOAD_SAVE.md, .codex/workflows/auditing.md, docs/internal/04_RELEASE_OPS.md, tools/workboard.py, tests/test_workboard_cli.py, docs/project/index.html, docs/project/graph.svg | `tests/test_workboard_cli.py`: 12 passed; `tests/`: 49 passed; `validate`: 0 errors / 0 warnings; `render`: HTML/SVG regenerated; `git diff --check`: PASS; commit `6b780f1` pushed | |
| WB-004 | public docs impact を triage する | Done | building | Workboard | | WB-003 | SESSION_STATE.md, README.md, README_en.md, QUICKSTART.md, QUICKSTART_en.md, CHEATSHEET.md, CHEATSHEET_en.md, CHANGELOG.md, docs/slides/index.html, docs/slides/index-en.html, docs/tasks/workboard-initial-pilot-tasks.md | 5.3 / 5.4 read-only triage complete; public front-door update deferred; CHANGELOG updated; `validate`: 0 errors / 0 warnings; focused pytest: 12 passed | |
| WB-005 | auditing gate を判断する | Done | building | Workboard | | WB-004 | WORKBOARD.md, docs/tasks/workboard-initial-pilot-tasks.md, CHANGELOG.md | User approved AUDITING gate on 2026-05-12 | |
| WB-006 | WORKBOARD initial pilot を監査する | Done | auditing | Workboard | | WB-005 | WORKBOARD.md, tools/workboard.py, tests/test_workboard_cli.py, docs/tasks/workboard-initial-pilot-tasks.md, docs/project/index.html, docs/project/graph.svg, CHANGELOG.md | No blocking findings; `validate`: 0 errors / 0 warnings; `render`: PASS; focused pytest: 12 passed; tests: 49 passed; gitleaks: no leaks found | |
| WB-007 | pilot closure を判断する | Done | auditing | Workboard | | WB-006 | WORKBOARD.md, docs/tasks/workboard-initial-pilot-tasks.md, .codex/current-phase.md | User approved pilot closure and release boundary prep on 2026-05-12 | |
| WB-008 | release boundary を準備する | Done | auditing | Release | | WB-007 | docs/internal/04_RELEASE_OPS.md, docs/internal/10_DISTRIBUTION_MODEL.md, CHANGELOG.md, WORKBOARD.md, docs/tasks/workboard-initial-pilot-tasks.md | Release checklist prepared; retrospective and explicit release execution approval remain open | |
| WB-009 | release readiness を承認する | Active | auditing | Release | retrospective を行い、version / ZIP asset / checksum / GitHub Release 実行の承認を得る | WB-008 | docs/internal/04_RELEASE_OPS.md, docs/internal/10_DISTRIBUTION_MODEL.md, CHANGELOG.md, WORKBOARD.md | Not run: pending release readiness approval | |

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
- Verification: 5.3 / 5.4 read-only triage と public docs `rg` search を実施。quick-load / quick-save / gate / release は既存 public docs で十分説明済み。`WORKBOARD.md` / `docs/project/*` は fresh template user の front door に出さず、maintainer / project-state surface として内部に閉じる。`CHANGELOG.md` は `Unreleased` の実態ズレを修正した。`python tools/workboard.py validate`: 0 errors / 0 warnings。`python tools/workboard.py render`: PASS。`python -m pytest tests/test_workboard_cli.py -q -p no:cacheprovider --basetemp ...`: 12 passed（sandbox ACL で一度失敗後、権限外で同一 focused tests を再実行）。
- Evidence: `SESSION_STATE.md`, `README.md`, `README_en.md`, `QUICKSTART.md`, `QUICKSTART_en.md`, `CHEATSHEET.md`, `CHEATSHEET_en.md`, `CHANGELOG.md`, `docs/slides/index.html`, `docs/slides/index-en.html`, `docs/tasks/workboard-initial-pilot-tasks.md`
- Next action: なし。次は WB-005 で AUDITING へ進むか判断する。
- Blockers: なし

### WB-005: auditing gate を判断する

- Goal: WORKBOARD initial pilot を AUDITING へ進めるか、残りの BUILDING 修正を切るか判断する。
- Context: WB-004 では public first path への WORKBOARD 露出を避け、`CHANGELOG.md` と project-state artifacts だけを更新する判断になった。
- Definition of Done: user approval を得て、AUDITING に進む場合は `.codex/current-phase.md` と `WORKBOARD.md` を auditing 開始状態へ更新する。進まない場合は残りの BUILDING card を切る。
- Verification: 2026-05-12 に user approval を受け、AUDITING へ進む判断を確定した。
- Evidence: `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md`, `CHANGELOG.md`
- Next action: なし。WB-006 で監査を開始する。
- Blockers: なし

### WB-006: WORKBOARD initial pilot を監査する

- Goal: WORKBOARD initial pilot の R1-R4 成果物を監査し、Green State か残リスク付き継続かを判断できる状態にする。
- Context: R1/R2 で validator/render、R3 で workflow contract、WB-004 で public docs impact triage が完了した。
- Definition of Done: changed files、spec/ADR/design/tasks/code consistency、generated artifacts、verification evidence を確認し、findings と残リスクを記録する。
- Verification: changed files、spec / ADR / design / tasks / implementation / generated artifacts の整合性を確認。blocking findings なし。`python tools/workboard.py validate`: 0 errors / 0 warnings。`python tools/workboard.py render`: PASS。`python -m pytest tests/test_workboard_cli.py -q -p no:cacheprovider --basetemp ...`: 12 passed。`python -m pytest tests -q -p no:cacheprovider --basetemp ...`: 49 passed。`gitleaks detect --no-git --source . --redact --verbose`: no leaks found（local `.pytest_cache` は permission denied で skip）。
- Evidence: `WORKBOARD.md`, `tools/workboard.py`, `tests/test_workboard_cli.py`, `docs/tasks/workboard-initial-pilot-tasks.md`, `docs/project/index.html`, `docs/project/graph.svg`, `CHANGELOG.md`
- Next action: なし。WB-007 で pilot closure または release 境界へ進むか判断する。
- Blockers: なし

### WB-007: pilot closure を判断する

- Goal: WORKBOARD initial pilot の監査結果を確認し、pilot closure または release 境界へ進むか判断する。
- Context: WB-006 audit は blocking findings なし。残リスクは local `.pytest_cache` が gitleaks scan で permission denied skip された環境ノイズのみ。
- Definition of Done: user approval を得て、pilot を完了扱いにするか、release / follow-up card を切る。
- Verification: 2026-05-12 に user approval を受け、pilot closure と release boundary prep へ進む判断を確定した。
- Evidence: `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md`, `.codex/current-phase.md`
- Next action: なし。WB-008 で release boundary prep を開始する。
- Blockers: なし

### WB-008: release boundary を準備する

- Goal: WORKBOARD initial pilot 後の release boundary に進めるか判断できるよう、release checklist と配布判断点を整理する。
- Context: pilot は closure 承認済み。実際の tag、release asset、GitHub Release は別の explicit release approval が必要。
- Definition of Done: `docs/internal/04_RELEASE_OPS.md` の基準に沿って tests、critical bugs、quality gate、documentation、WORKBOARD generated artifacts、retrospective の状態を整理し、release 実行前の承認点を明示する。
- Verification: release checklist を整理。All Tests Green: PASS（12 focused / 49 broader）。No Critical Bugs: PASS（blocking findings なし）。Quality Gate Passed: PASS（WB-006 audit green）。Documentation Updated: PASS（CHANGELOG / WORKBOARD / tasks）。WORKBOARD Updated: PASS（validate / render 対象）。Retrospective Done: 未実施。Release execution approval: 未承認。
- Evidence: `docs/internal/04_RELEASE_OPS.md`, `docs/internal/10_DISTRIBUTION_MODEL.md`, `CHANGELOG.md`, `WORKBOARD.md`, `docs/tasks/workboard-initial-pilot-tasks.md`
- Next action: なし。WB-009 で retrospective と release 実行承認を扱う。
- Blockers: なし

### WB-009: release readiness を承認する

- Goal: WORKBOARD initial pilot 後の release 実行可否を判断する。
- Context: release boundary prep では、retrospective と explicit release execution approval が未完了として残った。tag、ZIP asset、checksum、GitHub Release はまだ作成しない。
- Definition of Done: retrospective を実施し、version / tag / ZIP asset / checksum / GitHub Release の scope を承認する。承認されない場合は release を保留し、follow-up card を切る。
- Verification: 未実行。release readiness approval 待ち。
- Evidence: `docs/internal/04_RELEASE_OPS.md`, `docs/internal/10_DISTRIBUTION_MODEL.md`, `CHANGELOG.md`, `WORKBOARD.md`
- Next action: retrospective を行い、release 実行可否と配布物 scope の user approval を得る。
- Blockers: なし

## Dependency Map

- WB-001 -> none
- WB-002 -> WB-001
- WB-003 -> WB-001, WB-002
- WB-004 -> WB-003
- WB-005 -> WB-004
- WB-006 -> WB-005
- WB-007 -> WB-006
- WB-008 -> WB-007
- WB-009 -> WB-008
