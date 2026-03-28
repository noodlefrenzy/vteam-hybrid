# agent-notes: { ctx: "how to add or modify agents in the manifest", deps: [agents/manifest.yaml, agents/_capabilities.yaml], state: active, last: "copilot-cli@2026-03-22" }

# Agents — Platform-Agnostic Persona Definitions

This directory is the **source of truth** for all vteam-hybrid agent personas.

## Structure

```
agents/
├── manifest.yaml        # All 19 agents: metadata, capabilities, constraints
├── _capabilities.yaml   # Abstract capability → platform tool name mapping
├── README.md            # This file
├── sato.md              # Platform-agnostic persona prose
├── tara.md
├── cam.md
└── ... (19 total)
```

## How It Works

1. **`manifest.yaml`** defines each agent's metadata (description, priority, abstract capabilities, constraints, model preference).
2. **`_capabilities.yaml`** maps abstract capabilities (e.g., `read_files`) to platform-specific tool names (e.g., `Read` for Claude Code, `read` for Copilot).
3. **`*.md` files** contain the persona prose — behavioral instructions, thinking style, voice — with zero platform-specific references.

Platform-specific files (`.claude/agents/`, `.github/agents/`) are **generated** from these sources by `scripts/generate-platform.py`.

## Adding a New Agent

1. Add the agent entry to `manifest.yaml` with all required fields.
2. Create a `{name}.md` file with the persona prose.
3. Run `python3 scripts/generate-platform.py all` to generate platform files.
4. Commit both the source files and generated output.

## Modifying an Existing Agent

1. Edit `manifest.yaml` (for metadata changes) or the `*.md` file (for behavior changes).
2. Run `python3 scripts/generate-platform.py all` to regenerate.
3. Commit both source and generated files.

## Adding a New Platform

1. Add a new platform section to `_capabilities.yaml` with tool name mappings.
2. Add a generation function to `scripts/generate-platform.py`.
3. Run and verify.
