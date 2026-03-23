<!-- agent-notes: { ctx: "universal cross-platform agent instructions", deps: [agents/manifest.yaml, commands/manifest.yaml], state: active, last: "copilot-cli@2026-03-22" } -->
# AGENTS.md — vteam-hybrid

> **This file is generated.** It provides universal cross-platform instructions readable by any AI coding agent (Copilot, Codex, Cursor, Gemini, Claude Code). Edit the source manifests in `agents/` and `commands/`, then run `python3 scripts/generate-platform.py agents-md`.

## Project

This project uses the **vteam-hybrid methodology** — a structured approach to AI-assisted software development with 19 specialized agent personas organized across 7 phases.

## Team Methodology

The methodology is fully documented in `docs/`:

- **7 Phases:** Discovery → Architecture → Implementation → Parallel Work → Code Review → Debugging → Human Interaction
- **19 Personas:** Each with defined responsibilities, thinking styles, and capability boundaries
- **Governance:** Architecture Decision Gate, adversarial debate protocol, scope reduction gate
- **Quality:** TDD mandatory, 15-item Done Gate, security veto, test coverage veto

Full details: `docs/methodology/phases.md`, `docs/methodology/personas.md`

## Agents

- **archie** (P1): Lead architect combining system design, data modeling, and API contract design. Use for architectural decisions, ADR ...
- **cam** (P0): Human interface agent for vision elicitation and structured review. Use proactively when the user presents a vague id...
- **cloud-architect** (cloud): Cloud solution architect adapting to any cloud platform (AWS, Azure, GCP). Use for cloud architecture design, service...
- **cloud-costguard** (cloud): Cloud cost analysis and optimization specialist for any cloud platform. Use to review architectures for cost, right-s...
- **cloud-netdiag** (cloud): Cloud network diagnostics and enterprise constraint discovery for any cloud platform. Use proactively before deployme...
- **code-reviewer** (P1): Multi-perspective code reviewer combining Vik (simplicity/maintainability), Tara (test quality/coverage), and Pierrot...
- **dani** (P1): Design and UX agent combining design exploration, sacrificial concepts, user flow design, accessibility review, and f...
- **debra** (P2): Data scientist and ML specialist. Use for telemetry design, experimentation, model training, data analysis, and visua...
- **diego** (P2): Technical writer and developer experience specialist. Use when documentation needs writing, updating, or reviewing — ...
- **grace** (P0): Sprint tracking, work distribution, and cross-team coordination agent. Manages project boards, tracks velocity, runs ...
- **ines** (P1): DevOps, SRE, and chaos engineering agent combining infrastructure management, CI/CD, SLO design, alerting, and fault ...
- **pat** (P0): Product and program management agent combining backlog ownership, acceptance criteria, prioritization, KPI tracking, ...
- **pierrot** (P1): Security and compliance agent combining penetration testing, vulnerability scanning, license auditing, and regulatory...
- **prof** (P2): Pedagogical agent that explains architectural and implementation choices made by the team. Assumes developer competen...
- **sato** (P0): Principal software engineer who writes production code. Use after tests exist (Tara writes the failing tests first, S...
- **tara** (P0): Test-focused agent that writes failing tests before implementation (TDD red phase), reviews test coverage, and mainta...
- **user-chorus** (P2): Multi-archetype user panel for usability feedback. Use during design phases, usability testing, and feature demos. Pr...
- **vik** (P1): Veteran code reviewer focused on simplicity, maintainability, and pattern enforcement. Use for deep code review of ch...
- **wei** (P2): Devil's advocate and assumption challenger. Use when the team is converging too quickly, during architecture debates,...

## Commands / Workflows

- **adr**: Create a new Architecture Decision Record (agents: archie)
- **aws-review**: Multi-lens AWS deployment readiness review (agents: cloud-architect, cloud-costguard, cloud-netdiag)
- **azure-review**: Multi-lens Azure deployment readiness review (agents: cloud-architect, cloud-costguard, cloud-netdiag)
- **cloud-update**: Research and update cloud service landscape (agents: cloud-architect)
- **code-review**: Multi-perspective code review on current changes (agents: vik, tara, pierrot)
- **design**: Design exploration with sacrificial concepts (agents: dani)
- **devcontainer**: Set up a devcontainer for this project (agents: ines)
- **doctor**: Read-only project health check (agents: sato)
- **gcp-review**: Multi-lens GCP deployment readiness review (agents: cloud-architect, cloud-costguard, cloud-netdiag)
- **handoff**: Create session handoff document for next session (agents: grace)
- **kickoff**: Full discovery workflow with board setup (agents: cam, pat, archie, wei, grace)
- **pin-versions**: Pin dependency versions and update SBOM (agents: pierrot)
- **plan**: Implementation planning workflow (agents: pat, cam)
- **quickstart**: Fast 5-min onboarding, skips full kickoff (agents: cam, pat)
- **restack**: Reconsider and update the tech stack (agents: archie)
- **resume**: Resume from a previous session handoff (agents: grace)
- **retro**: Kaizen retrospective on sprint/session work (agents: grace)
- **review**: Guided human review session for completed work (agents: cam)
- **scaffold-ai-tool**: Scaffold an AI/data-centric tool project (agents: sato)
- **scaffold-cli**: Scaffold a CLI project (agents: sato)
- **scaffold-static-site**: Scaffold a static site for GitHub Pages (agents: sato)
- **scaffold-web-monorepo**: Scaffold a web/mobile monorepo (agents: sato)
- **sprint-boundary**: Mandatory end-of-sprint workflow (agents: grace, vik, pierrot, tara)
- **tdd**: Implement a feature using strict TDD (agents: tara, sato)
- **whatsit**: Research and explain a technology or concept

## Conventions

- **Commits:** Conventional commits format, one commit per work item
- **Board:** Backlog → Ready → In Progress → In Review → Done
- **TDD:** Tests before implementation (always)
- **ADRs:** Architecture Decision Records before implementation
- **Agent-notes:** Metadata on all non-excluded files (`docs/methodology/agent-notes.md`)
- **Done Gate:** 15-item checklist before closing any work item (`docs/process/done-gate.md`)

## Boundaries

- Never skip tests — Tara has veto power on coverage
- Never implement without an ADR for architectural decisions
- Never skip the Done Gate checklist
- Security and compliance have veto power (Pierrot)
- When multiple personas are triggered, invoke ALL of them

## Key Documentation

| Doc | Purpose |
|-----|--------|
| `docs/methodology/phases.md` | 7-phase team methodology |
| `docs/methodology/personas.md` | 19-agent persona catalog |
| `docs/methodology/agent-notes.md` | File metadata protocol |
| `docs/process/team-governance.md` | Triggers, debate protocol, gates |
| `docs/process/done-gate.md` | 15-item completion checklist |
| `docs/process/gotchas.md` | Implementation patterns and pitfalls |
| `docs/process/operational-baseline.md` | Cross-cutting operational concerns |
| `docs/adrs/` | Architecture Decision Records |

## Platform-Specific Configuration

This project supports multiple AI coding platforms:

- **Claude Code:** `CLAUDE.md` + `.claude/agents/` + `.claude/commands/`
- **GitHub Copilot:** `.github/copilot-instructions.md` + `.github/agents/` + `.github/prompts/`
- **Codex CLI:** This `AGENTS.md` file + future `.codex/config.toml`
- **Cursor:** Future `.cursor/rules/`
- **Gemini:** Future `.gemini/GEMINI.md`

The source of truth for agent definitions is `agents/manifest.yaml`. Platform-specific files are generated by `scripts/generate-platform.py`.
