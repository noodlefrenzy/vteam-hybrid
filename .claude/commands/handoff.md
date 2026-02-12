<!-- agent-notes: { ctx: "session handoff for continuity across sessions", deps: [CLAUDE.md, docs/plans/], state: active, last: "grace@2026-02-12" } -->
Create a session handoff document so the next session can pick up where this one left off.

## Steps

1. **Assess current state.** In parallel, run:
   - `git log --oneline -10` — recent commits
   - `git status` — working tree state
   - `git diff --stat` — uncommitted changes summary
   - Check the project board if configured: `gh project item-list <NUMBER> --owner @me --format json` (skip if no board)

2. **Summarize what was done.** Review the work completed in this session:
   - What features/fixes were implemented
   - What tests were written/updated
   - What docs were created/updated
   - What ADRs were created
   - What's committed vs. uncommitted

3. **Identify what's next.** Based on the current plan (check `docs/plans/`) and any in-flight work:
   - What's the immediate next task?
   - What's blocked and on what?
   - What decisions are pending human input?
   - What open questions remain?

4. **Write the handoff file.** Create or update `.claude/handoff.md` with this structure:

```markdown
# Session Handoff

**Created:** <today's date>
**Session summary:** <1-2 sentence summary>

## What Was Done
- <bulleted list of accomplishments>

## Current State
- **Branch:** <current branch>
- **Last commit:** <hash + message>
- **Uncommitted changes:** <description or "none">
- **Tests:** <passing/failing/not run>
- **Board status:** <summary or "no board configured">

## What To Do Next (in order)
1. <next task with enough context to execute>
2. <following task>
3. ...

## Open Questions
- <anything that needs human input>

## Key Context
- <any non-obvious context the next session needs>
- <files that were being actively worked on>
- <gotchas discovered during this session>
```

5. **Commit the handoff.** If there are uncommitted changes, ask the user if they want to commit before creating the handoff. Then commit the handoff file itself.

## Important

- Be specific in "What To Do Next" — include file paths, function names, and enough detail that the next session doesn't need to re-discover context.
- Don't include sensitive information (tokens, credentials, personal data) in the handoff.
- If the session discovered patterns or gotchas, update `CLAUDE.md` as well — the handoff is ephemeral, `CLAUDE.md` is durable.
- Add agent-notes frontmatter to the handoff file per `docs/agent-notes-protocol.md`.
