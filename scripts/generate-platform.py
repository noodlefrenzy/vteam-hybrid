#!/usr/bin/env python3
# agent-notes: { ctx: "multi-platform file generator from manifests", deps: [agents/manifest.yaml, agents/_capabilities.yaml, commands/manifest.yaml], state: active, last: "copilot-cli@2026-03-22" }
"""
generate-platform.py — Generate platform-specific files from vteam-hybrid manifests.

Modes:
  extract   Extract persona/command prose from .claude/ into agents/ and commands/
  copilot   Generate GitHub Copilot adapter files in .github/
  agents-md Generate root AGENTS.md cross-platform bridge
  all       Do everything (for initial migration)

Usage:
  python3 scripts/generate-platform.py all
  python3 scripts/generate-platform.py extract
  python3 scripts/generate-platform.py copilot
  python3 scripts/generate-platform.py agents-md
"""

import os
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def read_file(path):
    with open(path) as f:
        return f.read()

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  {'created' if not path.exists() else 'wrote'}: {path.relative_to(ROOT)}")

# ---------------------------------------------------------------------------
# EXTRACT: .claude/agents/*.md → agents/*.md (strip YAML frontmatter)
# ---------------------------------------------------------------------------
def extract_persona_prose():
    """Extract platform-agnostic persona prose from Claude Code agent files."""
    src_dir = ROOT / ".claude" / "agents"
    dst_dir = ROOT / "agents"
    count = 0
    for src in sorted(src_dir.glob("*.md")):
        content = read_file(src)
        # Strip YAML frontmatter (everything between first --- and second ---)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                body = parts[2].lstrip("\n")
            else:
                body = content
        else:
            body = content
        dst = dst_dir / src.name
        write_file(dst, body)
        count += 1
    print(f"  Extracted {count} persona prose files to agents/")

# ---------------------------------------------------------------------------
# EXTRACT: .claude/commands/*.md → commands/*.md (normalize $ARGUMENTS)
# ---------------------------------------------------------------------------
def extract_command_prose():
    """Extract platform-agnostic command prose from Claude Code command files."""
    src_dir = ROOT / ".claude" / "commands"
    dst_dir = ROOT / "commands"
    skip = {"sync-ghcp.md", "sync-template.md"}  # deleted
    count = 0
    for src in sorted(src_dir.glob("*.md")):
        if src.name in skip:
            continue
        content = read_file(src)
        # Replace $ARGUMENTS with {arguments} for platform-agnostic form
        body = content.replace("$ARGUMENTS", "{arguments}")
        dst = dst_dir / src.name
        write_file(dst, body)
        count += 1
    print(f"  Extracted {count} command prose files to commands/")

# ---------------------------------------------------------------------------
# COPILOT: Generate .github/agents/*.agent.md
# ---------------------------------------------------------------------------
def generate_copilot_agents():
    """Generate GitHub Copilot agent files from manifest + persona prose."""
    manifest = load_yaml(ROOT / "agents" / "manifest.yaml")
    caps = load_yaml(ROOT / "agents" / "_capabilities.yaml")
    copilot_tools = caps["platforms"]["github-copilot"]["tool_names"]

    agents_dir = ROOT / ".github" / "agents"
    count = 0

    for name, agent in manifest["agents"].items():
        # Map capabilities to Copilot tool names (deduplicated, nulls removed)
        tools = []
        seen = set()
        for cap in agent["capabilities"]:
            tool = copilot_tools.get(cap)
            if tool and tool not in seen:
                tools.append(tool)
                seen.add(tool)

        # Build YAML frontmatter
        desc = agent["description"].strip().replace("\n", " ")
        # Collapse multiple spaces
        desc = re.sub(r"\s+", " ", desc)
        frontmatter = f"---\nname: {name}\ndescription: >\n  {desc}\ntools:\n"
        for t in tools:
            frontmatter += f"  - {t}\n"
        frontmatter += "---\n\n"

        # Read persona prose
        prose_file = ROOT / "agents" / agent["persona_file"]
        if prose_file.exists():
            prose = read_file(prose_file)
        else:
            prose = f"# {name}\n\nPersona prose not yet extracted.\n"

        dst = agents_dir / f"{name}.agent.md"
        write_file(dst, frontmatter + prose)
        count += 1

    print(f"  Generated {count} Copilot agent files in .github/agents/")

# ---------------------------------------------------------------------------
# COPILOT: Generate .github/prompts/*.prompt.md
# ---------------------------------------------------------------------------
def generate_copilot_prompts():
    """Generate GitHub Copilot prompt files from command manifest + prose."""
    manifest = load_yaml(ROOT / "commands" / "manifest.yaml")
    agent_manifest = load_yaml(ROOT / "agents" / "manifest.yaml")
    caps = load_yaml(ROOT / "agents" / "_capabilities.yaml")
    copilot_tools = caps["platforms"]["github-copilot"]["tool_names"]

    prompts_dir = ROOT / ".github" / "prompts"
    count = 0

    for name, cmd in manifest["commands"].items():
        # Collect unique tools from all required agents
        tools = []
        seen = set()
        for agent_name in cmd.get("agents_required", []):
            agent = agent_manifest["agents"].get(agent_name, {})
            for cap in agent.get("capabilities", []):
                tool = copilot_tools.get(cap)
                if tool and tool not in seen:
                    tools.append(tool)
                    seen.add(tool)

        desc = cmd["description"]
        frontmatter = f"---\nmode: agent\ndescription: \"{desc}\"\ntools:\n"
        for t in tools:
            frontmatter += f"  - {t}\n"
        frontmatter += "---\n\n"

        # Read command prose
        prose_file = ROOT / "commands" / cmd["workflow_file"]
        if prose_file.exists():
            prose = read_file(prose_file)
            # Convert {arguments} back to a Copilot-friendly form
            prose = prose.replace("{arguments}", "$PROMPT_INPUT")
        else:
            prose = f"# {name}\n\nWorkflow prose not yet extracted.\n"

        dst = prompts_dir / f"{name}.prompt.md"
        write_file(dst, frontmatter + prose)
        count += 1

    print(f"  Generated {count} Copilot prompt files in .github/prompts/")

# ---------------------------------------------------------------------------
# COPILOT: Generate .github/copilot-instructions.md
# ---------------------------------------------------------------------------
def generate_copilot_instructions():
    """Generate the Copilot project-wide instructions file."""
    manifest = load_yaml(ROOT / "agents" / "manifest.yaml")

    # Build agent reference table
    agent_table = "| Agent | Priority | Description |\n|-------|----------|-------------|\n"
    for name, agent in manifest["agents"].items():
        desc = re.sub(r"\s+", " ", agent["description"].strip())
        if len(desc) > 100:
            desc = desc[:97] + "..."
        agent_table += f"| @{name} | {agent['priority']} | {desc} |\n"

    content = (
"<!-- agent-notes: { ctx: \"Copilot project-wide instructions, generated from manifest\", deps: [agents/manifest.yaml, CLAUDE.md], state: active, last: \"copilot-cli@2026-03-22\" } -->\n"
"# Copilot Instructions — vteam-hybrid\n"
"\n"
"> **This file is generated.** Edit `agents/manifest.yaml`, `commands/manifest.yaml`, or `docs/` source files, then run `python3 scripts/generate-platform.py copilot`.\n"
"\n"
"## Project Overview\n"
"\n"
"This project uses the **vteam-hybrid methodology** — a phase-dependent hybrid team of 19 specialized AI agents. For full details:\n"
"\n"
"- **Phases:** `docs/methodology/phases.md` (7-phase model)\n"
"- **Personas:** `docs/methodology/personas.md` (19-agent catalog)\n"
"- **Governance:** `docs/process/team-governance.md` (triggers, debate protocol, gates)\n"
"- **Done Gate:** `docs/process/done-gate.md` (15-item completion checklist)\n"
"\n"
"## Available Agents\n"
"\n"
f"{agent_table}\n"
"\n"
"## Development Workflow\n"
"\n"
"1. **Discovery** — Use @cam for vision elicitation, @pat for requirements\n"
"2. **Architecture** — Use @archie for ADRs, @wei for adversarial debate\n"
"3. **Implementation** — Use @tara for failing tests (TDD red), @sato to make them pass (green)\n"
"4. **Review** — Use @vik + @tara + @pierrot for multi-lens code review\n"
"5. **Coordination** — Use @grace for sprint tracking and board management\n"
"\n"
"## Critical Rules\n"
"\n"
"- **TDD is mandatory:** @tara writes failing tests before @sato implements\n"
"- **ADR before code:** Architectural decisions require an ADR (`docs/adrs/`)\n"
"- **Done Gate:** Every work item passes the 15-item checklist before closing\n"
"- **Don't skip agents:** When a situation triggers multiple personas, invoke ALL of them\n"
"- **Security veto:** @pierrot has veto power on security and compliance\n"
"\n"
"## Conventions\n"
"\n"
"- Conventional commits format\n"
"- One commit per work item\n"
"- Board status flow: Backlog → Ready → In Progress → In Review → Done\n"
"- Agent-notes metadata on all non-excluded files (see `docs/methodology/agent-notes.md`)\n"
"\n"
"## Process Documentation\n"
"\n"
"| Doc | Purpose |\n"
"|-----|--------|\n"
"| `docs/methodology/phases.md` | 7-phase team methodology |\n"
"| `docs/methodology/personas.md` | 19-agent persona catalog |\n"
"| `docs/process/team-governance.md` | Triggers, debate protocol, gates |\n"
"| `docs/process/done-gate.md` | 15-item Done Gate checklist |\n"
"| `docs/process/gotchas.md` | Implementation patterns and pitfalls |\n"
"| `docs/process/operational-baseline.md` | Cross-cutting operational concerns |\n"
)

    dst = ROOT / ".github" / "copilot-instructions.md"
    write_file(dst, content)
    print(f"  Generated copilot-instructions.md")

# ---------------------------------------------------------------------------
# AGENTS.MD: Generate root AGENTS.md cross-platform bridge
# ---------------------------------------------------------------------------
def generate_agents_md():
    """Generate the root AGENTS.md universal cross-platform file."""
    manifest = load_yaml(ROOT / "agents" / "manifest.yaml")
    cmd_manifest = load_yaml(ROOT / "commands" / "manifest.yaml")

    # Agent summary
    agent_list = ""
    for name, agent in manifest["agents"].items():
        desc = re.sub(r"\s+", " ", agent["description"].strip())
        if len(desc) > 120:
            desc = desc[:117] + "..."
        agent_list += f"- **{name}** ({agent['priority']}): {desc}\n"

    # Command summary
    cmd_list = ""
    for name, cmd in cmd_manifest["commands"].items():
        agents = ", ".join(cmd.get("agents_required", []))
        cmd_list += f"- **{name}**: {cmd['description']}"
        if agents:
            cmd_list += f" (agents: {agents})"
        cmd_list += "\n"

    content = (
"<!-- agent-notes: { ctx: \"universal cross-platform agent instructions\", deps: [agents/manifest.yaml, commands/manifest.yaml], state: active, last: \"copilot-cli@2026-03-22\" } -->\n"
"# AGENTS.md — vteam-hybrid\n"
"\n"
"> **This file is generated.** It provides universal cross-platform instructions readable by any AI coding agent (Copilot, Codex, Cursor, Gemini, Claude Code). Edit the source manifests in `agents/` and `commands/`, then run `python3 scripts/generate-platform.py agents-md`.\n"
"\n"
"## Project\n"
"\n"
"This project uses the **vteam-hybrid methodology** — a structured approach to AI-assisted software development with 19 specialized agent personas organized across 7 phases.\n"
"\n"
"## Team Methodology\n"
"\n"
"The methodology is fully documented in `docs/`:\n"
"\n"
"- **7 Phases:** Discovery → Architecture → Implementation → Parallel Work → Code Review → Debugging → Human Interaction\n"
"- **19 Personas:** Each with defined responsibilities, thinking styles, and capability boundaries\n"
"- **Governance:** Architecture Decision Gate, adversarial debate protocol, scope reduction gate\n"
"- **Quality:** TDD mandatory, 15-item Done Gate, security veto, test coverage veto\n"
"\n"
"Full details: `docs/methodology/phases.md`, `docs/methodology/personas.md`\n"
"\n"
"## Agents\n"
"\n"
f"{agent_list}\n"
"## Commands / Workflows\n"
"\n"
f"{cmd_list}\n"
"## Conventions\n"
"\n"
"- **Commits:** Conventional commits format, one commit per work item\n"
"- **Board:** Backlog → Ready → In Progress → In Review → Done\n"
"- **TDD:** Tests before implementation (always)\n"
"- **ADRs:** Architecture Decision Records before implementation\n"
"- **Agent-notes:** Metadata on all non-excluded files (`docs/methodology/agent-notes.md`)\n"
"- **Done Gate:** 15-item checklist before closing any work item (`docs/process/done-gate.md`)\n"
"\n"
"## Boundaries\n"
"\n"
"- Never skip tests — Tara has veto power on coverage\n"
"- Never implement without an ADR for architectural decisions\n"
"- Never skip the Done Gate checklist\n"
"- Security and compliance have veto power (Pierrot)\n"
"- When multiple personas are triggered, invoke ALL of them\n"
"\n"
"## Key Documentation\n"
"\n"
"| Doc | Purpose |\n"
"|-----|--------|\n"
"| `docs/methodology/phases.md` | 7-phase team methodology |\n"
"| `docs/methodology/personas.md` | 19-agent persona catalog |\n"
"| `docs/methodology/agent-notes.md` | File metadata protocol |\n"
"| `docs/process/team-governance.md` | Triggers, debate protocol, gates |\n"
"| `docs/process/done-gate.md` | 15-item completion checklist |\n"
"| `docs/process/gotchas.md` | Implementation patterns and pitfalls |\n"
"| `docs/process/operational-baseline.md` | Cross-cutting operational concerns |\n"
"| `docs/adrs/` | Architecture Decision Records |\n"
"\n"
"## Platform-Specific Configuration\n"
"\n"
"This project supports multiple AI coding platforms:\n"
"\n"
"- **Claude Code:** `CLAUDE.md` + `.claude/agents/` + `.claude/commands/`\n"
"- **GitHub Copilot:** `.github/copilot-instructions.md` + `.github/agents/` + `.github/prompts/`\n"
"- **Codex CLI:** This `AGENTS.md` file + future `.codex/config.toml`\n"
"- **Cursor:** Future `.cursor/rules/`\n"
"- **Gemini:** Future `.gemini/GEMINI.md`\n"
"\n"
"The source of truth for agent definitions is `agents/manifest.yaml`. Platform-specific files are generated by `scripts/generate-platform.py`.\n"
)

    dst = ROOT / "AGENTS.md"
    write_file(dst, content)
    print(f"  Generated AGENTS.md")

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate-platform.py <mode>")
        print("Modes: extract, copilot, agents-md, all")
        sys.exit(1)

    mode = sys.argv[1]

    if mode in ("extract", "all"):
        print("\n=== Extracting persona prose ===")
        extract_persona_prose()
        print("\n=== Extracting command prose ===")
        extract_command_prose()

    if mode in ("copilot", "all"):
        print("\n=== Generating Copilot agent files ===")
        generate_copilot_agents()
        print("\n=== Generating Copilot prompt files ===")
        generate_copilot_prompts()
        print("\n=== Generating Copilot instructions ===")
        generate_copilot_instructions()

    if mode in ("agents-md", "all"):
        print("\n=== Generating AGENTS.md ===")
        generate_agents_md()

    print("\nDone!")

if __name__ == "__main__":
    main()
