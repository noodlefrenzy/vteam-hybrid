---
agent-notes: { ctx: "comparison of vteam-hybrid vs Claude Code Agent Teams", deps: [docs/hybrid-teams.md, docs/team_personas.md, CLAUDE.md], state: active, last: "archie@2026-02-16" }
---

# How We Compare: vteam-hybrid vs Claude Code Agent Teams

Claude Code now offers experimental [Agent Teams](https://code.claude.com/docs/en/agent-teams) — a built-in system for coordinating multiple Claude Code sessions working in parallel. This document compares the two approaches, maps capabilities, identifies gaps, and evaluates migration paths.

## Executive Summary

vteam-hybrid and Agent Teams solve overlapping but distinct problems. vteam-hybrid is a **methodology** — it defines _who_ does _what_ in _which_ organizational structure at each development phase. Agent Teams is an **execution runtime** — it provides the machinery for multiple Claude sessions to coordinate. The ideal end state is vteam-hybrid's methodology running on Agent Teams' infrastructure.

| Dimension | vteam-hybrid (current) | Agent Teams |
|-----------|----------------------|-------------|
| **What it is** | Methodology + agent definitions + commands | Runtime for multi-session coordination |
| **Parallelism** | Simulated (subagents within one session) | Real (separate Claude Code instances) |
| **Agent identity** | 18 personas with scoped tools + behavioral rules | Generic teammates with spawn prompts |
| **Coordination** | CLAUDE.md instructions + custom commands | Shared task list + mailbox + hooks |
| **Phase model** | 7 phases with dynamic team assembly | One team per session, fixed lead |
| **Token cost** | Lower (subagents summarize back) | Higher (each teammate is a full session) |

## Capability Mapping

### What maps directly

These vteam-hybrid concepts have near-exact equivalents in Agent Teams.

| vteam-hybrid | Agent Teams | Notes |
|---|---|---|
| Phase 4: Parallel Work (Grace coordinates) | Lead coordinates teammates | Grace's role maps to the lead session. Workers map to teammates. |
| Phase 5: Code Review (3 parallel lenses) | Parallel code review | Documented as a primary use case. Spawn Vik, Tara, Pierrot as teammates. |
| Phase 6: Debugging (competing hypotheses) | Competing hypotheses pattern | Documented as a primary use case. Teammates investigate and challenge each other via messaging. |
| Adversarial Debate Protocol | Inter-agent messaging | Wei challenging Archie maps to direct teammate-to-teammate communication. No need for coordinator relay. |
| Sprint task tracking (Grace) | Shared task list with dependencies | Built-in task states (pending/in-progress/completed) with dependency blocking. |
| Cam as single human interface | Lead session as human interface | Lead handles all human communication. Teammates work independently. |
| Done-gate checklist | `TaskCompleted` hook | Exit code 2 blocks completion. Veto power becomes programmatic enforcement. |
| "Don't implement, coordinate" (Cam, Grace) | Delegate mode (`Shift+Tab`) | Lead restricted to coordination-only tools — no code editing. |
| Plan-before-implement (Architecture phase) | Plan approval workflow | Teammates work in read-only plan mode until lead approves their approach. |

### What maps partially

These concepts exist in both systems but with meaningful differences.

| vteam-hybrid | Agent Teams | Gap |
|---|---|---|
| 18 agent personas (`.claude/agents/`) | Teammates with spawn prompts | Personas must be embedded in spawn prompts or loaded via CLAUDE.md. No `.claude/agents/` support for teammates — they aren't subagents. |
| Scoped tool access (Cam: read-only, Tara: tests-only) | All teammates inherit lead's permissions | **No per-teammate permission scoping.** Restrictions become advisory (prompt-based) rather than enforced. |
| Phase-dependent team assembly (7 phases) | One team per session, fixed lead | **No dynamic team reconfiguration.** Can't swap team composition at phase boundaries without tearing down. |
| Agent-notes protocol (fast context bootstrapping) | Teammates load project context (CLAUDE.md, MCP, skills) | Agent-notes still work — teammates read the same filesystem. But concurrent edits risk overwriting notes. |
| Custom commands (`/project:tdd`, `/project:code-review`) | Natural language instructions to the lead | Commands become lead instructions. The lead interprets and creates tasks + teammates accordingly. |
| Phase nesting (Parallel Work contains Implementation pipelines) | No nested teams | **Teammates cannot spawn their own teams.** Nested pipelines must be flattened or handled within a single teammate's session. |

### What has no equivalent

These vteam-hybrid features have no counterpart in Agent Teams.

| vteam-hybrid Feature | Impact | Workaround |
|---|---|---|
| Veto powers (Tara on coverage, Pierrot on security) | Specific agents can block progress | Implement via `TaskCompleted` hooks that run test/security checks. Advisory in spawn prompts for persona-level enforcement. |
| Priority tiers (P0/P1/P2 agents) | Controls which agents are invoked based on work type | Lead decides which teammates to spawn. Tier logic goes in CLAUDE.md or command instructions. |
| Lens system (Archie has Architecture + Data + API lenses) | One agent, multiple perspectives | Each lens can become a separate teammate, or keep as a single teammate with multi-lens spawn prompt. |
| Session handoff (`/project:handoff` + `/project:resume`) | Cross-session continuity | Agent Teams has **no session resumption for teammates**. Handoff artifacts in `docs/tracking/` remain the best mechanism. |
| Sprint boundary workflow | Enforced process gates between sprints | No equivalent. Keep as a lead-driven workflow using existing command structure. |

## Architecture Comparison

### Current: Single-session with simulated parallelism

```
┌─────────────────────────────────────────────┐
│              Claude Code Session             │
│                                              │
│  CLAUDE.md (methodology + rules)             │
│       │                                      │
│       ▼                                      │
│  Coordinator (reads phase, selects team)     │
│       │                                      │
│       ├──► Subagent: Vik (review)            │
│       ├──► Subagent: Tara (review)  ◄── parallel but │
│       ├──► Subagent: Pierrot (review)    report back  │
│       │                                  to caller    │
│       ▼                                      │
│  Coordinator (synthesizes results)           │
│       │                                      │
│       ▼                                      │
│  Human                                       │
└─────────────────────────────────────────────┘
```

- Subagents run within the session's context budget
- Results summarized back to coordinator
- No inter-agent communication — everything routes through coordinator
- Phase switching is instantaneous (same session, different instructions)

### Agent Teams: Multi-session with real parallelism

```
┌───────────────────┐
│   Lead (Cam)      │◄──── Human interacts here
│   Shared task list │
│   Mailbox         │
└──┬──┬──┬──────────┘
   │  │  │
   │  │  └──────────────────────┐
   │  └──────────┐              │
   ▼             ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Teammate │ │ Teammate │ │ Teammate │
│ (Vik)    │◄►│ (Tara)   │◄►│(Pierrot) │
│          │ │          │ │          │
│ Own ctx  │ │ Own ctx  │ │ Own ctx  │
│ Own tools│ │ Own tools│ │ Own tools│
└──────────┘ └──────────┘ └──────────┘
     ◄──── direct messaging ────►
```

- Each teammate is an independent Claude Code instance
- Teammates message each other directly (no coordinator relay)
- Shared task list with dependency management and file-locked claiming
- Lead can delegate (never touches code) or participate
- Phase switching requires spawning/shutting down teammates

## Phase-by-Phase Fit Assessment

How well each vteam-hybrid phase maps to Agent Teams.

| Phase | Fit | Rationale |
|-------|-----|-----------|
| **1. Discovery** | Medium | Blackboard model needs open contribution. Agent Teams supports messaging but the "shared workspace" metaphor is less natural than a single session where all personas contribute to one document. A single session with subagents may actually be better here. |
| **2. Architecture** | High | Ensemble + adversarial debate maps well. Archie as lead teammate, Wei as challenger teammate, direct messaging for debate rounds. Plan approval workflow enforces ADR-before-code. |
| **3. Implementation** | Low | TDD pipeline is strictly sequential (Tara → Sato → Sato → Tara). Agent Teams adds overhead for a 2-agent pipeline with hard dependencies. Better as a single session or subagent workflow. |
| **4. Parallel Work** | Very High | This is the primary use case for Agent Teams. Grace as lead, multiple worker teammates, shared task list with self-claiming. Direct upgrade. |
| **5. Code Review** | Very High | Documented as a primary Agent Teams use case. Three reviewer teammates, parallel lenses, lead synthesizes. Almost 1:1. |
| **6. Debugging** | High | Competing hypotheses pattern is a documented use case. Teammates investigate independently and challenge each other via direct messaging. |
| **7. Human Interaction** | N/A | This phase is about human communication, not multi-agent work. The lead session handles this natively. |

### Recommendation: Hybrid execution model

Not every phase benefits from Agent Teams. The optimal approach uses both:

```
Phase 1 (Discovery)       → Single session (blackboard works better in one context)
Phase 2 (Architecture)    → Agent Teams (debate + plan approval)
Phase 3 (Implementation)  → Single session (sequential pipeline, no parallelism needed)
Phase 4 (Parallel Work)   → Agent Teams (primary use case)
Phase 5 (Code Review)     → Agent Teams (primary use case)
Phase 6 (Debugging)       → Agent Teams (competing hypotheses)
Phase 7 (Human)           → Single session (just the lead)
```

## What We Gain from Agent Teams

**Real parallelism.** Current subagents run within one session and report back. Teammates are independent instances that actually work concurrently.

**Direct inter-agent communication.** Wei can challenge Archie directly without routing through a coordinator. Debate rounds happen naturally via messaging rather than through orchestrated subagent invocations.

**Built-in task coordination.** The shared task list with dependency management, file-locked claiming, and status tracking replaces the need for Grace to manually manage a board within conversation context.

**Quality gate enforcement via hooks.** `TaskCompleted` and `TeammateIdle` hooks provide programmatic enforcement of done-gates and veto powers — stronger than prompt-based "don't skip the gate" rules.

**Independent context windows.** Each teammate gets a full context window. No more competing for context budget within a single session. Particularly valuable for parallel work where each stream needs deep codebase understanding.

**Teammate steering.** You can message individual teammates directly (`Shift+Up/Down` in-process mode) to redirect their approach without going through the lead. This is impossible with subagents.

## What We Lose

**Fine-grained tool scoping.** vteam-hybrid's tool access matrix (Cam: read-only, Tara: tests-only writes, Pierrot: scan-only bash) cannot be enforced. All teammates inherit the lead's permissions. This is a security/discipline regression.

**Instant phase switching.** In a single session, the coordinator switches phases by changing which personas are active — zero overhead. Agent Teams requires spawning and shutting down teammates at phase boundaries, with context loss for each new teammate.

**Token efficiency.** Each teammate is a full Claude Code session. For a 3-person review team, that's 3x the base context cost. The current subagent approach summarizes results back, using far fewer tokens.

**Session continuity.** `--resume` doesn't restore in-process teammates. The handoff/resume workflow (`docs/tracking/` artifacts) remains necessary, and teammates' context is lost between sessions.

**Nested orchestration.** Teammates can't spawn their own teams. Phase 4's nested pattern (Parallel Work containing multiple Implementation pipelines) can't be directly expressed. Each implementation pipeline within parallel work must be handled by a single teammate internally.

**Deterministic workflow control.** Custom commands (`/project:tdd`) encode precise step sequences. Agent Teams relies on natural language instructions to the lead, which introduces interpretation variance.

## Migration Path

A phased approach — adapt the phases that benefit most from Agent Teams first, leave the rest as-is.

### Stage 1: Code Review + Parallel Work

**Target phases:** 4 and 5 (Very High fit)
**Changes:**
- Update `/project:code-review` to instruct the lead to spawn 3 reviewer teammates with persona-specific spawn prompts drawn from `.claude/agents/{vik,tara,pierrot}.md`
- Update Phase 4 commands to spawn worker teammates instead of subagents
- Add `TaskCompleted` hook to enforce done-gate checklist
- Add file ownership rules to prevent concurrent edit conflicts

### Stage 2: Debugging + Architecture

**Target phases:** 2 and 6 (High fit)
**Changes:**
- Update `/project:adr` to spawn Archie + Wei as teammates with plan approval required
- Update debugging workflow to spawn hypothesis teammates with direct messaging
- Add `TeammateIdle` hook to redirect idle teammates to next task

### Stage 3: Evaluate and refine

**Assess:**
- Token cost impact vs. quality improvement
- Whether Phases 1, 3, and 7 benefit from migration (likely not)
- Whether scoped tool access is a real problem in practice or adequately handled by spawn prompts
- Whether the single-team-per-session limitation constrains sprint workflows

### What stays the same regardless

- **CLAUDE.md** — methodology and rules. Teammates read this automatically.
- **Agent-notes protocol** — still valuable for context bootstrapping across all sessions.
- **18 persona definitions** — behavioral rules, lenses, and expertise remain. The delivery mechanism changes (spawn prompts instead of subagent invocations), not the content.
- **Tracking artifacts** — `docs/tracking/` remains the cross-session continuity mechanism, especially given Agent Teams' resumption limitations.
- **Done-gate checklist** — migrates from prompt-based to hook-enforced, but the 12 items stay.
- **Sprint boundary workflow** — remains a lead-driven process, potentially enhanced by Agent Teams for parallel retrospective analysis.

## Configuration

To enable Agent Teams alongside vteam-hybrid:

```json
// .claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "teammateMode": "in-process"
}
```

Use `"teammateMode": "tmux"` for split-pane mode if running inside tmux or iTerm2.

## Key Limitations to Watch

These Agent Teams limitations directly affect vteam-hybrid workflows:

| Limitation | Impact on vteam-hybrid |
|---|---|
| One team per session | Can't run Discovery team and then switch to Architecture team in the same session without cleanup + recreation |
| No nested teams | Phase 4's nested Implementation pipelines must be flattened — each teammate handles its own TDD cycle internally |
| No per-teammate permissions | Tool access matrix becomes advisory. Cam _can_ write files even though the persona says read-only |
| No session resumption for teammates | Sprint continuity relies entirely on tracking artifacts, not session state |
| Experimental status | API surface may change. Don't over-invest in tight coupling to current mechanics |
| Shutdown can be slow | Sprint boundary workflow may need patience when cleaning up large teams |
