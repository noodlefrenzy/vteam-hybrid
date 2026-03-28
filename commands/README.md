# agent-notes: { ctx: "how to add or modify commands in the manifest", deps: [commands/manifest.yaml], state: active, last: "copilot-cli@2026-03-22" }

# Commands — Platform-Agnostic Workflow Definitions

This directory is the **source of truth** for all vteam-hybrid commands/workflows.

## Structure

```
commands/
├── manifest.yaml          # All 25 commands: metadata, agents, phases
├── README.md              # This file
├── tdd.md                 # Platform-agnostic workflow prose
├── kickoff.md
└── ... (25 total)
```

## How It Works

1. **`manifest.yaml`** defines each command's metadata (description, arguments, required/optional agents, phase).
2. **`*.md` files** contain the workflow prose — steps, gates, checkpoints — using `{arguments}` as a platform-agnostic parameter placeholder.

Platform-specific files (`.claude/commands/`, `.github/prompts/`) are **generated** from these sources by `scripts/generate-platform.py`.

## Parameter Substitution

| Source (here) | Claude Code | GitHub Copilot |
|---|---|---|
| `{arguments}` | `$ARGUMENTS` | `$PROMPT_INPUT` |

## Adding a New Command

1. Add the command entry to `manifest.yaml`.
2. Create a `{name}.md` file with the workflow prose using `{arguments}` for parameters.
3. Run `python3 scripts/generate-platform.py all`.
4. Commit both source and generated files.

## Modifying an Existing Command

1. Edit `manifest.yaml` (for metadata) or the `*.md` file (for workflow changes).
2. Run `python3 scripts/generate-platform.py all`.
3. Commit both source and generated files.
