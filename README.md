<!-- agent-notes: { ctx: "public-facing README for GitHub template repo", deps: [CLAUDE.md, docs/template-guide.md, docs/methodology/phases.md, docs/methodology/personas.md], state: active, last: "diego@2026-02-25" } -->

# vteam-hybrid

A virtual development team for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — 18 AI agent personas, a 7-phase hybrid methodology, and 24 workflow commands covering the full development lifecycle.

## What This Is

vteam-hybrid is a GitHub repo template that turns Claude Code into a structured development team. Instead of a single AI assistant, you get specialized agents — an architect, a tester, a security reviewer, a project manager — that collaborate through defined phases with built-in quality gates.

**You only need to know 5 agents to start.** The rest activate automatically when the work demands it.

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI)
- Git
- [GitHub CLI](https://cli.github.com/) (`gh`) — for project board integration (optional but recommended)

## How It Works

```mermaid
graph LR
    Human["Human Developer"]

    subgraph "Claude Code + vteam-hybrid"
        Coord["Coordinator<br/><em>reads CLAUDE.md, selects phase</em>"]

        subgraph "P0 — Core (always available)"
            Cam["Cam<br/>Vision &<br/>Elicitation"]
            Sato["Sato<br/>Implementation"]
            Tara["Tara<br/>Tests (TDD)"]
            Pat["Pat<br/>Product &<br/>Priorities"]
            Grace["Grace<br/>Tracking &<br/>Coordination"]
        end

        subgraph "P1 — Essential (invoked when needed)"
            Archie["Archie<br/>Architecture"]
            Vik["Vik<br/>Code Review"]
            Pierrot["Pierrot<br/>Security"]
            Dani["Dani<br/>Design & A11y"]
            Ines["Ines<br/>DevOps & SRE"]
        end

        subgraph "P2 + Cloud (situational)"
            Others["Diego · Wei · Debra<br/>User Chorus · Cloud Specialists"]
        end
    end

    Human <-->|"natural language"| Coord
    Coord -->|"invokes"| Cam
    Coord -->|"invokes"| Sato
    Coord -->|"invokes"| Tara
    Coord -->|"invokes"| Pat
    Coord -->|"invokes"| Grace
    Coord -.->|"when needed"| Archie
    Coord -.->|"when needed"| Vik
    Coord -.->|"when needed"| Pierrot
    Coord -.->|"when needed"| Dani
    Coord -.->|"when needed"| Ines
    Coord -.->|"situational"| Others
```

## The 7 Phases

The coordinator automatically selects the right team structure for each phase of work:

| Phase | When | Lead | What Happens |
|-------|------|------|-------------|
| 1. Discovery | New idea or vague request | Cam | Probing, clarifying, pressure-testing the vision |
| 2. Architecture | Design decisions needed | Archie | ADR + adversarial debate with Wei |
| 3. Implementation | Code to write | Tara then Sato | TDD: Tara writes failing tests, Sato makes them pass |
| 4. Parallel Work | 3+ independent items | Grace | Multiple agents working concurrently |
| 5. Code Review | Changes to review | Vik + Tara + Pierrot | Three lenses: simplicity, tests, security |
| 6. Debugging | Bug to fix | Sato | Shared investigation with Tara, Vik, Pierrot |
| 7. Human Interaction | User consultation needed | Cam | Single point of contact for the human |

## Quick Start

1. **Use this template** — click "Use this template" on GitHub, or clone and reinitialize
2. **Scaffold your tech stack:**
   - `/project:scaffold-cli` — Python or Rust CLI
   - `/project:scaffold-web-monorepo` — TypeScript monorepo (Next.js, React)
   - `/project:scaffold-ai-tool` — Python AI/ML tool (FastAPI, Streamlit)
   - `/project:scaffold-static-site` — Static site (GitHub Pages)
3. **Run discovery** — `/project:kickoff` to define your product and set up tracking
4. **Start building** — `/project:tdd <feature>` for TDD-driven development

## Command Reference

### Lifecycle

| Command | What It Does |
|---------|-------------|
| `/project:kickoff` | Full 5-phase discovery workflow with board setup |
| `/project:plan` | Create an implementation plan for a feature |
| `/project:tdd` | TDD workflow: Tara writes failing tests, Sato implements |
| `/project:code-review` | Three-lens code review (simplicity, tests, security) |
| `/project:review` | Guided human review session with Cam |
| `/project:sprint-boundary` | Sprint retro, backlog sweep, process gate, next sprint setup |
| `/project:handoff` | Save session state for the next session to resume |
| `/project:resume` | Pick up from a previous session's handoff |
| `/project:retro` | Kaizen retrospective with GitHub issues for findings |

### Design & Architecture

| Command | What It Does |
|---------|-------------|
| `/project:design` | Sacrificial concept exploration with Dani |
| `/project:adr` | Create a new Architecture Decision Record |
| `/project:restack` | Re-evaluate tech stack choices |

### Scaffolding

| Command | What It Does |
|---------|-------------|
| `/project:scaffold-cli` | Scaffold a CLI project (Python/Rust) |
| `/project:scaffold-web-monorepo` | Scaffold a web/mobile monorepo (TypeScript) |
| `/project:scaffold-ai-tool` | Scaffold an AI/data tool (Python) |
| `/project:scaffold-static-site` | Scaffold a static site (GitHub Pages) |

### Maintenance

| Command | What It Does |
|---------|-------------|
| `/project:pin-versions` | Pin dependency versions, update SBOM |
| `/project:sync-template` | Reapply template evolutions to an in-flight repo |
| `/project:devcontainer` | Set up a dev container for any stack |
| `/project:sync-ghcp` | Sync agent definitions to GitHub Copilot format |

### Cloud

| Command | What It Does |
|---------|-------------|
| `/project:aws-review` | AWS deployment readiness review |
| `/project:azure-review` | Azure deployment readiness review |
| `/project:gcp-review` | GCP deployment readiness review |
| `/project:cloud-update` | Refresh cloud service landscape research |

## Key Features

- **TDD Pipeline** — Tara writes failing tests first, Sato makes them pass. Structural quality enforcement, not just "write tests."
- **Adversarial Debate** — Wei challenges architectural decisions through structured multi-round debate. Catches design flaws before implementation.
- **Agent-Notes Protocol** — Structured metadata at the top of every file lets agents decide whether to read a file before opening it. Reduces context waste.
- **Session Handoff/Resume** — `/project:handoff` saves session state; `/project:resume` picks up where you left off. Solves the ephemeral context problem.
- **Done Gate** — 13-item quality checklist every work item must pass. Tests, types, lint, review, accessibility, SBOM, and more.

## Learning Path

Read in this order. Stop when you have enough:

| # | Doc | Time | What You'll Learn |
|---|-----|------|-------------------|
| 1 | [Template Guide](docs/template-guide.md) | 5 min | What's included, how to customize |
| 2 | [Phases (TL;DR)](docs/methodology/phases.md#tldr) | 2 min | The 7 phases at a glance |
| 3 | [Phases (full)](docs/methodology/phases.md) | 10 min | How each phase works, who participates |
| 4 | [Personas](docs/methodology/personas.md) | skim | The 18-agent roster, capabilities, tiers |

## Template Lineage

- **vteam-base** — Foundation: core personas, TDD, ADRs
- **vteam-agentapalooza** — Extended: full 32-agent roster
- **vteam-hybrid** (this) — Consolidated: 32 agents merged to 18, hybrid methodology, agent-notes protocol

## License

[MIT](LICENSE)
