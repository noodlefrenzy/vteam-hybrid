<!-- agent-notes: { ctx: "Copilot project-wide instructions, generated from manifest", deps: [agents/manifest.yaml, CLAUDE.md], state: active, last: "copilot-cli@2026-03-22" } -->
# Copilot Instructions — vteam-hybrid

> **This file is generated.** Edit `agents/manifest.yaml`, `commands/manifest.yaml`, or `docs/` source files, then run `python3 scripts/generate-platform.py copilot`.

## Project Overview

This project uses the **vteam-hybrid methodology** — a phase-dependent hybrid team of 19 specialized AI agents. For full details:

- **Phases:** `docs/methodology/phases.md` (7-phase model)
- **Personas:** `docs/methodology/personas.md` (19-agent catalog)
- **Governance:** `docs/process/team-governance.md` (triggers, debate protocol, gates)
- **Done Gate:** `docs/process/done-gate.md` (15-item completion checklist)

## Available Agents

| Agent | Priority | Description |
|-------|----------|-------------|
| @archie | P1 | Lead architect combining system design, data modeling, and API contract design. Use for architect... |
| @cam | P0 | Human interface agent for vision elicitation and structured review. Use proactively when the user... |
| @cloud-architect | cloud | Cloud solution architect adapting to any cloud platform (AWS, Azure, GCP). Use for cloud architec... |
| @cloud-costguard | cloud | Cloud cost analysis and optimization specialist for any cloud platform. Use to review architectur... |
| @cloud-netdiag | cloud | Cloud network diagnostics and enterprise constraint discovery for any cloud platform. Use proacti... |
| @code-reviewer | P1 | Multi-perspective code reviewer combining Vik (simplicity/maintainability), Tara (test quality/co... |
| @dani | P1 | Design and UX agent combining design exploration, sacrificial concepts, user flow design, accessi... |
| @debra | P2 | Data scientist and ML specialist. Use for telemetry design, experimentation, model training, data... |
| @diego | P2 | Technical writer and developer experience specialist. Use when documentation needs writing, updat... |
| @grace | P0 | Sprint tracking, work distribution, and cross-team coordination agent. Manages project boards, tr... |
| @ines | P1 | DevOps, SRE, and chaos engineering agent combining infrastructure management, CI/CD, SLO design, ... |
| @pat | P0 | Product and program management agent combining backlog ownership, acceptance criteria, prioritiza... |
| @pierrot | P1 | Security and compliance agent combining penetration testing, vulnerability scanning, license audi... |
| @prof | P2 | Pedagogical agent that explains architectural and implementation choices made by the team. Assume... |
| @sato | P0 | Principal software engineer who writes production code. Use after tests exist (Tara writes the fa... |
| @tara | P0 | Test-focused agent that writes failing tests before implementation (TDD red phase), reviews test ... |
| @user-chorus | P2 | Multi-archetype user panel for usability feedback. Use during design phases, usability testing, a... |
| @vik | P1 | Veteran code reviewer focused on simplicity, maintainability, and pattern enforcement. Use for de... |
| @wei | P2 | Devil's advocate and assumption challenger. Use when the team is converging too quickly, during a... |


## Development Workflow

1. **Discovery** — Use @cam for vision elicitation, @pat for requirements
2. **Architecture** — Use @archie for ADRs, @wei for adversarial debate
3. **Implementation** — Use @tara for failing tests (TDD red), @sato to make them pass (green)
4. **Review** — Use @vik + @tara + @pierrot for multi-lens code review
5. **Coordination** — Use @grace for sprint tracking and board management

## Critical Rules

- **TDD is mandatory:** @tara writes failing tests before @sato implements
- **ADR before code:** Architectural decisions require an ADR (`docs/adrs/`)
- **Done Gate:** Every work item passes the 15-item checklist before closing
- **Don't skip agents:** When a situation triggers multiple personas, invoke ALL of them
- **Security veto:** @pierrot has veto power on security and compliance

## Conventions

- Conventional commits format
- One commit per work item
- Board status flow: Backlog → Ready → In Progress → In Review → Done
- Agent-notes metadata on all non-excluded files (see `docs/methodology/agent-notes.md`)

## Process Documentation

| Doc | Purpose |
|-----|--------|
| `docs/methodology/phases.md` | 7-phase team methodology |
| `docs/methodology/personas.md` | 19-agent persona catalog |
| `docs/process/team-governance.md` | Triggers, debate protocol, gates |
| `docs/process/done-gate.md` | 15-item Done Gate checklist |
| `docs/process/gotchas.md` | Implementation patterns and pitfalls |
| `docs/process/operational-baseline.md` | Cross-cutting operational concerns |
