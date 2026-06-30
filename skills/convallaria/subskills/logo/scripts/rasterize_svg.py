#!/usr/bin/env python3
"""Rasterize an SVG into one or more PNG sizes."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_RENDER_TIMEOUT_SECONDS = 60


def render_with_cairosvg(svg: Path, out: Path, size: int, timeout: int) -> bool:
    snippet = (
        "import sys\n"
        "import cairosvg\n"
        "size = int(sys.argv[3])\n"
        "cairosvg.svg2png(url=sys.argv[1], write_to=sys.argv[2], output_width=size, output_height=size)\n"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", snippet, str(svg), str(out), str(size)],
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"CairoSVG timed out after {timeout} seconds while rendering {svg}.") from exc

    if result.returncode == 0:
        return True

    detail = result.stderr.strip() or result.stdout.strip()
    if "ModuleNotFoundError" in detail or "No module named" in detail:
        return False

    raise RuntimeError(f"CairoSVG failed while rendering {svg}: {detail}")


def render_with_cli(svg: Path, out: Path, size: int, timeout: int) -> bool:
    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        subprocess.run([rsvg, "-w", str(size), "-h", str(size), "-o", str(out), str(svg)], check=True, timeout=timeout)
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
            timeout=timeout,
        )
        return True

    return False


def render_with_quicklook(svg: Path, out: Path, size: int, timeout: int) -> bool:
    """Use macOS QuickLook when dedicated SVG renderers are unavailable."""
    if platform.system() != "Darwin":
        return False

    qlmanage = shutil.which("qlmanage")
    if not qlmanage:
        return False

    try:
        with tempfile.TemporaryDirectory(prefix="convallaria-svg-") as tmp:
            tmp_dir = Path(tmp)
            subprocess.run(
                [qlmanage, "-t", "-s", str(size), "-o", str(tmp_dir), str(svg)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout,
            )
            candidates = sorted(tmp_dir.glob(f"{svg.name}*.png")) or sorted(tmp_dir.glob("*.png"))
            if not candidates:
                return False
            shutil.move(str(candidates[0]), out)
            return True
    except Exception:
        return False


def rasterize(svg: Path, out_dir: Path, sizes: list[int], prefix: str | None, timeout: int) -> list[Path]:
    if not svg.exists():
        raise FileNotFoundError(f"SVG not found: {svg}")
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = prefix or svg.stem
    outputs = []
    for size in sizes:
        out = out_dir / f"{stem}-{size}.png"
        if not render_with_cairosvg(svg, out, size, timeout):
            if not render_with_cli(svg, out, size, timeout):
                if not render_with_quicklook(svg, out, size, timeout):
                    raise RuntimeError(
                        "No SVG renderer found. Install CairoSVG with Cairo, rsvg-convert, "
                        "or Inkscape. On macOS, qlmanage can also be used when available."
                    )
        outputs.append(out)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--out", type=Path, default=Path("logo/png"))
    parser.add_argument("--sizes", type=int, nargs="+", default=[16, 32, 64, 128, 256, 512, 1024])
    parser.add_argument("--prefix")
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_RENDER_TIMEOUT_SECONDS,
        help="Maximum seconds to wait for each external renderer invocation.",
    )
    args = parser.parse_args()

    try:
        outputs = rasterize(args.svg, args.out, args.sizes, args.prefix, args.timeout)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
