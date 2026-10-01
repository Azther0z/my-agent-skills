# Shared Artifact Contract

Use this reference for `plan`, `apply`, `verify`, and `archive`. It is the common contract that keeps the lifecycle modes interoperable.

## Paths

Active changes live at:

```text
docs/change/<change-name>/
├── proposal.md
├── spec/
│   └── <capability>.md
├── design.md
└── tasks.md
```

Main capability specs live at `docs/spec/<capability>.md`. Archived changes live at `docs/change/archive/YYYY-MM-DD-<change-name>/`.

Every proposed change needs all four artifact categories:

- `proposal.md`
- at least one delta spec under `spec/`
- `design.md`
- `tasks.md`

Do not replace the four-file contract with a single plan document or silently omit an artifact for a small change.

## Delta Specs

Delta specs describe behavior relative to the matching main spec; they are not full copies. Use only sections that apply:

```markdown
# <Capability> Delta Spec

## Purpose
<Only for a new capability or a materially changed purpose.>

## ADDED Requirements

### Requirement: <New behavior>
The system SHALL <observable behavior>.

#### Scenario: <Scenario name>
- GIVEN <starting condition>
- WHEN <event or action>
- THEN <observable result>

## MODIFIED Requirements

### Requirement: <Existing behavior>
<Only changed requirement text or scenarios.>

## REMOVED Requirements

### Requirement: <Deprecated behavior>
<Reason it is being removed.>

## RENAMED Requirements

- FROM: `### Requirement: <Old name>`
- TO: `### Requirement: <New name>`
```

A pure refactor still needs a delta explaining the behavior that must remain unchanged or explicitly stating the preservation requirement.

## Design Decisions

`design.md` uses compact decision blocks:

```markdown
### Decision: <Name>
<Choice, rationale, alternatives, and consequences when meaningful.>
```

Use `None.` exactly when a required decision subpart has no meaningful content. Link an existing ADR only when one exists and is relevant. The `plan` mode does not create `CONTEXT.md` or ADRs as a side effect of delegating questions to `my-grilling`; its companion call is no-artifact only.

## Tasks

Tasks must be ordered, actionable, and small enough for `apply` to execute one at a time. Each implementation task includes all three metadata lines:

```markdown
- [ ] 1.1 <Concrete implementation task>
  - Acceptance: <What must be true>
  - Verify: <Command or manual check>
  - Files: <Expected files or areas>
```

The final verification section may contain tests, typechecks, lint, builds, manual checks, or review steps with the same metadata.

## Plan Artifact Boundaries

`plan` works in this order:

1. `proposal.md`
2. Each required delta spec file under `spec/`
3. `design.md`
4. `tasks.md`

At each boundary it reads the artifacts already settled, inspects relevant code and docs, asks the whole currently unblocked question frontier, and summarizes the proposed artifact. It waits for explicit confirmation before writing exactly that next artifact, then stops. It does not create later artifacts as a side effect.

If the user abandons a plan before the first boundary is confirmed, leave no files. If the user stops after one or more artifacts exist, preserve the partial active change and report exactly what remains.
