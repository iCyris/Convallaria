# Atelier

Atelier is an agentic design suite that turns loose creative intent into structured brand systems, production-ready assets, and design handoff.

It is designed to work as both a Codex plugin and a standalone skill. The project acts as a design director for AI-assisted work: it classifies the user's request, routes to the right subskill or reference workflow, uses deterministic scripts for fragile asset operations, and produces artifacts that designers, engineers, and other agents can continue.

## What Atelier Does

Atelier coordinates professional design work across seven connected areas:

- **Brand concepting**: turn an early product idea, audience, mood, or positioning note into a usable brand direction.
- **Design-system extraction**: formalize an existing visual language from screenshots, websites, codebases, documents, or mood descriptions.
- **Logo and icon production**: guide logo systems, SVG handling, favicon sets, app icons, social avatars, and platform exports.
- **Image optimization**: compress, convert, resize, and document bitmap assets for delivery.
- **Design tokens**: translate visual decisions into CSS variables, Tailwind extensions, JSON tokens, and implementation handoff.
- **UI visual QA**: review interfaces against a design system, screenshot, token set, or brand direction.
- **Asset packaging**: assemble final brand packs, manifests, and handoff notes for designers, engineers, and agents.

## Core Idea

Atelier is intentionally modular. The parent skill does not try to hold every design rule in one long instruction file. Instead, it routes work to focused resources:

```text
User request
  |
  v
Atelier router
  |
  |-- brand concepting
  |-- design-system extraction
  |-- logo system
  |-- image optimization
  |-- design tokens
  |-- UI visual QA
  `-- asset export
```

This keeps context lean while still allowing complex multi-step workflows such as:

```text
brand idea -> brand concept -> logo system -> design tokens -> asset pack
```

or:

```text
screenshots -> design-refine -> DESIGN.md -> token handoff -> visual QA
```

## Project Structure

```text
atelier/
|-- .codex-plugin/
|   `-- plugin.json
|-- skills/
|   `-- atelier/
|       |-- SKILL.md
|       |-- agents/
|       |   `-- openai.yaml
|       |-- references/
|       |-- scripts/
|       |-- templates/
|       `-- subskills/
|           `-- design-refine/
`-- claude/
    |-- CLAUDE.md
    `-- commands/
```

## Bundled Subskill

Atelier currently vendors one complete subskill:

```text
skills/atelier/subskills/design-refine/
```

`design-refine` extracts and formalizes design systems from existing material. It produces a structured `DESIGN.md` and a polished HTML report. The vendored copy is treated as a preserved dependency: do not modify it unless the task is explicitly to update that subskill.

## References

Atelier uses focused reference files for progressive disclosure:

- `references/routing.md`: task classification and workflow composition
- `references/brand-concept.md`: brand strategy and visual direction workflow
- `references/logo-system.md`: logo, SVG, favicon, app icon, and export workflow
- `references/image-optimize.md`: bitmap compression and conversion workflow
- `references/design-tokens.md`: token conversion and implementation handoff
- `references/ui-visual-qa.md`: visual QA and design-system compliance checks
- `references/asset-export.md`: final packaging and handoff workflow

## Scripts

Atelier includes small deterministic tools for operations that should not be rewritten by hand each time.

### Route a request

```bash
cd skills/atelier
python3 scripts/route_task.py "extract a design system from these screenshots and export logo pngs"
```

### Rasterize SVG assets

```bash
cd skills/atelier
python3 scripts/rasterize_svg.py logo/source/logo.svg --out logo/png --sizes 16 32 64 128 256 512 1024
```

The SVG rasterizer uses CairoSVG when available, then falls back to `rsvg-convert` or Inkscape.

### Optimize images

```bash
cd skills/atelier
python3 scripts/optimize_images.py input.png --out images --formats webp jpeg --max-width 1600 --quality 82
```

The image optimizer requires Pillow and writes an `image-manifest.json`.

### Validate a manifest

```bash
cd skills/atelier
python3 scripts/validate_outputs.py asset-manifest.json
```

## Output Convention

For multi-file deliverables, Atelier uses a project-local output shape:

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

The `asset-manifest.json` records inputs, outputs, producer steps, assumptions, open questions, and recommended next actions.

## Codex Usage

Atelier can be used as a Codex plugin through:

```text
.codex-plugin/plugin.json
```

The plugin exposes the skill directory:

```text
skills/
```

The main skill is:

```text
skills/atelier/SKILL.md
```

Starter prompts:

- Use Atelier to turn this visual reference into a design system.
- Use Atelier to create a brand direction and logo asset plan.
- Use Atelier to optimize and package these design assets.

## Claude Code Usage

Claude Code entry points live in:

```text
claude/commands/
```

The commands are lightweight wrappers around the shared Atelier skill:

- `atelier.md`
- `atelier-brand.md`
- `atelier-logo.md`
- `atelier-refine.md`
- `atelier-optimize.md`

## Language Behavior

Atelier source files are written in English. Generated design deliverables should use the user's requested language. If the user does not specify a language, mirror the language of the user's request.

## Design Philosophy

Atelier treats design as both feeling and system.

It should help an agent notice the atmospheric qualities of a brand, but also convert those qualities into files that survive production: tokens, SVGs, exports, manifests, reports, and handoff notes. It favors clear routing, explicit assumptions, reusable templates, and script-backed asset operations.

The goal is not to replace a designer's judgment. The goal is to give AI-assisted design work a better studio: one that can hold mood, structure, craft, and delivery in the same room.

