---
agent-notes: { ctx: "WezTerm + tmux setup guide for devcontainer workflow", deps: [docs/guides/agent-teams-setup.md, .devcontainer/devcontainer.json], state: active, last: "diego@2026-02-22" }
---

# WezTerm + tmux Setup for Devcontainers

A guide to setting up WezTerm on Windows with a great tmux experience inside devcontainers on WSL2. Covers fonts, colors, true color passthrough, and the keybindings that make tmux comfortable.

## 1. Install WezTerm

Download from [wezfurlong.org/wezterm](https://wezfurlong.org/wezterm/installation.html) or:

```powershell
winget install wez.wezterm
```

## 2. Install a Nerd Font

Nerd Fonts patch developer fonts with icons used by tmux status bars, `lsd`, `starship`, and other CLI tools. Pick one:

| Font | Style | Get it |
|------|-------|--------|
| **JetBrains Mono** | Clean, purpose-built for code | [nerdfonts.com](https://www.nerdfonts.com/font-downloads) → "JetBrainsMono Nerd Font" |
| **FiraCode** | Ligatures (arrows, comparisons) | [nerdfonts.com](https://www.nerdfonts.com/font-downloads) → "FiraCode Nerd Font" |
| **CaskaydiaCove** | Microsoft's Cascadia Code + nerd glyphs | [nerdfonts.com](https://www.nerdfonts.com/font-downloads) → "CaskaydiaCove Nerd Font" |

Install on Windows: download the zip, extract, select all `.ttf` files, right-click → **Install for all users**.

Or via scoop:

```powershell
scoop bucket add nerd-fonts
scoop install nerd-fonts/JetBrainsMono-NF
```

## 3. WezTerm Config

WezTerm uses a Lua config file. Create `%USERPROFILE%\.wezterm.lua` (e.g. `C:\Users\YourName\.wezterm.lua`):

```lua
local wezterm = require("wezterm")
local config = wezterm.config_builder()

-- === Font ===
config.font = wezterm.font("JetBrainsMono Nerd Font")
config.font_size = 12.0
-- If you picked FiraCode and want ligatures:
-- config.font = wezterm.font("FiraCode Nerd Font")
-- config.harfbuzz_features = { "calt=1", "liga=1" }

-- === Color scheme ===
-- WezTerm ships with 700+ schemes. Some good ones for long coding sessions:
config.color_scheme = "Catppuccin Mocha"  -- warm, easy on the eyes
-- Alternatives worth trying:
-- config.color_scheme = "Tokyo Night"
-- config.color_scheme = "Kanagawa (Gogh)"
-- config.color_scheme = "Dracula (Official)"
-- config.color_scheme = "rose-pine"
-- Browse all: wezfurlong.org/wezterm/colorschemes

-- === Window ===
config.window_padding = { left = 4, right = 4, top = 4, bottom = 4 }
config.window_decorations = "RESIZE"  -- minimal chrome, no title bar
config.initial_cols = 200
config.initial_rows = 50

-- === Cursor ===
config.default_cursor_style = "BlinkingBar"
config.cursor_blink_rate = 500

-- === Tab bar ===
-- Disable WezTerm's tab bar — tmux handles multiplexing
config.enable_tab_bar = false

-- === Scrollback ===
config.scrollback_lines = 10000
-- Scroll through output even when an interactive app is running:
config.enable_scroll_bar = true

-- === WSL default domain ===
-- Launch directly into WSL instead of PowerShell
config.default_domain = "WSL:Ubuntu"
-- If your distro has a different name, check: wsl --list
-- config.default_domain = "WSL:Ubuntu-22.04"

-- === True color & undercurl ===
-- These ensure colors pass through correctly to tmux and apps inside it
config.term = "wezterm"

-- === Keys ===
-- Don't let WezTerm eat keys that tmux needs
config.disable_default_key_bindings = false
config.keys = {
  -- Ctrl+Shift+H: open scrollback in pager (useful when tmux copy mode isn't enough)
  { key = "H", mods = "CTRL|SHIFT", action = wezterm.action.ShowDebugOverlay },

  -- Quick font size (Ctrl+= / Ctrl+-)
  { key = "=", mods = "CTRL", action = wezterm.action.IncreaseFontSize },
  { key = "-", mods = "CTRL", action = wezterm.action.DecreaseFontSize },
  { key = "0", mods = "CTRL", action = wezterm.action.ResetFontSize },
}

return config
```

After saving, WezTerm hot-reloads — you'll see changes immediately.

### Browsing color schemes

WezTerm has a built-in scheme browser. Press `Ctrl+Shift+P` to open the command palette, then type "color" to find **"Pick Color Scheme"**. Preview schemes live before committing.

## 4. tmux Config

Create `~/.tmux.conf` inside your WSL distro (this will be available in devcontainers if you mount your home or copy it in):

```bash
# === True color support ===
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",wezterm:RGB"
set -ag terminal-overrides ",xterm-256color:RGB"

# === General ===
set -g mouse on                    # scroll, click panes, resize with mouse
set -g history-limit 50000         # generous scrollback
set -g base-index 1                # windows start at 1, not 0
setw -g pane-base-index 1          # panes too
set -g renumber-windows on         # fill gaps when closing windows
set -sg escape-time 10             # faster key response (important for vim/neovim)
set -g focus-events on             # let apps know when pane gets focus

# === Status bar ===
set -g status-position top
set -g status-style "bg=#1e1e2e,fg=#cdd6f4"  # Catppuccin Mocha colors
set -g status-left-length 40
set -g status-right-length 60

# Left: session name
set -g status-left "#[fg=#a6e3a1,bold] #S #[default] "

# Right: host + time
set -g status-right "#[fg=#89b4fa]#H #[fg=#6c7086]│ #[fg=#f9e2af]%H:%M "

# Window tabs
set -g window-status-format " #[fg=#6c7086]#I:#W "
set -g window-status-current-format " #[fg=#cba6f7,bold]#I:#W "
set -g window-status-separator ""

# Pane borders
set -g pane-border-style "fg=#313244"
set -g pane-active-border-style "fg=#cba6f7"

# === Pane navigation (Alt+arrow, no prefix needed) ===
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# === Better split keys ===
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# === Reload config ===
bind r source-file ~/.tmux.conf \; display "Config reloaded"
```

Apply without restarting:

```bash
tmux source-file ~/.tmux.conf
```

### Matching tmux colors to your WezTerm scheme

The tmux config above uses Catppuccin Mocha hex values. If you pick a different WezTerm color scheme, update the status bar colors to match. The key values to change:

| Variable | Catppuccin Mocha | What it colors |
|----------|-----------------|----------------|
| Status bg | `#1e1e2e` | Status bar background |
| Status fg | `#cdd6f4` | Default status text |
| Green | `#a6e3a1` | Session name |
| Blue | `#89b4fa` | Hostname |
| Yellow | `#f9e2af` | Clock |
| Mauve | `#cba6f7` | Active window/pane border |
| Surface0 | `#313244` | Inactive pane border |
| Overlay0 | `#6c7086` | Inactive window text |

## 5. Get tmux Config Into Devcontainers

The devcontainer doesn't automatically see your WSL home directory. A few options:

**Option A: Mount it (simplest)**

Add to `.devcontainer/devcontainer.json`:

```json
"mounts": [
  "source=${localEnv:HOME}/.tmux.conf,target=/root/.tmux.conf,type=bind,readonly"
]
```

**Option B: Copy in post-create**

Add to `.devcontainer/post-create.sh`:

```bash
# Copy tmux config if available on host
[ -f "/root/.tmux.conf" ] || cat > /root/.tmux.conf << 'TMUX'
# ... paste your tmux.conf contents here ...
TMUX
```

**Option C: Dotfiles repo**

WezTerm config + tmux config + shell config in a git repo. Point your devcontainer at it:

```json
"settings": {
  "dotfiles.repository": "https://github.com/YOU/dotfiles",
  "dotfiles.installCommand": "install.sh"
}
```

This is the most portable option — works in Codespaces too.

## 6. The Full Chain

Here's what the color/font pipeline looks like end-to-end:

```
WezTerm (Windows)
  └─ font: JetBrainsMono Nerd Font (rendered on Windows)
  └─ colors: Catppuccin Mocha (256 + true color)
  └─ TERM=wezterm
  │
  └─► WSL2 (Ubuntu)
        └─ tmux
        │    └─ TERM=tmux-256color
        │    └─ terminal-overrides for RGB passthrough
        │    └─ status bar with matching Catppuccin colors
        │
        └─► Devcontainer (Docker)
              └─ inherits tmux session (if mounted/copied .tmux.conf)
              └─ Claude Code → Agent Teams split panes
```

True color works through the full chain because:
1. WezTerm supports true color natively
2. `set -ag terminal-overrides ",wezterm:RGB"` tells tmux to pass true color through
3. The devcontainer shell inherits the tmux session's terminal capabilities

## 7. Verify Everything Works

Inside tmux (in WSL or the devcontainer):

```bash
# True color test — should show a smooth gradient, not banding
curl -s https://raw.githubusercontent.com/gnachman/iTerm2/master/tests/24-bit-color.sh | bash

# Or a quick inline test — should show actual red/green/blue, not approximations
printf "\x1b[38;2;255;0;0mRED\x1b[0m \x1b[38;2;0;255;0mGREEN\x1b[0m \x1b[38;2;0;0;255mBLUE\x1b[0m\n"

# Nerd font icons — should show icons, not boxes
echo -e "\uf121 code  \uf419 git  \ue711 node  \ue73c python  \ue7a8 rust"

# tmux color count
tmux display -p "#{client_termfeatures}"
# Should include: 256,RGB
```

## Troubleshooting

**Colors look washed out or wrong in tmux**
Check that `TERM` is set correctly. Inside tmux: `echo $TERM` should show `tmux-256color`, not `screen` or `screen-256color`. If tmux-256color isn't available, install the terminfo: `sudo apt install ncurses-term`.

**Nerd font icons show as boxes**
WezTerm isn't using the Nerd Font. Check that the font name in `.wezterm.lua` exactly matches what's installed. Open WezTerm's debug overlay (`Ctrl+Shift+L`) and check the font log.

**Mouse scroll doesn't work in tmux**
Make sure `set -g mouse on` is in your `.tmux.conf`. If you're inside a devcontainer, verify the config was mounted/copied correctly.

**Pane borders look like `q` characters instead of lines**
The terminal is falling back to ASCII line-drawing. This usually means the locale is wrong. Inside the container: `export LANG=en_US.UTF-8` and ensure `locales` is installed.

**WezTerm opens PowerShell instead of WSL**
Check that `config.default_domain = "WSL:Ubuntu"` is set and matches your distro name. Run `wsl --list` in PowerShell to see exact names.

**Slow key response / ESC delay**
The `escape-time 10` setting in tmux helps, but if you still see lag, try `set -sg escape-time 0`. Some vim/neovim plugins may conflict — test without them first.
