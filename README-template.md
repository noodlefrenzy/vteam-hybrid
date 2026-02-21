---
agent-notes: { ctx: "reference doc for template contents and usage", deps: [CLAUDE.md, docs/methodology/personas.md, docs/methodology/phases.md], state: canonical, last: "diego@2026-02-12" }
---

# vteam-hybrid Template Reference

This document explains what the vteam-hybrid template provides and how to use it effectively.

## What This Template Is

vteam-hybrid is a GitHub repo template for projects that use Claude Code with a virtual team methodology. It provides:

1. **18 specialized agent personas** organized into priority tiers (P0 Core, P1 Essential, P2 Regular, Cloud Specialists)
2. **7-phase hybrid team methodology** that adapts the team structure to the current development phase
3. **Agent-notes protocol** for fast context bootstrapping across sessions
4. **21 command workflows** covering the full development lifecycle
5. **Architecture Decision Records** and documentation structure
6. **Cloud specialist agents** that adapt to AWS, Azure, or GCP

## Template Lineage

- **vteam-base** — Foundation template: core personas, TDD workflow, ADR conventions
- **vteam-agentapalooza** — Extended template: adds the full 32-agent roster
- **vteam-hybrid** (this template) — Consolidated template: 32 agents reduced to 18 via capability-based merging, plus hybrid team methodology and agent-notes protocol

## Key Innovations Over Previous Templates

### Agent Consolidation (32 → 18)

Related personas were merged into single agents with multiple "lenses":
- Pat = PO Pat + PM Priya (product + program management)
- Grace = Gantt Grace + TPM Tomas (tracking + coordination)
- Archie = Archie + Schema Sam + Contract Cass (architecture + data + API)
- Dani = Dani + UI Uma (design + UX + accessibility)
- Pierrot = Pierrot + RegRaj (security + compliance)
- Ines = Ines + On-Call Omar + Breaker Bao (DevOps + SRE + chaos)
- Cloud Architect = Azure/AWS/GCP Architect (one agent, adapts to target cloud)
- Cloud CostGuard = Azure/AWS/GCP Cost Guard (same)
- Cloud NetDiag = Azure/AWS/GCP Net Diag (same)

### Hybrid Team Methodology

Instead of a fixed hierarchy, the coordinator selects the appropriate team composition at each phase transition:
- **Discovery** — Blackboard model, anyone contributes ideas
- **Architecture** — Ensemble + adversarial debate
- **Implementation** — Strict TDD pipeline (Tara → Sato)
- **Parallel Work** — Market model, agents self-claim independent work
- **Code Review** — Three parallel independent reviewers
- **Debugging** — Blackboard, shared problem space
- **Human Interaction** — Single point of contact (Cam)

### Agent-Notes Protocol

Structured metadata at the top of every file that lets agents bootstrap context without reading entire files. Provides purpose, dependencies, state, and last modifier in ~50 words.

## Getting Started

### 1. Create a Repo from This Template

Click "Use this template" on GitHub, or clone and reinitialize:

```bash
git clone <this-repo> my-project
cd my-project
rm -rf .git
git init
git add -A
git commit -m "chore: initialize from vteam-hybrid template"
```

### 2. Scaffold Your Tech Stack

Run one of the scaffold commands:
- `/project:scaffold-cli` — Python or Rust CLI tool
- `/project:scaffold-web-monorepo` — TypeScript monorepo with Next.js, React, etc.
- `/project:scaffold-ai-tool` — Python AI/ML tool with FastAPI, Streamlit, etc.
- `/project:scaffold-static-site` — Static site for GitHub Pages

### 3. Run Discovery

Use `/project:kickoff` to run the full 5-phase discovery workflow before building.

### 4. Start Building

Follow the TDD workflow: `/project:tdd <feature>` for each piece of work.

## File Map

| Path | Purpose |
|------|---------|
| `CLAUDE.md` | Master project instructions — start here |
| `docs/methodology/personas.md` | Full 18-agent persona catalog |
| `docs/methodology/phases.md` | 7-phase team methodology |
| `docs/agent-notes-protocol.md` | Agent-notes format specification |
| `docs/adrs/template.md` | ADR template |
| `docs/adrs/0001-*.md` | Conventional commits ADR |
| `docs/adrs/0002-*.md` | TDD workflow ADR |
| `docs/adrs/0003-*.md` | Hybrid team architecture ADR |
| `.claude/agents/*.md` | 18 runnable agent definitions |
| `.claude/commands/*.md` | 21 workflow commands |
| `docs/research/*-landscape.md` | Cloud service landscape files |

## Customization Guide

### Adding a New Agent

1. Create `.claude/agents/<name>.md` with the proper frontmatter (see existing agents for format)
2. Add the agent to `docs/methodology/personas.md`
3. Update `docs/methodology/phases.md` with the agent's phase participation
4. Update the roster table in `CLAUDE.md`

### Modifying an Existing Agent

Edit the agent file directly. Update `last` in its agent-notes. If the change affects phase participation, update `docs/methodology/phases.md`.

### Adding a New Command

Create `.claude/commands/<name>.md` with an agent-notes HTML comment as the first line. Add the command to the table in `CLAUDE.md`.

### Scaling Notes

- **Small project (1 team, 1-3 agents):** Collapse further. Sato absorbs Ines's infra work. Code-reviewer covers all review. Pat handles all planning.
- **Medium project (2-3 teams):** Full roster. Grace earns her keep with cross-team coordination.
- **Large project (4+ teams):** Every role is distinct. Consider splitting consolidated agents back into specialists.
