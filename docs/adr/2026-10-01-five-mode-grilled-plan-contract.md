---
status: accepted
---

# Use A Five-Mode Grilled Plan Contract

## Context

The former proposal skill separated read-only exploration from proposal creation and defaulted to a oneshot path. Consolidation needs one public planning mode without making vague requests unexpectedly write files. The existing four-artifact change contract remains valuable to `apply`, `verify`, and `archive`.

## Decision

Expose one combined `plan` mode alongside `init`, `apply`, `verify`, and `archive`. `plan` always starts with frontier-based requirements grilling. It uses no-artifact `my-grilling` delegation when available, asks for local confirmation before writing for vague SDD-shaped requests, and requires confirmation at every artifact boundary. Once the current artifact is fully understood, it writes exactly one next artifact in this order: `proposal.md`, each delta spec, `design.md`, and `tasks.md`. If the user abandons the work before the first boundary, it writes nothing. The four-artifact contract and plain Markdown paths remain unchanged.

## Considered Options

- Keep separate explore and propose modes: preserves the old no-write boundary exactly, but defeats the intended single public planning workflow.
- Keep a oneshot default: minimizes interaction, but makes assumptions harder to catch before writing the change contract.
- Write immediately on entering plan: reduces friction, but creates unwanted artifacts for vague or abandoned ideas.

## Consequences

Planning takes more interaction and no longer has a oneshot path, but each artifact is backed by an explicit shared-understanding checkpoint. The old `explore` and `propose` names now route to the combined plan workflow, so their former behavior should not be described as separate public modes. Partial changes remain visible when the user stops after one or more confirmed artifacts.
