# Convallaria

<p align="center">
  <img src="assets/brand/convallaria-mark.png" alt="Convallaria logo" width="420">
</p>

Convallaria cultivates quiet brand systems from first feeling to final assets.

It is an agentic design suite meant to behave less like a prompt collection and more like a small design studio for agents: route the brief, load the right workflow, keep taste and implementation connected, use deterministic scripts for fragile asset work, and leave behind files another designer, engineer, or agent can continue.

## What It Does

| Area | Use it for | Typical outputs |
| --- | --- | --- |
| Brand concepting | Positioning, voice, audience, visual territories, creative direction | `BRAND.md` |
| End-to-end brand packs | Full identity flow from rough idea to logo, tokens, exports, and handoff | `BRAND.md`, `LOGO_SPEC.md`, `tokens/`, `logo/`, `asset-manifest.json`, `handoff/` |
| Design-system extraction | Formalizing an existing visual language from screenshots, sites, code, docs, or mood references | `DESIGN.md`, `report.html` |
| Logo and icon production | SVG source, logo rules, favicons, app icons, social avatars, platform exports | `LOGO_SPEC.md`, `logo/` |
| Image optimization | Compression, conversion, responsive variants, metadata stripping | `images/`, `image-manifest.json` |
| Design tokens | CSS variables, Tailwind extensions, JSON tokens, TypeScript theme objects | `tokens/` |
| UI visual QA | Screenshot review, token drift checks, responsive visual QA | `DESIGN_QA.md`, `screenshots/` |
| Asset packaging | Manifests, handoff notes, final brand packs | `asset-manifest.json`, `handoff/` |

## Quick Start

Use Convallaria as a Codex plugin through `.codex-plugin/plugin.json`; the plugin exposes `skills/`, and the main skill is `skills/convallaria/SKILL.md`.

Starter prompts:

```text
Use Convallaria to create a complete brand pack for this product idea.
Use Convallaria to turn these screenshots into a design system.
Use Convallaria to produce logo exports and a handoff manifest.
Use Convallaria to QA this UI against the attached brand system.
```

For Claude Code, run the local install script once to sync the command entry points into `.claude/`:

```bash
python3 scripts/conva.py install
```

Then use commands such as:

```text
/conva
/conva-brand
/conva-logo
/conva-refine
/conva-optimize
```

`conva` is the short command prefix for Convallaria.

For other AI coding tools, point the agent at `AGENTS.md` first, then at `skills/convallaria/SKILL.md`. The parent skill explains how to route a request and which subskill to read. When the tool cannot load Codex or Claude adapters, use the files directly:

```text
Read AGENTS.md.
Use skills/convallaria/SKILL.md.
For this request, route to the relevant subskill under skills/convallaria/subskills/.
Create or update asset-manifest.json when multiple files are produced.
```

## Development Loop

Install, update, check, or remove the local adapters with one entry point:

```bash
python3 scripts/conva.py install
python3 scripts/conva.py update
python3 scripts/conva.py doctor
python3 scripts/conva.py uninstall
```

Convallaria is not published to a public Codex or Claude marketplace by this repository. It is maintained as a local plugin project: the script syncs Claude Code adapters into `.claude/`, refreshes Codex plugin metadata, and prints the next local Codex plugin command when it can infer one.

Run the project smoke test:

```bash
python3 scripts/conva.py doctor
```

Use `--skip-raster` only when an SVG brand asset needs rasterization and the machine lacks CairoSVG, `rsvg-convert`, Inkscape, or macOS QuickLook:

```bash
python3 scripts/conva.py doctor --skip-raster
```

After editing the skill, refresh local integration surfaces:

```bash
python3 scripts/conva.py update
```

That script:

- syncs root `CLAUDE.md` and `claude/commands/*.md` into `.claude/`
- updates `.codex-plugin/plugin.json` with a Codex cachebuster version
- prints the next Codex reinstall command when it can infer the local marketplace
- optionally runs the smoke test

Codex reads updated skill metadata in a new thread after reinstalling the plugin. Claude Code reads updated `.claude/` command files after the sync step.

## Observable Outcomes

Convallaria is considered runnable when these checks hold:

- The Codex plugin manifest points at `skills/`, and `skills/convallaria/SKILL.md` exists.
- Claude Code command wrappers are synced into `.claude/commands/`.
- Generic AI tools can start from `AGENTS.md` and `skills/convallaria/SKILL.md` without needing platform-specific adapters.
- The router classifies both narrow tasks and complete brand-pack requests.
- The README script examples run with the documented dependencies.
- A complete brand-pack workflow can name its required deliverables before generation.
- Multi-file work records assumptions, generated outputs, quality checks, and next actions in `asset-manifest.json`.
- Logo and bitmap transforms use deterministic scripts when source assets exist.
- Durable project files, templates, references, examples, and handoff artifacts are authored in English.
- Brand outputs pass the craft gate: decisions are specific, traceable, usable in production, and not a pile of disconnected AI-generated copy or images.

## Workflow Shape

Convallaria is intentionally modular. The parent skill routes work to focused subskills instead of loading every design rule at once:

```text
User request
  |
  v
Convallaria router
  |
  |-- concept
  |-- pack
  |-- design-refine
  |-- logo
  |-- images
  |-- tokens
  |-- audit
  `-- export
```

Common compositions:

```text
brand idea -> pack -> concept -> logo -> tokens -> export
```

```text
screenshots -> design-refine -> DESIGN.md -> token handoff -> visual QA
```

```text
source SVG -> logo -> raster export -> images -> export
```

## Subskills

Convallaria uses focused subskills for progressive disclosure. Convallaria-owned subskills use concise one-word names:

- `routing.md`: task classification and workflow composition
- `subskills/concept/`: brand strategy and visual direction workflow
- `subskills/pack/`: complete brand creation, delivery, and quality gate
- `subskills/logo/`: logo, SVG, favicon, app icon, and export workflow
- `subskills/images/`: bitmap compression and conversion workflow
- `subskills/tokens/`: token conversion and implementation handoff
- `subskills/audit/`: visual QA and design-system compliance checks
- `subskills/export/`: final packaging and handoff workflow

The vendored `skills/convallaria/subskills/design-refine/` folder is treated as a preserved dependency and keeps its upstream name. It should not be modified unless the task is explicitly to update that subskill.

## Scripts

Route a request:

```bash
cd skills/convallaria
python3 scripts/route_task.py "create a complete brand pack from positioning to logo, tokens, and handoff assets"
```

Rasterize SVG assets:

```bash
cd skills/convallaria
python3 subskills/logo/scripts/rasterize_svg.py logo/source/logo.svg --out logo/png --sizes 16 32 64 128 256 512 1024
```

The SVG rasterizer uses CairoSVG when available, then falls back to `rsvg-convert`, Inkscape, or macOS QuickLook when available.

Optimize images:

```bash
cd skills/convallaria
python3 subskills/images/scripts/optimize_images.py input.png --out images --formats webp jpeg --max-width 1600 --quality 82
```

Validate a manifest:

```bash
cd skills/convallaria
python3 subskills/export/scripts/validate_outputs.py asset-manifest.json
```

Refresh local integrations:

```bash
python3 scripts/conva.py update
```

## Output Convention

For multi-file deliverables, Convallaria uses a project-local output shape:

```text
convallaria-output/
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

`asset-manifest.json` records inputs, outputs, producer steps, quality checks, assumptions, open questions, and recommended next actions.

## Project Structure

```text
convallaria/
|-- .codex-plugin/
|   `-- plugin.json
|-- assets/
|   `-- brand/
|       `-- convallaria-mark.png
|-- CLAUDE.md
|-- claude/
|   `-- commands/
|-- scripts/
|   |-- conva.py
|   |-- smoke_test.py
|   `-- update_convallaria.py
`-- skills/
    `-- convallaria/
        |-- SKILL.md
        |-- routing.md
        |-- agents/
        |-- scripts/
        |   `-- route_task.py
        `-- subskills/
            |-- audit/
            |-- concept/
            |-- design-refine/
            |-- export/
            |-- images/
            |-- logo/
            |-- pack/
            `-- tokens/
```

`.claude/` is a generated local Claude Code adapter directory created by `scripts/conva.py sync`; it is intentionally ignored by git. The Claude Code guide lives at root `CLAUDE.md`, and command adapter sources live under `claude/commands/`.

## Language Policy

Convallaria project files, templates, references, examples, and durable deliverables are authored in English. If a consuming project explicitly requires localization, keep the Convallaria source of truth in English and treat localized copies as secondary exports.

## Design Philosophy

Convallaria treats design as both atmosphere and system.

Good agentic design work should be able to hold feeling, constraints, source files, tokens, exports, manifests, and handoff in one continuous thread. The goal is not to replace a designer's judgment. The goal is to give AI-assisted design work a better studio: one where taste is observable, assets are traceable, and delivery is not an afterthought.
