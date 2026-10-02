---
name: my-ticket
description: >-
  Draft, refine, review, split, and prepare compact work tickets for Jira,
  GitHub Issues, or another configured tracker. Use this when the user asks to
  write, improve, groom, review, link, or publish a story, task, bug, spike,
  change ticket, or subtask. A ticket is a self-contained execution brief that
  points to planning, spec-driven, design, and decision artifacts; this skill
  does not
  create or modify those artifacts and does not publish externally without an
  explicit configured integration and authorization.
sources:
  - https://agentskills.io/specification
  - https://www.atlassian.com/agile/project-management/user-stories
  - https://www.atlassian.com/agile/project-management/definition-of-ready
  - https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/
  - https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues

---

# My Ticket

Create a compact work-tracking ticket that is useful to the implementer,
reviewer, and person accepting the work. The ticket captures the execution
contract; it does not replace a plan, an SDD change, a design record, or an ADR.

## Operating Contract

- A **ticket** is the tracker work item. “Story”, “task”, “bug”, and “spike”
  are ticket types; “ticket” is the umbrella term.
- A story/change ticket normally represents one externally coherent outcome and
  one acceptance boundary. It may require several subtasks.
- An Epic or initiative is a larger grouping of change tickets. Do not equate
  an Epic with an SDD change.
- In the common case, one story/change ticket corresponds to one SDD change
  folder. Treat that as a useful association, not a mandatory one-to-one rule.
- A subtask is an implementation assignment inside the parent ticket. It does
  not become a separate change merely because it has its own files or tests.
- A ticket may be created before any plan, grilling, or SDD artifacts exist.
  That initial ticket is an intake brief, not proof that the work is ready to
  implement.
- Tickets point to existing `plan.md`, SDD artifacts, ADRs, code, and related
  tickets. Ticket work does not create, rewrite, or become the source of truth
  for those artifacts.
- Do not create `docs/change/<name>/ticket.md` as a default side effect. This
  skill produces a copy-ready ticket payload. Write a repository draft only
  when the user specifies a target path; inspect it first and ask before
  overwriting existing content. `my-planning` and
  `my-spec-driven-development` own their own artifacts.
- Jira and GitHub Issues are supported ticket targets; use the platform-specific
  mappings below. For any other tracker, require an explicitly configured
  integration and known field mapping.
- Do not invent tracker commands, issue keys/numbers, links, fields, workflows,
  or integration capabilities. Without a configured tracker integration, stop
  at a reviewable payload for manual copy or an explicitly requested local
  draft.
- Never claim that a ticket was created or updated externally without actual
  evidence of that operation.

## Ticket And Artifact Relationship

The lifecycle is convergent, not a required linear order:

```text
ticket first  ─┐
plan first     ├──> one change understood well enough to execute
SDD first      ─┘
```

The entry point does not determine artifact authority:

| Concern | Authority |
|---|---|
| Tracker identity, type, assignee, status, priority, parent links | Tracker fields |
| Concise current why/what, scope, guidance, acceptance summary | Ticket description |
| Route, work graph, dependencies, progress, next action | `my-planning` plan |
| Durable observable behavior | SDD proposal and delta specs |
| Routine implementation choices | SDD design |
| Architectural rationale, alternatives, and tradeoffs | Relevant ADR; other artifacts may state the resulting constraint and link it |
| Ordered implementation checklist | SDD `tasks.md` |

When a ticket exists first, use it as a request and context while invoking the
appropriate planning or SDD skill. Re-confirm material behavior and scope
there; do not mechanically promote the ticket text into formal artifacts.
When artifacts exist first, use them as source material for a concise ticket,
without copying their full detail.

After the artifacts are settled, the ticket should link to them. If an artifact
does not exist yet, do not invent a link; leave the reference out or label it
as a planned follow-up. A ticket update is a projection of settled context,
not a new planning decision.

## Ticket Boundary

Keep one change/story/task/bug ticket when it has:

- one externally meaningful outcome;
- one coherent acceptance boundary;
- one primary owner or team, even if several people implement subtasks;
- one scope that can be prioritized, reviewed, and tracked together; and
- a size that fits the team's delivery horizon after decomposition.

Split into sibling tickets when the work has a separate outcome, acceptance
boundary, priority or release decision, owner/team, or meaningful independent
value. Keep it as subtasks when the pieces are only different implementation
assignments required to satisfy the same parent outcome.

Do not split only because the change touches multiple files or layers. Do not
keep unrelated outcomes together only because they share a codebase.

### Parent ticket versus subtask

The parent ticket answers: “What change is delivered, for whom or for what
operational purpose, and how do we accept it?”

Each subtask answers: “What bounded implementation assignment must be completed
to deliver that parent change?” A subtask still needs an outcome, acceptance,
verification, and owned area, but may reference the parent for shared context.
If a subtask needs its own independent rationale, release decision, or
acceptance by a different stakeholder, reconsider whether it is a sibling
ticket instead.

SDD tasks and tracker subtasks are not automatically one-to-one. `tasks.md` is
an execution checklist for the formal change; map its items to tracker work
only when the team's tracking practice needs that decomposition.

## Ticket Content Contract

Use the following compact structure. Keep sections short and omit a section
only when it genuinely does not apply. Do not hide an unknown behind a confident
sentence; name it as an open question or blocker.

```markdown
## Context / As-is
<Current behavior, problem, or operational state. Include evidence when useful.>

## Outcome / To-be
<What will be true after this ticket, and who or what benefits.>

## Scope

### In scope
- <Included behavior or boundary>

### Out of scope
- <Explicitly excluded behavior or follow-up>

## Guidance
- <Settled constraint, interface, compatibility, safety, or implementation direction>

## Acceptance criteria
- [ ] <Observable condition>
- [ ] <Relevant edge case or failure behavior>

## Verification
<Tests, commands, review, migration check, or manual check.>

## Dependencies / open questions
- <Only relevant blocker, dependency, or unresolved decision>

## References
- <Plan, SDD artifact, ADR, code, parent ticket, or related ticket>
```

For a new capability, “As-is” can describe the current absence or workaround.
For a bug, state the observed behavior and impact. For a refactor or
maintenance task, state the current condition and the preserved behavior. For a
spike, replace implementation acceptance with the question answered, evidence
produced, and explicit decision or follow-up.

### What self-contained means

Someone unfamiliar with the change should be able to answer from the ticket:

1. Why is this work needed?
2. What outcome is expected?
3. What is and is not included?
4. What constraints must not be violated?
5. What evidence will make it done?
6. Where can deeper rationale or formal detail be found?

Self-contained does **not** mean copying the full plan, every design
alternative, a complete API specification, an entire task graph, or the
conversation history. If a reader needs a link to discover the basic outcome,
scope, or acceptance, the ticket is too thin. If the ticket contains detailed
route exploration or alternatives no implementer must choose between, it is too
long or the detail belongs in a linked artifact.

For an ordinary story, aim for a compact description that can be scanned in one
pass—often roughly 200–500 words excluding references. This is a diagnostic,
not a hard limit: complexity must not be hidden merely to satisfy a word count.
Prefer headings and bullets over dense prose.

## Tracker Field Mapping

Use tracker fields for tracker concerns and the description for execution
context. Never invent values for fields the user or repository has not supplied.

| Information | Jira | GitHub Issues |
|---|---|---|
| Summary | Summary/title field | Issue title |
| Story, task, bug, spike | Configured issue type | Configured issue type when available; otherwise suggest a label only when the repository's label convention is known |
| Epic/initiative membership | Parent or Epic Link field | Milestone, project, or parent issue only when the repository/org supports it and that relationship fits; do not imply these are equivalent to a Jira Epic |
| Assignee, priority, sprint, estimate, labels | Jira fields, only when known or requested | Assignee, labels, milestone, project, or other repository-supported fields, only when known or requested |
| As-is, to-be, scope, guidance | Description | Issue body |
| Acceptance and verification | Description checklist or configured fields | Issue body checklist or configured fields |
| Dependency relationship | Jira issue link/parent relationship plus a short note | A supported native relationship when available; otherwise a verified issue link and short note in the body |
| Plan, spec, design, ADR | Description References plus native links where available | Markdown references in the body; use verified URLs and supported native links where available |

GitHub Issues may have organization- or repository-specific issue types, labels,
projects, milestones, and parent/child features. Check what is actually
available before mapping a ticket concept to one; do not invent a label or
assume Jira's Epic, sprint, priority, estimate, or issue-link semantics exist.

Do not put status, assignee, sprint, or estimate in prose as if that were the
authoritative field. Do not use an Epic link as a substitute for the ticket's
own outcome.

## Modes

Select the requested mode explicitly. If the user does not name one, use the
lightest mode that satisfies the request and say whether the result is intake,
shaping, or ready for implementation.

### `draft` — create a ticket brief

Use when the user asks to write a new ticket. Inspect available repository
evidence and existing artifacts, but do not create or modify them.

1. Identify the ticket type and parent context without equating an Epic with
   the change.
2. Extract or establish as-is, to-be, scope, guidance, acceptance, and
   verification.
3. Ask only material blocker questions. Record non-material uncertainty under
   `Dependencies / open questions`.
4. Produce the Summary, field suggestions, and copy-ready description. If the
   user explicitly asks to save a local draft, use only the specified target
   path and preserve existing content.
5. Mark the readiness honestly:
   - `intake`: the request is recorded but material shaping remains;
   - `shaping`: the ticket is being clarified or linked to artifacts;
   - `ready`: an implementer can start without reopening material decisions.

If no plan or SDD artifact exists, do not fabricate one and do not claim the
ticket is formally specified.

### `refine` — improve an existing ticket

Use when the user provides a Jira ticket, GitHub issue, or other supported
tracker work item and asks to make it implementation-ready.

1. Read the supplied ticket and any explicitly linked artifacts.
2. Preserve the ticket's identity, requested outcome, and known tracker fields.
3. Detect missing, contradictory, or implementation-prescriptive content.
4. Ask the material frontier in one focused round.
5. Return a proposed replacement description or field update. Do not edit a
   plan, spec, design, ADR, or code to resolve a ticket gap.
6. If the ticket's outcome or scope must change, call that out as a decision
   for the user rather than silently rewriting intent.

### `review` — assess readiness and boundary

Report findings first. Check:

- one coherent outcome and acceptance boundary;
- clear as-is and to-be states;
- explicit in/out scope;
- guidance limited to settled constraints;
- testable acceptance and proportionate verification;
- true dependencies and open decisions;
- appropriate parent Epic and ticket type;
- parent-ticket versus subtask boundary; and
- valid, useful references without invented paths or links.

Classify findings as `blocking`, `important`, or `optional`. Do not rewrite or
publish unless the user asks for a correction.

### `link` — add references to existing artifacts

Use when a ticket exists and a plan, SDD change, ADR, code review, or related
ticket now exists.

1. Verify each reference exists or is supplied by the user.
2. Explain what each link is for; do not add a link merely to make the ticket
   look complete.
3. Produce a minimal description update that adds or corrects the References
   section and, if necessary, a one-line context note.
4. Do not alter the referenced artifact and do not copy its full content into
   the ticket.

### `split` — choose tickets versus subtasks

Use when a change may be too large for one ticket or the user asks for a
breakdown.

1. Start from the parent outcome and acceptance boundary.
2. Identify independent outcomes, owners, release decisions, and acceptance
   boundaries.
3. Recommend sibling tickets for independent outcomes; recommend subtasks for
   implementation assignments within one outcome.
4. Draft each proposed ticket or subtask with its own outcome, acceptance,
   verification, scope, and dependency note.
5. Show the proposed hierarchy before any external creation. Do not edit a plan
   or SDD task list as a side effect.

### `publish` — explicit external tracker action

Only use this when the user explicitly asks to create or update an external
ticket and a configured integration or authorized tool is actually available.

Before acting, confirm the target project, issue type, parent, fields to change,
and exact description. Show the payload and obtain confirmation for the external
write. If no integration is available, return the copy-ready payload instead.
Report the actual tracker identifier/link and fields changed (for example, a
Jira issue key or GitHub issue number/URL); never infer success from a request
that merely looked valid.

## Handoff To Planning And SDD

This skill does not resolve a ticket's material product or architecture
questions by writing planning artifacts. Use the boundaries explicitly:

- If the ticket is too vague to define the route, invoke `my-planning wayfind`
  or `full` separately.
- If the ticket needs a durable behavior contract, invoke
  `my-spec-driven-development plan` separately.
- If the ticket needs only a compact implementation route, invoke
  `my-planning quick` or `full` separately.
- After those artifacts settle, invoke `my-ticket refine` or `link` to update
  the ticket's concise summary and references.

The ticket may exist before those handoffs and remain useful during them, but it
does not become a hidden fifth SDD artifact. The plan and SDD skills do not need
to preserve ticket prose as canonical content; they should record their own
confirmed outcome, scope, behavior, and decisions.

## Final Response

Report:

- ticket type, parent relationship, and readiness;
- proposed Summary and description or the exact fields to change;
- boundary decision: parent ticket, sibling ticket, or subtask;
- references added or still missing;
- material open questions and blockers;
- whether anything was actually published externally.

Do not claim that an intake ticket is implementation-ready, that a reference
exists when it was not checked, or that a Jira/GitHub issue was updated without
evidence.
