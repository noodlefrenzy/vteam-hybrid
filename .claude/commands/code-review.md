<!-- agent-notes: { ctx: "three-lens code review + review doc output", deps: [docs/team_personas.md, .claude/agents/code-reviewer.md], state: active, last: "grace@2026-02-14" } -->
Run a multi-perspective code review on the current changes.

This combines three persona lenses from the v-team (see `docs/team_personas.md`). Review the staged/unstaged changes or the most recent commits and apply each lens.

---

## Lens 1: Vik (Simplicity & Maintainability)

Review through the eyes of a veteran engineer asking "could a junior understand this at 2am during an incident?"

- Unnecessary complexity or abstraction?
- Clever code that should be obvious code?
- N+1 queries or hidden performance issues?
- Concurrency risks?
- Naming that obscures intent?
- Is the code organized so that the next person can find things?

---

## Lens 2: Tara (Test Quality & Coverage)

Review through the eyes of a testing expert:

- Are the new/changed code paths covered by tests?
- Are unhappy paths and edge cases tested?
- Do tests verify behavior or implementation details? (Prefer behavior.)
- Is the test pyramid balanced? (Too many e2e? Not enough unit?)
- Are test names descriptive enough to serve as documentation?
- Any flaky test risks (timing, ordering, external dependencies)?

---

## Lens 3: Pierrot (Security Surface)

Review through the eyes of a security and compliance expert:

- Auth or authorization changes? Are they correct?
- User input being handled safely? (Injection, XSS, SSRF?)
- Secrets or credentials exposed?
- New dependencies introduced? Any known vulnerabilities or license issues?
- Data handling changes? (PII, encryption, logging sensitive data?)
- New attack surface exposed?

---

## Output

Organize findings by lens and severity:

- **Critical** — Must fix before merging. Security vulnerabilities, data loss risks, broken functionality.
- **Important** — Should fix. Maintainability issues, missing test coverage for key paths, potential performance problems.
- **Suggestion** — Consider fixing. Style, naming, minor improvements.

If no issues found for a lens, say so explicitly — a clean bill of health is useful information.

---

## Review Document

For non-trivial reviews (M-sized or larger changes, Critical/Important findings, new patterns, or anything with teaching value), write a review document to `docs/code-reviews/{{date}}-<topic>.md`. These serve as learning artifacts for early-career developers.

The document should include context, all findings with explanations of *why* they matter (not just what's wrong), and a **Lessons** section with generalizable takeaways. See the code-reviewer agent definition for the full template.

When in doubt about whether a review is "large enough" to document — document it. The cost of an extra doc is low; the cost of lost knowledge is high.
