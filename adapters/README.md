# agent-notes: { ctx: "adapter directory overview", deps: [agents/manifest.yaml, agents/_capabilities.yaml], state: active, last: "copilot-cli@2026-03-22" }

# Platform Adapters

This directory contains platform-specific overrides and notes for each supported AI coding platform.

## Structure

```
adapters/
├── claude-code/
│   └── overrides.yaml    # Claude Code-specific generation notes
├── github-copilot/
│   └── overrides.yaml    # Copilot-specific generation notes
└── README.md             # This file
```

## How Adapters Work

The generation script (`scripts/generate-platform.py`) reads:
1. `agents/manifest.yaml` — agent metadata (source of truth)
2. `agents/_capabilities.yaml` — capability-to-tool mapping per platform
3. `agents/*.md` — persona prose (platform-agnostic)
4. `commands/manifest.yaml` — command metadata
5. `commands/*.md` — workflow prose (platform-agnostic)
6. `adapters/{platform}/overrides.yaml` — platform-specific overrides (optional)

And generates platform-specific files:
- `.claude/agents/*.md` + `.claude/commands/*.md` for Claude Code
- `.github/agents/*.agent.md` + `.github/prompts/*.prompt.md` + `.github/copilot-instructions.md` for Copilot
- `AGENTS.md` for universal cross-platform use

## Adding a New Platform

1. Create `adapters/{platform}/overrides.yaml` with platform notes
2. Add tool mappings to `agents/_capabilities.yaml`
3. Add a generation function to `scripts/generate-platform.py`
4. Run and verify
