<!-- agent-notes: { ctx: "mandatory sprint boundary: retro + sweep + gate", deps: [CLAUDE.md, docs/team_personas.md, docs/hybrid-teams.md], state: active, last: "grace@2026-02-14" } -->
Run the mandatory sprint boundary workflow for: $ARGUMENTS

This is the **canonical end-of-sprint process**. It must be run at every sprint boundary — it is NOT optional and should NOT require the user to trigger it manually. When Grace detects that the sprint's work is complete (all sprint items are Done or explicitly deferred), this workflow triggers automatically.

---

## Step 1: Sprint Retro (Automatic)

Run `/project:retro` inline. This is not a suggestion — it happens now, as part of this workflow. The retro will:

1. Reflect on the sprint.
2. Create a retrospective document in `docs/retrospectives/`.
3. Create GitHub issues labeled `process-improvement` for every identified problem.
4. Update `CLAUDE.md` with lessons learned.

**Do not skip this step.** Do not ask the user if they want a retro. Just run it.

---

## Step 2: Backlog Sweep

After the retro, sweep the entire backlog to catch orphaned or user-created issues:

1. **List ALL open issues** on the repo: `gh issue list --state open --json number,title,labels,assignees --limit 500`.
2. **Categorize every issue:**
   - **Current sprint (done):** Issues labeled `sprint:N` (current sprint) that are Done → verify they're closed. Close any that aren't.
   - **Current sprint (not done):** Issues labeled `sprint:N` that are NOT Done → these must be explicitly addressed: carry forward to next sprint, or defer with rationale.
   - **Prior sprint (still open):** Issues labeled `sprint:M` where M < N → these are **orphans**. Flag each one. They must be carried forward, re-triaged, or closed with explanation.
   - **No sprint label:** Issues with no `sprint:*` label → these are either user-created or fell through the cracks. Triage each one: assign to next sprint, add to backlog, or close with explanation.
3. **Report findings** to the user:
   - "Sprint N complete: X issues closed, Y carried forward, Z orphans found, W new/unassigned issues triaged."
   - List each non-closed issue with its disposition.
4. **Get user confirmation** on the triage decisions before applying labels.

This step is critical because it:
- Catches issues that were never picked up
- Picks up issues the user created directly on the repo (allowing user influence on the backlog)
- Prevents work from silently disappearing between sprints

---

## Step 3: Process-Improvement Gate

Before the next sprint can begin, verify that process-improvement issues from the retro have been addressed:

1. **List process-improvement issues:** `gh issue list --label "process-improvement" --state open --json number,title`.
2. **For each open process-improvement issue:**
   - If it can be resolved now (e.g., updating a process doc, adding a checklist), resolve it immediately.
   - If it requires sprint work, it MUST be included in the next sprint — add `sprint:N+1` label.
   - It cannot simply be ignored or deferred indefinitely.
3. **Gate check:** If any process-improvement issue is neither resolved nor scheduled for the next sprint, **block sprint start** and flag to the user.

---

## Step 4: Next Sprint Setup

Once the gate passes:

1. **Create `sprint:N+1` label** if it doesn't exist.
2. **Carry forward items:** Apply `sprint:N+1` label to all carried-forward issues.
3. **Sprint planning:** Invoke Pat for prioritization of the next sprint's backlog.
4. **Update board:** Move next-sprint items to **Ready** status on the project board.
5. **Announce:** Summarize the next sprint's scope to the user.
