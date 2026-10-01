# Plan Mode: Grill And Propose A Change

Use `plan` for explicit specification, change-proposal, or spec-driven change
work. It combines the former exploration and proposal entry points into one
public flow. It is not a generic implementation-plan mode.

## Write Boundary

Plan is write-capable but never writes merely because a request is vaguely
change-shaped:

- Always begin with a requirements-grilling loop.
- For an explicit request to create, capture, or update a specification or
  proposal, proceed toward the first artifact once its questions are settled.
- For a vague SDD-shaped request, grill first and ask for clear write
  confirmation before creating the first artifact.
- At every artifact boundary, summarize the settled understanding and wait for
  explicit confirmation before writing.
- If the user abandons the work before the first boundary is confirmed, write
  no files. If a partial change already exists, preserve it and report it.

The mandatory grill is a design-tree interview: ask the whole currently
unblocked question frontier, wait for answers, recompute the frontier, and do
not silently decide product or design choices. The user may answer with a
custom decision rather than one of the recommended options.

## Grilling Integration

When `my-grilling` is available, invoke it in **no-artifact** mode for the
questioning loop. If it is unavailable, use the same frontier-question
workflow locally. Do not ask the companion to create `CONTEXT.md`, ADRs, or
other side artifacts. This skill owns the change artifacts; decisions belong
in `design.md` unless an existing ADR is explicitly relevant.

## Artifact Sequence

Use the shared contract in `references/shared/artifact-contract.md`. Work in
this order and create exactly one next artifact at each confirmed boundary:

1. `proposal.md`
2. Each needed delta spec file under `spec/`
3. `design.md`
4. `tasks.md`

Do not wait for an arbitrary number of answers. Continue grilling until the
current artifact's questions are settled, present a concise shared-understanding
summary, obtain confirmation, write that artifact, and stop. On the next
invocation, reread the settled artifacts and ask only newly unblocked
questions. Never repeat a settled question without a reason.

## Proposal Artifact

Create the first artifact at:

```text
docs/change/<change-name>/proposal.md
```

Use this structure:

```markdown
# Proposal: <Title>

## Intent
<What problem this solves and why it matters.>

## Scope

In scope:
- <Included behavior or work>

Out of scope:
- <Explicit non-goals>

## Approach
<High-level direction, not implementation minutiae.>

## Affected Specs
- `<capability>`: <added | modified | removed | renamed behavior summary>

## Impact
- `<path-or-area>`: <expected impact>
```

Derive a kebab-case change name unless the user supplied one. If a similarly
named active change exists and continuation is not clear, ask before writing.

## Delta Specs, Design, And Tasks

Delta specs describe only behavior changed relative to matching main specs.
Use the `ADDED`, `MODIFIED`, `REMOVED`, and `RENAMED` sections from the shared
artifact contract and include at least one concrete scenario.

`design.md` records current context, compact decision blocks, implementation
notes, verification commands, and risks. Use `None.` for an applicable empty
decision subpart. `tasks.md` is an ordered implementation checklist; every
implementation task includes `Acceptance`, `Verify`, and `Files` lines.

Inspect the repository, existing main specs, and settled artifacts before each
boundary. Keep documents concise and behavior-focused. Do not copy a huge code
summary into the plan.

## Quality And Stop Rules

- Specs describe observable behavior, not private call sequences.
- Design explains how and why code should change.
- Tasks are small enough for `apply` to execute one at a time.
- A pure refactor still needs an explicit behavior-preservation delta.
- Stop when a question is genuinely ambiguous, a named change collides, or a
  write would exceed the confirmed scope.

## Completion Report

After all artifacts exist, report the change path, artifacts created, main
specs consulted or missing, assumptions and open questions, and recommend
`my-spec-driven-development apply <change-name>` when implementation is ready.
