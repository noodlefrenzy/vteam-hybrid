<!-- agent-notes: { ctx: "full discovery workflow, 5-phase + mandatory board", deps: [docs/team_personas.md, docs/hybrid-teams.md], state: active, last: "grace@2026-02-14", key: ["board creation is mandatory not optional", "issues created as repo issues then added to project", "project linked to repo via gh project link"] } -->
Run a full discovery workflow for: $ARGUMENTS

This is a phased process. Complete each phase and get explicit human confirmation before moving to the next. Reference `docs/team_personas.md` for persona details.

---

## Phase 1: Vision Elicitation (Coach Cam)

Slow down. Do NOT jump to solutions. Your job is to make the human's vision legible — often to themselves for the first time.

- Ask probing questions: "What problem does this solve? For whom? What does success look like? What would make you say this failed?"
- Use the 5 Whys to find root motivations behind surface-level requests.
- Try "what if we did the opposite?" to pressure-test assumptions.
- Surface hidden constraints: timeline, budget, existing systems, skill gaps.
- Propose alternatives the human hasn't considered.

**Checkpoint:** Summarize your understanding of the vision, goals, and constraints. Ask: "Did I get this right? What did I miss?"

**Tracking artifact:** After the human confirms, produce `docs/tracking/YYYY-MM-DD-<topic>-discovery.md` summarizing the vision, goals, constraints, and key insights from elicitation. Use the standard tracking format from `docs/tracking/README.md`. Set **Prior Phase** to "None".

---

## Phase 2: Sacrificial Concepts (Dani)

Generate 2-3 intentionally different approaches. These are **sacrificial** — designed to provoke reactions, not to be implemented as-is.

- Vary on key dimensions: complexity, user model, technical approach, scope.
- Label each explicitly as sacrificial: "This is meant to be torn apart."
- Present trade-offs for each approach.
- Ask: "Which resonates most? Which do you hate? Why?"

**Checkpoint:** Summarize which direction the human is leaning and why. Confirm before proceeding.

---

## Phase 3: Architecture Assessment (Archie + Pierrot)

Based on the chosen direction:

- Propose a high-level architecture. Keep it simple — boxes and arrows, not a thesis.
- Identify key technology decisions that need to be made.
- For each significant choice, create an ADR using `/project:adr`.
- Flag risks and unknowns.
- **Threat model:** Archie creates the data flow diagrams, then Pierrot creates the initial threat model at `docs/security/threat-model.md` — STRIDE analysis, trust boundaries, attack surface inventory. This doesn't need to be exhaustive yet; it grows with the system.
- **Performance budget:** If the project has performance-sensitive requirements (user-facing latency, batch processing throughput, resource constraints), create an initial `docs/performance-budget.md` with targets.

**Checkpoint:** Summarize architectural direction, key decisions, and initial threat surface. Confirm.

**Tracking artifact:** After the human confirms, produce `docs/tracking/YYYY-MM-DD-<topic>-architecture.md` summarizing the chosen architecture, key ADRs created, technology decisions, and threat surface. Use the standard tracking format from `docs/tracking/README.md`. Set **Prior Phase** to the discovery artifact.

---

## Phase 4: Acceptance Criteria (Pat)

Turn the vision into concrete, testable requirements:

- Break the vision into user stories or feature areas.
- Write acceptance criteria for the first milestone.
- Define MVP scope — what's in, what's explicitly out.
- Prioritize ruthlessly. "What's the smallest thing we could ship that would be useful?"

**Checkpoint:** Review the acceptance criteria with the human. Confirm scope.

---

## Phase 5: Planning (Grace + Tara)

Create the implementation plan:

- Create a plan document in `docs/plans/` using `/project:plan`.
- Identify the first sprint's work.
- Note which v-team personas should be actively engaged during implementation.
- Flag any remaining open questions or risks.
- **Test strategy:** Tara creates `docs/test-strategy.md` — what gets tested at which level, coverage targets, test data approach. This guides all future test writing.
- **Tech debt register:** Grace initializes `docs/tech-debt.md` (it will be empty, but the structure is in place for tracking).

**Checkpoint:** Review the plan. Confirm the human is ready to start building.

**Tracking artifact:** After the human confirms, produce `docs/tracking/YYYY-MM-DD-<topic>-plan.md` summarizing the plan goals, first sprint scope, test strategy decisions, and open risks. Use the standard tracking format from `docs/tracking/README.md`. Set **Prior Phase** to the architecture artifact.

### GitHub Project Board Setup (Mandatory)

After the plan is confirmed, create a GitHub Projects board to track the work. This is **not optional** — a project board is required for sprint tracking, backlog sweeps, and retro gating.

1. Detect the repo owner and name: `gh repo view --json owner,name`.
2. Create the project: `gh project create --title "<project-name>" --owner @me`.
3. Link the project to this repo: `gh project link <NUMBER> --owner @me --repo <owner>/<repo>`.
4. Create work items as **repo issues** (not draft items), each with a clear title, acceptance criteria from Phase 4, and a `sprint:1` label for first-sprint items:
   - `gh issue create --title "..." --body "..." --label "sprint:1"` (for first sprint)
   - `gh issue create --title "..." --body "..."` (for backlog items)
5. Add each issue to the project: `gh project item-add <NUMBER> --owner @me --url <issue-url>`.
6. Set initial statuses: first sprint items → **Ready**, everything else → **Backlog**.
7. Update the `CLAUDE.md` GitHub Project Board Integration section — uncomment and fill in `project-number` and `project-owner`.
8. Confirm: "Board created and linked to repo with N items. First sprint has M items in Ready."
