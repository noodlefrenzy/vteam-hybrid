---
agent-notes: { ctx: "artifact-driven phase tracking protocol", deps: [docs/methodology/agent-notes.md, CLAUDE.md], state: active, last: "grace@2026-02-16" }
---

# Phase Tracking Artifacts

This directory holds lightweight tracking artifacts that capture decisions and state at each workflow phase. They create an audit trail and enable cross-session continuity.

## Naming Convention

```
YYYY-MM-DD-<topic>-<phase>.md
```

**Phases:** `discovery`, `architecture`, `plan`, `implementation`, `review`, `debug`

**Examples:**
- `2026-02-16-auth-system-discovery.md`
- `2026-02-16-auth-system-architecture.md`
- `2026-02-17-auth-system-plan.md`

## Artifact Format

Every tracking artifact follows this structure (~20 lines, not exhaustive research docs):

```markdown
---
agent-notes: { ctx: "<phase> tracking for <topic>", deps: [...], state: active, last: "<agent>@<date>" }
---

# <Phase>: <Topic>

**Date:** YYYY-MM-DD
**Lead:** <agent>
**Status:** Active | Complete | Blocked
**Prior Phase:** <link or "None">

## Key Decisions
- ...

## Artifacts Produced
- ...

## Open Questions
- ...

## Next Phase
- ...
```

## When Artifacts Are Produced

| Command | Phase | Trigger |
|---------|-------|---------|
| `/project:kickoff` Phase 1 | `discovery` | After vision elicitation checkpoint |
| `/project:kickoff` Phase 3 | `architecture` | After architecture assessment checkpoint |
| `/project:kickoff` Phase 5 | `plan` | After planning checkpoint |
| `/project:plan` | `plan` | After plan document is written |
| `/project:tdd` | `implementation` | After TDD work is complete |
| `/project:code-review` | `review` | After review findings are compiled |

Phases 2 and 4 of kickoff are intermediate — their output folds into the adjacent phase artifacts.

## Lifecycle

1. **Created** during the relevant workflow phase with status `Active`
2. **Updated** if the phase revisits decisions (status stays `Active`)
3. **Completed** when the next phase begins (status → `Complete`)
4. **Archived** at sprint boundary — moved to `docs/tracking/archive/sprint-N/`

## Cross-Session Continuity

- `/project:handoff` references the latest tracking artifacts so the next session has phase context
- `/project:resume` can read tracking artifacts to reconstruct where a multi-phase workflow left off
- Each artifact links to its **Prior Phase** artifact, creating a navigable chain

## Design Rationale

- **`docs/tracking/`** not `.copilot-tracking/` — artifacts are committed to the repo as an audit trail
- **No forced `/clear`** — our phases nest and interleave; artifacts are additive context, not replacements
- **Lightweight format** — ~20 lines per artifact, summaries not exhaustive research
- **Archive at sprint boundary** — prevents the tracking directory from growing unbounded
- **Prior Phase links** — each artifact links backward, creating a decision chain
