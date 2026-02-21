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

### Session Entry Protocol (Mandatory)
Before writing any code — including types, tests, or ADRs — answer these three questions:
1. **Do GitHub issues exist for this work?** If no → create them (Pat + Grace).
2. **Does this work involve an architectural decision?** If yes → Architecture Gate (Archie + Wei as standalone agents).
3. **Am I about to write implementation code?** If yes → Tara writes tests first.

If you received a detailed plan (from plan mode, a prior session, or the human), the plan is **input to this protocol**, not a bypass of it. See `docs/process/gotchas.md` § Process for the full anti-pattern description.

### Don't Run With Vague Input
Engage Cam first: probe, clarify, pressure-test. Only implement once the vision is concrete.

### Ask the Human When Stuck
If blocked by environment, tools, permissions, or you've tried twice — ask. Don't heroically waste turns.

### Proxy Mode
When the human declares unavailability (e.g., "I'm going to bed"), the coordinator routes product questions to Pat instead of the human. Pat uses `docs/product-context.md` to answer within the human's known preferences, with conservative defaults for uncovered areas. Pat cannot approve ADRs, change scope, make architectural choices, merge to main, or override vetoes — those block until the human returns. All proxy decisions are logged in `.claude/handoff.md` under `## Proxy Decisions (Review Required)`. Proxy mode ends when the human sends any message. See `docs/process/gotchas.md` § Process for the full guardrail table.

### Don't Skip the Done Gate
Every work item passes the gate before closing. Review the full 13-item checklist at `docs/process/done-gate.md`. The non-negotiables: tests pass, code reviewed, board updated through "In Review" → "Done."

### Don't Skip Agents
When a situation triggers multiple personas, invoke ALL of them. Overlapping coverage is intentional. The only exception is when the user explicitly asks to skip one.

### ADR Before Implementation
Never implement a feature with a pending ADR without writing the ADR first.

### Architecture Gate (Mandatory)
Before entering Implementation (Phase 3) for any sprint item that involves an architectural decision — new patterns, new integrations, technology choices, data model changes, new package boundaries — the following gate **must** pass:

1. **ADR exists** — Archie has written an ADR for the decision.
2. **Wei has challenged it** — Wei has been invoked as a standalone agent on the ADR. This is not optional.
3. **Debate is tracked** — The multi-round debate (Archie vs Wei) is recorded in `docs/tracking/YYYY-MM-DD-<topic>-debate.md`.
4. **Resolution documented** — The coordinator has summarized which challenges were addressed, which were accepted as risks, and what changed.

If the sprint plan includes items that trigger this gate, the coordinator must identify them at sprint planning and note "**Requires Architecture Gate:** ADR + Wei debate" on each one. See `docs/process/team-governance.md` § Architecture Decision Gate for the full checklist.

**How to recognize architectural decisions:** If you're choosing *how* to structure something (not just *what* to build), it's architectural. Examples: adding a new package, choosing between two libraries, designing an API contract, changing data flow between stages, introducing a new external dependency. When in doubt, route through the gate — a 10-minute debate is cheaper than a bad decision baked into code.

## Development Workflow

### Per Work Item
1. **Start** — Move issue to **"In Progress"** on the board. Do this BEFORE writing any code.
2. **TDD** — Red → Green → Refactor. M+ items: Tara writes failing tests first as standalone agent.
3. **Commit** — One commit per issue, conventional message, `Closes #N`.
4. **Review** — Move issue to **"In Review"** on the board. Then invoke code-reviewer (Vik + Tara + Pierrot). Fix Critical/Important findings.
5. **Done Gate** — Full checklist at `docs/process/done-gate.md`.
6. **Close** — Move issue to **"Done"** on the board. Push.

**Status transitions are mandatory and ordered.** Every item must pass through In Progress → In Review → Done. Skipping "In Review" is a process violation that will be flagged in the sprint retro. See Grace's Board Status Rules for enforcement details.

**STOP**: Do not start the next item until step 6 is complete.

### Commit Discipline
Commit and push after every reasonable chunk of work. One commit per issue. Conventional commits format.

### Kaizen
After each sprint or coding session: retro in `docs/retrospectives/`, update this file with new patterns.

## GitHub Board

<!-- Board details are configured during kickoff (Phase 5) — project creation is NOT optional -->
<!-- project-number: -->
<!-- project-owner: -->

**Status flow:** Backlog → Ready → **In Progress** → **In Review** → Done

**Required statuses:** The board MUST have all 5 status options configured. If "In Review", "Ready", or "Backlog" are missing, add them before starting any sprint work (see `/project:kickoff` Phase 5 Step 2 for setup commands).

Grace manages board status. Pat manages priorities. Issues use `sprint:N` labels. Board creation is mandatory during `/project:kickoff`.

### Board Status Commands

Use these commands to move items through statuses. You need the project's Status field ID and the option IDs for each status.

```bash
# 1. Look up field IDs and status option IDs (do this once per session)
gh project field-list <NUMBER> --owner <OWNER> --format json
# Find the "Status" field → note its field ID
# Find each option (Backlog, Ready, In Progress, In Review, Done) → note their option IDs

# 2. Get the item ID for an issue
gh project item-list <NUMBER> --owner <OWNER> --format json
# Find the item matching your issue number → note its item ID

# 3. Get the project node ID (needed for item-edit)
gh project list --owner <OWNER> --format json
# Find the project → note its node ID

# 4. Move an item to a new status
gh project item-edit --project-id <PROJECT_NODE_ID> --id <ITEM_ID> --field-id <STATUS_FIELD_ID> --single-select-option-id <STATUS_OPTION_ID>
```

**Per-item transitions only.** Never batch-update all items. Each item transitions individually as work progresses.

## Sprint Boundary (Mandatory)

Run `/project:sprint-boundary` when all sprint items are Done or deferred. This triggers:
1. Retro → `docs/retrospectives/`
2. Backlog sweep (catches orphans + user-created issues)
3. Process-improvement gate (blocks next sprint if unresolved)
4. Tech debt review → `docs/tech-debt.md`
5. Diego docs sweep
6. Archive tracking artifacts → `docs/tracking/archive/sprint-N/`
7. Periodic passes (dead code, dep health) every 3 sprints
8. Next sprint setup (Pat prioritizes, Grace sets up board)

## Session Management

**Context is finite.** Sprints generate massive agent output. To avoid mid-sprint context exhaustion:

1. **Plan waves before executing.** At sprint start, break issues into waves by size/dependency. Document in `docs/sprints/sprint-N-plan.md`.
2. **One wave per session.** Execute a wave, commit, then run `/project:handoff` to capture state. Start the next wave in a fresh session.
3. **Background agents write to files.** Use `run_in_background: true` for agents whose detailed output isn't needed in the main conversation. Read summaries, not full output.
4. **Read `docs/code-map.md` first.** Orient from the map rather than exploring the codebase from scratch each session.
5. **Commit frequently.** Uncommitted work is the most expensive thing to reconstruct across sessions.
6. **Tracking artifacts carry phase context.** Commands produce lightweight artifacts in `docs/tracking/` at each workflow phase. These survive across sessions — read them to pick up where a previous session left off. See `docs/tracking/README.md` for the protocol.

## Process Docs Index

| Doc | Purpose |
|-----|---------|
| `docs/code-map.md` | Package structure, public APIs, data flow — **read first** |
| `docs/process/team-governance.md` | Agent roster, triggers, debate protocol, voice |
| `docs/process/done-gate.md` | 13-item Done Gate checklist |
| `docs/process/doc-ownership.md` | Who owns which docs, update triggers |
| `docs/process/gotchas.md` | Implementation patterns and known pitfalls |
| `docs/hybrid-teams.md` | 7-phase team methodology |
| `docs/team_personas.md` | 18-agent persona catalog |
| `docs/tech-debt.md` | Technical debt register |
| `docs/test-strategy.md` | Test pyramid and coverage targets |
| `docs/tracking/README.md` | Phase tracking artifact protocol and format |
| `docs/product-context.md` | Human's product philosophy (Pat maintains) |
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
│   ├── tracking/          # Phase tracking artifacts (see README.md)
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
