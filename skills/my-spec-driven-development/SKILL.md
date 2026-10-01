---
name: my-spec-driven-development
description: >-
  Use this skill whenever the user asks to initialize or backfill specs,
  explore or propose a spec-driven change, apply a docs/change proposal,
  verify an implementation against its change artifacts, or archive a
  completed change. It consolidates those workflows into the five modes
  init, plan, apply, verify, and archive. Recognize legacy my-* spec-workflow
  names and explicit explore/propose language as aliases, but do not trigger
  for a generic implementation plan without explicit specification,
  change-artifact, or spec-driven-development intent.
sources:
  - "https://github.com/Fission-AI/OpenSpec/tree/main"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/opsx.md"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/workflows.md"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/editing-changes.md"
  - "https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/existing-projects.md"
  - "https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/spec-driven-development/SKILL.md"
  - "https://www.skills.sh/mattpocock/skills/batch-grill-me"
---

# My Spec-Driven Development

Route a Markdown spec-driven workflow through one portable skill. The detailed instructions are split by mode so the router stays short and each workflow can be loaded without dragging unrelated lifecycle rules into context.

## Operating Contract

- This skill owns `docs/spec/`, `docs/change/`, and the active change lifecycle.
- Do not use the `openspec` CLI, `openspec/` directories, stores, schemas, generated instructions, or `.openspec.yaml`.
- Read this file, the selected mode reference, and the shared references that mode names before acting. Do not load every mode reference by default.
- Preserve unrelated user changes. Do not commit, push, install skills, or change an external system as part of a mode.
- `plan` is the only mode with a mandatory requirements-grilling loop. `my-grilling` may supply the questions in no-artifact mode; use the local frontier-question fallback when it is unavailable.

## Public Modes

| User intent | Mode | Read |
|---|---|---|
| Backfill current behavior into main specs | `init` | `references/modes/init.md` |
| Explore or propose a spec-driven change | `plan` | `references/modes/plan.md` |
| Implement an active change | `apply` | `references/modes/apply.md` |
| Check implementation against a change | `verify` | `references/modes/verify.md` |
| Sync specs and close a completed change | `archive` | `references/modes/archive.md` |

The public contract is deliberately five modes. Legacy `my-init-spec`, `my-explore-and-propose-spec`, `my-apply-change`, `my-verify-change`, and `my-archive-change` names are migration aliases for the corresponding modes; they do not justify keeping separate skill directories.

## Mode Selection

1. Honor an explicit mode or an unambiguous lifecycle request.
2. Treat explicit `spec`, `specification`, `proposal`, `change artifact`, `explore`, and `propose` requests as `plan` intent unless the user clearly asked for `init`, `apply`, `verify`, or `archive`.
3. A vague SDD-shaped request may enter `plan` to grill and establish shared understanding, but it must obtain write confirmation before creating its first artifact.
4. Do not infer a mutating mode when more than one active change or workflow interpretation fits. Ask the user to choose.
5. Do not trigger this skill for a generic implementation plan, design discussion, or ordinary coding request with no explicit SDD/spec intent.

## Shared References

Read these with the selected mode when relevant:

- `references/shared/artifact-contract.md` — change files, delta specs, and plan artifact boundaries.
- `references/shared/path-and-selection.md` — paths, naming, change selection, and archive rules.
- `references/shared/validation.md` — common quality and evidence checks.

## Final Response

Report the selected mode, paths touched, evidence or verification performed, remaining work, and any skipped check with its reason. Do not claim a mode completed when a required artifact, task, or verification step remains open.
