---
agent-notes: { ctx: "Competitive analysis vs HVE Core", deps: [docs/methodology/phases.md, docs/methodology/personas.md], state: active, last: "claude@2026-02-16" }
---

# How We Compare To: HVE Core

| Field | Value |
|-------|-------|
| **Competitor** | HVE Core (Hypervelocity Engineering) |
| **Maintainer** | Microsoft (internal/open-source) |
| **Target AI Platform** | GitHub Copilot (VS Code) |
| **Repository** | Internal org reference (`hve-core`) |
| **Date Evaluated** | 2026-02-16 |
| **Evaluated By** | Claude (automated analysis) |

---

## 1 — Executive Summary

HVE Core is Microsoft's enterprise prompt engineering framework for GitHub Copilot. It transforms AI-assisted development through a **Research → Plan → Implement → Review (RPI)** methodology that constrains what the AI can do at each phase, forcing verification before implementation. The single biggest takeaway: HVE Core's **artifact-driven context handoff** — where each phase produces a file that becomes the next phase's input, with chat context cleared between phases — is a pattern we should seriously consider adopting. Our agent-notes protocol optimizes context *within* a session; their artifact protocol optimizes context *across* phases.

---

## 2 — At a Glance

| Capability | vteam-hybrid | HVE Core | Notes |
|------------|:---:|:---:|-------|
| **Phase-separated workflows** | ✅ 7 phases | ✅ 4 phases (RPI) | We have more phases; they have stricter isolation |
| **Specialized agents** | ✅ 18 agents | ✅ 18 agents | Same count, very different composition |
| **Context optimization** | ✅ agent-notes | ⚠️ artifact handoff | Different strategies; both effective |
| **TDD enforcement** | ✅ pipeline model | ❌ | Not a focus of HVE Core |
| **Adversarial debate** | ✅ explicit protocol | ❌ | We have structured debate; they don't |
| **Veto/governance** | ✅ Pierrot + Tara | ❌ | No governance model in HVE Core |
| **Artifact audit trail** | ⚠️ ADRs + docs | ✅ `.copilot-tracking/` | They produce per-task audit trails automatically |
| **Auto-applied instructions** | ❌ | ✅ glob-based stacking | Instructions auto-activate by file pattern |
| **Schema validation pipeline** | ❌ | ✅ JSON schema + CI | Frontmatter validated against schemas in CI |
| **Collection/distribution** | ❌ | ✅ role-based packages | Maturity-gated distribution system |
| **Subagent delegation** | ✅ parallel teams | ✅ `runSubagent` | Similar concept, different implementation |
| **Scaffolding commands** | ✅ 4 scaffold types | ❌ | We have project scaffolding; they don't |
| **Sprint ceremonies** | ✅ boundary ritual | ❌ | We have structured sprint lifecycle |
| **Cross-platform scripts** | ❌ | ✅ .sh + .ps1 | Skills provide both Bash and PowerShell |
| **IDE integration** | ❌ CLI-native | ✅ VS Code extension | They ship a VS Code extension |
| **Prompt input variables** | ❌ | ✅ `${input:var}` | Reusable prompts with user-supplied values |
| **Done gate checklist** | ✅ 12 items | ❌ | No explicit completion criteria |
| **Agent personality/voice** | ✅ distinct voices | ❌ | Our agents have character; theirs are functional |
| **Cloud-adaptive agents** | ✅ multi-cloud | ❌ | We have cloud specialists; they don't |
| **Documentation ownership** | ✅ explicit matrix | ❌ | We assign doc ownership; they don't |

---

## 3 — Architecture Comparison

### 3.1 Core Philosophy

| Aspect | vteam-hybrid | HVE Core |
|--------|-------------|----------|
| **Central metaphor** | Virtual team with phase-adaptive composition | Constraint-based workflow pipeline |
| **Key insight** | Different work phases need different org structures | When AI knows it can't implement, it verifies instead |
| **Optimization target** | Team dynamics and human-AI collaboration | AI output quality through behavioral constraints |
| **Context strategy** | Minimize reads (agent-notes) | Isolate phases (artifact handoff + `/clear`) |

### 3.2 Agent Architecture

**vteam-hybrid** organizes agents as a *team of specialists* with personalities, lenses, and governance:
- Agents have distinct voices (Pierrot's dark humor, Wei's contrarianism)
- Consolidated agents expose multiple lenses (Archie = architecture + data + API)
- Explicit hierarchy: P0 (always present) → P1 (essential) → P2 (specialist)
- Governance model with veto power and escalation paths

**HVE Core** organizes agents as *workflow nodes* in a constrained pipeline:
- Agents are functionally defined (task-researcher, task-planner, task-implementor)
- Each agent has strict behavioral constraints (researcher can't implement)
- Specialized generators (Jupyter, Streamlit, data spec, architecture diagrams)
- No governance model — constraint enforcement replaces team governance

### 3.3 Workflow Model

**vteam-hybrid — 7 phases with adaptive org models:**
```
Discovery (blackboard) → Architecture (ensemble+debate) → Implementation (TDD pipeline)
    ↕                         ↕                               ↕
Debugging (blackboard)   Code Review (ensemble)         Parallel Work (market)
                              ↕
                     Human Interaction (hierarchical)
```
- Phases can nest (parallel work contains multiple implementation pipelines)
- Coordinator selects org model per phase
- No forced context clearing between phases

**HVE Core — 4 phases with strict isolation:**
```
Research → Plan → Implement → Review → (loop back if needed)
    ↓          ↓         ↓           ↓
 research.md  plan.md  changes.md  review.md
```
- Each phase clears chat context (`/clear`)
- Artifacts are the *only* context bridge between phases
- Review can trigger return to any earlier phase
- Single autonomous mode (rpi-agent) for simple tasks

---

## 4 — What They Do Better

### 4.1 Artifact-Driven Phase Isolation

HVE Core's strongest innovation. Each RPI phase produces a dated artifact in `.copilot-tracking/`:
```
.copilot-tracking/
├── research/  2025-02-16-feature-research.md
├── plans/     2025-02-16-feature-plan.instructions.md
├── details/   2025-02-16-feature-details.md
├── changes/   2025-02-16-feature-changes.md
└── reviews/   2025-02-16-feature-review.md
```
**Why this matters:** By clearing context between phases and using artifacts as the only bridge, they eliminate "context contamination" — where assumptions from research leak into implementation without verification. Our agent-notes optimize within-session context loading but don't address cross-phase contamination.

### 4.2 Auto-Applied Instruction Stacking

Instructions use glob patterns to auto-activate by file type:
```yaml
applyTo: '**/*.py, **/*.ipynb'  # Python + Jupyter
applyTo: '**/tests/**/*.ts'     # TypeScript tests only
```
Multiple matching instructions stack without conflict. We have nothing equivalent — our coding standards live in CLAUDE.md as a monolith. Their pattern-based system scales better as projects grow.

### 4.3 Schema Validation Pipeline

Every artifact type (agent, prompt, instruction, skill) has a JSON schema. CI validates frontmatter against schemas on every PR:
```
instruction-frontmatter.schema.json → validates .instructions.md
agent-frontmatter.schema.json       → validates .agent.md
prompt-frontmatter.schema.json      → validates .prompt.md
skill-frontmatter.schema.json       → validates SKILL.md
```
We have no automated validation of our agent definitions or command files.

### 4.4 Collection-Based Distribution

Role-targeted artifact packages with maturity gating:
- `stable` → all channels
- `preview` → pre-release only
- `experimental` → pre-release only
- `deprecated` → never distributed

This enables selective adoption. Teams can install just the RPI workflow, or just the PR review agent, without pulling the entire framework. Our template is all-or-nothing.

### 4.5 Prompt Input Variables

```yaml
${input:topic}          # Required user input
${input:chat:true}      # Optional with default
```
Integrated with VS Code's input UI. Our commands don't have a standardized variable system — they rely on free-text in the prompt.

### 4.6 Specialized Generators

Purpose-built agents for common outputs:
- `gen-jupyter-notebook` — EDA notebooks from data sources
- `gen-streamlit-dashboard` — multi-page dashboards
- `gen-data-spec` — data dictionaries and profiles
- `arch-diagram-builder` — ASCII diagrams from IaC

We handle these through general-purpose agents (Debra for notebooks, Archie for diagrams), but dedicated generators with optimized prompts likely produce better results for these specific tasks.

---

## 5 — What We Do Better

### 5.1 Phase-Adaptive Team Composition

Our 7 org models (blackboard, ensemble, pipeline, market, adversarial debate, hierarchical, composite) give the coordinator a richer vocabulary for organizing work. HVE Core uses a single linear pipeline for everything. When a debugging session needs open brainstorming, their pipeline model is a poor fit; our blackboard model is purpose-built for it.

### 5.2 TDD as a First-Class Workflow

Our TDD pipeline (Tara writes failing tests → Sato makes them pass → Sato refactors) is structurally enforced with a dedicated command (`/project:tdd`). HVE Core has no testing methodology — quality assurance lives entirely in the review phase, which is reactive rather than proactive.

### 5.3 Adversarial Debate Protocol

Structured multi-round debate for high-stakes decisions:
1. Primary agent + challenger invoked in parallel
2. Primary responds to each challenger point
3. Optional rebuttal (capped at 3 rounds)
4. Coordinator summarizes resolution

HVE Core has no equivalent. Their review phase catches issues after implementation; our debate protocol catches them during design.

### 5.4 Governance and Veto Power

Pierrot (security) and Tara (testing) have explicit veto authority with documented escalation paths. This prevents shipping insecure or untested code regardless of deadline pressure. HVE Core relies on the review phase catching issues, with no formal blocking mechanism.

### 5.5 Agent-Notes Context Protocol

Our agent-notes frontmatter lets agents decide *whether to read a file* before opening it:
```yaml
agent-notes: { ctx: "Redis cache wrapper", deps: [src/db.ts], state: active, hot: "200ms p99" }
```
HVE Core has no equivalent — agents must open files to understand them, consuming context budget on irrelevant code.

### 5.6 Sprint Lifecycle Management

`/project:sprint-boundary` triggers a mandatory ritual: retro, backlog sweep, process gate, tech debt review, doc sweep, periodic passes. HVE Core has no concept of sprints or ceremony — it's task-focused, not cadence-focused.

### 5.7 Done Gate (12-Item Checklist)

Explicit completion criteria covering tests, linting, review, accessibility, docs, migrations, API compat, tech debt, and SBOM. HVE Core's review phase is freeform — no standardized checklist, no minimum quality bar.

### 5.8 Agent Personality and Voice

Our agents have distinct personalities that improve human readability and make outputs distinguishable. Pierrot's dark humor in security findings, Wei's contrarian challenges, Vik's grizzled veteran code reviews. HVE Core agents are functionally named and personality-free.

---

## 6 — Adoption Candidates

### 6.1 HIGH PRIORITY

| What | Why | Effort | How |
|------|-----|--------|-----|
| **Artifact-driven phase tracking** | Creates audit trail, prevents context contamination | Medium | Add `docs/tracking/` with dated artifacts per task; update commands to produce/consume them |
| **Auto-applied instruction files** | Scales coding standards beyond monolithic CLAUDE.md | Medium | Create `.claude/instructions/` with glob-based activation; requires Claude Code platform support or manual `@include` conventions |
| **Schema validation for agent defs** | Catches broken agent/command definitions before use | Low | Add JSON schemas for `.claude/agents/*.md` and `.claude/commands/*.md` frontmatter; validate in CI |

### 6.2 MEDIUM PRIORITY

| What | Why | Effort | How |
|------|-----|--------|-----|
| **Maturity labels on agents/commands** | Enables incremental rollout of new capabilities | Low | Add `maturity: stable\|preview\|experimental` to agent-notes frontmatter |
| **Prompt input variables** | Standardizes variable passing in commands | Medium | Define a `${input:name}` convention for command files; document in command authoring guide |
| **Dedicated generator agents** | Better outputs for common artifact types | Medium | Create focused agents for notebooks, dashboards, data specs alongside existing generalist agents |

### 6.3 LOW PRIORITY / WATCH

| What | Why | Effort | How |
|------|-----|--------|-----|
| **Collection-based distribution** | Useful if we modularize for other teams | High | Would require rearchitecting template into composable packages |
| **Cross-platform skill scripts** | Only matters if Windows adoption grows | Low | Add `.ps1` alternatives to `scripts/` directory |
| **VS Code extension** | We're CLI-native; this is a platform bet | High | Only relevant if we expand beyond Claude Code |

---

## 7 — Key Differences in Philosophy

| Dimension | vteam-hybrid | HVE Core |
|-----------|-------------|----------|
| **Trust model** | Trust the team; govern with vetoes | Trust the constraint; prevent bad behavior structurally |
| **Context model** | Optimize reads within session | Isolate context across phases |
| **Quality model** | Proactive (TDD + debate + done gate) | Reactive (review phase catches issues) |
| **Scaling model** | Consolidate agents, expand lenses | Add specialized generators |
| **Human model** | Collaborative (Cam as coach) | Delegative (user triggers workflows) |
| **Knowledge model** | Structured docs with ownership | Artifact trail with dates |
| **Platform coupling** | Claude Code (CLI) | GitHub Copilot (VS Code) |

The fundamental philosophical difference: **vteam-hybrid models a team of humans working together** (with all the governance, debate, and ceremony that implies), while **HVE Core models a constrained pipeline** (where quality comes from limiting what each step can do). Neither is wrong — they optimize for different failure modes. We optimize against team dysfunction; they optimize against context contamination.

---

## 8 — Risks and Considerations

- **Artifact overhead**: Producing dated tracking files for every task adds file management burden. Need a cleanup/archival strategy to prevent `docs/tracking/` from becoming a graveyard.
- **Platform divergence**: Their instruction stacking and input variables are deeply integrated with VS Code / Copilot. Adopting similar patterns in Claude Code CLI may require workarounds or upstream feature requests.
- **Over-constraining phases**: Their strict `/clear` between phases works for Copilot's context model but may not map well to Claude Code's longer context windows. We might get more value from softer phase boundaries.
- **Generator sprawl**: Adding dedicated generator agents risks the roster bloat we worked hard to eliminate (32 → 18). Consider adding generators as *lenses* on existing agents rather than new agents.

---

## 9 — Action Items

- [ ] **Prototype artifact tracking** — Add `docs/tracking/` structure and update one command (e.g., `/project:tdd`) to produce phase artifacts. Evaluate whether the audit trail justifies the overhead.
- [ ] **Draft instruction file convention** — Design a `.claude/instructions/` pattern with glob-based comments since Claude Code doesn't natively support auto-application. Test with 2-3 file-type-specific standards.
- [ ] **Add agent-def schema validation** — Create JSON schemas for agent and command frontmatter. Add a validation script to `scripts/`.
- [ ] **Add maturity labels** — Update agent-notes spec to include `maturity` field. Tag all current agents as `stable`.
- [ ] **Evaluate generator lenses** — Determine whether Debra (data/ML) and Archie (diagrams) should gain explicit generator lenses, or whether standalone generator agents are warranted.

---

## Appendix A — Source Material

| Source | Path |
|--------|------|
| HVE Core README | `../../../hve-core/README.md` |
| HVE Core RPI Methodology | `../../../hve-core/docs/rpi/why-rpi.md` |
| HVE Core Agent Catalog | `../../../hve-core/.github/CUSTOM-AGENTS.md` |
| HVE Core Artifact Architecture | `../../../hve-core/docs/architecture/ai-artifacts.md` |
| HVE Core Collection Manifests | `../../../hve-core/collections/` |
| vteam-hybrid Team Personas | `../team_personas.md` |
| vteam-hybrid Hybrid Teams | `../methodology/phases.md` |
| vteam-hybrid Agent-Notes Protocol | `../agent-notes-protocol.md` |
| vteam-hybrid Done Gate | `../process/done-gate.md` |

