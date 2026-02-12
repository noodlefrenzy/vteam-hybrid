<!-- agent-notes: { ctx: "full discovery workflow, 5-phase", deps: [docs/team_personas.md, docs/hybrid-teams.md], state: active, last: "cam@2026-02-12" } -->
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

---

## Phase 2: Sacrificial Concepts (Dani)

Generate 2-3 intentionally different approaches. These are **sacrificial** — designed to provoke reactions, not to be implemented as-is.

- Vary on key dimensions: complexity, user model, technical approach, scope.
- Label each explicitly as sacrificial: "This is meant to be torn apart."
- Present trade-offs for each approach.
- Ask: "Which resonates most? Which do you hate? Why?"

**Checkpoint:** Summarize which direction the human is leaning and why. Confirm before proceeding.

---

## Phase 3: Architecture Assessment (Archie)

Based on the chosen direction:

- Propose a high-level architecture. Keep it simple — boxes and arrows, not a thesis.
- Identify key technology decisions that need to be made.
- For each significant choice, create an ADR using `/project:adr`.
- Flag risks and unknowns.

**Checkpoint:** Summarize architectural direction and key decisions. Confirm.

---

## Phase 4: Acceptance Criteria (Pat)

Turn the vision into concrete, testable requirements:

- Break the vision into user stories or feature areas.
- Write acceptance criteria for the first milestone.
- Define MVP scope — what's in, what's explicitly out.
- Prioritize ruthlessly. "What's the smallest thing we could ship that would be useful?"

**Checkpoint:** Review the acceptance criteria with the human. Confirm scope.

---

## Phase 5: Planning (Grace)

Create the implementation plan:

- Create a plan document in `docs/plans/` using `/project:plan`.
- Identify the first sprint's work.
- Note which v-team personas should be actively engaged during implementation.
- Flag any remaining open questions or risks.

**Checkpoint:** Review the plan. Confirm the human is ready to start building.
