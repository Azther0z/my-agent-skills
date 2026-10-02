---
status: accepted
---

# Keep Work Tickets Separate From Planning Artifacts

## Context

An Epic or initiative groups a much larger body of work than one SDD change.
In the common case, a tracker story or issue describes one externally meaningful
change, while subtasks decompose the implementation inside that ticket. The
repository's planning and SDD artifacts have different jobs: a plan owns the
route and progress, SDD artifacts own durable behavior and the formal
implementation contract, and ADRs own architectural rationale and tradeoffs.

Tickets are often created before grilling, planning, or specification. Treating
them only as the final output of planning creates a chicken-and-egg problem.
Treating them as the source of truth creates the opposite problem: tracker prose
becomes an informal fifth SDD artifact and drifts from the formal documents.

## Decision

Create a separate `my-ticket` skill for drafting, refining, reviewing, linking,
and splitting tracker work items. A ticket is a compact execution brief with
as-is, to-be, scope, guidance, acceptance, verification, dependencies, and
references. It may exist first as an intake brief or be composed later from
settled artifacts.

The ticket points to `my-planning` plans, SDD artifacts, ADRs, code, and related
tickets, but ticket operations do not create or modify those artifacts. There
is no default `docs/change/<name>/ticket.md`. Jira and GitHub Issues are
documented ticket targets; other trackers require an explicitly configured
integration and field mapping. Without a configured integration,
`my-ticket` produces a reviewable copy-ready payload and does not publish
externally.

The ticket is self-contained for execution, not self-contained as the entire
project history. The ticket owns the concise current what/why/scope/done and
guidance summary; linked artifacts own route detail, durable contracts, routine
implementation choices, and task graphs. Architectural rationale,
alternatives, and tradeoffs live only in the ADR.

## Considered Options

- **Fold ticket drafting into `my-planning`**: convenient for plan-first work, but
  makes ticket semantics part of the planning artifact lifecycle and encourages
  local ticket copies to drift.
- **Make the ticket a fifth SDD artifact**: gives one formal sequence, but
  fails when a ticket is created first and duplicates the existing four-artifact
  contract.
- **Use a local `ticket.md` beside `plan.md`**: supports ticket-first work, but
  creates another canonical-looking file when an external tracker is the actual
  ticket system.
- **Keep ticket drafting separate**: preserves a ticket-first entry point while
  keeping planning and SDD artifacts authoritative for their own concerns.

## Consequences

Users can draft a useful intake ticket before the route is known, then link the
same ticket to formal artifacts as they are created. A ticket remains compact
and readable instead of becoming a design dump. Planning and SDD workflows stay
portable and do not assume tracker access.

The ticket and artifacts can still drift if users update only one side. The
separate skill therefore includes explicit refine, review, and link workflows,
and it must distinguish a proposed copy-ready update from an actual external
tracker write for Jira, GitHub Issues, or another configured integration.
