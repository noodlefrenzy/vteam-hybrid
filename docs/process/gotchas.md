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

- **Plans don't replace process (Plan-as-Bypass anti-pattern).** A detailed implementation plan (from plan mode, a prior session, or a human-provided spec) is **input** to the V-Team phases, not a bypass. The plan still needs: GitHub issues (Grace), architecture gate if applicable (Archie + Wei as standalone agents), TDD (Tara → Sato), code review (Vik + Tara + Pierrot), and Done Gate. **Detection signal:** if the coordinator's first tool call is `Read` on a source file (not `docs/code-map.md`, governance docs, or the sprint plan), it's likely in bypass mode. See `2026-02-20-process-violation-plan-bypass.md` for the full retro.

- **Wei must be invoked as a standalone agent.** The coordinator's own analysis of trade-offs is not a substitute for invoking Wei as a standalone agent during architecture debates. If an ADR claims "Wei debate resolved" but no Wei agent was spawned, the gate has not passed.

- **Use scripts for stable logic, commands for evolving knowledge.** Static scripts are ideal when the rules are well-defined and unlikely to change. But when automation requires understanding things that change externally — evolving formats, shifting best practices, new API conventions — prefer a Claude Code command over a script. Commands bring current understanding (and can web-search) on every run.

- **Proxy mode is conservative, not permissive.** When the human is unavailable and Pat is acting as proxy, Pat defaults to the safer, more reversible option. The guardrails are strict:

  | Pat CAN (proxy) | Pat CANNOT (proxy) |
  |-----------------|-------------------|
  | Prioritize backlog items | Approve or reject ADRs |
  | Accept features against existing criteria | Change project scope |
  | Answer questions covered by product-context.md | Make architectural choices |
  | Defer items to next sprint | Merge to main |
  | Apply conservative defaults | Override Pierrot or Tara vetoes |

  When a question falls outside proxy authority, it blocks until the human returns. All proxy decisions are logged in `.claude/handoff.md` under `## Proxy Decisions (Review Required)`.

- **Product-context is a hypothesis, not ground truth.** `docs/product-context.md` captures Pat's model of the human's product philosophy — it's an educated guess that improves over time. The human can correct it at any time. When the human overrides a product-context-based recommendation, Pat updates the doc and logs the correction in the Correction Log table. Don't treat product-context entries as immutable rules.

- **Phase 1b must precede acceptance criteria writing.** Pat's Human Model Elicitation (kickoff Phase 1b) must complete before Pat writes acceptance criteria (Phase 4). The product context informs what "done" means to this human. Skipping 1b means acceptance criteria are written without understanding the human's quality bar, scope appetite, or non-negotiables.
