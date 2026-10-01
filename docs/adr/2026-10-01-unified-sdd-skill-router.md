---
status: accepted
---

# Consolidate The SDD Lifecycle Behind One Skill Router

## Context

The repository had separate skills for initializing specs, proposing changes, applying changes, verifying implementations, and archiving changes. Their contracts share paths, artifact formats, and lifecycle rules, so users and maintainers had to discover several overlapping entry points. The generic `my-grilling` skill is reusable outside spec-driven development and should not be absorbed into this workflow.

## Decision

Use one portable `my-spec-driven-development` skill with a compact router and per-mode plus shared references. Its public lifecycle modes are `init`, `plan`, `apply`, `verify`, and `archive`. Perform a hard source-repository cutover by removing the five superseded skill directories, while recognizing their names as migration aliases in the new skill. Keep `my-grilling` separate and use it only as an optional no-artifact question provider with a local fallback.

## Considered Options

- Keep five independent skills: preserves existing entry points, but keeps duplicated contracts and fragmented discovery.
- Use one monolithic reference: reduces file count, but weakens progressive disclosure and makes unrelated lifecycle edits harder to isolate.
- Keep compatibility wrapper directories: eases direct old-name invocation, but creates duplicate triggers and a second maintenance surface.

## Consequences

The lifecycle has one discoverable entry point and shared rules have one source of truth. The mode references remain independently readable and maintainable. Direct consumers of the deleted source directories must migrate to the unified skill or its aliases; installed copies outside this repository are not changed by this decision. The router must keep generic implementation planning out of its trigger boundary.
