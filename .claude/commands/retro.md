<!-- agent-notes: { ctx: "kaizen retrospective workflow", deps: [docs/team_personas.md], state: active, last: "grace@2026-02-12" } -->
Reflect on the work done in this session. Consider:

1. What went well?
2. What was harder than expected?
3. Were there any recurring patterns or friction points?
4. What would have made the work easier or faster?
5. Are there any new conventions, gotchas, or patterns to document?
6. Which v-team personas (see `docs/team_personas.md`) were effectively engaged during this session? Which were missing?
7. Were there moments where a persona's perspective would have caught an issue earlier?
8. Should any persona definitions in `docs/team_personas.md` be updated based on this experience?

Then take these actions:
- Create a retrospective file at `docs/retrospectives/{{date}}-<topic>.md` summarizing the reflection. Add agent-notes frontmatter per `docs/agent-notes-protocol.md`.
- Update `CLAUDE.md` with any new patterns, conventions, or lessons learned.
- Create or update custom commands in `.claude/commands/` if a repeatable workflow emerged during this session.
- If any architectural decisions were made implicitly, capture them as ADRs in `docs/adrs/`.
