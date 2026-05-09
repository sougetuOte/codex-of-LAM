# Claude archive / delete gate

Status: Delete approved for Codex template cleanup
Date: 2026-05-09

## Purpose

Wave 3 legacy cleanup leaves one high-risk action: deciding whether tracked `.claude/`
material should be archived, deleted, or kept as legacy reference.

This gate exists so that Codex parity does not silently turn into destructive cleanup.
The current approved path is to delete `.claude/` from `codex-of-LAM` after a
separate legacy reference snapshot has been confirmed outside this template repo.

## Current evidence

- `git ls-files .claude` reports 104 tracked files.
- Top-level distribution docs point archive / delete decisions for legacy Claude Code material to `docs/migration/`, not to a present runtime directory.
- `docs/migration/claude-legacy-inventory.md` classifies `.claude/` families by `codex_adopted`, `codex_reexpress`, `decide_later`, and `archive_runtime_specific`.
- Wave 3 non-destructive cleanup confirmed no mojibake hits in the checked docs and no remaining quickstart / cheatsheet rewrite need.
- Legacy reference snapshot confirmed at `C:\work6\LivingArchitectModel-legacy-v4.6.1-reference`.
  - Source remote: `https://github.com/sougetuOte/LivingArchitectModel.git`
  - Snapshot: `v4.6.1`, commit `c72051b`.

## Cross-check findings before deletion

Date: 2026-05-09

Deleting `.claude/` from this repo is approved for the next cleanup commit.
The pre-delete cleanup blockers below have been retired.

Retired blockers:

- `pyproject.toml` no longer writes JUnit XML to `.claude/test-results.xml`.
  - Current path: `test-results.xml`, ignored by `**/test-results.xml`.
- `tests/test_pre_compact.py` no longer imports `.claude/hooks/pre-compact.py`.
  - Current role: retirement guard that checks this gate remains documented.
- `tests/test_lam_stop_hook.py` no longer imports `.claude/hooks/lam-stop-hook.py`.
  - Current role: retirement guard that checks this gate remains documented.
- top-level distribution docs no longer mention `.claude/` as a present directory.
  - Current wording points readers to `docs/migration/` for legacy archive / delete decisions.
- `.gitignore` no longer contains `.claude/` runtime-state ignores.

Remaining blockers:

- None found in the pre-delete cleanup scope above.
- `.claude/` deletion still requires final diff review and verification before commit.

Non-blocking historical references:

- Older specs, designs, audit reports, and migration docs can continue to mention `.claude/` as historical source material.
- These should not be mass-edited unless they are user-facing distribution docs or active runtime configuration.

## Legacy Reference Location

Do not keep Claude runtime material in the public `codex-of-LAM` template branch.
Use the external local reference snapshot instead:

- `C:\work6\LivingArchitectModel-legacy-v4.6.1-reference`

Rationale:

- `codex-of-LAM` is intended to be a public Codex template / starter kit.
- Keeping `.claude/` in the default branch makes the template appear mixed-mode.
- A separate snapshot preserves legacy reference value without confusing new Codex users.

## Delete Candidates

Approved for deletion from `codex-of-LAM`:

- `.claude/`

## Required Gate Before Archive / Delete

Before committing deletion:

1. Confirm the exact file list with `git ls-files .claude`.
2. Confirm the external reference snapshot path and revision.
3. Document restore procedure.
4. Run `git diff --check`.
5. Run focused tests if code, hooks, scripts, or importable Python files are moved or deleted.
6. Review the deletion diff before commit.

## Restore Procedure

If a legacy Claude file is needed later:

1. Read it from `C:\work6\LivingArchitectModel-legacy-v4.6.1-reference`.
2. Re-express the needed behavior as Codex docs, workflow, skill, or tests.
3. Do not restore `.claude/` as an active runtime directory in `codex-of-LAM`
   without a new approval gate.

## Recommendation

Delete `.claude/` from `codex-of-LAM` in the next cleanup commit, then verify
that the public template branch remains Codex-only.
