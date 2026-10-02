---
status: accepted
---

# Use A Living Plan Prelude For Lightweight Changes

## Context

The repository has a formal `my-spec-driven-development` lifecycle with four
artifact categories: proposal, delta specs, design, and tasks. That contract is
valuable for durable behavior and higher-risk work, but it is too much ceremony
for many ordinary changes. The repository currently has no structured artifact
for either a single implementation plan or a large plan that must survive
multiple sessions.

Several external planning approaches informed this decision. OpenSpec
describes a lightweight default and fuller artifacts for higher-risk changes.
Superpowers separates bounded in-chat design from detailed implementation
plans. Wshobson's Conductor uses a living `plan.md`, explicit task statuses,
checkpoints, dependencies, and archive-not-delete history. Its task
coordination guidance also distinguishes true blockers from optional
coordination and requires acceptance, ownership, interface contracts, and
scope boundaries.

## Decision

Add `my-planning` with a self-contained lifecycle for `quick`, `full`,
`wayfind`, `maintain`, `promote`, and `archive` modes. Plan-only work uses one
living file at `docs/change/<change-name>/plan.md`. The plan embeds its work or
decision graph. Tracker ticket drafting is intentionally delegated to the
separate `my-ticket` skill rather than treated as a planning artifact export.

When a plan needs formal specification, `my-planning promote` hands the same
folder to `my-spec-driven-development plan`; the SDD skill alone owns formal
artifact creation, grilling, and boundary approvals. After the first confirmed
formal artifact is created, SDD changes only the plan prelude's frontmatter to
`status: promoted` and links the formal change folder. The plan body then stays
frozen as provenance. The formal artifacts become the complete implementation
contract when all required categories exist; apply, verify, and archive remain
blocked until then.

## Considered Options

- **Use a separate `docs/plans/` tree**: keeps lightweight and formal plans
  visually separate, but creates two lifecycles and requires a fragile export
  or copy step.
- **Reuse `proposal.md` as the light plan**: maximizes filename reuse, but
  makes a plan-only artifact look like the first formal SDD boundary and loses
  the distinction between intent and an implementation plan.
- **Make every plan use the full SDD contract**: preserves one formal shape,
  but recreates the overkill that motivated this skill.

## Consequences

Small work gets a durable, maintainable plan without four formal artifacts.
Large but settled work can use phases, checkpoints, and embedded dependencies;
large and uncertain work can use a decision map before implementation tasks
exist. Promotion avoids a second plan location, avoids duplicating the SDD
workflow in `my-planning`, freezes provenance at a clear boundary, and
preserves the SDD gates.

The `docs/change/` directory can contain intentionally incomplete plan-only
folders. SDD selection and validation must recognize them as planning preludes
and refuse to treat them as implementation-ready changes. Ticket publication,
native dependency links, and external tracker setup remain outside the default
plan lifecycle and are handled by `my-ticket` when explicitly requested.
