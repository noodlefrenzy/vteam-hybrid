---
agent-notes:
  ctx: "13-item Done Gate checklist for work items"
  deps: [CLAUDE.md]
  state: active
  last: "coordinator@2026-02-18"
---
# Done Gate — Detailed Checklist

Extracted from CLAUDE.md to reduce context window load. Referenced by CLAUDE.md § Workflow.

Every work item must pass this gate before closing:

1. **Tests pass** with zero failures.
2. **Typecheck passes** with zero errors. If the project uses a type-checked language, the type checker must pass independently of tests (e.g., Vitest uses esbuild with no type checking, so `tsc` can fail even when tests pass). This catches missing imports, wrong generics, stale type references after migrations, and mock type mismatches.
3. **Formatted** per project's formatter (no diffs).
4. **Linted** with zero warnings.
5. **Code reviewed** — the code-reviewer agent (or at minimum one review lens) has been invoked.
6. **Acceptance criteria met** — the feature works as specified, not just "tests pass."
7. **Docs current** — if the change affects user-facing behavior, Diego has updated docs.
8. **Accessibility reviewed** — if any frontend/UI file was changed, Dani (accessibility lens) has reviewed.
9. **Board updated** — status has passed through "In Progress" → "In Review" → "Done" in order (not skipping any). Verify by checking the item's current status on the board (`gh project item-list <NUMBER> --owner <OWNER> --format json`). If "In Review" status doesn't exist on the board, this is a board configuration failure — fix it before proceeding (see `/project:kickoff` Phase 5 Step 2).
10. **Migration safe** — if schema/data changes are involved, Archie's migration safety checklist passes.
11. **API compatible** — if API contracts changed, backward compatibility verified or new version created.
12. **Tech debt logged** — if shortcuts were taken, they're recorded in `docs/tech-debt.md`.
13. **SBOM current** — if dependencies were added/removed/upgraded, Pierrot has updated the SBOM.
