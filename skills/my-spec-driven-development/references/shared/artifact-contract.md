# Shared Artifact Contract

Use this reference for `plan`, `apply`, `verify`, and `archive`. It is the common contract that keeps the lifecycle modes interoperable.

## Paths

Active changes live at:

```text
docs/change/<change-name>/
├── plan.md                 # Optional my-planning precursor; not sufficient for apply
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

`plan.md` is an optional lightweight precursor created by `my-planning`. It may
exist alone while a change is being shaped, and it remains as frozen provenance
after the first formal artifact is created. It does not count as any of the four
required categories and never authorizes `apply`, `verify`, or `archive`.

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

Across SDD artifacts, architectural rationale, alternatives, and tradeoffs live
only in ADRs. A proposal may state the user-facing motivation and high-level
approach; specs state observable behavior; design and tasks may state concise
constraints or actions and link the ADR, but none duplicates its architectural
rationale.

`design.md` records implementation choices that do not meet the local ADR
threshold. For an architectural decision, it may state the resulting constraint
briefly and link the ADR without copying the rationale.

For a routine implementation choice, use:

```markdown
### Implementation choice: <Name>
<Choice and short implementation-specific reason.>
```

For an architectural constraint, use only a terse statement and link its ADR:

```markdown
### Architectural constraint: <Name>
<One-line constraint.> (ADR: `docs/adr/YYYY-MM-DD-<slug>.md`)
```

Do not duplicate the ADR's rationale, alternatives, or tradeoffs. Create a new
ADR only when the decision meets the local ADR criteria, as a separate
confirmed step through `my-grilling with-artifact`; supersede an accepted ADR
instead of rewriting its decision history. ADRs remain outside the four
required SDD artifact categories. The `plan` mode does not create
`CONTEXT.md` or ADRs as a side effect of delegating questions to
`my-grilling`; its normal companion call is no-artifact only.

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

When a plan-only `plan.md` already exists in the change folder, read it as
settled planning context before asking new questions. Do not rewrite or delete
its body; the metadata-only transition below is the sole permitted prelude
update. Create the next formal artifact at the normal boundary.

### Freeze A Promoted Plan Prelude

When `plan.md` exists and no formal SDD artifact has yet been created, it is
planning input. At the first confirmed formal artifact boundary:

1. Include in the boundary summary that the write will create the one next
   formal artifact and transition the plan prelude's metadata.
2. After the formal artifact is successfully written, update only `plan.md`
   frontmatter to `status: promoted`, set `formal_change` to the
   `docs/change/<change-name>/` folder path, and update its `updated` date.
3. Do not rewrite the prelude body. From then on it is read-only provenance;
   SDD artifacts own subsequent decisions and progress.

The metadata transition is part of the first confirmed SDD boundary, not a
separate formal artifact. If an existing formal artifact proves the boundary
already happened but the metadata transition was interrupted, repair only
those frontmatter fields and report the repair.

If the user abandons a plan before the first formal boundary is confirmed, create no formal artifacts and preserve any pre-existing `plan.md`. If the user stops after one or more formal artifacts exist, preserve the partial active change and report exactly what remains.
