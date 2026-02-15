---
agent-notes:
  ctx: "12-item Done Gate checklist for work items"
  deps: [CLAUDE.md]
  state: active
  last: "coordinator@2026-02-15"
---
# Done Gate — Detailed Checklist

Extracted from CLAUDE.md to reduce context window load. Referenced by CLAUDE.md Workflow section.

Every work item must pass this gate before closing:

1. **Tests pass** with zero failures.
2. **Formatted** per project's formatter (no diffs).
3. **Linted** with zero warnings.
4. **Code reviewed** — the code-reviewer agent (or at minimum one review lens) has been invoked.
5. **Acceptance criteria met** — the feature works as specified, not just "tests pass."
6. **Docs current** — if the change affects user-facing behavior, Diego has updated docs.
7. **Accessibility reviewed** — if any frontend/UI file was changed, Dani (accessibility lens) has reviewed.
8. **Board updated** — status is "In Review" → "Done" (not skipping "In Review").
9. **Migration safe** — if schema/data changes are involved, Archie's migration safety checklist passes.
10. **API compatible** — if API contracts changed, backward compatibility verified or new version created.
11. **Tech debt logged** — if shortcuts were taken, they're recorded in `docs/tech-debt.md`.
12. **SBOM current** — if dependencies were added/removed/upgraded, Pierrot has updated the SBOM.
