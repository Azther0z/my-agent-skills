# Shared Validation

Use proportionate evidence and report what was actually checked.

## Artifact Checks

- Required artifacts exist before `apply`, `verify`, or `archive` proceeds.
- Delta specs contain observable requirements and concrete scenarios.
- `design.md` decisions agree with the proposal and implementation direction.
- Every task has an acceptance condition, verification method, and file area.
- Checked tasks have evidence that acceptance and verification succeeded.

## Implementation Checks

- Requirements and scenarios map to implementation evidence or an explicit reason they are not code-backed.
- Tests assert intended behavior instead of merely exercising a code path.
- Main specs will remain coherent after archive.
- Do not nitpick style unless it creates behavior or maintenance risk.

## Mode Reports

- `plan`: report the artifact created at the current boundary and the next unanswered frontier; do not claim the proposal is complete until all four artifact categories exist.
- `apply`: report completed and remaining tasks plus task-level verification.
- `verify`: report completeness, correctness, and coherence findings first.
- `archive`: report main specs updated, delta operations, archive path, and warnings accepted by the user.

When a command is unavailable or disproportionate, record `N/A` with the reason rather than implying it ran. Never hide skipped checks.
