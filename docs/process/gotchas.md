---
agent-notes:
  ctx: "implementation gotchas and established patterns"
  deps: [CLAUDE.md]
  state: active
  last: "coordinator@2026-02-15"
---
# Known Patterns and Gotchas

Extracted from CLAUDE.md to reduce context window load. Read this when working on implementation or debugging tasks. Projects populate sections as they discover gotchas.

## Testing Patterns

<!-- Add project-specific testing gotchas here as you discover them -->

## Adapter / Integration Gotchas

<!-- Add gotchas related to adapters, external APIs, SDKs here -->

## Build and Run

<!-- Add build, bundling, and runtime gotchas here -->

## Architecture Patterns

<!-- Add architecture patterns and constraints here -->

## Process

- **Use scripts for stable logic, commands for evolving knowledge.** Static scripts are ideal when the rules are well-defined and unlikely to change. But when automation requires understanding things that change externally — evolving formats, shifting best practices, new API conventions — prefer a Claude Code command over a script. Commands bring current understanding (and can web-search) on every run.
