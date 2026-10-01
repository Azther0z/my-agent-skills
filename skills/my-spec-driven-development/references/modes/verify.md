# Verify Mode: Check A Change

Use `verify` before archive or whenever the user asks whether implementation
matches an active change. This mode reports findings; it does not edit code or
artifacts unless the user explicitly asks for fixes.

Read `references/shared/artifact-contract.md`,
`references/shared/path-and-selection.md`, and
`references/shared/validation.md` first.

## Process

1. Read the full change artifacts and matching main specs.
2. Inspect relevant implementation and test files.
3. Check completeness, correctness, and coherence.
4. Run relevant tests, lint, typecheck, or build commands when feasible and
   proportionate.
5. Produce a findings-first report.

## Completeness

Check that:

- Every required artifact exists.
- Every task is checked or intentionally deferred.
- Checked tasks satisfy their `Acceptance` condition.
- Checked tasks have evidence for `Verify`, or a clear reason it was skipped.
- Every delta requirement has implementation evidence or an explicit reason it
  is not code-backed.
- Every scenario has test coverage or a credible manual verification path.

Unchecked implementation tasks and missing required behavior are critical.

## Correctness

Check that:

- Implementation matches `ADDED`, `MODIFIED`, `REMOVED`, and `RENAMED`
  requirements.
- Scenario edge cases are handled.
- Removed behavior is removed or blocked.
- Renamed user-visible concepts have no stale names where they matter.
- Tests assert intended behavior rather than only exercising code paths.

Use references such as `src/file.ts:123` when available.

## Coherence And Severity

Check that code follows major design decisions, artifacts do not contradict
one another, implementation fits repository patterns, and main specs make
sense after archive. Do not nitpick style without a behavior or maintenance
risk.

- `CRITICAL`: must fix before archive.
- `WARNING`: fix or explicitly accept.
- `SUGGESTION`: optional improvement.

Prefer lower severity when evidence is uncertain, but explain what is missing.

## Report Format

```markdown
## Verification Report: <change-name>

### Summary
| Dimension | Status |
|---|---|
| Completeness | <status> |
| Correctness | <status> |
| Coherence | <status> |

### Findings
1. [CRITICAL] <issue>
   Evidence: `<file>:<line>` or artifact reference.
   Recommendation: <specific next action>.

### Verification Run
- `<command>`: <result>

### Final Assessment
<Ready to archive / not ready / ready with warnings.>
```

If there are no findings, say so clearly and list residual risks or checks not
run.
