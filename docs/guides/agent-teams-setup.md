---
agent-notes: { ctx: "practical setup guide for Agent Teams in devcontainer", deps: [.devcontainer/devcontainer.json, .devcontainer/post-create.sh, docs/methodology/agent-teams-runtime.md], state: active, last: "diego@2026-02-22" }
---

# Getting Agent Teams Running in a Devcontainer

Agent Teams needs tmux for split-pane teammates. VS Code's integrated terminal doesn't handle tmux well — you'll want a proper terminal connected to the devcontainer instead. This guide covers the full setup.

## Prerequisites

- Docker Desktop (or Podman/Orbstack) running
- [Dev Container CLI](https://github.com/devcontainers/cli) installed: `npm install -g @devcontainers/cli`
- An `ANTHROPIC_API_KEY` environment variable (or you'll authenticate interactively inside the container)

## Option A: Dev Container CLI (Recommended)

The fastest path. No VS Code involved.

### 1. Build and start the container

```bash
devcontainer up --workspace-folder .
```

This builds the image, runs `post-create.sh` (installs tmux + Claude Code), and leaves the container running.

### 2. Connect with a proper terminal

```bash
devcontainer exec --workspace-folder . bash
```

You're now in a shell inside the container, at the project root, with your full terminal emulator (iTerm2, Windows Terminal, Alacritty, whatever you launched from).

### 3. Start tmux

```bash
tmux
```

Agent Teams detects the tmux session and spawns teammates as split panes automatically.

### 4. Launch Claude Code

```bash
claude --model opus
```

**Important:** Always use `--model opus`. Teammates do not inherit the lead's model — without this flag they may use a different (weaker) model. See `docs/methodology/agent-teams-runtime.md` § Known Issues.

You're ready. When Claude Code spawns teammates, they'll appear as tmux splits in your terminal.

## Option B: Docker Compose (For Persistent Environments)

If you want the container to survive restarts or share it across sessions.

### 1. Create a `docker-compose.yml` (if you don't have one)

```yaml
services:
  dev:
    build:
      context: .
      dockerfile: .devcontainer/Dockerfile
    # Or use the image directly:
    # image: mcr.microsoft.com/devcontainers/base:ubuntu-22.04
    volumes:
      - .:/workspaces/project:cached
    environment:
      - CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    command: sleep infinity
```

### 2. Start and attach

```bash
docker compose up -d
docker compose exec dev bash
```

Then `tmux` + `claude --model opus` as in Option A steps 3-4.

### 3. Clean up

```bash
docker compose down
```

## Option C: GitHub Codespaces

For cloud-hosted development — no local Docker needed.

### 1. Create the Codespace

From the repo on GitHub: **Code > Codespaces > Create codespace on feature/agent-teams**.

Or via CLI:

```bash
gh codespace create --repo OWNER/REPO --branch feature/agent-teams
```

### 2. SSH into the Codespace (skip the browser terminal)

```bash
gh codespace ssh
```

This gives you a proper terminal connection. The browser-based terminal works but has the same tmux limitations as VS Code's.

### 3. Start tmux and Claude Code

```bash
tmux
claude --model opus
```

The devcontainer's `postCreateCommand` already installed tmux and Claude Code.

### 4. Stop when done

```bash
gh codespace stop
```

## Passing Your API Key

The container needs `ANTHROPIC_API_KEY` to run Claude Code. Several options:

**Environment variable (simplest):** Export it in your host shell before `devcontainer up`:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
devcontainer up --workspace-folder .
devcontainer exec --workspace-folder . bash
```

The dev container CLI forwards your environment automatically.

**Docker secret / compose env file:** For docker compose, use an `.env` file (already in `.gitignore`):

```
ANTHROPIC_API_KEY=sk-ant-...
```

**Codespaces secrets:** Go to GitHub **Settings > Codespaces > Secrets** and add `ANTHROPIC_API_KEY`. It's injected automatically into every Codespace.

**Interactive auth:** If no key is set, `claude` will prompt you to authenticate on first run.

## Verifying the Setup

Once you're in a tmux session inside the container:

```bash
# Confirm tmux is running
tmux list-sessions
# Should show your active session

# Confirm Claude Code is installed
claude --version

# Confirm Agent Teams is enabled
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
# Should print: 1

# Confirm hooks are executable
ls -la .claude/hooks/
# Should show done-gate.sh and teammate-idle.sh with +x

# Quick hook smoke test
echo '{}' | .claude/hooks/done-gate.sh
# Should print "All checks passed" (no tooling detected in template state)
```

## tmux Basics for Agent Teams

If you're new to tmux, here's enough to work with Agent Teams. All shortcuts start with `Ctrl-b` (the prefix key).

| Action | Keys |
|--------|------|
| Switch between panes | `Ctrl-b` then arrow keys |
| Zoom a pane (fullscreen toggle) | `Ctrl-b z` |
| Scroll up in a pane | `Ctrl-b [` then arrow/PgUp (press `q` to exit) |
| Kill a pane | `Ctrl-b x` then confirm `y` |
| Detach from session (keeps running) | `Ctrl-b d` |
| Reattach | `tmux attach` |
| List sessions | `tmux ls` |

When Agent Teams spawns teammates, new panes appear automatically. You don't need to create them manually. Use arrow-key switching to watch different teammates work.

## Troubleshooting

**"no server running on /tmp/tmux-..."**
You're not in a tmux session. Run `tmux` first, then `claude --model opus`.

**Teammates don't appear as split panes**
Agent Teams falls back to in-process mode if tmux isn't detected. Make sure you started `claude` from *inside* a tmux session, not from a bare shell.

**Teammates use a weaker model**
Teammates don't inherit `--model`. Always launch with `claude --model opus`.

**"permission denied" on hooks**
Run `chmod +x .claude/hooks/*.sh` — the post-create script does this, but if you rebuilt the container without running it, the executable bits may be missing.

**VS Code terminal issues with tmux**
This is a known limitation of VS Code's terminal emulator. It doesn't properly handle tmux's escape sequences, leading to rendering glitches, broken splits, and input issues. Use one of the options above instead. If you must use VS Code, open an external terminal (`Terminal > Run Active File in External Terminal` or just open iTerm2/Windows Terminal separately).

**Container doesn't have Claude Code**
The `postCreateCommand` may have failed silently. Run manually:
```bash
npm install -g @anthropic-ai/claude-code
```

## What's Next

Once you're running, see `docs/methodology/agent-teams-runtime.md` for:
- Which phases use Agent Teams vs. subagents
- How to use the spawn prompt templates
- What the governance hooks enforce
- Known issues and workarounds
- How to disable Agent Teams per-user or per-session
