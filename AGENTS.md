# AGENTS.md

## Purpose
- This repository is the source of truth for reusable agent skills maintained by Azther0z.
- Skills must be portable and must not assume the dotfiles repository is present.

## Repository Contract
- Each skill lives at `skills/<name>/SKILL.md`.
- Keep supporting references, scripts, assets, and agent definitions inside that skill directory.
- Keep generated workspaces, Python bytecode, runtime captures, and local dependencies out of Git.
- Validate skill frontmatter and run relevant evaluations before publishing changes.
- Update the repository README when adding or removing a shareable skill.
