# Shared Paths And Selection

## Main And Change Specs

- Main specs: `docs/spec/<capability>.md`.
- Active changes: `docs/change/<change-name>/`.
- Archived changes: `docs/change/archive/YYYY-MM-DD-<change-name>/`.
- Use stable product or domain capability names, not implementation-only names.
- Derive a kebab-case change name unless the user supplied one.

Do not use `openspec/`, `.openspec.yaml`, OpenSpec stores, or generated instructions. This workflow writes plain Markdown only.

## Change Selection

For `apply`, `verify`, and `archive`:

1. Use the named change when the user gives one.
2. Infer from conversation context only when unambiguous.
3. If exactly one active change exists under `docs/change/` excluding `archive/`, use it and say so.
4. If multiple active changes exist, ask the user to choose.
5. Never implement, verify, or archive an archived change unless the user explicitly asks to inspect or resurrect it.

For `plan`, update an existing folder only when the user is clearly continuing the same work. A folder containing only `plan.md` is a compatible `my-planning` prelude: read it when the user asks to promote or continue that change, and do not mistake it for a complete formal change. At the first formal artifact, freeze the prelude by setting `status: promoted`, `formal_change: docs/change/<change-name>/`, and the current `updated` date; do not edit its body afterward. Otherwise ask before reusing a name or creating a similarly named change.

## Existing Specs And User Changes

Read existing main specs before proposing or merging deltas. Preserve their requirements unless implementation evidence clearly contradicts them. If code and spec disagree, report the mismatch and ask whether the spec should document current behavior or desired behavior.

Inspect the working tree before edits and preserve unrelated changes. Never silently overwrite hand-written intent, active change artifacts, or another user's work.

## Archive Naming

When archiving, use today's date unless the change name already starts with `YYYY-MM-DD-`. Do not stack a second date prefix. Stop on an archive target collision rather than overwriting it.
