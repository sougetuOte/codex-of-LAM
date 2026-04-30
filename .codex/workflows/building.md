# BUILDING Workflow

## Goal

Implement approved tasks with t-wada style TDD wherever practical.

## Cycle

1. Red: write or update a focused failing test that expresses the requirement.
2. Green: add the smallest production change that passes the test.
3. Refactor: improve structure while keeping tests green.
4. Sync docs and tasks with the actual result.
5. Report changed files and verification results.

## Guardrails

- If a requirement is ambiguous, return to PLANNING.
- If a change crosses module boundaries, expand the test scope.
- If a test cannot be written first, document why in the task file.
