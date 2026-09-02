# ADR Format

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create the `docs/adr/` directory lazily, only when the first ADR is needed.

## One Decision Per ADR

One ADR records exactly one architectural decision: one chosen architectural outcome and its rationale. A decision may contain multiple implementation details that directly realize that outcome.

Split decisions into separate ADRs when the choices can be accepted, rejected, or reversed independently. Do not combine independently changeable choices under a broad topic or title. Multiple consequences do not make an ADR cover multiple decisions.

An ADR must have a real decision. Do not create an ADR whose `Decision` section is `None.`.

## Required Format

Every ADR must use the following frontmatter and body sections, in this order:

```md
---
status: proposed
---

# {Short title of the decision}

## Context

{Why this decision is needed and the constraints that shape it. Use `None.` only when there is no additional context worth recording.}

## Decision

{The single chosen architectural outcome and its rationale. This section must not be `None.`.}

## Considered Options

{Meaningful alternatives, their trade-offs, and why they were not selected. Use `None.` when no alternatives or trade-offs are worth preserving.}

## Consequences

{Important results, constraints, or follow-up effects of the decision. Use `None.` when there are no consequences worth recording.}
```

`status` is required frontmatter and must be one of:

- `proposed`
- `accepted`
- `deprecated`
- `superseded by ADR-NNNN`, where `NNNN` is the number of the ADR that supersedes this one

The exact empty marker for an applicable but empty section is `None.`. Do not omit a required heading or replace the marker with a blank section, `N/A`, or a prose explanation that does not state the section is empty.

## Validity Checklist

Before accepting an ADR, verify all of the following:

- It records exactly one architectural decision.
- Its chosen outcome is stated in `Decision` and that section is not `None.`.
- Independently changeable choices are split into separate ADRs.
- Required `status` frontmatter is present and uses an allowed value.
- `Context`, `Decision`, `Considered Options`, and `Consequences` headings are present and in the required order.
- `Considered Options` includes options, trade-offs, and rejection rationale when alternatives were evaluated; otherwise it contains exactly `None.`.
- Any other applicable empty section contains exactly `None.`.

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When To Offer An ADR

All three of these must be true:

1. Hard to reverse: the cost of changing your mind later is meaningful.
2. Surprising without context: a future reader will look at the code and wonder why it was done this way.
3. The result of a real trade-off: there were genuine alternatives and one was picked for specific reasons.

If a decision is easy to reverse, skip it. If it is not surprising, nobody will wonder why. If there was no real alternative, there is nothing to record beyond doing the obvious thing.

### What Qualifies

- Architectural shape: `We're using a monorepo.` `The write model is event-sourced, the read model is projected into Postgres.`
- Integration patterns between contexts: `Ordering and Billing communicate via domain events, not synchronous HTTP.`
- Technology choices that carry lock-in: database, message bus, auth provider, deployment target. Not every library, just the ones that would take a quarter to swap out.
- Boundary and scope decisions: `Customer data is owned by the Customer context; other contexts reference it by ID only.` The explicit no-s are as valuable as the yes-s.
- Deliberate deviations from the obvious path: `We're using manual SQL instead of an ORM because X.` Anything where a reasonable reader would assume the opposite.
- Constraints not visible in the code: `We cannot use AWS because of compliance requirements.` `Response times must be under 200ms because of the partner API contract.`
- Rejected alternatives when the rejection is non-obvious. If GraphQL was considered and REST was picked for subtle reasons, record it so the discussion does not repeat in six months.
