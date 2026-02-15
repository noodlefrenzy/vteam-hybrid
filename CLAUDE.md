# CLAUDE.md — Project Instructions for Claude Code

## Project Overview

<!-- TODO: Replace this section with your project's overview after scaffolding -->

**Project Name:** [Your Project Name]
**Description:** [Brief description of what this project does]
**Tech Stack:** [Language, framework, key libraries — update after running a scaffold command]

**Codebase map:** `docs/code-map.md` — read this first to understand the package structure, public APIs, and data flow.

## Agent-Notes Protocol (MANDATORY)

Every non-excluded file must have agent-notes metadata. See `docs/agent-notes-protocol.md` for spec.

1. Every new file gets agent-notes (excluded: pure JSON, lock files, binaries).
2. Every edit updates `last` to `<agent>@<date>`.
3. `ctx` under 10 words, `deps` = direct deps only, `state` must be accurate.

## Team & Process

**Methodology:** Phase-dependent hybrid teams. See `docs/hybrid-teams.md` for the 7-phase model.

| Phase | Lead | Key Pattern |
|-------|------|------------|
| Discovery | Cam | Elicit before implementing |
| Architecture | Archie | ADR before code |
| Implementation | Tara → Sato | TDD red-green-refactor |
| Parallel Work | Grace | Market / self-claim |
| Code Review | Vik + Tara + Pierrot | Three parallel lenses |
| Debugging | Sato | Blackboard with Tara, Vik, Pierrot |
| Sprint Boundary | Grace | `/project:sprint-boundary` (mandatory) |

**Full details:** Agent roster, persona triggers, debate protocol, voice rules → `docs/process/team-governance.md`
**Doc ownership:** Who maintains what → `docs/process/doc-ownership.md`

## Critical Rules

### Don't Run With Vague Input
Engage Cam first: probe, clarify, pressure-test. Only implement once the vision is concrete.

### Ask the Human When Stuck
If blocked by environment, tools, permissions, or you've tried twice — ask. Don't heroically waste turns.

### Don't Skip the Done Gate
Every work item passes the gate before closing. Review the full 12-item checklist at `docs/process/done-gate.md`. The non-negotiables: tests pass, code reviewed, board updated through "In Review" → "Done."

### Don't Skip Agents
When a situation triggers multiple personas, invoke ALL of them. Overlapping coverage is intentional. The only exception is when the user explicitly asks to skip one.

### ADR Before Implementation
Never implement a feature with a pending ADR without writing the ADR first.

## Development Workflow

### Per Work Item
1. **Start** — Move issue to "In Progress."
2. **TDD** — Red → Green → Refactor. M+ items: Tara writes failing tests first as standalone agent.
3. **Commit** — One commit per issue, conventional message, `Closes #N`.
4. **Review** — Invoke code-reviewer (Vik + Tara + Pierrot). Fix Critical/Important findings.
5. **Done Gate** — Full checklist at `docs/process/done-gate.md`.
6. **Close** — Move issue to "In Review" → "Done". Push.

**STOP**: Do not start the next item until step 6 is complete.

### Commit Discipline
Commit and push after every reasonable chunk of work. One commit per issue. Conventional commits format.

### Kaizen
After each sprint or coding session: retro in `docs/retrospectives/`, update this file with new patterns.

## GitHub Board

<!-- Board details are configured during kickoff (Phase 5) — project creation is NOT optional -->
<!-- project-number: -->
<!-- project-owner: -->

**Status flow:** Todo → **In Progress** → **In Review** → Done

Grace manages board status. Pat manages priorities. Issues use `sprint:N` labels. Board creation is mandatory during `/project:kickoff`.

## Sprint Boundary (Mandatory)

Run `/project:sprint-boundary` when all sprint items are Done or deferred. This triggers:
1. Retro → `docs/retrospectives/`
2. Backlog sweep (catches orphans + user-created issues)
3. Process-improvement gate (blocks next sprint if unresolved)
4. Tech debt review → `docs/tech-debt.md`
5. Diego docs sweep
6. Periodic passes (dead code, dep health) every 3 sprints
7. Next sprint setup (Pat prioritizes, Grace sets up board)

## Session Management

**Context is finite.** Sprints generate massive agent output. To avoid mid-sprint context exhaustion:

1. **Plan waves before executing.** At sprint start, break issues into waves by size/dependency. Document in `docs/sprints/sprint-N-plan.md`.
2. **One wave per session.** Execute a wave, commit, then run `/project:handoff` to capture state. Start the next wave in a fresh session.
3. **Background agents write to files.** Use `run_in_background: true` for agents whose detailed output isn't needed in the main conversation. Read summaries, not full output.
4. **Read `docs/code-map.md` first.** Orient from the map rather than exploring the codebase from scratch each session.
5. **Commit frequently.** Uncommitted work is the most expensive thing to reconstruct across sessions.

## Process Docs Index

| Doc | Purpose |
|-----|---------|
| `docs/code-map.md` | Package structure, public APIs, data flow — **read first** |
| `docs/process/team-governance.md` | Agent roster, triggers, debate protocol, voice |
| `docs/process/done-gate.md` | 12-item Done Gate checklist |
| `docs/process/doc-ownership.md` | Who owns which docs, update triggers |
| `docs/process/gotchas.md` | Implementation patterns and known pitfalls |
| `docs/hybrid-teams.md` | 7-phase team methodology |
| `docs/team_personas.md` | 18-agent persona catalog |
| `docs/tech-debt.md` | Technical debt register |
| `docs/test-strategy.md` | Test pyramid and coverage targets |
| `docs/adrs/` | Architecture Decision Records |

## Project Structure

```
.
├── CLAUDE.md              # This file (slim — details in docs/process/)
├── docs/
│   ├── code-map.md        # Codebase structural overview
│   ├── process/           # Extracted process docs (governance, gates, gotchas)
│   ├── sprints/           # Sprint wave plans
│   ├── adrs/              # Architecture Decision Records
│   ├── retrospectives/    # Sprint retros
│   ├── sbom/              # SBOM + dependency decisions
│   └── security/          # Threat model
├── .claude/
│   ├── agents/            # Subagent persona definitions (18 agents)
│   └── commands/          # Custom slash commands
└── scripts/               # Automation scripts
```

## Custom Commands

| Command | Purpose |
|---------|---------|
| `/project:kickoff` | Full discovery workflow (5 phases) |
| `/project:design` | Sacrificial concept exploration |
| `/project:plan` | Implementation planning |
| `/project:adr` | Create a new ADR |
| `/project:tdd` | Strict TDD implementation |
| `/project:code-review` | Three-lens code review |
| `/project:review` | Guided human review session |
| `/project:retro` | Kaizen retrospective |
| `/project:sprint-boundary` | Mandatory sprint boundary workflow |
| `/project:handoff` | Session handoff for continuity |
| `/project:resume` | Resume from a previous handoff |
| `/project:scaffold-*` | Project scaffolding (cli, web-monorepo, ai-tool, static-site) |
| `/project:cloud-update` | Refresh cloud landscape research |
| `/project:aws-review` | Multi-lens AWS review |
| `/project:azure-review` | Multi-lens Azure review |
| `/project:gcp-review` | Multi-lens GCP review |
| `/project:pin-versions` | Pin dependency versions and update SBOM |
| `/project:sync-template` | Reapply vteam-hybrid template evolutions |
| `/project:sync-ghcp` | Sync agents to GitHub Copilot format |
