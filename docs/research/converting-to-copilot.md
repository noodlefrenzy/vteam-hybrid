<!-- agent-notes: { ctx: "multi-platform conversion plan for vteam-hybrid", deps: [CLAUDE.md, .claude/agents/, .claude/commands/, .claude/commands/sync-ghcp.md, docs/methodology/personas.md, docs/methodology/phases.md], state: active, last: "copilot-cli@2026-03-22" } -->

# Converting vteam-hybrid to Multi-Platform: Copilot, Codex, Gemini & Beyond

> **Status:** Research / Pre-ADR  
> **Goal:** Make vteam-hybrid work on GitHub Copilot (primary target) while retaining full Claude Code support, and architect the abstraction so that Codex CLI and Gemini Code Assist are incremental additions — not rewrites.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Landscape Analysis](#2-landscape-analysis)
3. [What's Already Platform-Agnostic](#3-whats-already-platform-agnostic)
4. [What Must Be Abstracted](#4-what-must-be-abstracted)
5. [The Abstraction Layer](#5-the-abstraction-layer)
6. [Platform Adapter Specifications](#6-platform-adapter-specifications)
7. [The AGENTS.md Bridge](#7-the-agentsmd-bridge)
8. [Migration Strategy](#8-migration-strategy)
9. [Future-Proofing Principles](#9-future-proofing-principles)
10. [Risk Analysis](#10-risk-analysis)
11. [Open Questions](#11-open-questions)

---

## 1. Problem Statement

vteam-hybrid encodes a powerful, platform-agnostic methodology (7 phases, 19 personas, governance protocols, TDD workflows) — but that methodology is currently _welded_ to Claude Code's implementation primitives:

- **Agent definitions** live in `.claude/agents/*.md` with Claude-specific YAML frontmatter (`tools: Read, Write, Edit, Bash`, `maxTurns`, `model: inherit`).
- **Commands** live in `.claude/commands/*.md` with `$ARGUMENTS` substitution and prose-based agent invocation.
- **Project instructions** live in `CLAUDE.md`, a file only Claude Code reads.
- **Agent spawning** relies on Claude Code's Task tool with `mode: "background"` and sub-agent orchestration.

The existing `/sync-ghcp` command proves one-way generation _works_, but it produces a static snapshot that drifts. We need a live, multi-platform architecture where:

1. The methodology is the single source of truth.
2. Platform-specific files are generated or adapter-mediated.
3. Adding a new platform is an afternoon of adapter work, not a rewrite.

---

## 2. Landscape Analysis

### 2.1 Platform Configuration Formats (as of March 2026)

| Platform | Instruction File | Agent Format | Command/Prompt Format | Tool Names |
|---|---|---|---|---|
| **Claude Code** | `CLAUDE.md` (root) | `.claude/agents/*.md` (YAML frontmatter + prose) | `.claude/commands/*.md` (prose + `$ARGUMENTS`) | `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`, `WebSearch`, `WebFetch`, `NotebookEdit` |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/agents/*.agent.md` (YAML frontmatter + prose) | `.github/prompts/*.prompt.md` (YAML frontmatter + prose) | `read`, `editFiles`, `runInTerminal`, `search/codebase`, `fetch`, MCP servers |
| **OpenAI Codex CLI** | `AGENTS.md` (hierarchical, root → leaf) | No separate agent files; persona in `AGENTS.md` sections | No separate command files; skills as `SKILL.md` folders | `config.toml` sandbox policies; tools via MCP servers |
| **Gemini Code Assist** | Context files (drag-in or MCP) | No dedicated agent format; behavior via prompts + MCP tools | No command format; agentic chat with MCP integrations | Built-in file/terminal tools; MCP mandatory post-March 2026 |
| **Cursor** | `.cursor/rules/*.mdc` | No dedicated agent format; agentic via rules | No command format; rules-based | `read_file`, `edit_file`, `run_command`, `search` |

### 2.2 The AGENTS.md Convergence

The industry is converging on `AGENTS.md` (AAIF standard, 60k+ repos) as a cross-platform instruction file. Key facts:

- **Natively supported by:** Codex CLI, GitHub Copilot, Cursor, Windsurf, Amp, Devin
- **Claude Code:** Reads `CLAUDE.md` natively; can reference `AGENTS.md` via include or symlink
- **Gemini:** Uses `GEMINI.md` but the format is identical; MCP bridge underway
- **Format:** Plain Markdown with sections for build/test/lint, conventions, boundaries, architecture
- **Limitation:** No support for multi-agent orchestration, tool permissions, or persona definitions — it's "project context," not "team configuration"

**Implication:** AGENTS.md is necessary but not sufficient. It covers _project context_ but not _team methodology_. vteam-hybrid needs both.

### 2.3 Capability Gaps by Platform

| Capability | Claude Code | Copilot | Codex CLI | Gemini | Cursor |
|---|---|---|---|---|---|
| Named sub-agents with isolated tool access | ✅ Full | ✅ `.agent.md` | ❌ No isolation | ❌ No agents | ❌ No agents |
| Parallel agent orchestration | ✅ Task tool | ⚠️ Sequential | ❌ Single agent | ❌ Single agent | ❌ Single agent |
| Tool permission boundaries (allow/deny) | ✅ Per-agent | ✅ Per-agent | ⚠️ Global sandbox | ❌ Global only | ❌ Global only |
| Custom commands/workflows | ✅ `/commands` | ✅ `.prompt.md` | ⚠️ Skills (SKILL.md) | ❌ Prompt-only | ⚠️ Rules |
| Model selection per agent | ✅ `model:` field | ⚠️ Limited | ✅ `config.toml` | ❌ Fixed | ⚠️ User setting |
| Background/async agents | ✅ `mode: background` | ❌ Sequential | ❌ Sequential | ❌ Sequential | ❌ Sequential |
| Session persistence | ✅ Session state | ⚠️ Chat history | ⚠️ Session file | ❌ Ephemeral | ⚠️ Chat history |

---

## 3. What's Already Platform-Agnostic

These components are pure methodology and can be shared verbatim across all platforms:

| Component | Location | Notes |
|---|---|---|
| 7-Phase Model | `docs/methodology/phases.md` | Org structures, transitions, outputs — zero platform deps |
| 19 Persona Definitions (conceptual) | `docs/methodology/personas.md` | Thinking styles, responsibilities, voice rules |
| Governance Rules | `docs/process/team-governance.md` | Triggers, debate protocol, architecture gate, scope gate |
| Done Gate Checklist | `docs/process/done-gate.md` | 15 items; only "board updated" has tool-specific implementation |
| Phase Tracking Protocol | `docs/process/tracking-protocol.md` | Markdown artifact naming and lifecycle |
| Agent-Notes Protocol | `docs/methodology/agent-notes.md` | File metadata format — works in any codebase |
| Adversarial Debate Format | `docs/process/team-governance.md` § Debate | Multi-round exchange tracking format |
| Operational Baseline | `docs/process/operational-baseline.md` | Cross-cutting concerns checklist |
| ADR Template & Process | `docs/adrs/template.md` | Architecture Decision Records |
| Gotchas & Patterns | `docs/process/gotchas.md` | Implementation anti-patterns |

**Key insight:** ~70% of vteam-hybrid's value is in `docs/`. This content doesn't need conversion — it needs to be _referenced_ by each platform's instruction file.

---

## 4. What Must Be Abstracted

### 4.1 Agent Definitions (19 agents × N platforms)

**Current state:** Each agent is a `.claude/agents/*.md` file with:
```yaml
---
name: sato
description: Principal software engineer
tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
model: inherit
maxTurns: 50
---
# Persona prompt...
```

**What varies per platform:**
- YAML frontmatter field names (`tools` vs `allowed_tools` vs nothing)
- Tool name vocabulary (`Read` vs `read` vs `read_file`)
- Permission model (allowlist vs blocklist vs global sandbox)
- Model selection mechanism
- Turn/iteration limits

**What is platform-agnostic:**
- Persona name, description, thinking style
- The prose body (behavioral instructions)
- Conceptual capability profile (what the agent _should_ be able to do)

### 4.2 Commands/Workflows (27 commands × N platforms)

**Current state:** Prose workflows in `.claude/commands/*.md` with:
- `$ARGUMENTS` for parameter substitution
- Narrative agent invocation ("invoke Tara as a standalone agent")
- Inline bash recipes
- Cross-references to other commands (`/adr`, `/tdd`)

**What varies per platform:**
- File location and format (`.prompt.md`, `SKILL.md`, rules, or nothing)
- Parameter substitution syntax
- Agent invocation mechanism
- Available tool vocabulary in workflow steps

### 4.3 Project Instructions (CLAUDE.md → per-platform)

**Current state:** `CLAUDE.md` combines:
- Project context (name, stack, structure)
- Methodology references (phase table, persona triggers)
- Process rules (session entry protocol, commit discipline)
- Platform-specific syntax (tracking adapter HTML comments, agent spawn instructions)

### 4.4 Agent Orchestration Patterns

The methodology assumes agents can be:
1. **Spawned in parallel** (e.g., Vik + Tara + Pierrot for code review)
2. **Chained sequentially** (e.g., Tara writes tests → Sato implements)
3. **Gated** (e.g., Architecture Gate requires Archie + Wei debate before proceeding)
4. **Scoped** (e.g., Cam cannot write files; Pierrot cannot edit code)

Platforms that lack sub-agent isolation (Codex, Gemini, Cursor) need **degraded-mode** strategies.

---

## 5. The Abstraction Layer

### 5.1 Architecture: Three-Tier Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    METHODOLOGY LAYER (shared)                    │
│                                                                  │
│  docs/methodology/    docs/process/    docs/adrs/                │
│  phases.md            team-governance  template.md               │
│  personas.md          done-gate.md     0001-*.md                 │
│  agent-notes.md       gotchas.md                                 │
│                       tracking-protocol.md                       │
│                       operational-baseline.md                    │
│                                                                  │
│  ── Pure Markdown, zero platform dependencies ──                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PERSONA MANIFEST (new, shared)                 │
│                                                                  │
│  agents/                                                         │
│  ├── manifest.yaml          # All 19 agents: name, description,  │
│  │                          # capability profile, constraints    │
│  ├── sato.md                # Persona prose (platform-agnostic)  │
│  ├── tara.md                #   — behavioral instructions        │
│  ├── cam.md                 #   — thinking style, voice          │
│  ├── ...                    #   — no tool names, no frontmatter  │
│  └── _capabilities.yaml    # Abstract capability taxonomy        │
│                                                                  │
│  commands/                                                       │
│  ├── manifest.yaml          # All 27 commands: name, description,│
│  │                          # required agents, inputs, outputs   │
│  ├── tdd.md                 # Workflow prose (platform-agnostic) │
│  ├── kickoff.md             #   — steps, gates, checkpoints     │
│  └── ...                    #   — no $ARGUMENTS, no tool refs   │
│                                                                  │
│  ── Structured metadata + portable prose ──                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PLATFORM ADAPTERS (per-platform)                │
│                                                                  │
│  .claude/                   .github/                             │
│  ├── agents/*.md            ├── agents/*.agent.md                │
│  ├── commands/*.md          ├── prompts/*.prompt.md              │
│  └── (CLAUDE.md at root)    └── copilot-instructions.md          │
│                                                                  │
│  .codex/                    .gemini/                              │
│  ├── AGENTS.md              ├── GEMINI.md                        │
│  ├── config.toml            └── mcp-servers.json                 │
│  └── skills/                                                     │
│      └── */SKILL.md         .cursor/                             │
│                             └── rules/*.mdc                      │
│                                                                  │
│  ── Generated from Persona Manifest, platform-specific ──        │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 The Persona Manifest (`agents/manifest.yaml`)

This is the new single source of truth for _who the agents are_ and _what they can do_, expressed in platform-neutral terms:

```yaml
# agents/manifest.yaml
version: "1.0"

capabilities:
  read_files:       "Read file contents from the workspace"
  write_files:      "Create or overwrite files"
  edit_files:       "Make targeted edits to existing files"
  run_terminal:     "Execute shell commands"
  search_codebase:  "Search file contents (grep/ripgrep)"
  find_files:       "Find files by name/pattern (glob)"
  web_search:       "Search the internet"
  web_fetch:        "Fetch a URL"
  edit_notebooks:   "Edit Jupyter notebooks"

agents:
  sato:
    description: "Principal software engineer who writes production code"
    priority: P0
    capabilities: [read_files, write_files, edit_files, run_terminal, search_codebase, find_files, web_search, web_fetch]
    constraints: []
    model_preference: standard    # standard | fast | premium
    max_iterations: 50
    persona_file: sato.md

  tara:
    description: "Test-focused agent — writes failing tests (TDD red phase)"
    priority: P0
    capabilities: [read_files, write_files, edit_files, run_terminal, search_codebase, find_files]
    constraints: ["Must not write implementation code", "Veto power on test coverage"]
    model_preference: standard
    max_iterations: 30
    persona_file: tara.md

  cam:
    description: "Human interface agent — vision elicitation and review"
    priority: P0
    capabilities: [read_files, search_codebase, find_files, web_search, web_fetch]
    constraints: ["Must not write or edit files", "Must not execute commands"]
    model_preference: standard
    max_iterations: 20
    persona_file: cam.md

  pierrot:
    description: "Security and compliance — veto power"
    priority: P1
    capabilities: [read_files, run_terminal, search_codebase, find_files, web_search, web_fetch]
    constraints: ["Must not write or edit code files", "Veto power on security"]
    model_preference: standard
    max_iterations: 30
    persona_file: pierrot.md

  # ... remaining 15 agents follow same pattern
```

### 5.3 The Capability Mapping (`agents/_capabilities.yaml`)

Maps abstract capabilities to each platform's concrete tool names:

```yaml
# agents/_capabilities.yaml
version: "1.0"

platforms:
  claude-code:
    read_files: Read
    write_files: Write
    edit_files: Edit
    run_terminal: Bash
    search_codebase: Grep
    find_files: Glob
    web_search: WebSearch
    web_fetch: WebFetch
    edit_notebooks: NotebookEdit

  github-copilot:
    read_files: read
    write_files: editFiles
    edit_files: editFiles
    run_terminal: runInTerminal
    search_codebase: "search/codebase"
    find_files: "search/codebase"
    web_search: fetch
    web_fetch: fetch
    edit_notebooks: null  # Not supported

  codex-cli:
    # Codex uses global sandbox policies, not per-agent tools
    # Capabilities map to config.toml settings
    read_files: implicit
    write_files: "sandbox_mode: workspace-write"
    edit_files: "sandbox_mode: workspace-write"
    run_terminal: "shell_tool: true"
    search_codebase: implicit
    find_files: implicit
    web_search: "web_search: cached|live"
    web_fetch: "web_search: cached|live"
    edit_notebooks: implicit

  cursor:
    read_files: read_file
    write_files: create_file
    edit_files: edit_file
    run_terminal: run_command
    search_codebase: search
    find_files: list_dir
    web_search: null
    web_fetch: null
    edit_notebooks: null

  gemini-code-assist:
    # Gemini uses MCP for all tool access post-March 2026
    read_files: "mcp:file/read"
    write_files: "mcp:file/write"
    edit_files: "mcp:file/edit"
    run_terminal: "mcp:terminal/run"
    search_codebase: "mcp:search/code"
    find_files: "mcp:search/files"
    web_search: "mcp:web/search"
    web_fetch: "mcp:web/fetch"
    edit_notebooks: null
```

### 5.4 The Command Manifest (`commands/manifest.yaml`)

```yaml
# commands/manifest.yaml
version: "1.0"

commands:
  tdd:
    description: "Implement a feature using strict TDD"
    arguments:
      - name: feature
        description: "Feature to implement"
        required: true
    agents_required: [tara, sato]
    agents_optional: [vik, pierrot]
    workflow_file: tdd.md
    phase: implementation

  kickoff:
    description: "Full discovery workflow with board setup"
    arguments:
      - name: project_description
        description: "What to build"
        required: true
    agents_required: [cam, pat, archie, wei, grace]
    agents_optional: [dani, pierrot]
    workflow_file: kickoff.md
    phase: discovery

  code-review:
    description: "Multi-perspective code review"
    agents_required: [vik, tara, pierrot]
    agents_optional: [archie]
    workflow_file: code-review.md
    phase: review

  # ... remaining 24 commands
```

### 5.5 Degraded Mode for Limited Platforms

Platforms without sub-agent isolation (Codex, Gemini, Cursor) get **single-agent persona switching**:

```markdown
## Degraded Mode: Single-Agent Persona Rotation

When the platform cannot spawn isolated sub-agents:

1. **Persona Prefix:** Prepend the persona's behavioral instructions to each prompt turn.
2. **Tool Scoping:** Include explicit "you MUST NOT" instructions instead of technical tool blocking.
3. **Sequential Orchestration:** Run personas one at a time instead of in parallel.
4. **Gate Enforcement:** Use explicit checkpoints ("STOP. Switch to Tara persona before continuing.")

Example (Codex CLI with AGENTS.md):

```text
## Current Persona: Tara (Test Engineer)
You are Tara. You write failing tests ONLY. You must NOT write implementation code.
You must NOT execute code. Write the test file and STOP.

After tests are written, switch to:
## Current Persona: Sato (Implementation Engineer)
You are Sato. Make the failing tests pass. Do not modify test files.
```

**Fidelity loss is acceptable** — the methodology still works at ~80% effectiveness
in single-agent mode. The governance rules, phase gates, and checklists remain
fully enforced regardless of platform capability.
```

---

## 6. Platform Adapter Specifications

### 6.1 Claude Code Adapter (current — becomes "just another adapter")

**Input:** `agents/manifest.yaml` + `agents/*.md` + `commands/manifest.yaml` + `commands/*.md`  
**Output:** `.claude/agents/*.md`, `.claude/commands/*.md`, `CLAUDE.md`

Generation rules:
1. Read `agents/manifest.yaml` → for each agent, emit `.claude/agents/{name}.md` with:
   - YAML frontmatter: `name`, `description`, `tools` (mapped via `_capabilities.yaml` → `claude-code`), `model` (mapped from `model_preference`), `maxTurns`
   - `disallowedTools`: invert the capability list (full set minus agent's capabilities)
   - Body: contents of `agents/{persona_file}`
2. Read `commands/manifest.yaml` → for each command, emit `.claude/commands/{name}.md` with:
   - Agent-notes comment (from manifest metadata)
   - Body: contents of `commands/{workflow_file}`, with `{feature}` → `$ARGUMENTS` substitution
3. Generate `CLAUDE.md` from a template that references `docs/` methodology files

### 6.2 GitHub Copilot Adapter (primary conversion target)

**Input:** Same as above  
**Output:** `.github/agents/*.agent.md`, `.github/prompts/*.prompt.md`, `.github/copilot-instructions.md`

Generation rules:
1. Read `agents/manifest.yaml` → for each agent, emit `.github/agents/{name}.agent.md` with:
   - YAML frontmatter: `name`, `description`, `tools` (mapped via `_capabilities.yaml` → `github-copilot`)
   - No `maxTurns` (Copilot doesn't support it; omit or note in description)
   - No `disallowedTools` (Copilot uses allowlists)
   - Body: contents of `agents/{persona_file}`
2. Read `commands/manifest.yaml` → for each command, emit `.github/prompts/{name}.prompt.md` with:
   - YAML frontmatter: `mode: agent`, `description`, `tools` (union of all required agents' tools)
   - Body: contents of `commands/{workflow_file}`, adapted for Copilot prompt syntax
3. Generate `.github/copilot-instructions.md` from methodology template

### 6.3 Codex CLI Adapter

**Input:** Same as above  
**Output:** `AGENTS.md` (hierarchical), `.codex/config.toml`, optional `skills/` directories

Generation rules:
1. Generate root `AGENTS.md` combining:
   - Project context (from methodology docs)
   - Persona catalog (condensed from manifest — all 19 agents described in sections)
   - Phase model and governance rules (referenced or inlined)
   - Current-persona switching instructions
2. Generate `.codex/config.toml` with sandbox and tool policies
3. For complex commands, generate `skills/{command}/SKILL.md` directories

### 6.4 Gemini Code Assist Adapter

**Input:** Same as above  
**Output:** Context files, MCP server configurations

Generation rules:
1. Generate a comprehensive context document (methodology + personas + commands)
2. Generate MCP server configurations for tool access
3. Generate agentic-mode prompt templates for each workflow

### 6.5 Cursor Adapter

**Input:** Same as above  
**Output:** `.cursor/rules/*.mdc`

Generation rules:
1. For each agent, generate `.cursor/rules/{name}.mdc` with behavioral instructions and explicit constraints
2. Generate `.cursor/rules/_methodology.mdc` with phase model and governance
3. Generate `.cursor/rules/_project.mdc` with project context

---

## 7. The AGENTS.md Bridge

Given the industry convergence on AGENTS.md, vteam-hybrid should generate a root-level `AGENTS.md` regardless of primary platform. This serves as:

1. **Universal fallback** — any AI coding tool can read it
2. **Onboarding doc** — humans and agents alike get oriented
3. **Lowest common denominator** — project context without team orchestration

### Proposed AGENTS.md Structure

```markdown
# AGENTS.md — vteam-hybrid

## Project
[Generated from project context]

## Build & Test
[Generated from project toolchain]

## Conventions
[Generated from docs/team-directives.md]

## Architecture
[Generated from latest ADRs]

## Team Methodology
This project uses the vteam-hybrid methodology with 19 specialized AI personas.
For full details, see docs/methodology/phases.md and docs/methodology/personas.md.

## Boundaries
- Never skip tests (Tara has veto power)
- Never implement without an ADR for architectural decisions
- Always follow the Done Gate checklist (docs/process/done-gate.md)
```

**Relationship to platform-specific files:**
- `CLAUDE.md` → superset of `AGENTS.md` with Claude Code-specific agent spawning and tool syntax
- `copilot-instructions.md` → superset of `AGENTS.md` with Copilot agent references
- `AGENTS.md` → universal base that all platforms can read

---

## 8. Migration Strategy

### Phase 1: Extract (Create the Persona Manifest)

1. Create `agents/manifest.yaml` by extracting metadata from existing `.claude/agents/*.md` files
2. Create `agents/_capabilities.yaml` with the tool mapping tables
3. Create platform-agnostic `agents/*.md` persona prose files (strip YAML frontmatter from existing agent files)
4. Create `commands/manifest.yaml` by cataloging existing `.claude/commands/*.md` files
5. Create platform-agnostic `commands/*.md` workflow prose files (strip agent-notes headers, normalize `$ARGUMENTS` to `{argument_name}`)

**Validation:** Re-generate `.claude/agents/*.md` and `.claude/commands/*.md` from the manifest. Diff against originals. They should be functionally identical.

### Phase 2: Adapt (Build the Copilot Adapter)

1. Write the Copilot adapter generation logic (can be a script or a command)
2. Generate `.github/agents/*.agent.md` for all 19 agents
3. Generate `.github/prompts/*.prompt.md` for all 27 commands
4. Generate `.github/copilot-instructions.md`
5. Generate root `AGENTS.md`

**Validation:** Use Copilot in VS Code with the generated files. Verify that agents respond with correct personas and tool access.

### Phase 3: Test (Dual-Platform Verification)

1. Run the same workflow (e.g., `/tdd write-auth-service`) on both Claude Code and Copilot
2. Compare: persona accuracy, tool usage, governance compliance, output quality
3. Document fidelity gaps and degraded-mode behaviors
4. Iterate on persona prose and adapter logic

### Phase 4: Extend (Codex, Gemini, Cursor)

1. Write Codex CLI adapter (AGENTS.md + config.toml + skills)
2. Write Gemini adapter (context files + MCP)
3. Write Cursor adapter (rules files)
4. Each adapter follows the same pattern: read manifest → emit platform files

### Phase 5: Automate (Generator Command/Script)

1. Create a `/generate-platform` command (or `scripts/generate-platform.sh`) that:
   - Reads the persona and command manifests
   - Accepts a `--platform` flag (`claude-code`, `github-copilot`, `codex-cli`, `gemini`, `cursor`, `all`)
   - Emits the correct files for the specified platform
2. Wire this into CI so platform files stay in sync with manifest changes
3. Replace the existing `/sync-ghcp` command with this generalized generator

---

## 9. Future-Proofing Principles

### 9.1 Methodology Over Mechanism

The methodology docs (`docs/methodology/`, `docs/process/`) must never reference platform-specific tool names, file paths, or invocation syntax. They describe _what_ and _why_, never _how_ at the platform level.

**Test:** Can you read `docs/methodology/phases.md` and understand the methodology without knowing what Claude Code, Copilot, or Codex are? If yes, it's properly abstracted.

### 9.2 Manifest Is Source of Truth

No platform-specific file should be hand-edited. All `.claude/`, `.github/`, `.codex/`, `.cursor/`, `.gemini/` files are **generated artifacts**. Changes flow:

```
agents/manifest.yaml  ──→  generate  ──→  .claude/agents/*.md
agents/sato.md         ──→  generate  ──→  .github/agents/sato.agent.md
commands/manifest.yaml ──→  generate  ──→  .codex/skills/tdd/SKILL.md
```

If someone edits a generated file directly, the next generation run overwrites it. This is intentional — it prevents drift.

### 9.3 Capability Profiles, Not Tool Lists

Agent definitions should express _what an agent can conceptually do_ (read code, execute commands, search the web), not _which platform tools they use_. The mapping layer handles translation.

This means when a platform adds a new tool (e.g., Copilot adds `notebookEdit`), you update `_capabilities.yaml` once, re-generate, and every agent that needs notebook access gets it.

### 9.4 Graceful Degradation Over Feature Parity

Not every platform supports every capability. The system should degrade gracefully:

| Missing Capability | Degradation Strategy |
|---|---|
| No sub-agent isolation | Single-agent persona rotation with explicit constraints |
| No parallel agents | Sequential execution with context passing |
| No tool permission boundaries | Prose-based "MUST NOT" instructions |
| No custom commands | Inline workflow instructions in agent prompts |
| No web search | Skip research steps; note limitation |
| No model selection | Use platform default; note in generated file |

### 9.5 The 30-Minute Adapter Test

A new platform adapter should be writable in 30 minutes by someone who:
1. Knows the target platform's configuration format
2. Has read `agents/manifest.yaml` and `_capabilities.yaml`
3. Can write a simple template-based generator

If it takes longer, the abstraction layer is leaking platform concerns upward.

### 9.6 Version the Manifest Schema

The manifest files (`manifest.yaml`, `_capabilities.yaml`) should have a `version` field. When the schema evolves:
1. Bump the version
2. Write a migration script (old schema → new schema)
3. All adapters check the version and fail-fast if they don't support it

### 9.7 MCP as Universal Tool Bridge

The Model Context Protocol (MCP) is becoming the de facto standard for tool integration across AI coding agents. Long-term, the capability mapping may converge to MCP server URIs rather than platform-specific tool names:

```yaml
# Future state: all capabilities map to MCP
capabilities:
  read_files: "mcp:filesystem/read"
  write_files: "mcp:filesystem/write"
  run_terminal: "mcp:terminal/execute"
  search_codebase: "mcp:search/code"
  web_search: "mcp:web/search"
```

When all platforms support MCP natively, the per-platform tool mapping becomes unnecessary — everything routes through MCP servers.

---

## 10. Risk Analysis

### High Risk

| Risk | Impact | Mitigation |
|---|---|---|
| Platform format changes break adapters | Generated files become invalid | `/sync-ghcp` precedent: use runtime research, not static assumptions. Adapter validates output against platform spec. |
| Manifest complexity grows unmanageable | Editing 19 agents in YAML becomes tedious | Keep manifest minimal (metadata only). Prose stays in separate `.md` files. Tooling validates manifest. |
| Claude Code loses parity with generated files | Team works on Claude Code but generated Copilot files drift | CI check: `generate --platform all && git diff --exit-code` — fail if generated files are stale |

### Medium Risk

| Risk | Impact | Mitigation |
|---|---|---|
| Persona fidelity loss on limited platforms | Agents behave generically instead of in-character | Invest in persona prose quality. Run comparison tests. Accept ~80% fidelity on limited platforms. |
| AGENTS.md standard evolves incompatibly | Generated AGENTS.md becomes non-compliant | Pin to AAIF spec version. Monitor spec changes. |
| Tracking adapters multiply maintenance burden | N platforms × M trackers = N×M combinations | Tracking is already abstracted; keep it that way. Board adapter is independent of platform adapter. |

### Low Risk

| Risk | Impact | Mitigation |
|---|---|---|
| New platform emerges | Need yet another adapter | 30-minute adapter test ensures this is cheap |
| MCP standardizes everything | Capability mapping becomes unnecessary | This is the _desired_ outcome — less maintenance |

---

## 11. Open Questions

1. **Where does the manifest live?** Options:
   - [x] `agents/` at repo root (clean, visible, tool-agnostic)
   - `docs/platform/` (groups with methodology docs)
   - `.vteam/` (hidden, keeps root clean)

2. **Script or command for generation?** Options:
   - `scripts/generate-platform.sh` (portable, no AI needed)
   - [x] `/generate-platform` command (AI-assisted, can web-search for format updates — like current `/sync-ghcp`)
   - Both (script for CI, command for interactive use)

3. **Should generated files be committed?** Options:
   - [x] Yes: users on each platform see their files without running a generator
   - No: reduces repo clutter, ensures freshness
   - Recommended: **Yes, with CI staleness check**

4. **How to handle platform-specific features that have no manifest equivalent?** Examples:
   - Copilot's `mcp-servers` field
   - Codex's `approval_policy` setting
   - Claude Code's `maxTurns`
   - [x] Answer: platform-specific overrides file (`adapters/{platform}/overrides.yaml`)

5. **What's the MVP?** For a first release, ship:
   - [x] Persona manifest + capability mapping
   - [x] Claude Code adapter (proving the manifest reproduces current state)
   - [x] Copilot adapter (primary conversion target)
   - [x] Root AGENTS.md generation
   - [x] Skip Codex/Gemini/Cursor until demand exists

---

## Appendix A: Existing Prior Art in This Repo

- **`/sync-ghcp` command** (`.claude/commands/sync-ghcp.md`): One-way Claude→Copilot sync. Uses runtime web research for format freshness. This becomes the template for the Copilot adapter, but the new system replaces its source of truth (manifest instead of `.claude/agents/`).
- **`docs/research/squad-vs-vteam-architectural-comparison.md`**: Compares vteam-hybrid with Squad (another multi-agent system for Copilot). Relevant insights on Copilot's agent capabilities and limitations.
- **Tracking adapter pattern** (`docs/integrations/`): Already demonstrates the adapter pattern for board integrations. The platform adapter follows the same philosophy.

## Appendix B: File Tree After Full Conversion

```
.
├── AGENTS.md                          # Universal cross-platform (generated)
├── CLAUDE.md                          # Claude Code instructions (generated)
├── agents/                            # 🆕 Source of truth
│   ├── manifest.yaml                  # All 19 agents: metadata + capabilities
│   ├── _capabilities.yaml             # Abstract → platform tool mapping
│   ├── sato.md                        # Persona prose (platform-agnostic)
│   ├── tara.md
│   ├── cam.md
│   ├── ... (16 more)
│   └── README.md                      # How to add/modify agents
├── commands/                          # 🆕 Source of truth
│   ├── manifest.yaml                  # All 27 commands: metadata
│   ├── tdd.md                         # Workflow prose (platform-agnostic)
│   ├── kickoff.md
│   ├── ... (25 more)
│   └── README.md                      # How to add/modify commands
├── adapters/                          # 🆕 Platform-specific overrides
│   ├── claude-code/
│   │   └── overrides.yaml
│   ├── github-copilot/
│   │   └── overrides.yaml
│   ├── codex-cli/
│   │   └── overrides.yaml
│   └── README.md
├── .claude/                           # Generated for Claude Code
│   ├── agents/*.md
│   └── commands/*.md
├── .github/                           # Generated for GitHub Copilot
│   ├── agents/*.agent.md
│   ├── prompts/*.prompt.md
│   └── copilot-instructions.md
├── docs/                              # Shared methodology (unchanged)
│   ├── methodology/
│   ├── process/
│   ├── adrs/
│   ├── integrations/
│   └── research/
└── scripts/
    └── generate-platform.sh           # 🆕 Adapter generator
```
