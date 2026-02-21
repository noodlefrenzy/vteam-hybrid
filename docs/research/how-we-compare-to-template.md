---
agent-notes: { ctx: "Competitive analysis template", deps: [docs/methodology/phases.md, docs/team_personas.md], state: canonical, last: "claude@2026-02-16" }
---

<!-- HOW TO USE THIS TEMPLATE:
     1. Copy this file as how-we-compare-to-<name>.md
     2. Replace every [COMPETITOR] with the competitor's name
     3. Fill in each section — all 9 sections are required
     4. Mark any section that genuinely doesn't apply as "N/A — [reason]"
     5. Every claim in sections 4-5 must include a concrete example
     6. At a Glance table uses ✅ (has), ⚠️ (partial), ❌ (missing) only
     7. Adoption Candidates grouped by HIGH / MEDIUM / LOW priority
     8. Remove this comment block when done -->

# How We Compare To: [COMPETITOR]

| Field | Value |
|-------|-------|
| **Competitor** | [Full name and any subtitle] |
| **Maintainer** | [Organization or individual] |
| **Target AI Platform** | [e.g., GitHub Copilot, Claude Code, Cursor, etc.] |
| **Repository** | [Link or reference] |
| **Date Evaluated** | [YYYY-MM-DD] |
| **Evaluated By** | [Name or agent] |

---

## 1 — Executive Summary

<!-- 3-5 sentences. What is [COMPETITOR], who is it for, and what's the single biggest
     takeaway from this comparison? -->

---

## 2 — At a Glance

<!-- Side-by-side feature matrix. Use ✅ (has), ⚠️ (partial), ❌ (missing).
     Add or remove rows as appropriate for the competitor. Keep the table
     focused on capabilities that matter — don't pad with irrelevant rows. -->

| Capability | vteam-hybrid | [COMPETITOR] | Notes |
|------------|:---:|:---:|-------|
| **Phase-separated workflows** | | | |
| **Specialized agents** | | | |
| **Context optimization** | | | |
| **TDD enforcement** | | | |
| **Adversarial debate** | | | |
| **Veto/governance** | | | |
| **Artifact audit trail** | | | |
| **Sprint ceremonies** | | | |
| **Done gate checklist** | | | |
| **Agent personality/voice** | | | |
| **Documentation ownership** | | | |
<!-- Add rows specific to [COMPETITOR]'s strengths -->

---

## 3 — Architecture Comparison

### 3.1 Core Philosophy

| Aspect | vteam-hybrid | [COMPETITOR] |
|--------|-------------|----------|
| **Central metaphor** | Virtual team with phase-adaptive composition | |
| **Key insight** | Different work phases need different org structures | |
| **Optimization target** | Team dynamics and human-AI collaboration | |
| **Context strategy** | Minimize reads (agent-notes) | |

### 3.2 Agent Architecture

<!-- How does [COMPETITOR] organize its agents/personas/roles compared to our
     team-of-specialists model? Cover: composition, hierarchy, governance. -->

### 3.3 Workflow Model

<!-- Diagram or describe [COMPETITOR]'s workflow phases/pipeline and contrast
     with our 7-phase adaptive model. -->

---

## 4 — What They Do Better

<!-- Honest assessment. Each subsection should:
     - Name the capability
     - Explain how [COMPETITOR] implements it
     - Show a concrete example (code snippet, config, diagram)
     - Explain why it matters (what failure mode it prevents)
     Number subsections 4.1, 4.2, etc. -->

---

## 5 — What We Do Better

<!-- Same honest assessment in our favor. Same structure:
     - Name the capability
     - Explain our implementation
     - Show a concrete example
     - Explain why it matters
     Number subsections 5.1, 5.2, etc. -->

---

## 6 — Adoption Candidates

<!-- Concrete things we should consider adopting from [COMPETITOR].
     Group by priority tier. Each item needs: What, Why, Effort, How. -->

### 6.1 HIGH PRIORITY

| What | Why | Effort | How |
|------|-----|--------|-----|
| | | | |

### 6.2 MEDIUM PRIORITY

| What | Why | Effort | How |
|------|-----|--------|-----|
| | | | |

### 6.3 LOW PRIORITY / WATCH

| What | Why | Effort | How |
|------|-----|--------|-----|
| | | | |

---

## 7 — Key Differences in Philosophy

<!-- The deeper "why" behind the divergence. Use a comparison table
     and a 1-2 paragraph synthesis. -->

| Dimension | vteam-hybrid | [COMPETITOR] |
|-----------|-------------|----------|
| **Trust model** | Trust the team; govern with vetoes | |
| **Context model** | Optimize reads within session | |
| **Quality model** | Proactive (TDD + debate + done gate) | |
| **Scaling model** | Consolidate agents, expand lenses | |
| **Human model** | Collaborative (Cam as coach) | |
| **Knowledge model** | Structured docs with ownership | |
| **Platform coupling** | Claude Code (CLI) | |

---

## 8 — Risks and Considerations

<!-- What could go wrong if we adopt their patterns? Bullet list,
     each with a concrete risk and mitigation suggestion. -->

---

## 9 — Action Items

<!-- Concrete next steps with checkboxes. Each should be actionable
     without further research. -->

- [ ] **[Action]** — [Description]

---

## Appendix A — Source Material

<!-- Optional. Link to files, docs, repos consulted during this analysis.
     Use relative paths for local files. -->

| Source | Path |
|--------|------|
| | |
