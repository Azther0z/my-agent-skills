---
name: my-planning
description: >-
  Use this whenever the user wants to understand, inspect, challenge, or refine
  what the agent thinks should happen: plans, approaches, roadmaps, breakdowns,
  decision/dependency maps, or updates to existing plans. Support general work
  such as research, learning, writing, events, operations, and software. Make
  the agent's interpretation, evidence, assumptions, options, recommendations,
  steps, and risks understandable to the human. Default to no-artifact
  conversation; save a living Markdown plan only when explicitly requested.
  Use quick, full, or wayfind depth as needed, and maintain or archive saved
  plans. Do not execute the plan. Route formal SDD lifecycle operations to
  my-spec-driven-development and tracker ticket work to my-ticket.
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

Help the human retrieve context from the agent until both understand the work
and the proposed route. `my-grilling` helps the agent understand the human;
`my-planning` helps the human understand the agent. They serve the same mutual
understanding from opposite directions.

The primary output is an inspectable explanation, not a file or a task list.
Expose what you understood, what supports it, what remains uncertain, what you
recommend, and the consequences. Let the human question, correct, or reject
that account. Give decision-relevant reasons and evidence, not a transcript of
internal deliberation.

Support any work: a study program, research project, article, community event,
operational process, or software change. Use the domain's language and evidence;
do not translate everything into code, files, tests, or SDD artifacts.

## Interaction And Artifact Policy

- `no-artifact`: explain and refine the plan in conversation. You may inspect
  relevant, authorized materials, but do not create, edit, or move project files.
- `with-artifact`: run the same understanding loop and create or maintain one
  living Markdown plan within the explicitly requested artifact scope.

Default to `no-artifact`. An ordinary "make a plan" or "explain your approach"
request is conversation-first. An explicit request to save a plan document,
update a named plan file, or archive a saved plan authorizes only that artifact
operation, not execution of the planned work. Inspecting or resuming a saved
plan does not itself authorize edits.

Honor `no artifact`, `no docs`, `questions only`, or `chat only` as `no-artifact`;
honor `with artifact`, `with docs`, `save the plan`, or `write plan.md` as
`with-artifact`. An explicit no-artifact instruction takes priority over the
usual saved-plan behavior: report proposed updates without applying them.

Artifact policy and planning depth are independent. `quick`, `full`, and
`wayfind` work in either policy. Keep those depth values in saved frontmatter;
do not change an existing plan's metadata merely to switch interaction policy.

## Shared Understanding Loop

1. **Ground the explanation.** Read the request and relevant available evidence.
   Separate explicit human requirements, checked facts, recommendations,
   assumptions, and unknowns. A missing fact is not permission to invent one.
2. **Show your current understanding.** State the intended outcome, scope,
   constraints, and what success would look like. Make misinterpretations easy
   to spot before presenting a detailed route.
3. **Expose the proposed route.** Explain the steps, their order and dependencies,
   expected results, and how success will be checked. Show why this route fits
   the evidence, meaningful alternatives and tradeoffs, and what would change
   your recommendation. Flag estimates and their basis rather than inventing
   precise time, cost, or resource commitments.
4. **Expose uncertainty and effects.** Name assumptions, risks, missing evidence,
   irreversible steps, external effects, and decisions reserved for the human.
   Explain what can be planned now and what depends on an unresolved choice.
5. **Let the human inspect and challenge.** Invite questions about any part of
   the account. Answer the actual question before adding detail or asking for
   more context. When challenged, re-check the relevant evidence; correct the
   interpretation and every affected step rather than defending the old plan.
6. **Check shared understanding.** Summarize the resulting route, accepted
   assumptions, and remaining unknowns. Use the `question` tool when available
   to ask whether this matches the human's intent; do not infer agreement from
   silence or from merely answering a factual question. Continue on corrections,
   or pause if the human wants to stop. Keep confirmation of understanding
   distinct from an option to execute.

Use the `question` tool for material human decisions and confirmation. Put the
recommended option first, mark it `(Recommended)`, and explain tradeoffs in the
descriptions; rely on the tool's custom-answer option. Batch independent,
currently unblocked decisions together. If the tool is unavailable, use concise
numbered questions with recommendations.

Do not turn this into another grilling interview. Lead with the agent's
explanation; ask only for context or choices that materially change it. A
missing prerequisite should hold up its dependent branch, not prevent you from
explaining the rest. Offer optional depth rather than dumping every possible
detail at once. The loop ends when the human confirms the shared account,
including any explicitly accepted uncertainty, not when a document is filled.

Shared understanding is not authorization to execute. This skill stops at
planning; identify the next action and any approval it needs. An explicit save
request may produce a draft for review once material blockers are settled, but
do not describe that draft as an agreed or active plan without confirmation.

## Operating Contract

- Use plain language in conversation and plain Markdown for saved plans. Do not
  require a repository, CLI, issue tracker, plugin, or another planning system.
- In artifact mode, use an explicitly requested path or the existing plan's
  location. Otherwise default to `docs/change/<change-name>/plan.md` in the
  current workspace. This is a storage convention, not a software requirement.
  If no writable workspace is established, ask for a location before saving.
- A saved plan is the canonical source while the work is plan-only. Do not
  create a second live plan for the same effort.
- Preserve unrelated work and existing plan history. Never silently overwrite a
  user's plan, formal SDD artifacts, or another active change.
- Inspect accessible facts yourself: supplied materials, active plans, research,
  schedules, resource records, and relevant policies. For software, also inspect
  repository status, code, tests, configuration, specs, and ADRs. Ask the human
  only for context or decisions the authorized sources cannot answer.
- Ask only material blockers for `quick` and `full` plans. A question is
  material when its answer changes the outcome, scope, approach, commitments,
  safety, dependencies, or success checks. Label non-material uncertainty as an
  assumption instead of opening a long interview; never present it as agreement.
- Do not execute deliverables, send messages, book, purchase, commit, push,
  install, publish, or change an external system as part of planning. Evidence
  inspection is not permission to carry out research or prototypes proposed as
  work items.
- A plan is allowed to change as work reveals new information. Explain a
  material correction before any downstream work relies on the obsolete route;
  update a saved plan only when its maintenance is authorized.

## Modes

Select the lightest mode that can hold the work. Honor an explicit mode first;
otherwise classify from available evidence and the user's intent. These are
planning depths or lifecycle operations, not automatic permission to save files.

| Intent or shape | Mode | Result |
|---|---|---|
| Small, understood work that fits one focused session | `quick` | A concise explanation and route; saved only if requested |
| Settled work spanning sessions or several reviewable outcomes | `full` | A detailed route with phases, dependencies, and checkpoints |
| Work whose destination or route is still unclear | `wayfind` | An explained decision map with a frontier and unknown areas |
| Resume, inspect, reconcile, or update a saved plan | `maintain` | An evidence-backed status explanation; authorized corrections preserve history |
| Hand a plan into the formal SDD lifecycle | `promote` | A handoff to SDD; this skill does not create formal artifacts |
| Close a saved plan-only effort | `archive` | An explicitly requested archive, or a handoff to SDD archive |

For drafting, refining, reviewing, linking, or splitting a Jira or tracker
ticket, route to `my-ticket`. A ticket is not a planning mode or a fifth SDD
artifact.

Do not choose `wayfind` merely because an effort is large. Use `full` when the
work is already understood well enough to describe reviewable outcomes. Use
`wayfind` when unresolved decisions are what make the route unknowable.

## Scale And Escalation

Use these as heuristics, not gates:

- **Quick**: one outcome, low or moderate risk, understood activities and
  resources, and roughly three to ten work items without complicated coordination.
- **Full**: multiple sessions, several independently verifiable outcomes, a
  meaningful dependency graph, or a need for phase checkpoints. Keep phases
  small enough to review and verify; do not split work into categories merely to
  make a longer list.
- **Wayfind**: a new initiative, an unfamiliar domain, or a major transition where
  the destination, key decisions, or dependency route is not yet clear. It
  produces shared understanding and a map, not execution deliverables.
- **Consider SDD promotion for software** when durable behavior specifications,
  API/schema/migration contracts, security/privacy boundaries, or a formal
  verify/archive lifecycle warrant it. Explain the recommendation and get the
  user's agreement to hand off. Large or risky non-software work does not
  automatically become SDD work.

If a quick plan grows beyond its scale, explain the change in depth. For an
authorized saved-plan update, keep its history and change its frontmatter to
`mode: full` or `mode: wayfind`. Do not start a second plan just because the
first estimate was wrong.

## Plan Location And Metadata

This section applies only to `with-artifact`. Create the directory lazily. The
default plan-only folder has this shape:

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

- `draft`: the route is proposed but shared understanding is not yet confirmed.
- `active`: the human confirmed the plan, or authorized work is underway.
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
`wayfind` uses the map sections below before it has an execution graph. In
`no-artifact`, explain the same substance in conversation without requiring
document headings, frontmatter, or a filesystem path.

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
<The result the human wants and how they will recognize success.>

## Scope

### In scope
- ...

### Out of scope
- ...

## Current State
- Evidence inspected: ...
- Human requirements: ...
- Relevant existing situation: ...
- Assumptions: ...
- Unknowns: ...

## Approach
<The proposed route, why it fits, meaningful alternatives, and what would
change the recommendation. For architectural decisions, keep durable rationale
in the ADR; state only the resulting constraint here and link that ADR.>

## Work Graph

### Phase 1: <Name>
- [ ] 1.1 <Reviewable outcome or concrete work item>
  - Depends on: None
  - Acceptance: <Observable result>
  - Verify: <Evidence, review, observation, exercise, or test>
  - Areas/resources: <Affected materials, people, resources, or files>

## Validation And Risks
- Validation: ...
- Risk: ...
  - Mitigation: ...

## Decisions
- YYYY-MM-DD — <routine planning choice, who confirmed it, and short reason>
- Architectural constraint: <one-line constraint>; ADR: <link>

## Understanding Check
- Confirmed with the human: ...
- Still proposed or unresolved: ...

## Progress
- YYYY-MM-DD — <what changed, evidence, and next action>

## Next Action
<The smallest useful next step.>
```

### Work item rules

- Prefer a reviewable outcome over a category-only bucket: "pilot one workshop
  and review participant feedback" instead of "do logistics". In software, use
  vertical slices rather than "do all database work".
- Every item has an outcome, acceptance condition, verification method, and
  affected areas or resources. Use domain-appropriate checks: source coverage
  for research, a practice exercise for learning, editorial review for writing,
  or a readiness checklist for an event. Do not invent test commands for work
  that has no software surface, or write vague "handle edge cases" items.
- Record ordinary, reversible planning choices here. When a choice
  qualifies as an architectural decision, record its rationale, alternatives,
  and tradeoffs only in an ADR; other artifacts may state the resulting
  constraint briefly and link that ADR. Create a new ADR only through a
  separately confirmed `my-grilling with-artifact` step; do not create one as a
  side effect of maintaining this plan.
- `Depends on` names only true prerequisites. Use `None` for work that can
  start now. Never create cycles; minimize chain depth and identify the
  critical path.
- Add an optional `Interface contract` when another work item or agent relies
  on a handoff, deliverable format, behavior, or ownership boundary. Include
  owners, timing, and resource estimates only where useful; label unconfirmed
  assignments and estimates instead of making commitments for other people.
- Mark completion only after the acceptance and verification evidence exists.
  Record a review, observation, exercise result, inspection, or other proof;
  for software, a test result or commit SHA can be supporting evidence.
- Keep related preparation, execution, checking, and documentation in the same
  work item when they form one independently verifiable outcome.

### Full-plan additions

For `full`, add:

```markdown
## Checkpoints

| Phase | Exit evidence | Status |
|---|---|---|
| 1 | <review, observation, exercise, test, or other evidence> | pending |
```

Each phase should deliver something reviewable. Add a final integration and
outcome check where needed; do not leave all verification as an unowned final
phase.

## Quick Mode

Use `quick` for requests such as "plan a study session", "explain your approach
to this article", or "what files and steps should we touch?".

1. Inspect the relevant materials and current situation. A repository evidence
   pass is appropriate only when the work involves a repository.
2. Explain the understood outcome, scope, evidence, proposed steps, meaningful
   alternatives, success checks, and risks at a concise level.
3. Ask one compact batch of material blockers, if any; label other assumptions.
   Invite scrutiny and follow the shared understanding loop.
4. In `no-artifact`, keep the route in conversation. In `with-artifact`, save
   one plan with a short work graph, acceptance, verification, and risks. Do
   not create formal SDD artifacts for a quick plan.
5. Report what is confirmed versus proposed, the next action, and checks not
   run. Include a plan path only when an artifact exists.

## Full Mode

Use `full` when the route is known but the work will cross sessions or needs
coordination.

1. Do the same evidence pass and understanding loop as `quick`, then explain
   the delivery boundary, reviewable outcomes, phase exits, critical path, and
   independent work.
2. Separate hard blockers from soft coordination preferences. Do not claim
   parallelism where items depend on an unsettled shared decision, the same
   scarce resource, or overlapping ownership.
3. Include affected areas/resources, handoff contracts where needed, acceptance,
   verification, out-of-scope work, and risks. Explain estimates and proposed
   ownership rather than silently assigning people or budgets.
4. Add checkpoints and a `Next Action` that names the current frontier.
5. Keep the route in conversation unless saving was requested; if saved, keep
   one living plan. Do not create or publish tracker tickets; route ticket
   drafting or maintenance to `my-ticket`.

## Wayfind Mode

Use `wayfind` when unresolved decisions make the route unclear, even for a small
effort. Explain the map and the dependencies before asking the human to choose.
The plan is a shared map of decisions, not a disguised execution backlog or an
excuse to replace explanation with an interview. It can remain entirely in
conversation.

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
  - Type: research | trial | human decision | task
  - Depends on: None
  - Question: <The decision to resolve>

## Not Yet Specified
- <In-scope area visible but not yet sharp enough to become an actionable
  execution work item>

## Out Of Scope
- <Work consciously ruled beyond the destination>
```

Rules for the map:

- Name the destination before listing decisions. The destination fixes scope.
- A decision node is a question whose prerequisites are settled, not a coding
  task or tracker issue.
- Facts are agent work: inspect relevant authorized materials and primary
  sources. Decisions remain the user's decisions; show the options, evidence,
  recommendation, tradeoffs, and unknowns before asking them to choose.
- Use `research` for missing facts, `trial` for a question needing an experiment
  or rehearsal, `human decision` for a preference or commitment, and `task` only
  for manual work that blocks a decision. Existing `prototype` and `grilling`
  labels can remain as aliases; do not rewrite old maps solely for terminology.
  Planning identifies a trial or research work item; it does not authorize
  executing it. An extended human-context interview may be handed to
  `my-grilling`, but is not the default planning interaction.
- Keep unresolved but currently unformulatable work under `Not Yet Specified`.
  Keep deliberately excluded work under `Out Of Scope`; never let either list
  masquerade as an available execution task.
- Explain the whole current frontier. Inspect factual prerequisites yourself;
  ask all independent, currently unblocked human decision nodes in one round.
  After the user's answers, record them in `Decisions So Far`, recompute
  dependencies, and continue with the newly unblocked frontier. Do not impose
  an arbitrary one-node-per-session limit; pause when the user asks, a genuine
  blocker prevents progress, or the session ends.
- After each answer, explain how it changes the map and recommendation. When
  the route clears, check shared understanding and recommend `quick` or `full`
  as appropriate, or SDD promotion for relevant software work; do not silently
  start execution.
- For a saved map, if a node produces an architectural decision that meets ADR
  criteria, pause that artifact branch for a separately confirmed
  `my-grilling with-artifact` ADR step. Record only its resulting constraint
  and ADR link in the saved map. In `no-artifact`, explain the decision without
  creating an ADR or making documentation a prerequisite for conversation.

## Maintain Mode

Use `maintain` for "resume the plan", "update the plan", "what is left?",
"is this plan stale?", "mark this complete", or "reconcile the plan with the
current work". Explain the reconciliation to the human; a file update is not a
substitute for shared understanding.

1. Select the named plan or established plan location. If none is named, scan
   the current workspace's `docs/change/*/plan.md` and exclude archived folders;
   ask when more than one active plan fits. Do not search unrelated locations.
2. If the plan has `status: promoted` or any confirmed formal SDD artifact already
   exists in its change folder, do not edit `plan.md`. Inspect content and
   context: an unrelated file named `proposal.md` or `design.md` in a general
   workspace does not by itself establish SDD promotion. Report a confirmed
   prelude as frozen provenance and hand off to the appropriate
   `my-spec-driven-development` mode. If promotion metadata is missing, explain
   that SDD owns the metadata-only repair under its shared artifact contract;
   a read-only request does not authorize that repair.
3. Otherwise, read the complete plan and the current evidence it names:
   deliverables, reviews, records, or other domain checks. For software, include
   relevant status/diff, implementation, tests, and linked ADRs/specs.
4. Reconcile each item:
   - `[ ]` pending and not started;
   - `[~]` in progress, with the current stopping point;
   - `[x]` complete, with acceptance and verification evidence;
   - `[!]` blocked, with the actual blocker and next resolution;
   - `[-]` intentionally skipped, with the reason and consequence.
5. Explain the proposed corrections and their evidence. In `no-artifact`,
   report them without editing. When updates are explicitly authorized, update
   progress, checkpoints, decisions, risks, status, and `updated` date in place;
   append a concise progress entry without erasing earlier reasoning.
6. If new evidence disproves the approach, distinguish the smallest safe
   correction from a material change. Ask before changing outcome, scope,
   commitments, externally visible behavior, or an architectural decision.
   Once confirmed, explain the revision and update affected work items within
   the authorized artifact scope; do not execute the revised work here.
7. Recompute dependencies and the next frontier. Remove a blocker only when
   its evidence is present, not because the task feels probably done.
8. Report stale assumptions, missing evidence, blocked items, and the next
   action. Do not claim the plan is current if relevant evidence was not checked.

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
is not a substitute for the formal contract. This is an optional software
specialization, not the destination of every general plan. Use `promote` when
software work needs durable behavior specs, formal design decisions, task-level
verification, or a verify/archive lifecycle and the user agrees to the handoff.
`my-planning` does not create or update formal SDD artifacts;
`my-spec-driven-development` owns their format, grilling, approval boundaries,
and lifecycle.

Before handing off:

1. Read the full saved plan or confirmed conversational account. Inspect the
   intended change folder so the handoff does not collide with formal work. If
   the plan is saved elsewhere, identify its path in the handoff; do not copy or
   relocate it without permission, or claim it is already a compatible prelude.
2. Summarize the outcome, scope, settled decisions, risks, and remaining
   questions. Do not decide unresolved behavior for the user.
3. Direct the user to `my-spec-driven-development plan <change-name>`. That
   skill reads any compatible prelude, consults main specs and ADRs, performs
   its required grilling, and creates only the next confirmed formal artifact.
4. Do not create a plan file merely to hand off a conversation, or mark a saved
   plan promoted yet. For an existing compatible prelude, the SDD plan mode
   performs that transition only after its first formal artifact is created
   successfully.

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
4. For the default layout, move the whole folder to
    `docs/change/archive/YYYY-MM-DD-<change-name>/` without overwriting an
    existing target. Use today's date unless the change name already starts
    with `YYYY-MM-DD-`; do not add a second date prefix.

For a custom location, explain and confirm the archive destination and affected
files first; do not move a shared folder or unrelated materials. An explicit
`no-artifact` request allows only an archive recommendation, not a move.

If formal SDD artifacts exist, stop and hand the change to
`my-spec-driven-development archive`; do not bypass its delta-spec sync and
verification rules.

## Final Response

Report:

- artifact policy, planning depth or lifecycle mode, and a short scale rationale;
- the understood outcome and proposed route, at the human's requested depth;
- what the human confirmed versus what remains proposed;
- assumptions, alternatives, risks, blockers, and stale evidence;
- verification actually performed and skipped checks with reasons;
- the next proposed action and any authorization or handoff it needs;
- only if an artifact exists: its path, status, and actual file changes.

In `no-artifact`, do not invent a plan path or imply that anything was saved.
Never claim shared understanding without human confirmation, or claim the work
is complete when unchecked items, unresolved blockers, or required formal
artifacts remain. A finished planning conversation does not mean finished work.
