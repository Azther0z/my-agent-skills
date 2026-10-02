# My Agent Skills

Reusable agent skills for OpenCode and other tools supporting the Agent Skills format.

## Install

Install all skills globally with:

```bash
npx skills add Azther0z/my-agent-skills --global --skill '*'
```

Use `--skill '*'` instead of `--all`: the latter also targets every supported agent.

Install selected skills with:

```bash
npx skills add Azther0z/my-agent-skills --global --skill my-agentic-repo
```

The `npx skills` CLI installs the skills under the user's agent directories and maintains its generated lock file at `~/.agents/.skill-lock.json` where applicable. This repository contains skill source only; it does not contain runtime installation state.

## Skills

### Human context

| Skill | Use case | Short description |
| --- | --- | --- |
| `my-grilling` | Clarify a request through a structured interview. | Asks focused questions in decision-frontier rounds; can optionally maintain project context and ADRs. |
| `my-planning` | Plan, break down, or map software work. | Creates and maintains lightweight plans, roadmaps, and decision/dependency maps. |

**Workflow:** Promote a lightweight plan to `my-spec-driven-development` when the work needs formal change artifacts.

### Coding

| Skill | Use case | Short description |
| --- | --- | --- |
| `my-conventional-git` | Choose branches, commits, PR wording, or release conventions. | Applies repository-aware Conventional Git practices. |
| `my-spec-driven-development` | Manage a formal spec-driven software change. | Owns the init, plan, apply, verify, and archive lifecycle for change artifacts. |

**Workflow:** Formal change artifacts follow `my-spec-driven-development`'s lifecycle: init → plan → apply → verify → archive.

### Agent context

| Skill | Use case | Short description |
| --- | --- | --- |
| `my-skill-creator` | Create, improve, or evaluate an agent skill. | Helps build skills and measure their behavior with evaluations. |
| `my-agentic-repo` | Set up or improve an agent-aware repository. | Creates and maintains high-signal `AGENTS.md` instructions as the canonical source. |

### Ad hoc

| Skill | Use case | Short description |
| --- | --- | --- |
| `my-parse-pdf` | Extract, OCR, or create a searchable Markdown companion from a PDF. | Produces a grounded Markdown companion, inspects every page, and preserves visual evidence. |
| `my-llm-wiki` | Build or query a personal LLM knowledge base. | Maintains its source evidence, compiled wiki pages, and operating instructions. |
| `my-ticket` | Draft, refine, review, split, or publish a tracker ticket. | Creates compact Jira or GitHub Issues tickets that link to—but do not own—plans and specs. |
| `my-create-artifact` | Turn study material into learning resources. | Creates grounded study packs, quizzes, practice surfaces, and standalone learning maps. |

**Workflow:** When useful, `my-parse-pdf` can create the grounded source material for `my-create-artifact`. Tickets can be drafted before or after related planning or SDD artifacts; they are not a required step and do not replace those artifacts.
