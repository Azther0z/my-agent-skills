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

- `my-agentic-repo`: maintain high-signal repository agent instructions.
- `my-conventional-git`: apply repository-aware Conventional Git practices.
- `my-grilling`: conduct structured requirements interviews.
- `my-llm-wiki`: maintain an evidence-backed LLM knowledge base.
- `my-parse-pdf`: create grounded PDF Markdown derivatives with all-page visual evidence, crops, and safe diagram recovery.
- `my-create-artifact`: build grounded study packs, quizzes, practice surfaces, and standalone learning maps, including the C4 map mode.
- `my-spec-driven-development`: initialize, plan, apply, verify, and archive Markdown spec-driven changes through one mode-routed workflow.
- `my-skill-creator`: create, evaluate, and improve skills.
