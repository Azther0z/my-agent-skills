# Apply Mode: Implement A Change

Use `apply` to implement tasks from an active Markdown change under
`docs/change/<change-name>/`.

Read `references/shared/artifact-contract.md`,
`references/shared/path-and-selection.md`, and
`references/shared/validation.md` before editing code.

## Preflight

Before editing:

1. Read `proposal.md`, every delta spec under `spec/`, `design.md`, and
   `tasks.md`.
2. Read matching main specs under `docs/spec/<capability>.md` when present.
3. Inspect implementation and test files named by the artifacts or discovered
   from the repository.
4. Identify unchecked tasks.
5. Extract each task's `Acceptance`, `Verify`, and `Files` lines.

If a required artifact is missing, stop and ask whether to create or repair
the planning artifacts first. Do not implement from an incomplete proposal.

## Implementation Loop

Work task by task until all tasks are complete or a real blocker appears:

1. Announce the task briefly.
2. Use its `Files` line as a starting point and inspect the real edit surface.
3. Make the smallest code change that satisfies the task.
4. Check its acceptance condition.
5. Run its verification command or manual check when feasible.
6. Mark `- [ ]` as `- [x]` only after acceptance and verification pass, or a
   documented reason explains why verification was skipped.
7. Continue to the next unchecked task.

Use existing style and tooling. Do not introduce broad refactors that the
proposal does not request.

## Live Plan Updates

Artifacts are the live plan. If implementation proves one stale:

- Fix code when the artifact is the intended contract.
- Update the artifact first when the artifact is wrong and the better path is
  clear.
- Summarize and ask before making a material change to intent, scope,
  behavior, or design.
- Correct small task-list mistakes directly and report them.

Keep updates in the same change folder. Do not create a new change from apply.

## Stop Conditions

Pause and ask when a task is ambiguous, implementation would change core
intent, a risky migration/destructive/secret/production operation is not
covered, or verification repeatedly fails for a product or design reason.

## Completion Report

Report the change name and path, tasks completed, verification results and
skips, remaining tasks, and artifact updates. If all tasks are complete,
recommend `my-spec-driven-development verify <change-name>` before archive.
