# Init Mode: Backfill Main Specs

Use `init` when behavior already exists and the user wants reliable
`docs/spec/` main specs. This is a brownfield documentation workflow, not a
proposal for new behavior.

## Scope

Write only `docs/spec/<capability>.md` unless the user explicitly asks for
related change artifacts. Do not use this mode for new or changed behavior;
that belongs in `plan` and `docs/change/<change-name>/`.

If the user asks to backfill a whole project, first produce a short capability
map and recommend the smallest useful first batch. A good first batch is one
user-facing area, API surface, package, service, or domain about to change.
Ask for scope only when it cannot be inferred.

## Discover Evidence

Inspect relevant evidence before writing:

- Existing `docs/spec/` files.
- README, product docs, API docs, ADRs, and other human documentation.
- Routes, controllers, handlers, screens, commands, jobs, schemas,
  migrations, configuration, and public interfaces.
- Tests that encode expected behavior.
- Current naming and organization patterns.

Keep evidence paths internally. Cite them sparingly when they clarify
confidence; do not turn the spec into a code tour.

## Write Main Specs

For each selected capability, create or update:

```text
docs/spec/<capability>.md
```

Use this shape:

```markdown
# <Capability> Specification

## Purpose
<What this capability does for users, operators, or downstream systems.>

## Requirements

### Requirement: <Observable behavior>
The system SHALL <current implemented behavior>.

#### Scenario: <Concrete case>
- GIVEN <starting condition>
- WHEN <event or action>
- THEN <observable result>
```

Use `SHALL` or `MUST` only when implementation evidence shows behavior is
relied on. Use `SHOULD` for evidence-backed intended but non-strict behavior.
Avoid `MAY` unless optional behavior is explicitly implemented.

## Evidence And Uncertainty

Do not invent requirements from a quick code skim. When evidence is
incomplete, omit the claim or add a separate note after Requirements:

```markdown
## Evidence Gaps

- <Behavior> appears in `<path>`, but no test or public docs confirm its edge cases.
```

Describe externally visible awkward or likely relied-on behavior as current
behavior. Put suspected bugs or desired corrections in a future `plan`
proposal rather than disguising them as current requirements.

## Merge Existing Specs Carefully

If the target main spec exists:

- Read it before editing.
- Preserve existing requirements unless implementation clearly contradicts
  them.
- Report code/spec mismatches and ask whether to document current code or
  desired behavior.
- Never silently overwrite hand-written intent.

## Completion Report

Report specs created or updated, scope covered and skipped, evidence grouped
by capability, confidence, evidence gaps or mismatches, and a useful next
backfill batch when one is apparent.
