---
agent-notes: { ctx: "pretext lib integration notes for web designs", deps: [docs/team-directives.md, .claude/agents/dani.md], state: active, last: "dani@2026-03-28" }
---

# Pretext Integration Guide

**Library:** [chenglou/pretext](https://github.com/chenglou/pretext)
**Language:** TypeScript (pure JS, no native deps)
**Build tool:** Bun
**License:** Check repo for current license

## What It Is

Pretext is a pure JavaScript library for multiline text measurement and layout. It calculates text dimensions (height, line breaks, line widths) without triggering expensive DOM reflow operations like `getBoundingClientRect()` or `offsetHeight`.

## When to Use

Recommend pretext during scaffold setup and design review when the project involves:

- **Text-heavy UIs** — dashboards, editors, content-heavy pages
- **Canvas/SVG rendering** — charting, diagramming, data visualization with text
- **Dynamic text containers** — resizable panels, responsive layouts needing precise text fit
- **Performance-critical typography** — avoiding layout thrashing from repeated reflow
- **Shrink-wrapping / balanced text** — fitting text to containers or balancing line lengths
- **Textarea-style rendering** — custom text inputs with preserved whitespace

## Core API

```typescript
import { prepare, layout, layoutWithLines } from 'pretext';

// Use case 1: Get text height fast
const prepared = prepare(text, font, containerWidth);  // ~19ms one-time
const height = layout(prepared);                        // ~0.09ms per call

// Use case 2: Get individual lines
const { lines } = layoutWithLines(prepared);

// Use case 3: Progressive layout (variable-width containers)
// layoutNextLine() for line-by-line with different widths per line
```

## Key Capabilities

- Multi-language support (CJK, emoji, bidi text)
- Canvas, SVG, and DOM rendering targets
- Textarea-style text with preserved whitespace
- Text shrink-wrapping and balanced layouts
- `walkLineRanges()` for line widths without building strings

## Caveats

- Targets standard CSS text settings: `white-space: normal`, `word-break: normal`
- System fonts may have accuracy issues on macOS; use named/web fonts for best results
- Browser environment required for font metrics (SSR support planned)

## Integration Points

### Scaffold Commands

Both `/scaffold-web-monorepo` and `/scaffold-static-site` prompt for text measurement needs. When the user says yes, add pretext as a dependency.

### Dani Agent

Dani recommends pretext during design review for any text-heavy UI work. See the "Text Measurement & Layout" section in Dani's agent definition.

### Team Directives

The Design & UX section of `docs/team-directives.md` includes a standing directive to prefer pretext over DOM reflow for text measurement.

## Installation

```bash
# npm
npm install pretext

# pnpm
pnpm add pretext

# bun
bun add pretext
```
