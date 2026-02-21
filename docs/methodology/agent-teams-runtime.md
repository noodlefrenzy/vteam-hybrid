---
agent-notes: { ctx: "runtime guide for Agent Teams multi-session parallelism", deps: [docs/methodology/phases.md, docs/adrs/0006-agent-teams-integration.md, .claude/settings.json], state: active, last: "diego@2026-02-22" }
---

# Agent Teams Runtime Guide

Agent Teams enables real multi-session parallelism where each teammate is an independent Claude Code instance running in a tmux split pane. This guide documents when and how to use it.

## Phase-to-Runtime Mapping

| Phase | Runtime | Teammates | Rationale |
|-------|---------|-----------|-----------|
| 1. Discovery | Single session + subagents | 0 | Blackboard brainstorming is inherently serial |
| 2. Architecture | Agent Teams (2) | Proposer + Challenger | Adversarial debate needs independent reasoning chains |
| 3. Implementation | Single session + subagents | 0 | TDD pipeline is sequential by definition |
| 4. Parallel Work | Agent Teams (2-4) | Grace as lead, workers self-claim | Primary parallelism use case |
| 5. Code Review | Agent Teams (3) | Correctness + Coverage + Security | Independent review lenses prevent groupthink |
| 6. Debugging | Agent Teams (2) | Competing hypotheses | Independent investigation avoids confirmation bias |
| 7. Human Interaction | Single session | 0 | Just Cam, no parallelism needed |

## When to Use Agent Teams vs. Subagents

**Use Agent Teams when:**
- The phase benefits from independent reasoning chains (review, debate, parallel work)
- You need genuine parallelism, not simulated sequential execution
- Multiple agents need to work on different files simultaneously
- Adversarial quality matters (reviewers shouldn't see each other's findings)

**Use subagents (default) when:**
- The phase is inherently sequential (TDD, discovery)
- Only one agent needs to work at a time
- The task is small enough that parallelism overhead exceeds benefit
- Agent Teams is disabled or tmux is unavailable

**Fallback rule:** Subagent mode always works. If Agent Teams is disabled, unavailable, or the task doesn't justify the token cost, use subagents. No methodology change required.

## How to Spawn Teammates

### Prerequisites

1. Agent Teams is enabled: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (set in `.claude/settings.json`)
2. You're in a tmux session (teammates appear as split panes)
3. You've identified which phase you're in and which spawn prompts to use

### Spawn Workflow

1. **Read the spawn prompt template** from `.claude/spawn-prompts/phase-N-role.md`
2. **Fill in `[PLACEHOLDERS]`** with task-specific details (feature description, file list, etc.)
3. **Use Claude Code's teammate spawning** to create the teammate with the filled-in prompt
4. **Monitor progress** via the shared task list
5. **Synthesize results** when all teammates complete their tasks

### Spawn Prompt Templates

| File | Phase | Role | Persona |
|------|-------|------|---------|
| `phase-2-proposer.md` | Architecture | Proposer | Archie |
| `phase-2-challenger.md` | Architecture | Challenger | Wei |
| `phase-4-worker.md` | Parallel Work | Worker | varies |
| `phase-5-correctness.md` | Code Review | Correctness | Vik |
| `phase-5-coverage.md` | Code Review | Coverage | Tara |
| `phase-5-security.md` | Code Review | Security | Pierrot |
| `phase-6-hypothesis.md` | Debugging | Investigator | Sato |
| `phase-6-challenger.md` | Debugging | Challenger | Wei |

Each template instructs the teammate to read their `.claude/agents/*.md` persona file. **No second persona format exists** — the same persona definitions serve both subagent and teammate modes.

## Governance Hooks

Two hooks enforce governance automatically:

### `TaskCompleted` — Done Gate (Automated Subset)

**File:** `.claude/hooks/done-gate.sh`

Runs when any teammate (or the lead) marks a task as completed. Checks:

| Check | Done Gate Item | Enforcement |
|-------|---------------|-------------|
| Tests pass | Item 1 | `npm test` / `pytest` / `cargo test` |
| Formatted | Item 3 | `prettier --check` / `ruff format --check` / `cargo fmt --check` |
| Linted | Item 4 | `eslint` / `ruff check` / `cargo clippy` |

**Exit code 2** blocks task completion if any check fails. The teammate must fix the issue before completing the task.

**Graceful degradation:** If no test runner, formatter, or linter is detected (e.g., the template hasn't been scaffolded yet), the check is skipped and the hook exits 0.

The remaining 9 done-gate items require judgment and stay prompt-enforced:
- Typecheck (item 2), code review (5), acceptance criteria (6), docs (7), accessibility (8), board status (9), migration safety (10), API compat (11), tech debt (12), SBOM (13)

### `TeammateIdle` — Uncommitted Changes Guard

**File:** `.claude/hooks/teammate-idle.sh`

Runs when a teammate is about to go idle. If `git status --porcelain` shows changes, **exit code 2** blocks the idle transition with a message to commit first.

This prevents lost work — a teammate's uncommitted changes are the most expensive thing to reconstruct.

## Devcontainer / Codespaces

The `.devcontainer/` configuration provides a ready-to-go Agent Teams environment:

- **Base image:** Ubuntu 22.04 with Node.js 22 and GitHub CLI
- **Post-create:** Installs tmux, Claude Code, and project dependencies
- **Environment:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` set automatically

**Important:** Use a proper terminal (iTerm2, Windows Terminal, Alacritty), not VS Code's integrated terminal — it doesn't handle tmux well.

**Full setup guide:** `docs/guides/agent-teams-setup.md` — covers Dev Container CLI, Docker Compose, and GitHub Codespaces workflows.

## Disabling Agent Teams

Agent Teams is additive — disable it without affecting anything else:

**Per-user:** Create `.claude/settings.local.json`:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "0"
  }
}
```

**Per-session:** Set the environment variable before launching:
```bash
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0 claude
```

When disabled, all phases use subagent mode automatically. The spawn prompt templates and hooks still exist but are unused.

## Limitations

1. **No per-teammate permission scoping** — all teammates inherit the lead's permissions. Tool restrictions are prompt-based (spawn prompts say "Do NOT edit files" for reviewers).
2. **No session resumption** — if a teammate crashes, its context is lost. Mitigated by frequent commits and the `TeammateIdle` hook.
3. **No nested teams** — teammates cannot spawn their own teams. Phase 4 workers use subagents internally for TDD.
4. **Token cost** — each teammate is a full Claude Code session. Parallel phases cost 2-3x more than sequential subagent execution. Only use Agent Teams when the quality benefit (independent reasoning) justifies the cost.
5. **Experimental status** — Agent Teams API may change. Our integration is additive, so changes affect spawn prompts and hooks, not the core methodology.
