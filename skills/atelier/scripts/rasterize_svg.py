#!/usr/bin/env python3
"""Rasterize an SVG into one or more PNG sizes."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def render_with_cairosvg(svg: Path, out: Path, size: int) -> bool:
    try:
        import cairosvg  # type: ignore
    except Exception:
        return False
    cairosvg.svg2png(url=str(svg), write_to=str(out), output_width=size, output_height=size)
    return True


def render_with_cli(svg: Path, out: Path, size: int) -> bool:
    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        subprocess.run([rsvg, "-w", str(size), "-h", str(size), "-o", str(out), str(svg)], check=True)
        return True

    inkscape = shutil.which("inkscape")
    if inkscape:
        subprocess.run(
            [
                inkscape,
                str(svg),
                "--export-type=png",
                f"--export-filename={out}",
                f"--export-width={size}",
                f"--export-height={size}",
            ],
            check=True,
        )
        return True

    return False


def rasterize(svg: Path, out_dir: Path, sizes: list[int], prefix: str | None) -> list[Path]:
    if not svg.exists():
        raise FileNotFoundError(f"SVG not found: {svg}")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = prefix or svg.stem
    outputs = []
    for size in sizes:
        out = out_dir / f"{stem}-{size}.png"
        if not render_with_cairosvg(svg, out, size):
            if not render_with_cli(svg, out, size):
                raise RuntimeError("No SVG renderer found. Install CairoSVG, rsvg-convert, or Inkscape.")
        outputs.append(out)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--out", type=Path, default=Path("logo/png"))
    parser.add_argument("--sizes", type=int, nargs="+", default=[16, 32, 64, 128, 256, 512, 1024])
    parser.add_argument("--prefix")
    args = parser.parse_args()

    try:
        outputs = rasterize(args.svg, args.out, args.sizes, args.prefix)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
