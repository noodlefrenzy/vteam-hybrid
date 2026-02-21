---
agent-notes: { ctx: "ADR promoting Agent Teams adaptive hybrid to accepted", deps: [docs/adrs/template/0004-agent-teams-runtime-mapping.md, docs/methodology/phases.md], state: active, last: "archie@2026-02-22" }
---

# ADR-0006: Agent Teams Integration

## Status

Accepted

Promotes ADR-0004 Option D (Adaptive Hybrid) from exploratory to accepted with concrete implementation details.

## Context

ADR-0004 explored how vteam-hybrid's 18-persona, 7-phase methodology could map onto Claude Code's Agent Teams runtime. It identified Option D (Adaptive Hybrid) as the preliminary recommendation: use Agent Teams for phases that benefit from real parallelism, keep subagents for inherently sequential phases.

Since ADR-0004 was written:

1. Agent Teams is feature-complete enough to integrate — it supports tmux split panes, shared task lists, inter-agent messaging, and lifecycle hooks (`TaskCompleted`, `TeammateIdle`).
2. Our existing `.claude/agents/*.md` persona files work directly as teammate instructions — teammates load CLAUDE.md and can read any project file, so **no second persona format is needed**.
3. Hook-based governance (`TaskCompleted` with exit code 2 blocking) replaces prompt-only enforcement for the automatable subset of the done gate.

The key simplification over ADR-0004's original vision: **no phase-routing wrapper script**. The lead reads CLAUDE.md, sees the phase-to-runtime mapping table, and decides. A wrapper script adds a failure mode (script bugs, state management complexity) for zero benefit — the lead already knows which phase it's in.

Similarly, **no composite personas** (ADR-0004's "strategic composites" like Challenger = Wei+Pierrot). Each teammate reads one persona file. Composites were a premature optimization that would create a maintenance burden and blur accountability.

### Wei Debate Record

**Wei's challenges:**

1. *"Agent Teams is still experimental. Tight coupling risks rework."* — Mitigated: integration is additive. Subagent mode always works. If Agent Teams changes, we update spawn prompts and hooks, not the core methodology. The `.claude/agents/*.md` files are untouched.

2. *"Token cost of 3 parallel review teammates vs. 3 sequential subagent calls is ~3x."* — Accepted trade-off. The value is independent reasoning chains (reviewers don't see each other's findings and converge prematurely). Users who can't afford it disable Agent Teams via `settings.local.json`.

3. *"No per-teammate permission scoping means a reviewer teammate could edit files."* — Mitigated: spawn prompts explicitly instruct "Do NOT edit any files." Teammates are short-lived and task-scoped. Prompt-based restriction is acceptable for ephemeral sessions.

4. *"The plan says 'no phase-routing wrapper' but ADR-0004 Option D includes one."* — Agreed. The wrapper was over-engineering. Removing it is a deliberate simplification over ADR-0004's original vision.

## Decision

Adopt Option D (Adaptive Hybrid) from ADR-0004 with the following concrete implementation:

### Phase-to-Runtime Mapping

| Phase | Runtime | Teammates | Why |
|-------|---------|-----------|-----|
| 1. Discovery | Single session + subagents | 0 | Blackboard is serial |
| 2. Architecture | Agent Teams (2) | Proposer + Challenger | Adversarial debate needs independent reasoning |
| 3. Implementation | Single session + subagents | 0 | TDD pipeline is sequential |
| 4. Parallel Work | Agent Teams (2-4) | Grace as lead, workers self-claim | Primary parallelism use case |
| 5. Code Review | Agent Teams (3) | Correctness + Coverage + Security | Independent review lenses |
| 6. Debugging | Agent Teams (2) | Competing hypotheses | Independent investigation |
| 7. Human Interaction | Single session | 0 | Just Cam |

### Governance Layer

- **`TaskCompleted` hook** enforces automatable done-gate items: tests pass, code formatted, code linted. Exit code 2 blocks task completion. Degrades gracefully when no test runner/formatter/linter is detected.
- **`TeammateIdle` hook** prevents teammates from going idle with uncommitted changes.
- Remaining done-gate items (typecheck, code review, acceptance criteria, docs, accessibility, board status, migration safety, API compat, tech debt, SBOM) stay prompt-enforced.

### Teammate Spawning

Spawn prompt templates in `.claude/spawn-prompts/` instruct each teammate to read their `.claude/agents/*.md` persona file. Templates have `[PLACEHOLDERS]` for task-specific details. No composite personas — one persona per teammate.

### Fallback

Subagent mode always works. Agent Teams is additive. Disable by setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0` in `.claude/settings.local.json`.

## Consequences

### Positive

- Real parallelism for Phases 2, 4, 5, and 6 — independent context windows, genuine concurrent work
- Hook-based governance replaces prompt-only enforcement for tests, formatting, and linting
- Adversarial debate gets independent reasoning chains instead of simulated disagreement
- Single source of truth for personas — `.claude/agents/*.md` serves both subagent and teammate modes
- No breaking changes — existing subagent workflow is completely untouched
- Devcontainer support enables consistent environment for Agent Teams in Codespaces

### Negative

- Token cost increase for parallel phases (estimated 2-3x for Phases 4, 5)
- Two runtime models to understand (Agent Teams + subagents), though the mapping table makes selection mechanical
- Per-teammate permission scoping is prompt-based only, not enforced
- Agent Teams is experimental — API surface may change (mitigated by additive integration)

### Neutral

- 18 persona definitions unchanged — delivery mechanism varies but content does not
- CLAUDE.md gains one new section (~15 lines) with the phase-runtime mapping table
- Sprint boundary workflow, tracking artifacts, and done-gate checklist are unaffected
- ADR-0004 remains as reference material for the options analysis
