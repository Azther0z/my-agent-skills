# Archive Mode: Finalize A Change

Use `archive` to merge a completed change's delta specs into main specs and
move the full change folder into `docs/change/archive/`.

Read `references/shared/artifact-contract.md`,
`references/shared/path-and-selection.md`, and
`references/shared/validation.md` first.

## Pre-Archive Checks

Read the full change folder and confirm:

- `proposal.md`, `spec/`, `design.md`, and `tasks.md` exist.
- Every task is complete, or incomplete tasks are explicitly accepted by the
  user.
- At least one delta spec exists under `spec/`.
- Matching main specs under `docs/spec/` have been read.

Warn before archiving incomplete work and obtain explicit confirmation. Do not
silently pass warnings.

## Sync Delta Specs

Apply each delta intelligently to its matching main spec; never copy the delta
file wholesale. Preserve main-spec content not mentioned by the delta.

- `Purpose`: seed a new main spec from the delta, or preserve an existing
  purpose unless the delta explicitly changes it.
- `ADDED Requirements`: add requirements that do not exist; reconcile an
  existing one as a modification.
- `MODIFIED Requirements`: update only the named requirements or scenarios.
- `REMOVED Requirements`: remove the named requirement blocks.
- `RENAMED Requirements`: rename the heading and preserve its content unless
  the delta also modifies it.

The sync must be idempotent; do not duplicate requirements on a repeated run.

If multiple active changes touch one main spec, inspect all deltas. If order
matters or they conflict, ask whether to order, proceed, or stop. If a delta
is ambiguous enough to invent behavior, stop.

## Move To Archive

After successful sync:

1. Create `docs/change/archive/` if needed.
2. Use today's date unless the change name is already date-prefixed.
3. Stop on a target collision.
4. Move the whole change folder to the archive target.

Do not archive when sync failed or verification has unresolved critical issues
the user has not explicitly accepted.

## Completion Report

Report the archive path, main specs updated, requirements added/modified/
removed/renamed, warnings accepted, and verification not run. Recommend
`my-spec-driven-development init` only for a future independent backfill, not
as part of archiving.
