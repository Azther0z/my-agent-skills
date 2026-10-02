# Agent Skills Artifact Context

This context defines the repository-specific vocabulary for planning, ticket,
and spec-driven-development skills and how their artifacts relate.

## Language

**Epic**:
An external tracker grouping for multiple change tickets; it is substantially
broader than one SDD change. _Avoid_: treating an Epic as the same scope as a
single change folder.

**Story/change ticket**:
A tracker work item with one coherent change outcome and acceptance boundary.
It commonly corresponds to one SDD change, but can exist before planning or
specification. _Avoid_: treating ticket text as a formal SDD artifact.

**Subtask**:
An implementation assignment inside a parent ticket, used when several pieces
contribute to the same parent outcome. _Avoid_: using a subtask for an
independently valuable change with its own acceptance boundary.

**Plan prelude**:
The optional `docs/change/<name>/plan.md` created by `my-planning`. It is the
living source while plan-only; after the first formal SDD artifact, it is
frozen provenance with `status: promoted` and a link to its formal change.
_Avoid_: maintaining it as a second live plan after promotion.

**Formal SDD change**:
The `docs/change/<name>/` lifecycle owned by `my-spec-driven-development`,
requiring `proposal.md`, at least one delta spec under `spec/`, `design.md`,
and `tasks.md` before apply, verify, or archive. It may retain a plan prelude
as read-only provenance.

**Decision node**:
An unresolved question in a wayfinding plan whose dependencies determine when
it can be asked. It is not an implementation task or a tracker ticket.

**ADR**:
The canonical full record of an architectural decision and its rationale,
tradeoffs, and alternatives. Other artifacts may state the concise resulting
constraint and link the ADR, but do not duplicate its rationale.
