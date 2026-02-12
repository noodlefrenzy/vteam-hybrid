<!-- agent-notes: { ctx: "implementation planning workflow", deps: [docs/team_personas.md, docs/hybrid-teams.md], state: active, last: "pat@2026-02-12" } -->
I need to plan the implementation of: $ARGUMENTS

Before writing the plan, ensure the goal is well-understood. If the request is vague, first run through Coach Cam elicitation (see `docs/team_personas.md`) or use `/project:kickoff` for full discovery.

Create or update a plan document in `docs/plans/`. The plan should include:

1. **Goal** — What we're trying to achieve and why.
2. **Constraints** — Any relevant ADRs, conventions, or technical limitations.
3. **Approach** — Step-by-step implementation plan following TDD.
4. **Personas involved** — Which v-team personas should be consulted during implementation? (See `docs/team_personas.md`.)
5. **Open Questions** — Anything that needs clarification before starting.
6. **Acceptance Criteria** — How we'll know the work is done.

Check existing ADRs and plans for context before writing. Add agent-notes frontmatter per `docs/agent-notes-protocol.md`.
