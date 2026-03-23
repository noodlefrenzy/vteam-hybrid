<!-- tomux-guidance-version: 1.0.0 -->
<!-- tomux-source: https://github.com/vaughanknight/tomux/blob/main/templates/TOMUX_AGENT_GUIDANCE.md -->
<!-- agent-notes: { ctx: "vendored tomux agent guidance contract", deps: [], state: active, last: "copilot-cli@2026-03-23" } -->
# Tomux Agent Guidance

> This file instructs the AI agent to create structured progress data
> that the Tomux tmux plugin can visualise. Read and follow these rules.
>
> **Reading priority:** The *Essential Contract* section is all you need.
> The *Worked Examples* and *SQL Cheat Sheet* are reference material.
>
> **vteam-hybrid note:** This project uses the vteam-hybrid methodology which
> has its own phase and todo management conventions (see `CLAUDE.md`). The
> vteam conventions are a _superset_ of this contract — they comply with
> the tomux schema while adding wave-based planning, per-work-item lifecycle
> tracking, and multi-agent progress reporting. Follow `CLAUDE.md` first;
> this file is the reference contract for the underlying tomux data format.

---

## Essential Contract

### Table Setup (Idempotent)

Run these on **every skill entry**. The `todos` and `todo_deps` tables already
exist in the Copilot CLI session database — do **not** recreate them.

```sql
CREATE TABLE IF NOT EXISTS phases (
  id      TEXT PRIMARY KEY,   -- Short ID: 'ph1', 'research', 'clarify'
  name    TEXT,               -- Display name: 'Phase 1: Scaffold'
  ordinal INTEGER,            -- Sort order: 1, 2, 3 …
  status  TEXT DEFAULT 'pending'
    CHECK(status IN ('pending','in_progress','done','blocked'))
);

CREATE TABLE IF NOT EXISTS session_state (
  key   TEXT PRIMARY KEY,
  value TEXT
);
```

### Phase IDs

Use **short**, hyphen-free identifiers. Tomux renders these as pips — long names waste space.

| ✅ Good | ❌ Bad |
|---------|--------|
| `ph1`, `ph2` | `plan-033-ph1` |
| `w1`, `w2` | `phase-1`, `p033` |
| `research`, `clarify` | `my-long-phase-name` |

### Todo IDs

Format: **`{phase_id}-{task_id}`**

Tomux groups todos under phases by stripping the **last** hyphen-segment:

| Todo ID | → Extracted Phase |
|---------|-------------------|
| `ph1-t01` | `ph1` |
| `w1-tests` | `w1` |
| `research-auth` | `research` |

The prefix before the last hyphen **must** match an existing phase `id`.

### Status Values

All tables use the same four statuses:

```
pending  →  in_progress  →  done
                          →  blocked
```

### Session State Keys

| Key | Example Value | Purpose |
|-----|---------------|---------|
| `activity` | `"Implementing Phase 3"` | Current work description (shown in status bar) |
| `phase_heading` | `"Phase 3: Rendering"` | Active phase display name |
| `phase_number` | `"3"` | Active phase ordinal |
| `total_phases` | `"5"` | Total number of phases |
| `total_tasks` | `"12"` | Total tasks in the active phase |

### Clean Slate Rule

When starting a new plan, delete old data first:

```sql
DELETE FROM todos;
DELETE FROM phases;
DELETE FROM todo_deps;
DELETE FROM session_state;
```

### Per-Phase Task Cleanup

When advancing to a new phase, delete the previous phase's completed todos:

```sql
DELETE FROM todos WHERE id LIKE 'ph1-%';
UPDATE phases SET status = 'done' WHERE id = 'ph1';
UPDATE phases SET status = 'in_progress' WHERE id = 'ph2';
```

---

For worked examples and SQL cheat sheet, see the upstream documentation at
https://github.com/vaughanknight/tomux/blob/main/templates/TOMUX_AGENT_GUIDANCE.md
