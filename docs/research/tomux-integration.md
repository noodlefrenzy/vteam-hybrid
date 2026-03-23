<!-- agent-notes: { ctx: "tomux integration plan for vteam-hybrid", deps: [CLAUDE.md, agents/manifest.yaml, docs/methodology/phases.md, docs/process/team-governance.md], state: active, last: "copilot-cli@2026-03-23" } -->

# Integrating Tomux with vteam-hybrid

> **Status:** Research / Pre-ADR
> **Repo:** [vaughanknight/tomux](https://github.com/vaughanknight/tomux)
> **Goal:** Make vteam-hybrid agents drive tomux status bar pips automatically, giving users real-time visual progress on multi-phase AI work.

---

## Table of Contents

1. [What Tomux Is](#1-what-tomux-is)
2. [How It Works](#2-how-it-works)
3. [Where vteam-hybrid Already Overlaps](#3-where-vteam-hybrid-already-overlaps)
4. [The Integration Seam](#4-the-integration-seam)
5. [Mapping vteam Concepts to Tomux Concepts](#5-mapping-vteam-concepts-to-tomux-concepts)
6. [Implementation Plan](#6-implementation-plan)
7. [Which Agents and Commands Change](#7-which-agents-and-commands-change)
8. [Example Session Flow](#8-example-session-flow)
9. [Risks and Constraints](#9-risks-and-constraints)
10. [Open Questions](#10-open-questions)

---

## 1. What Tomux Is

Tomux is a **tmux plugin** that renders coloured pip progress indicators in the tmux status bar by reading from the Copilot CLI's SQLite session database. It's a **read-only observer** — it never writes to the database. The agent is responsible for writing structured phase/task data that tomux visualises.

```
■■■□□ ■■■□□□□  Implementing Phase 3
 ↑       ↑              ↑
phases  tasks       activity text
```

Key characteristics:
- **Zero dependencies** beyond tmux 3.2+ and sqlite3
- **Read-only** — polls `~/.copilot/session-state/{uuid}/session.db`
- **Agent-driven** — the AI agent writes the data; tomux just reads it
- **Bash 3.2 compatible** — works on stock macOS
- **Configurable** — colours, overflow thresholds, detail pane, refresh rate

---

## 2. How It Works

### 2.1 Data Flow

```
Agent (vteam-hybrid)                     Tomux (tmux plugin)
────────────────────                     ──────────────────
                                         
SQL tool writes to session.db   ──→      status.sh polls every 5s
  ├── phases table                       ├── Reads phases → phase pips
  ├── todos table                        ├── Reads todos → task pips
  └── session_state table                └── Reads session_state → activity text
                                         
                                         Renders: ■■●□□ ■■■□ Working on auth
```

### 2.2 Database Schema (tomux expects)

**`phases` table** (agent must CREATE):
```sql
CREATE TABLE IF NOT EXISTS phases (
  id      TEXT PRIMARY KEY,   -- Short ID: 'ph1', 'research'
  name    TEXT,               -- Display: 'Phase 1: Scaffold'
  ordinal INTEGER,            -- Sort order: 1, 2, 3
  status  TEXT DEFAULT 'pending'
    CHECK(status IN ('pending','in_progress','done','blocked'))
);
```

**`todos` table** (already exists in Copilot CLI):
- Tomux groups todos by phase using the ID prefix convention: `{phase_id}-{task_id}`
- e.g., `ph1-t01` belongs to phase `ph1`

**`session_state` table** (agent must CREATE):
```sql
CREATE TABLE IF NOT EXISTS session_state (
  key   TEXT PRIMARY KEY,
  value TEXT
);
```

Required keys: `activity`, `phase_heading`, `phase_number`, `total_phases`, `total_tasks`

### 2.3 ID Convention

Tomux extracts the phase from a todo ID by stripping the last hyphen-segment:

| Todo ID | → Phase |
|---------|---------|
| `ph1-t01` | `ph1` |
| `research-auth` | `research` |
| `impl-create-models` | `impl-create` ← **wrong!** |

**Critical rule:** Phase IDs must not contain hyphens, OR todo IDs must use exactly one hyphen separating `{phase}-{task}`.

---

## 3. Where vteam-hybrid Already Overlaps

### 3.1 Existing Todo System

vteam-hybrid already uses the `todos` and `todo_deps` tables in the Copilot CLI session database. The current convention (from `CLAUDE.md`):

```sql
INSERT INTO todos (id, title, description) VALUES
  ('user-auth', 'Create user auth module', 'Implement JWT auth...');
```

**Current ID format:** descriptive kebab-case (`user-auth`, `api-routes`, `fix-login-bug`)
**Tomux-required format:** `{phase_id}-{task_id}` (`ph1-auth`, `impl-routes`)

### 3.2 Existing Phase Model

vteam-hybrid's 7-phase methodology (`docs/methodology/phases.md`):

| Phase | vteam Name | Potential Tomux Phase |
|-------|-----------|----------------------|
| 1 | Discovery | `disc` |
| 2 | Architecture | `arch` |
| 3 | Implementation | `impl` |
| 4 | Parallel Work | `para` |
| 5 | Code Review | `rev` |
| 6 | Debugging | `dbg` |
| 7 | Human Interaction | `human` |

**But:** These are _methodology_ phases, not _work_ phases. A typical session doesn't walk through all 7. Instead, a session executes a sprint plan with work-item-specific phases like:
- Plan → Implement → Review → Done (for a feature)
- Scaffold → Configure → Test → Deploy (for setup)
- Research → Design → Debate → Decide (for architecture)

### 3.3 Existing Sprint/Wave Model

vteam-hybrid breaks sprints into waves (from session management rules):
- Each wave is a group of issues executed in one session
- Sprint plans live in `docs/sprints/sprint-N-plan.md`
- Grace manages board status transitions

**Key insight:** The tomux phases should map to the **wave structure** or **per-work-item lifecycle**, not the methodology's 7-phase model.

### 3.4 Existing Session State

The Copilot CLI already maintains `session_state` for its own purposes. Tomux adds specific keys to this table. There's no conflict — tomux uses keys (`activity`, `phase_heading`, etc.) that don't overlap with the CLI's internal keys.

---

## 4. The Integration Seam

The integration is **entirely in the instructions layer** — no code changes to tomux, no code changes to the Copilot CLI. We modify how vteam-hybrid agents use the SQL tool to write tomux-compatible data.

### 4.1 What Changes

| Component | Current | After Integration |
|-----------|---------|------------------|
| `CLAUDE.md` § SQL usage | Descriptive kebab-case IDs | `{phase}-{task}` format |
| `CLAUDE.md` § Session management | No phase tracking in DB | Creates `phases` table, updates `session_state` |
| Grace agent | Manages board only | Also manages tomux phases + activity |
| Per-work-item workflow | Updates `todos` status | Also updates `phases` and `session_state` |
| `/kickoff` command | Creates board | Also creates tomux phases |
| `/sprint-boundary` command | Runs retro | Also cleans up tomux state |
| `/handoff` command | Writes handoff.md | Also records phase state for resumption |
| `/resume` command | Reads handoff.md | Also restores tomux phases |

### 4.2 What Doesn't Change

- Agent personas (the 19 agents remain identical)
- Methodology docs (`docs/methodology/`, `docs/process/`)
- Done Gate checklist
- Governance rules
- Agent-notes protocol
- Tracking adapter (GitHub Projects / Jira)

---

## 5. Mapping vteam Concepts to Tomux Concepts

### 5.1 Sprint Wave → Tomux Phases

When Grace plans a sprint wave, the wave items become tomux phases:

```sql
-- Grace plans wave with 3 issues
INSERT INTO phases (id, name, ordinal, status) VALUES
  ('w1', 'Wave 1: Auth module',    1, 'pending'),
  ('w2', 'Wave 2: API endpoints',  2, 'pending'),
  ('w3', 'Wave 3: Test coverage',  3, 'pending');
```

### 5.2 Per-Work-Item Lifecycle → Tomux Phase with Tasks

Each work item has internal steps that become tomux tasks:

```sql
-- Starting work on issue #7 (Wave 1)
UPDATE phases SET status = 'in_progress' WHERE id = 'w1';

INSERT INTO todos (id, title, status) VALUES
  ('w1-tests',   'Tara: Write failing tests',       'pending'),
  ('w1-impl',    'Sato: Implement',                  'pending'),
  ('w1-review',  'Code review (Vik+Tara+Pierrot)',   'pending'),
  ('w1-gate',    'Done Gate checklist',               'pending');

INSERT OR REPLACE INTO session_state (key, value) VALUES
  ('activity',      'Auth module: writing tests'),
  ('phase_heading', 'Wave 1: Auth module'),
  ('phase_number',  '1'),
  ('total_phases',  '3'),
  ('total_tasks',   '4');
```

### 5.3 Activity Text → Current Agent Action

The `activity` session_state key should reflect what the active agent is doing:

| Agent Action | Activity Text |
|-------------|--------------|
| Cam running elicitation | `"Eliciting: auth requirements"` |
| Tara writing tests | `"TDD red: auth tests"` |
| Sato implementing | `"Implementing: auth module"` |
| Code review running | `"Review: Vik+Tara+Pierrot"` |
| Grace updating board | `"Board: moving to In Review"` |
| Sprint boundary | `"Sprint boundary: retro"` |

### 5.4 Parallel Agents → Multiple In-Progress Tasks

When vteam-hybrid spawns parallel agents (e.g., 3-lens code review), tomux shows them as simultaneous in-progress tasks:

```sql
INSERT INTO todos (id, title, status) VALUES
  ('rev-vik',     'Vik: simplicity lens',     'in_progress'),
  ('rev-tara',    'Tara: test coverage lens',  'in_progress'),
  ('rev-pierrot', 'Pierrot: security lens',    'in_progress');
```

Tomux displays: `●●●` (three amber in-progress pips)

### 5.5 Background Agents → Task Completion Updates

When a background agent completes, the coordinator updates its todo:

```sql
UPDATE todos SET status = 'done', updated_at = datetime('now') WHERE id = 'rev-vik';
INSERT OR REPLACE INTO session_state (key, value) VALUES
  ('activity', 'Review: 1/3 lenses complete');
```

Tomux displays: `■●●` → `■■●` → `■■■`

---

## 6. Implementation Plan

### Phase 1: Tomux-Compatible SQL Protocol

Add a new section to `CLAUDE.md` (and corresponding methodology docs) that defines the tomux-compatible SQL protocol. This is the core change — it's all instruction-level.

#### 6.1a Create `phases` and `session_state` Tables

Add to the session entry protocol: at the start of every session that will do work, create the tomux tables:

```sql
CREATE TABLE IF NOT EXISTS phases (
  id      TEXT PRIMARY KEY,
  name    TEXT,
  ordinal INTEGER,
  status  TEXT DEFAULT 'pending'
    CHECK(status IN ('pending','in_progress','done','blocked'))
);

CREATE TABLE IF NOT EXISTS session_state (
  key   TEXT PRIMARY KEY,
  value TEXT
);
```

This is idempotent — safe to run every session.

#### 6.1b Update Todo ID Convention

Change from descriptive kebab-case to `{phase}-{task}` format:

**Before:** `('user-auth', 'Create auth module', ...)`
**After:** `('w1-auth', 'Create auth module', ...)`

Where `w1` is the wave/phase ID.

**Single-phase sessions** (quick tasks, one-off fixes): Use a single phase `work` with todos like `work-fix`, `work-test`, `work-commit`.

#### 6.1c Update Session State on Every Transition

Add session_state updates to the per-work-item workflow:

| Workflow Step | Session State Update |
|--------------|---------------------|
| Start work item | `activity = "Starting: {title}"`, `phase_heading = "Wave N: {title}"` |
| Tara starts | `activity = "TDD red: {title}"` |
| Sato starts | `activity = "Implementing: {title}"` |
| Review starts | `activity = "Review: Vik+Tara+Pierrot"` |
| Done Gate | `activity = "Done Gate: {title}"` |
| Complete | `activity = "Complete: {title}"` |

### Phase 2: Agent Instruction Updates

Modify the agents that drive workflow state transitions:

#### Grace (sprint tracking)
- On wave planning: CREATE `phases` entries for each wave item
- On wave item start: UPDATE phase to `in_progress`
- On wave item done: UPDATE phase to `done`, clean up previous phase's todos
- On sprint boundary: DELETE all phases and todos (clean slate for next sprint)

#### Coordinator (the main agent)
- On session start: Run tomux table creation (idempotent)
- On todo creation: Use `{phase}-{task}` ID format
- On status transitions: UPDATE both `todos` and `session_state`
- On background agent completion: UPDATE todo status, update activity text

### Phase 3: Command Updates

#### `/kickoff`
- After board creation: Create initial tomux phases for the first sprint's waves
- Set session_state with overall plan info

#### `/handoff`
- Include current phase state in handoff.md
- Record which phases are done/in-progress/pending

#### `/resume`
- Restore tomux phase state from handoff
- Set session_state to reflect resumed position

#### `/sprint-boundary`
- Clean slate: DELETE FROM phases, todos, session_state
- Create new phases for the next sprint's waves

#### `/plan`
- When creating a plan with waves: Create corresponding tomux phases
- Each wave becomes a phase; each issue in a wave becomes tasks

### Phase 4: TOMUX_AGENT_GUIDANCE.md Integration

Copy `templates/TOMUX_AGENT_GUIDANCE.md` from the tomux repo into the vteam-hybrid project root (or reference it from `.github/copilot-instructions.md`). This provides the contract that the Copilot CLI reads.

**But:** vteam-hybrid's instructions are more sophisticated than the generic guidance. The vteam instructions should _supersede_ the generic guidance file, not duplicate it. Best approach:

1. Include `TOMUX_AGENT_GUIDANCE.md` for the contract/schema reference
2. Have `CLAUDE.md` and agent instructions use the vteam-specific patterns (wave-based phases, per-work-item lifecycle tasks) that _comply_ with the tomux contract but reflect the vteam methodology

---

## 7. Which Agents and Commands Change

### Instruction-Level Changes (no persona changes)

| File | Change | Scope |
|------|--------|-------|
| `CLAUDE.md` § SQL usage | Add tomux SQL protocol, change todo ID format, add session_state updates | Medium |
| `CLAUDE.md` § Session entry | Add idempotent `CREATE TABLE IF NOT EXISTS phases/session_state` | Small |
| `CLAUDE.md` § Per-work-item workflow | Add session_state updates at each transition | Medium |
| `agents/grace.md` | Add wave→phases creation, phase lifecycle management | Medium |
| `commands/kickoff.md` | Add initial phases creation after board setup | Small |
| `commands/handoff.md` | Add phase state to handoff document | Small |
| `commands/resume.md` | Add phase state restoration | Small |
| `commands/sprint-boundary.md` | Add phases/session_state cleanup | Small |
| `commands/plan.md` | Add phases creation for planned waves | Small |

### No Changes Required

| Component | Why |
|-----------|-----|
| All 19 agent persona files | Personas describe thinking style, not SQL patterns |
| `docs/methodology/*` | Phase model is conceptual, not tied to tomux |
| `docs/process/*` | Governance rules are process-level, not DB-level |
| Tracking adapters | Board integration is separate from tmux display |
| `agents/manifest.yaml` | Capability profiles don't change |
| `scripts/generate-platform.py` | Generation logic doesn't touch SQL patterns |

---

## 8. Example Session Flow

### User starts a sprint wave with 2 issues

```
Session Entry:
  → CREATE TABLE IF NOT EXISTS phases (...)
  → CREATE TABLE IF NOT EXISTS session_state (...)

Grace plans waves:
  → INSERT INTO phases VALUES ('w1', 'Wave 1: Auth', 1, 'pending')
  → INSERT INTO phases VALUES ('w2', 'Wave 2: API', 2, 'pending')
  → session_state: total_phases=2

Tmux status: □□  (two pending phase pips)

Start Issue #7 (Wave 1):
  → UPDATE phases SET status='in_progress' WHERE id='w1'
  → INSERT INTO todos: w1-tests, w1-impl, w1-review, w1-gate
  → session_state: activity="Auth: writing tests", phase_heading="Wave 1: Auth"

Tmux status: ●□ □□□□  (1 phase in-progress, 4 pending tasks)

Tara writes tests:
  → UPDATE todos SET status='in_progress' WHERE id='w1-tests'
  → session_state: activity="TDD red: auth tests"

Tmux status: ●□ ●□□□

Tara completes:
  → UPDATE todos SET status='done' WHERE id='w1-tests'
  → session_state: activity="Auth: implementing"

Tmux status: ●□ ■□□□

Sato implements:
  → UPDATE todos SET status='done' WHERE id='w1-impl'
  → session_state: activity="Auth: code review"

Tmux status: ●□ ■■□□

Code review (3 parallel agents):
  → UPDATE todos SET status='in_progress' WHERE id='w1-review'
  → session_state: activity="Review: Vik+Tara+Pierrot"
  → UPDATE todos SET status='done' WHERE id='w1-review'

Tmux status: ●□ ■■■□

Done Gate:
  → UPDATE todos SET status='done' WHERE id='w1-gate'
  → DELETE FROM todos WHERE id LIKE 'w1-%'
  → UPDATE phases SET status='done' WHERE id='w1'
  → UPDATE phases SET status='in_progress' WHERE id='w2'
  → session_state: activity="Starting Wave 2: API"

Tmux status: ■● □□□  (Wave 1 done, Wave 2 starting with new tasks)
```

---

## 9. Risks and Constraints

### 9.1 ID Format Migration

**Risk:** Changing todo ID format from `user-auth` to `w1-auth` breaks existing conventions.
**Mitigation:** The ID format is a convention in `CLAUDE.md`, not enforced by schema. Change is documentation-only. Old sessions with old-format IDs still work — tomux just shows them as ungrouped (flat display, no phase pips).

### 9.2 Phase ID Hyphen Ambiguity

**Risk:** Tomux extracts phase by stripping the last hyphen-segment. If a phase ID contains a hyphen (e.g., `code-review`), tomux misparses `code-review-t01` as phase `code-review`, task `t01` — which is actually correct. But `code-review-fix-lint` would parse as phase `code-review-fix`, task `lint` — wrong.
**Mitigation:** Use short, hyphen-free phase IDs (`w1`, `w2`, `rev`, `impl`). Document this as a hard rule.

### 9.3 Clean Slate on Sprint Boundary

**Risk:** The tomux contract says to DELETE all todos/phases when starting a new plan. vteam-hybrid's sprint boundary already does a state sweep. These must be coordinated.
**Mitigation:** Sprint boundary command explicitly runs tomux cleanup as part of its workflow.

### 9.4 Multi-Platform Compatibility

**Risk:** Tomux reads from `~/.copilot/session-state/`. This path is Copilot CLI-specific.
**Mitigation:** Tomux is explicitly a Copilot CLI integration. Other platforms (Claude Code, Codex) have their own session databases. Tomux integration only affects the Copilot CLI path. Claude Code has its own session state at `~/.copilot/` too, so this likely works cross-platform for any tool using the Copilot CLI session store.

### 9.5 Session State Conflicts

**Risk:** The Copilot CLI may use `session_state` keys that conflict with tomux's.
**Mitigation:** Tomux uses specific keys (`activity`, `phase_heading`, `phase_number`, `total_phases`, `total_tasks`). These are documented and unlikely to conflict. The `CREATE TABLE IF NOT EXISTS` is idempotent.

---

## 10. Open Questions

1. **Phase granularity:** Should each GitHub issue be a phase (wave model) or should the TDD lifecycle within a single issue be phases (lifecycle model)?
   - **Wave model:** `w1`, `w2`, `w3` — each issue is a phase, tasks are steps within it
   - **Lifecycle model:** `tests`, `impl`, `review` — each TDD step is a phase, tasks are sub-tasks
   - **Recommendation:** Wave model for multi-issue sessions, lifecycle model for single-issue sessions. Grace decides based on wave plan.

2. **Adoption mode:** Should tomux support be always-on or opt-in?
   - Always-on: Every session creates phases/session_state (zero cost if tmux not running)
   - Opt-in: Check for `TOMUX_AGENT_GUIDANCE.md` or a flag in `CLAUDE.md`
   - **Recommendation:** Always-on. The SQL is idempotent and costs nothing if tomux isn't installed.

3. **Should we vendor TOMUX_AGENT_GUIDANCE.md?**
   - Yes: Self-contained, no external dependency
   - No: Stay in sync with upstream tomux changes
   - **Recommendation:** Vendor it, but note the source version for future sync.

4. **Detail pane integration:** Tomux's `prefix+T` shows a full task breakdown. Should vteam-hybrid's task descriptions be optimized for this view?
   - e.g., shorter titles, consistent formatting, emoji status indicators
   - **Recommendation:** Yes, but as a polish pass after the core integration works.
