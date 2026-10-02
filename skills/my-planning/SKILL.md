---
name: my-planning
description: >-
  Create and maintain a living Markdown plan for software work, from a compact
  single-session implementation plan to a large multi-session decision map.
  Use this whenever the user asks for a plan, implementation plan, roadmap,
  breakdown, task graph, dependency map, wayfinding, or to update, resume,
  validate, or archive an existing plan. Default to a light plan; escalate to
  a full plan or wayfinding only when the scope or uncertainty requires it.
  Do not use this for explicit spec-driven lifecycle operations such as SDD
  init, formal change artifacts, apply, verify, or archive; use
  my-spec-driven-development for those operations or promote a plan first. Do
  not use this for drafting, reviewing, splitting, or publishing tracker
  tickets; use my-ticket for those operations.
sources:
  - https://agentskills.io/specification
  - https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md
  - https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/workflows.md
  - https://raw.githubusercontent.com/obra/superpowers/main/skills/writing-plans/SKILL.md
  - https://raw.githubusercontent.com/obra/superpowers/main/skills/brainstorming/SKILL.md
  - https://raw.githubusercontent.com/wshobson/agents/main/plugins/conductor/skills/track-management/SKILL.md
  - https://raw.githubusercontent.com/wshobson/agents/main/plugins/conductor/skills/track-management/references/details.md
  - https://raw.githubusercontent.com/wshobson/agents/main/plugins/agent-teams/skills/task-coordination-strategies/SKILL.md
  - https://raw.githubusercontent.com/wshobson/agents/main/plugins/conductor/skills/context-driven-development/SKILL.md
  - https://raw.githubusercontent.com/wshobson/agents/main/plugins/before-you-build/skills/before-you-build/SKILL.md

---

# My Planning

Create a plan that is useful before implementation and remains useful while
implementation changes what was previously understood. The default is one
small, living plan. A large effort gets a richer plan in the same format, not
a forced spec-driven ceremony.

## Operating Contract

- Use plain Markdown. Do not require a CLI, issue tracker, plugin, or another
  planning system.
- Plan-only changes live at `docs/change/<change-name>/plan.md`.
- The plan is the canonical source while the change is plan-only. Do not create
  a second plan file for the same change.
- Preserve unrelated work and existing plan history. Never silently overwrite a
  user's plan, formal SDD artifacts, or another active change.
- Inspect facts yourself: repository status, relevant code, tests, configuration,
  existing specs, ADRs, and active plans. Ask the user only for decisions or
  constraints the environment cannot answer.
- Ask only material blockers for `quick` and `full` plans. A question is
  material when its answer changes scope, behavior, architecture, safety,
  dependencies, or verification. Record non-material uncertainty as an
  assumption instead of opening a long interview.
- Do not implement code, commit, push, install, publish, or change an external
  system as part of planning.
- A plan is allowed to change during implementation. Update it before making a
  material change that would otherwise make the plan false.

## Modes

Select the lightest mode that can hold the work. Honor an explicit mode first;
otherwise classify from the repository evidence and the user's intent.

| Intent or shape | Mode | Result |
|---|---|---|
| Small, understood work that fits one focused session | `quick` | One concise living plan |
| Settled work spanning sessions or several vertical slices | `full` | One detailed plan with phases, dependencies, and checkpoints |
| Large work whose destination or route is still unclear | `wayfind` | A decision map with a frontier and fog-of-war sections |
| Resume, inspect, reconcile, or update a plan | `maintain` | Progress and plan corrections with history preserved |
| Hand a plan into the formal SDD lifecycle | `promote` | A handoff to SDD; this skill does not create formal artifacts |
| Finish a plan-only change | `archive` | An archived plan, or a handoff to SDD archive |

For drafting, refining, reviewing, linking, or splitting a Jira or tracker
ticket, route to `my-ticket`. A ticket is not a planning mode or a fifth SDD
artifact.

Do not choose `wayfind` merely because a feature is large. Use `full` when the
work is already understood well enough to describe implementation slices. Use
`wayfind` when unresolved decisions are what make the route unknowable.

## Scale And Escalation

Use these as heuristics, not gates:

- **Quick**: one outcome, low or moderate risk, known code surface, roughly
  three to ten work items, and no need for parallel agents or a shared tracker.
- **Full**: multiple sessions, several independently verifiable slices, a
  meaningful dependency graph, or a need for phase checkpoints. Keep phases
  small enough to review and verify; do not split work into layers merely to
  make a longer list.
- **Wayfind**: a greenfield effort, a major migration, or a large feature where
  the destination, key decisions, or dependency route is not yet clear. It
  produces decisions and a map, not implementation deliverables.
- **Promote to SDD** when the user explicitly wants formal specifications, when
  behavior must remain a durable contract, or when the change involves an API,
  schema, migration, security/privacy boundary, several capabilities, or a
  formal verify/archive lifecycle.

If a quick plan grows beyond its scale, keep its history and change its
frontmatter to `mode: full` or `mode: wayfind`. Do not start a second plan just
because the first estimate was wrong.

## Plan Location And Metadata

Create the directory lazily. A plan-only change has this shape:

```text
docs/change/<change-name>/
└── plan.md
```

Use a stable, kebab-case `<change-name>` based on the user’s name when given;
otherwise derive one from the outcome. If a similarly named active folder
exists, inspect it and ask before reusing it unless continuation is explicit.

Plan-only `plan.md` begins with:

```yaml
---
type: plan
name: <change-name>
mode: quick | full | wayfind
status: draft | active | blocked | complete | abandoned | superseded | promoted
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Keep `status` honest:

- `draft`: shape is being established; implementation has not started.
- `active`: the plan is approved or implementation is underway.
- `blocked`: progress cannot continue until a named dependency or decision is
  resolved.
- `complete`: all accepted work and verification are done.
- `abandoned`: the user stopped the effort without claiming completion.
- `superseded`: another plan replaces this one; link the replacement.
- `promoted`: the first formal SDD artifact exists. This plan is frozen
  provenance, not an active plan; add `formal_change: docs/change/<name>/` to
  link the SDD change folder.

## The Plan Document

Use the smallest version of this structure that is still useful. `quick` uses
the first sections and a short work graph. `full` adds phases and checkpoints.
`wayfind` uses the map sections below before it has an implementation graph.

```markdown
---
type: plan
name: <change-name>
mode: quick | full | wayfind
status: draft | active | blocked | complete | abandoned | superseded | promoted
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Plan: <Title>

## Outcome
<The user-visible or repository-level result this plan is meant to achieve.>

## Scope

### In scope
- ...

### Out of scope
- ...

## Current State
- Evidence inspected: ...
- Relevant existing behavior: ...
- Assumptions: ...

## Approach
<The chosen route and implementation approach. Keep architectural rationale
in its ADR; state only the resulting constraint here and link that ADR.>

## Work Graph

### Phase 1: <Name>
- [ ] 1.1 <Vertical slice or concrete work item>
  - Depends on: None
  - Acceptance: <Observable result>
  - Verify: <Command or manual check>
  - Files/areas: <Expected edit surface>

## Validation And Risks
- Validation: ...
- Risk: ...
  - Mitigation: ...

## Decisions
- YYYY-MM-DD — <routine planning/implementation choice and short reason>
- Architectural constraint: <one-line constraint>; ADR: <link>

## Progress
- YYYY-MM-DD — <what changed, evidence, and next action>

## Next Action
<The smallest useful next step.>
```

### Work item rules

- Prefer a vertical slice that produces observable behavior over a horizontal
  layer such as "do all database work".
- Every item has an outcome, acceptance condition, verification method, and
  files or areas. Do not write "handle edge cases" without naming them.
- Record ordinary, reversible implementation choices here. When a choice
  qualifies as an architectural decision, record its rationale, alternatives,
  and tradeoffs only in an ADR; other artifacts may state the resulting
  constraint briefly and link that ADR. Create a new ADR only through a
  separately confirmed `my-grilling with-artifact` step; do not create one as a
  side effect of maintaining this plan.
- `Depends on` names only true prerequisites. Use `None` for work that can
  start now. Never create cycles; minimize chain depth and identify the
  critical path.
- Add an optional `Interface contract` when another work item or agent relies
  on a name, shape, behavior, or file ownership boundary.
- Mark completion only after the acceptance and verification evidence exists.
  Record a commit SHA when one exists; otherwise record the command, test, or
  inspection that proves completion.
- Keep related setup, implementation, tests, and documentation in the same
  work item when they form one independently verifiable slice.

### Full-plan additions

For `full`, add:

```markdown
## Checkpoints

| Phase | Exit evidence | Status |
|---|---|---|
| 1 | <test, review, or manual result> | pending |
```

Each phase should deliver something reviewable. Add a final integration and
verification item; do not leave all testing as an unowned final phase.

## Quick Mode

Use `quick` for explicit requests such as "make a plan for this small change"
or "what files and steps should we touch?".

1. Inspect status, the repository contract, relevant files, existing tests,
   configuration, and nearby ADRs/specs.
2. Confirm the outcome, scope, and likely edit surface from the request and
   evidence.
3. Ask one compact batch of material blocker questions, if any. If none are
   needed, state assumptions in the plan.
4. Write one `plan.md` with a short work graph, acceptance, verification, and
   risks. Do not create `proposal.md`, delta specs, `design.md`, or `tasks.md`
   for a quick plan.
5. Report the plan path, assumptions, next action, and checks not run.

An explicit request to create a plan document authorizes this one plan artifact
after material blockers are settled. A vague request for advice without a
create/save instruction is chat-first; offer the path rather than writing.

## Full Mode

Use `full` when the route is known but the work will cross sessions or needs
coordination.

1. Do the same evidence pass as `quick`, then identify the delivery boundary,
   vertical slices, phase exits, critical path, and independent work.
2. Separate hard blockers from soft coordination preferences. Do not claim
   parallelism where two items edit the same load-bearing interface.
3. Include owned files/areas, interface contracts, acceptance, verification,
   out-of-scope work, and risks for each item.
4. Add checkpoints and a `Next Action` that names the current frontier.
5. Keep the plan as one living `plan.md`. Do not create or publish tracker
   tickets; route ticket drafting or maintenance to `my-ticket`.

## Wayfind Mode

Use `wayfind` when the work is too large or uncertain to hold in one session.
The plan is a shared map of decisions, not a disguised implementation backlog.

Add these sections:

```markdown
## Destination
<What reaching the end of the map means.>

## Notes
<Domain, standing constraints, relevant skills, and preferences.>

## Decisions So Far
- <Closed routine decision>: <short answer and evidence>
- <Architectural constraint>: <one-line outcome>; ADR: <link>

## Frontier
- [ ] <Decision node that is currently unblocked>
  - Type: research | prototype | grilling | task
  - Depends on: None
  - Question: <The decision to resolve>

## Not Yet Specified
- <In-scope area visible but not yet sharp enough to become an actionable
  implementation work item>

## Out Of Scope
- <Work consciously ruled beyond the destination>
```

Rules for the map:

- Name the destination before listing decisions. The destination fixes scope.
- A decision node is a question whose prerequisites are settled, not a coding
  task or tracker issue.
- Facts are agent work: inspect the repository and primary sources. Decisions
  remain the user's decisions; do not answer a human choice on their behalf.
- Use `research` for facts, `prototype` for a runnable question, `grilling` for
  human decisions, and `task` only for manual work that blocks a decision.
- Keep unresolved but currently unformulatable work under `Not Yet Specified`.
  Keep deliberately excluded work under `Out Of Scope`; never let either list
  masquerade as an available implementation task.
- Ask all independent, currently unblocked decision nodes in one frontier
  round. After the user's answers, record them in `Decisions So Far`, recompute
  dependencies, and continue with the newly unblocked frontier. Do not impose
  an arbitrary one-node-per-session limit; pause when the user asks, a genuine
  blocker prevents progress, or the session ends.
- When the map clears, stop planning and recommend `full` or `promote`; do not
  silently start implementation.
- If resolving a node produces an architectural decision that meets ADR
  criteria, pause that branch for a separately confirmed
  `my-grilling with-artifact` ADR step. Record only its resulting constraint
  and ADR link in the map.

## Maintain Mode

Use `maintain` for "resume the plan", "update the plan", "what is left?",
"is this plan stale?", "mark this complete", or "reconcile the plan with the
code".

1. Select the named plan. If none is named, scan `docs/change/*/plan.md` and
   exclude archived folders; ask when more than one active plan fits.
2. If the plan has `status: promoted` or any formal SDD artifact already exists
   in its folder, do not edit `plan.md`. Report that it is frozen provenance
   and hand off to the appropriate `my-spec-driven-development` mode. If a
   formal artifact exists but the promotion metadata is missing, ask SDD to
   repair only its promotion metadata and `updated` date as described in its
   shared artifact contract.
3. Otherwise, read the complete plan, current status/diff,
   implementation and tests named by the plan, and any linked ADRs/specs.
4. Reconcile each item:
   - `[ ]` pending and not started;
   - `[~]` in progress, with the current stopping point;
   - `[x]` complete, with acceptance and verification evidence;
   - `[!]` blocked, with the actual blocker and next resolution;
   - `[-]` intentionally skipped, with the reason and consequence.
5. Update progress, checkpoints, decisions, risks, status, and `updated` date
   in place. Append a concise progress entry; do not erase earlier reasoning.
6. If implementation disproves the approach, distinguish the smallest safe
   correction from a material change. Ask before changing outcome, scope,
   externally visible behavior, or an architectural decision. Once confirmed,
   record the revision and update affected work items before editing code.
7. Recompute dependencies and the next frontier. Remove a blocker only when
   its evidence is present, not because the task feels probably done.
8. Report stale assumptions, missing evidence, blocked items, and the next
   action. Do not claim the plan is current if relevant files were not checked.

Plan maintenance is not a rewrite pass. The history of why the route changed
is part of the artifact.

## Ticket Boundary And Handoff

Tickets are deliberately outside this skill's artifact lifecycle. A story or
task may correspond to the same externally meaningful change as a plan or SDD
change, but the ticket owns only its compact tracker brief. It does not create,
rewrite, or become the source of truth for `plan.md`, specs, design, tasks, or
ADRs.

If the user asks to turn a plan into a Jira ticket, invoke `my-ticket` with the
plan and any formal artifacts as references. Do not create local ticket files,
copy the full work graph into the ticket, or change the plan as a side effect.
If the user presents a ticket before planning begins, use it as request context
and independently confirm material outcome and scope in this workflow; the
formal artifact remains owned by the planning or SDD mode that creates it.

## Promote Mode And SDD Handoff

`plan.md` is intentionally compatible with the formal SDD change folder, but it
is not a substitute for the formal contract. Use `promote` when the work needs
durable behavior specs, formal design decisions, task-level verification, or a
verify/archive lifecycle. `my-planning` does not create or update formal SDD
artifacts; `my-spec-driven-development` owns their format, grilling, approval
boundaries, and lifecycle.

Before handing off:

1. Read the full plan and inspect the current change folder so the handoff does
   not collide with existing formal work.
2. Summarize the outcome, scope, settled decisions, risks, and remaining
   questions. Do not decide unresolved behavior for the user.
3. Direct the user to `my-spec-driven-development plan <change-name>`. That
   skill reads the prelude, consults main specs and ADRs, performs its required
   grilling, and creates only the next confirmed formal artifact.
4. Do not mark the plan promoted yet. The SDD plan mode performs that transition
   only after its first formal artifact has been created successfully.

The intended mapping is:

| Plan content | Formal artifact |
|---|---|
| Outcome, scope, approach, affected capability | `proposal.md` |
| Observable behavior and scenarios | `spec/<capability>.md` delta spec |
| Decisions, interfaces, risks, implementation notes | `design.md` |
| Work graph, acceptance, verification, files, blockers | `tasks.md` |

Use the SDD skill as the sole authority for formal artifact order and formats.
The prelude becomes frozen provenance at the first formal artifact boundary;
the formal artifacts own each confirmed concern as they are written and become
the complete implementation contract only when the required set exists.

If the user asks to turn a plan into tickets, hand off to `my-ticket`. Use the
plan's graph as source context for ticket boundary decisions, but keep the
ticket's description compact and point to the plan or SDD artifacts. Never
invent tracker commands or publish externally from a plan-only operation.

## Archive Mode

For a plan-only folder:

1. Confirm the user wants to close, abandon, or supersede it.
2. Ensure all accepted work is complete, explicitly deferred, or intentionally
   skipped; report remaining unchecked work.
3. Set the final status and append the reason/evidence to `Progress`.
4. Move the whole folder to
   `docs/change/archive/YYYY-MM-DD-<change-name>/` without overwriting an
   existing target. Use today's date unless the change name already starts
   with `YYYY-MM-DD-`; do not add a second date prefix.

If formal SDD artifacts exist, stop and hand the change to
`my-spec-driven-development archive`; do not bypass its delta-spec sync and
verification rules.

## Final Response

Report:

- selected mode and scale rationale;
- plan path and status;
- files or artifacts created/updated;
- decisions, assumptions, blockers, and stale evidence;
- verification actually performed and skipped checks with reasons;
- the next action or formal SDD handoff.

Never claim a plan is complete when unchecked work, unresolved blockers, or
required formal artifacts remain.
