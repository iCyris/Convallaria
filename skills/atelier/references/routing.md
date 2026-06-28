# Atelier Routing Guide

Use this guide when the user's request is mixed, ambiguous, or spans more than one design operation.

## Task Families

| Family | Use when the user asks for | Primary resource | Common outputs |
| --- | --- | --- | --- |
| Design-system extraction | extracting style, reverse-engineering visuals, formalizing existing UI, creating tokens from screenshots or code | `subskills/design-refine/SKILL.md` | `DESIGN.md`, `report.html` |
| Brand concepting | naming, positioning, personality, brand voice, creative direction, visual territories | `references/brand-concept.md` | `BRAND.md` |
| Logo system | logo concepts, SVG cleanup, favicon/app icon export, lockups, clear space | `references/logo-system.md` | `LOGO_SPEC.md`, `logo/` |
| Image optimization | compression, conversion, responsive variants, metadata removal | `references/image-optimize.md` | `images/`, `image-manifest.json` |
| Design tokens | CSS variables, Tailwind config, Style Dictionary, theme files | `references/design-tokens.md` | `tokens/` |
| UI visual QA | screenshot review, design-system compliance, responsive visual checks | `references/ui-visual-qa.md` | `DESIGN_QA.md`, screenshots |
| Asset export | final packaging, handoff, manifest, cross-tool delivery | `references/asset-export.md` | brand pack, handoff docs |

## Composition Patterns

### From a vague product idea to a usable identity

1. `brand-concept`
2. `logo-system`
3. `design-tokens`
4. `asset-export`

### From screenshots to an implementation-ready design system

1. `design-refine`
2. `design-tokens`
3. `ui-visual-qa` if there is an implementation to inspect
4. `asset-export`

### From an SVG logo to platform assets

1. `logo-system`
2. `image-optimize`
3. `asset-export`

### From an existing app to a design audit

1. `design-refine` if no design system exists
2. `ui-visual-qa`
3. `design-tokens` if token drift needs repair

## Routing Rules

- Route to the narrowest resource that can complete the task.
- Load `design-refine` only for extraction or formalization tasks; it is intentionally large.
- Use scripts for image transforms, SVG rasterization, and manifest validation.
- When multiple subskills are needed, create an `asset-manifest.json` early so each step can append outputs.
- Ask a concise clarifying question only when the target deliverable or source asset is impossible to infer.

