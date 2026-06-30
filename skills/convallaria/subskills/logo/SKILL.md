---
name: logo
description: "Logo and icon production workflow for image-led concepts, SVG cleanup, lockups, favicons, app icons, social avatars, platform exports, clear-space rules, and logo QA."
---

# Logo System Workflow

Use when: a user needs a mark, wordmark, lockup, favicon, app icon, social avatar, image-led logo concepts, SVG cleanup, or platform export.
Needs: brand direction, an existing source logo or SVG, or enough context to propose logo concepts honestly.
Produces: `LOGO_SPEC.md` and logo assets when source files are available.
Done when: source-of-truth files, usage rules, minimum sizes, export paths, and manifest entries are clear.

Use this reference for logo concepts, SVG cleanup, lockups, favicon sets, app icons, and platform-specific exports.

## Deliverables

Use `templates/LOGO_SPEC.md` when producing a logo system. A complete logo package should include:

- primary logo
- symbol or mark
- wordmark when relevant
- horizontal, stacked, and compact lockups when relevant
- monochrome, dark-background, and light-background variants
- clear-space and minimum-size rules
- misuse rules
- platform export set

## Concept Generation Rules

- For brand-new logo concepts, prefer generated bitmap concept images first. Use image generation or supplied visual references to explore proportion, gesture, material, and finish before committing to production geometry.
- Do not hand-write decorative SVG as the primary creative method unless the user explicitly asks for SVG-only work or the mark is intentionally simple geometric production art.
- Keep generated concepts in `logo/concepts/` with descriptive names and enough variants to compare direction, not tiny changes.
- Evaluate concepts for recognizability, distinct silhouette, small-size legibility, cultural fit, and whether any text or letterforms are clean enough to keep.
- After a concept direction is chosen, prepare production assets from the best source available: cleaned bitmap, vector redraw, traced source, or existing SVG. Treat SVG as a production and export format, not the default ideation canvas.
- For bitmap cleanup and preview variants, avoid long inline per-pixel processing in the agent session. Use `subskills/images/scripts/optimize_images.py` for deterministic resizing/conversion, and keep large-source processing explicit with size limits.
- Record concept prompts, selected direction, rejected directions, and source-to-output decisions in `LOGO_SPEC.md` and `asset-manifest.json`.

## SVG Source Rules

- Use SVG when there is an existing SVG to clean up, a selected concept needs vector production, or platform exports require vector source.
- Keep SVG source files editable and semantic.
- Preserve a transparent background unless the target platform requires a filled background.
- Use `viewBox` and avoid fixed-only sizing.
- Convert text to outlines only when the user needs portable final artwork and the font cannot be distributed.
- Keep source SVGs in `logo/source/`.

## Raster Export

Use `subskills/logo/scripts/rasterize_svg.py` from the parent `skills/convallaria/` directory for deterministic PNG export:

```bash
python3 subskills/logo/scripts/rasterize_svg.py logo/source/logo.svg --out logo/png --sizes 16 32 64 128 256 512 1024
```

The script will use CairoSVG when installed, then fall back to common command-line rasterizers if available.

## Recommended Sizes

| Target | Sizes |
| --- | --- |
| favicon | 16, 32, 48 |
| browser icons | 192, 512 |
| Apple touch icon | 180 |
| iOS app icon source | 1024 |
| macOS app icon source | 1024 |
| Android adaptive icon source | 432 foreground with safe zone |
| social avatar | 512, 1024 |
| Open Graph image | 1200 x 630 |

## QA Checklist

- The logo remains legible at 16 px if used as favicon.
- The mark works on dark and light backgrounds.
- Clear space is defined with a repeatable unit from the logo geometry.
- Exports are named by role and size.
- Every generated asset is listed in `asset-manifest.json`.
