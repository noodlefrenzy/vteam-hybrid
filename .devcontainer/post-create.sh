#!/usr/bin/env bash
# agent-notes: { ctx: "devcontainer post-create setup for Agent Teams", deps: [.devcontainer/devcontainer.json], state: active, last: "sato@2026-02-22" }
set -euo pipefail

# Install tmux (required for Agent Teams split panes)
sudo apt-get update && sudo apt-get install -y tmux

# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Make hooks executable
chmod +x .claude/hooks/*.sh 2>/dev/null || true

# Install project dependencies if detected
if [ -f "package.json" ]; then
  npm install
elif [ -f "pyproject.toml" ]; then
  pip install -e ".[dev]" 2>/dev/null || true
fi

echo "Post-create setup complete. tmux and Claude Code installed."
