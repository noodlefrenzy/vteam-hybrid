<!-- agent-notes: { ctx: "resume from previous session handoff", deps: [.claude/handoff.md, CLAUDE.md, docs/plans/], state: active, last: "grace@2026-02-12" } -->
Resume from a previous session's handoff.

## Steps

1. **Read the handoff file.** Read `.claude/handoff.md`. If it doesn't exist, tell the user there's no handoff to resume from and ask what they'd like to do.

2. **Read project context.** In parallel, read:
   - `CLAUDE.md` (already loaded, but review for any recent changes)
   - The current plan in `docs/plans/` (if referenced in the handoff)
   - The auto-memory file at the path shown in your system prompt (if it exists)

3. **Verify state.** Run these checks:
   - `git log --oneline -5` — does the last commit match what the handoff says?
   - `git status` — is the working tree clean? If not, investigate before proceeding.
   - If a project board is configured, quick scan of item statuses.

4. **Summarize to the user.** Give a brief (5-10 line) summary:
   - What the previous session accomplished
   - Current state of the project
   - What you're about to do next

5. **Ask for confirmation.** Before executing, ask: "Ready to pick up from here? Or would you like to adjust the plan?"

6. **Execute.** Proceed with the "What To Do Next" items from the handoff. Follow all CLAUDE.md conventions (TDD, conventional commits, agent-notes, etc.).

## If the user provides $ARGUMENTS

Treat the arguments as an override or addition to the handoff's "What To Do Next" section. For example:
- `/project:resume focus on issue #14` — prioritize that issue over the handoff's suggested order
- `/project:resume skip to deployment` — jump ahead in the plan

## Important

- Do NOT blindly trust the handoff. Verify against actual repo/board state. If there's a discrepancy, flag it.
- The handoff is a starting point, not a straitjacket. If the user wants to change direction, that's fine.
- After resuming and completing a significant chunk of work, consider running `/project:handoff` again to update the state for the next potential session break.
