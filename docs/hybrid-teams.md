---
agent-notes: { ctx: "phase-dependent team compositions for hybrid methodology", deps: [docs/team_personas.md, CLAUDE.md], state: canonical, last: "archie@2026-02-12" }
---

# Hybrid Team Methodology

Different development phases need different organizational structures. Instead of a fixed hierarchy, the coordinator selects the appropriate team composition at each phase transition. This document defines the 7 phases, their org models, and which agents participate.

## Core Insight

No single org structure works for everything:
- **Discovery** needs a shared workspace where anyone can contribute ideas (blackboard)
- **Implementation** needs a strict pipeline with clear handoffs (TDD pipeline)
- **Code review** needs multiple independent reviewers working in parallel (ensemble)
- **Debugging** needs open collaboration on a shared problem space (blackboard)

The coordinator's job is to recognize phase transitions and assemble the right team.

## The 7 Phases

### Phase 1: Discovery

**Org Model:** Blackboard (shared workspace, anyone contributes)

| Role | Agent | Responsibility |
|------|-------|---------------|
| Lead | **Cam** | Elicitation, probing, clarifying |
| Contribute | **Pat** | Business value, priorities |
| Contribute | **Dani** | Sacrificial concepts, user needs |
| Contribute | **Wei** | Challenge assumptions |
| Contribute | **User Chorus** | User perspective validation |
| Optional | **Debra** | Data/ML feasibility |

**How it works:** Cam leads elicitation. All contributing agents can add ideas to the "blackboard" (plan document). No hierarchy — the best idea wins regardless of source. Cam synthesizes and confirms with the human.

**Transition to next phase:** When the human confirms the vision is clear and the direction is chosen.

---

### Phase 2: Architecture

**Org Model:** Ensemble + Adversarial Debate

| Role | Agent | Responsibility |
|------|-------|---------------|
| Lead | **Archie** | System design, ADR authorship |
| Challenger | **Wei** | Devil's advocate on every decision |
| Reviewer | **Vik** | Simplicity check on proposed architecture |
| Constraint | **Pierrot** | Security surface assessment |
| Constraint | **Ines** | Operational feasibility |
| Optional | **Cloud Architect** | Cloud-specific design (if targeting cloud) |

**How it works:** Archie proposes architecture. Wei challenges it (adversarial debate protocol). Vik checks for over-engineering. Pierrot flags security concerns. Ines validates operational feasibility. Debates are multi-round — see the Adversarial Debate Protocol in CLAUDE.md.

**Transition to next phase:** When the ADR is accepted and the human approves the architecture.

---

### Phase 3: Implementation (TDD Pipeline)

**Org Model:** Pipeline (strict sequential handoffs)

| Stage | Agent | Responsibility |
|-------|-------|---------------|
| Red | **Tara** | Write failing tests |
| Green | **Sato** | Make tests pass with minimum code |
| Refactor | **Sato** | Clean up while keeping tests green |
| Verify | **Tara** | Confirm tests pass, coverage adequate |

**How it works:** Strict TDD pipeline. Tara writes failing tests first. Sato implements. Sato refactors. Tara verifies. No skipping steps. For items sized M or larger, Tara must be invoked as a standalone agent (not inlined by Sato).

**Transition to next phase:** When implementation is complete and tests pass.

---

### Phase 4: Parallel Work

**Org Model:** Market / Self-claim

| Role | Agent | Responsibility |
|------|-------|---------------|
| Coordinator | **Grace** | Work distribution, status tracking |
| Workers | **Sato** (x N) | Parallel implementation streams |
| Workers | **Tara** (x N) | Parallel test writing |
| Workers | **Dani** | UI/UX work (parallel to backend) |
| Workers | **Ines** | Infrastructure work (parallel to app code) |
| Workers | **Diego** | Documentation (parallel to implementation) |

**How it works:** Grace identifies independent work items that can proceed in parallel. Agents self-claim or are assigned non-overlapping work. Multiple Task tool calls launch parallel agent teams. Grace tracks progress and flags blockers.

**When to use:** When there are 3+ independent work items that don't share dependencies. Default to parallel unless there's a true data dependency between items.

**Transition to next phase:** When all parallel work items are complete.

---

### Phase 5: Code Review

**Org Model:** Ensemble (3 parallel reviewers)

| Role | Agent | Responsibility |
|------|-------|---------------|
| Coordinator | Orchestrator | Launches reviewers, synthesizes |
| Reviewer | **Vik** | Simplicity, maintainability |
| Reviewer | **Tara** | Test quality, coverage |
| Reviewer | **Pierrot** | Security surface |
| Optional | **Dani** | UI/UX review (if frontend changes) |

**How it works:** All three reviewers run in parallel (same message, multiple Task calls). Each provides independent findings. The coordinator synthesizes findings by severity. If a reviewer flags a blocking concern, it triggers adversarial debate with the implementer (Sato).

**Transition to next phase:** When all critical and important findings are addressed.

---

### Phase 6: Debugging

**Org Model:** Blackboard (shared problem space)

| Role | Agent | Responsibility |
|------|-------|---------------|
| Lead | **Sato** | Hypothesis generation, fix implementation |
| Contribute | **Tara** | Reproduce via failing test |
| Contribute | **Vik** | Pattern recognition, root cause intuition |
| Contribute | **Pierrot** | Security-related root causes |
| Optional | **Ines** | Infrastructure-related root causes |
| Optional | **Debra** | Data/ML-related root causes |

**How it works:** Shared "blackboard" — a debugging document where agents post hypotheses, observations, and evidence. Tara writes a failing test that reproduces the bug. Sato investigates and fixes. Vik contributes pattern-based intuition. Any agent can contribute if they spot something.

**Transition to next phase:** When the bug is fixed and the regression test passes.

---

### Phase 7: Human Interaction

**Org Model:** Hierarchical (single point of contact)

| Role | Agent | Responsibility |
|------|-------|---------------|
| Lead | **Cam** | All human-facing communication |
| Support | **Pat** | Business context for decisions |
| Support | **Grace** | Status updates, progress reports |

**How it works:** Cam is the single point of contact for the human. Other agents feed information to Cam, who synthesizes and presents it. This prevents the human from being overwhelmed by multiple agent voices. Cam translates between agent-speak and human-speak.

**When to use:** Any time the human needs to be consulted, informed, or asked for a decision. Cam is the default for all human interaction unless the human explicitly asks to speak to a specific agent.

---

## Phase Selection Flowchart

```
Is the user presenting a new idea or vague request?
  → YES → Phase 1: Discovery
  → NO ↓

Is there an architectural decision to make?
  → YES → Phase 2: Architecture
  → NO ↓

Is there code to write?
  → YES → Are there 3+ independent work items?
           → YES → Phase 4: Parallel Work (each item uses Phase 3 internally)
           → NO → Phase 3: Implementation
  → NO ↓

Is there code to review?
  → YES → Phase 5: Code Review
  → NO ↓

Is there a bug to fix?
  → YES → Phase 6: Debugging
  → NO ↓

Does the human need to be consulted?
  → YES → Phase 7: Human Interaction
```

## Phase Nesting

Phases can nest. Common patterns:

- **Parallel Work** contains multiple **Implementation** pipelines running concurrently
- **Discovery** may trigger **Architecture** for technical feasibility checks
- **Code Review** may trigger **Debugging** if a reviewer finds a bug
- **Any phase** can trigger **Human Interaction** when a decision is needed

The coordinator manages the phase stack — knowing which phase is active and which phases are suspended waiting for a sub-phase to complete.

## Agent Participation Summary

| Agent | Discovery | Architecture | Implementation | Parallel | Review | Debugging | Human |
|-------|:---------:|:------------:|:--------------:|:--------:|:------:|:---------:|:-----:|
| **Cam** | Lead | | | | | | Lead |
| **Sato** | | | Green+Refactor | Worker | | Lead | |
| **Tara** | | | Red+Verify | Worker | Reviewer | Contribute | |
| **Pat** | Contribute | | | | | | Support |
| **Grace** | | | | Coordinator | | | Support |
| **Archie** | | Lead | | | | | |
| **Dani** | Contribute | | | Worker | Optional | | |
| **Pierrot** | | Constraint | | | Reviewer | Contribute | |
| **Vik** | | Reviewer | | | Reviewer | Contribute | |
| **Ines** | | Constraint | | Worker | | Optional | |
| **Diego** | | | | Worker | | | |
| **Wei** | Contribute | Challenger | | | | | |
| **Debra** | Optional | | | | | Optional | |
| **User Chorus** | Contribute | | | | | | |
| **Cloud Architect** | | Optional | | | | | |
| **Cloud CostGuard** | | | | | | | |
| **Cloud NetDiag** | | | | | | | |
