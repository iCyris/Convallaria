---
name: atelier
description: "Agentic design suite for routing professional design work across brand concepting, design-system extraction, logo and icon production, image optimization, token handoff, visual QA, and asset packaging. Use when a user asks Codex to create, refine, inspect, formalize, export, or QA visual identity systems, design systems, logos, images, UI styling, or design handoff assets. Also use as the coordinating parent skill for the bundled design-refine subskill."
---

# Atelier

Atelier is a routing and production skill for design work. Treat it as the design director for a modular suite: classify the task, load only the relevant reference, use deterministic scripts for fragile asset operations, and produce polished deliverables that another agent or designer can continue.

All authored Atelier outputs must be in the user's requested language. If the user does not specify a language, mirror the user's language. Internal project files are written in English.

## Routing First

Start by identifying the task family:

- **Design-system extraction**: route to `subskills/design-refine/` without modifying that vendored subskill.
- **Brand concepting**: read `references/brand-concept.md`.
- **Logo and icon production**: read `references/logo-system.md`.
- **Image optimization**: read `references/image-optimize.md`.
- **Token handoff**: read `references/design-tokens.md`.
- **UI visual QA**: read `references/ui-visual-qa.md`.
- **Asset packaging or multi-step delivery**: read `references/asset-export.md`.
- **Unclear or mixed request**: read `references/routing.md`, then select a workflow.

For quick classification, run:

```bash
python3 scripts/route_task.py "user request here"
```

Use the script as an advisor, not as the final authority. Prefer the user's explicit intent over keyword matches.

## Core Workflows

### Extract a Design System

Use the vendored `design-refine` subskill when the user provides screenshots, a website, a codebase, a Figma export, a brand guide, or a mood description and asks for a formal design system.

1. Read `subskills/design-refine/SKILL.md`.
2. Follow its workflow exactly.
3. Produce `DESIGN.md` and the HTML report it specifies.
4. Do not edit any file inside `subskills/design-refine/` unless the user explicitly asks to update that subskill.

### Create a Brand Direction

Read `references/brand-concept.md` when the task starts from strategy, naming, personality, audience, positioning, visual territories, or early identity exploration. Use `templates/BRAND.md` as the output structure when the user wants a durable artifact.

### Produce Logo and Platform Assets

Read `references/logo-system.md` when the user asks for logo concepts, SVG cleanup, favicon sets, app icons, social avatars, or platform-specific logo exports. Use `scripts/rasterize_svg.py` for SVG-to-PNG export when a source SVG exists.

### Optimize Images

Read `references/image-optimize.md` when the user asks for compression, conversion, responsive variants, image manifests, metadata stripping, or delivery optimization. Use `scripts/optimize_images.py` when bitmap assets are present.

### Package a Handoff

Read `references/asset-export.md` when a task spans multiple outputs or needs a final brand pack. Use `templates/asset-manifest.json` to record source files, outputs, roles, and producer steps.

## Output Conventions

Use a project-local output folder unless the user names a destination:

```text
atelier-output/
|-- BRAND.md
|-- DESIGN.md
|-- LOGO_SPEC.md
|-- DESIGN_QA.md
|-- asset-manifest.json
|-- tokens/
|-- logo/
|-- images/
|-- screenshots/
`-- handoff/
```

For every multi-file deliverable, create or update `asset-manifest.json` with:

- project name and slug
- input files and their roles
- generated outputs and their producer skill
- token paths
- logo and image asset paths
- notes about assumptions, unresolved decisions, and next actions

## Quality Bar

- Preserve source material unless the user requests transformation.
- Prefer scripts for repetitive image, logo, token, and packaging work.
- Keep strategic writing specific enough for production decisions.
- Verify generated files exist before reporting completion.
- For frontend or UI QA tasks, use screenshots when possible and report concrete visual deviations.
- For brand and design outputs, name rationale, constraints, and anti-patterns so future agents can maintain the system.
