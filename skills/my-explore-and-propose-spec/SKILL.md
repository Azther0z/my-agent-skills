---
name: my-explore-and-propose-spec
description: "Use only when the user explicitly asks for a specification, spec-driven change proposal, or to start a docs/change workflow. Do not trigger for generic requests to propose a plan or write an implementation plan. Supports oneshot proposals by default and a step-by-step grilling path when requested. This is the default entry point for explicit spec and change work in the user's my-* change workflow."
sources:
  - "https://github.com/Fission-AI/OpenSpec/tree/main"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/opsx.md"
  - "https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/spec-driven-development/SKILL.md"
---

# My Explore And Propose Spec

For an explicit specification or change request, think through the idea and capture it as plain Markdown when it is ready. Preserve the useful OpenSpec artifact contract while removing OpenSpec-specific machinery.

Do not use the `openspec` CLI, `openspec/` directories, stores, schemas, generated instructions, or `.openspec.yaml`. This workflow owns only `docs/change/` and `docs/spec/`.

## Paths

Active changes live at:

```text
docs/change/<change-name>/
```

Required artifacts for every proposed change:

```text
docs/change/<change-name>/
├── proposal.md
├── spec/
│   └── <capability>.md
├── design.md
└── tasks.md
```

Main specs live at:

```text
docs/spec/<capability>.md
```

Archived changes later move to:

```text
docs/change/archive/YYYY-MM-DD-<change-name>/
```

Use `spec/` singular to align with the user's `docs/spec/...` preference. A change's files under `docs/change/<change>/spec/` are delta specs; files under `docs/spec/` are main specs.

## Modes

### Explore Mode

Use this for an explicit specification or change request when the user is not ready to write artifacts, asks to explore the change, asks for options about the change, or brings an unclear change problem.

- Read the relevant code and docs before forming conclusions.
- Ask useful questions only after inspecting facts you can discover yourself.
- Compare options, identify risks, and recommend a path when the evidence supports it.
- Do not write files or code unless the user explicitly asks to create or capture the specification or change.
- When the idea crystallizes, offer to create a proposed change under `docs/change/<change-name>/`.

### Propose Mode

Use this only when the user explicitly asks for a specification, spec-driven change proposal, or to start a docs/change workflow. Do not use it for a generic plan or implementation-plan request.

Choose an execution path explicitly when the user names one. Default to `oneshot`.

#### `oneshot` Path

Create the complete required artifact set in one pass after inspecting the repo. Keep artifacts concise and behavior-focused. Do not copy huge code summaries into them.

#### `grilling` Path

Use this path when the user asks for `grilling`, `step by step`, `progressive`, or one artifact at a time.

- Inspect the repo for relevant code, existing docs, and existing `docs/spec/` main specs.
- Work through the required artifacts in order: `proposal.md`, each needed delta spec under `spec/`, `design.md`, and `tasks.md`.
- Create exactly one artifact file per step, then stop and wait for the user's confirmation before creating the next artifact.
- At every artifact boundary, read the existing artifacts as settled context and ask only newly unblocked questions. Do not repeat questions whose answers are already recorded.
- If `my-grilling` is available, invoke it in with-artifact mode at each boundary. It may maintain domain docs and creates an ADR for each qualifying design decision; link that ADR from the corresponding `design.md` decision block.
- If `my-grilling` is unavailable, use the same frontier-question workflow locally without document mode. Do not create ADRs in this fallback path.
- If a decision does not meet the ADR criteria, keep it self-contained in `design.md` without an ADR link.

##### Embedded Grilling Fallback

Use this workflow only when the user selected the `grilling` path and `my-grilling` is unavailable:

1. Read the existing change artifacts and inspect any relevant code or docs before asking questions.
2. Build a decision tree from the user's goal. The frontier is every decision whose prerequisites are settled and can be asked without guessing at unanswered dependencies.
3. Ask the whole current frontier in one round, using concise questions with recommended answers and clear trade-offs. Ask the user to decide; do not decide silently.
4. Wait for the user's answers, then recompute the frontier. Continue until the questions needed for the next artifact are settled and the user confirms shared understanding.
5. Create only the next artifact in the required order, then stop. Do not update `CONTEXT.md`, create ADRs, or create any other document as a side effect of this fallback.
6. At the next artifact boundary, reread the artifacts and ask only newly unblocked questions. Treat answers already captured in those artifacts as settled and never repeat them without a reason.

In either path:

1. Derive a kebab-case `<change-name>` from the user's request unless they provide one.
2. If a target change already exists, update it only when the user is clearly continuing the same work; otherwise ask before overwriting or creating a similarly named change.

## Artifact Templates

### `proposal.md`

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

### `spec/<capability>.md`

Delta specs describe what changes relative to `docs/spec/<capability>.md`. They are not full copies of the main spec.

```markdown
# <Capability> Delta Spec

## Purpose

<Only include when creating a brand-new capability or materially changing the capability's purpose.>

## ADDED Requirements

### Requirement: <New behavior>
The system SHALL <observable behavior>.

#### Scenario: <Scenario name>
- GIVEN <starting condition>
- WHEN <event or action>
- THEN <observable result>

## MODIFIED Requirements

### Requirement: <Existing behavior>
<Only the changed requirement text or changed/new scenarios. Preserve unchanged main-spec content during archive.>

## REMOVED Requirements

### Requirement: <Deprecated behavior>
<Reason it is being removed.>

## RENAMED Requirements

- FROM: `### Requirement: <Old name>`
- TO: `### Requirement: <New name>`
```

Include only sections that apply, except that every change must have at least one delta spec file under `spec/`. A pure refactor still needs a spec delta explaining the externally observable behavior that must remain unchanged, or explicitly stating the preservation requirement.

### `design.md`

Design decisions use the same decision vocabulary as `my-grilling` and `references/ADR-FORMAT.md` where the concepts overlap: `Decision`, rationale, considered options, consequences, and the exact empty marker `None.`. Each `### Decision: <Name>` block represents one decision; split independently changeable decisions into separate blocks. Keep the block compact rather than copying the ADR section template. In the `grilling` path, link a qualifying ADR from the block; otherwise keep the decision self-contained.

```markdown
# Design: <Title>

## Context

<Current state and constraints discovered from the repo.>

## Decisions

### Decision: <Name>
<The chosen decision and rationale. Include considered options, their trade-offs, and consequences when meaningful; write `None.` when there are no meaningful options or consequences. If the grilling path creates an ADR, add a link such as `ADR: [ADR-NNNN](../../adr/NNNN-slug.md)`.>

## Implementation Notes

- `<path-or-component>`: <expected change>

## Verification Commands

- Build: `<full command, or N/A with reason>`
- Test: `<full command, or N/A with reason>`
- Lint: `<full command, or N/A with reason>`
- Typecheck: `<full command, or N/A with reason>`

## Risks

- <Risk and mitigation>
```

### `tasks.md`

```markdown
# Tasks

## 1. <Work Area>
- [ ] 1.1 <Concrete implementation task>
  - Acceptance: <What must be true when this task is complete>
  - Verify: <Specific command or manual check>
  - Files: <Expected files or areas touched>
- [ ] 1.2 <Concrete implementation task>
  - Acceptance: <What must be true when this task is complete>
  - Verify: <Specific command or manual check>
  - Files: <Expected files or areas touched>

## 2. Verify
- [ ] 2.1 <Test, typecheck, lint, manual verification, or review step>
  - Acceptance: <What must be true when verification is complete>
  - Verify: <Specific command or manual check>
  - Files: <Expected files or areas touched>
```

Tasks must be actionable, ordered, and small enough that `my-apply-change` can work through them one at a time. Each implementation task should include `Acceptance`, `Verify`, and `Files` lines so apply and verify can prove completion instead of relying on the checkbox alone.

## Quality Bar

- Specs describe observable behavior, not private implementation details.
- Design explains how the code should change and why.
- Tasks are an implementation checklist, not a second design document.
- Artifacts may evolve during implementation; they are the live plan, not a frozen phase gate.
- Prefer one focused change over a broad change that mixes unrelated intent.

## Final Response

After creating artifacts, report:

- Change path.
- Required artifacts created.
- Main specs consulted or missing.
- Key assumptions and open questions.
- Next step: use `my-apply-change <change-name>` when ready to implement.
