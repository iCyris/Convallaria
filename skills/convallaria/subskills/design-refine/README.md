# design-refine

Extract & formalize a complete design system from any source material.

## What It Does

```
User Input (anything)  →  design-refine  →  DESIGN.md + report.html
                                              │              │
                                              │              └─ Visual showcase
                                              │                 (full-page snap-scroll,
                                              │                  live components, extracted palette)
                                              │
                                              └─ Design Tokens (CSS vars + Tailwind config)
                                                 + Agentic style constraints
                                                 (AI-friendly, copy-paste-ready)
```

Feed it **any design source** — a screenshot, a brand guidelines PDF, a Figma export, a live website, a codebase with existing styles, or even a verbal description like "minimal, warm, Japanese-inspired" — and it produces two deliverables:

### DESIGN.md

A structured, 10-section design specification:

1. **Visual Theme & Atmosphere** — Literary description of the design's personality and feel
2. **Color Palette & Roles** — Every color with semantic names, hex/RGB values, and usage rules
3. **Typography Rules** — Font families, size scale, weight hierarchy, line-height principles
4. **Component Stylings** — Buttons, cards, inputs, nav, badges — with exact pixel values
5. **Layout Principles** — Spacing system, grid, whitespace philosophy, border-radius scale
6. **Depth & Elevation** — Shadow system, layering strategy, depth philosophy
7. **Do's and Don'ts** — Specific guardrails with exact values (not vague principles)
8. **Responsive Behavior** — Breakpoints, touch targets, collapsing strategy
9. **Design Tokens** — CSS custom properties + Tailwind `theme.extend` config, ready to drop into your project
10. **Agent Prompt Guide** — Quick color reference + example prompts so AI agents can use the system correctly

The Design Tokens section is the engineering bridge — you can copy the CSS variables into your stylesheet or the Tailwind config into `tailwind.config.js` and start building immediately.

### HTML Report

A polished, single-file visual presentation built from `templates/report.html`:

- **7 full-page sections** with CSS snap-scroll and touch damping for smooth navigation
- **Color palette showcase** with large swatches (click to copy hex values)
- **Typography specimens** rendered at actual sizes
- **Design Token reference table** with visual previews
- **Atomic component gallery** — buttons, cards, inputs, badges rendered live
- **Composite patterns** — hero sections, card grids, nav bars, forms assembled from the atoms
- **Guidelines** — Do's/Don'ts as a visual comparison grid

The report styles itself using the extracted palette, so it *feels like* the design system it's describing.

## Usage Scenarios

### From a screenshot or image

> "Here's a screenshot of Stripe's dashboard. Extract the design system."

The skill analyzes colors, typography, spacing, component patterns, and visual personality directly from the image. Where information isn't observable (e.g., responsive breakpoints), it infers reasonable defaults and marks them as inferred.

### From a website

> "Analyze https://linear.app and produce a design system."

Fetches the page, inspects the visual presentation, and extracts everything — colors, fonts, shadows, component styles, layout patterns.

### From a codebase

> "Look at the CSS/Tailwind config in this project and formalize it into a proper design system."

Scans `tailwind.config.js`, CSS/SCSS files, theme files, and component libraries. Extracts existing tokens and fills gaps where the codebase doesn't explicitly define values.

### From brand guidelines

> "Here's our brand book PDF. Turn it into a usable design system with tokens."

Reads the brand colors, typography choices, and usage rules, then extends them into a complete system with all the missing pieces (spacing, shadows, responsive behavior, etc.).

### From a verbal description

> "I want something warm, editorial, book-like. Serif headings, cream backgrounds, terracotta accents."

Interprets the aesthetic intent and constructs an entire design system that matches the described mood — with specific hex codes, font stacks, and component styles.

### From multiple sources

> "Here's our current website screenshot + our brand colors PDF + our Figma components. Unify them."

Combines signals from multiple inputs into a single coherent system, resolving conflicts and filling gaps.

## File Structure

```
design-refine/
├── SKILL.md             # Core instructions (383 lines)
├── README.md            # This file
├── .gitignore           # Git ignore rules
└── templates/
    └── report.html      # HTML report template (897 lines)
                         # 67 placeholder slots for AI-generated content
                         # Snap-scroll, nav dots, progress bar, fade animations,
                         # keyboard navigation, touch damping, print styles
```

## Language Behavior

The skill instructions are written in English for clarity. **All generated outputs (DESIGN.md and HTML report) automatically use the language the user writes in.** Chinese input → Chinese deliverables. English input → English deliverables.
