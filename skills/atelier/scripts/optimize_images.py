#!/usr/bin/env python3
"""Optimize bitmap images and write an image manifest."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_pillow():
    try:
        from PIL import Image, ImageOps
    except Exception as exc:
        raise RuntimeError("Pillow is required. Install it with `python3 -m pip install pillow`.") from exc
    return Image, ImageOps


def output_path(out_dir: Path, source: Path, width: int, fmt: str) -> Path:
    suffix = "jpg" if fmt == "jpeg" else fmt
    return out_dir / f"{source.stem}-{width}.{suffix}"


def save_variant(image, target: Path, fmt: str, quality: int) -> None:
    save_kwargs = {}
    normalized = fmt.upper()
    if fmt in {"jpeg", "webp", "avif"}:
        save_kwargs["quality"] = quality
    if fmt == "jpeg":
        normalized = "JPEG"
        if image.mode in {"RGBA", "LA", "P"}:
            from PIL import Image as PILImage

            background = PILImage.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            background.paste(image, mask=image.getchannel("A") if "A" in image.getbands() else None)
            image = background
        else:
            image = image.convert("RGB")
        save_kwargs["optimize"] = True
        save_kwargs["progressive"] = True
    elif fmt == "png":
        normalized = "PNG"
        save_kwargs["optimize"] = True
    elif fmt == "webp":
        normalized = "WEBP"
        save_kwargs["method"] = 6
    elif fmt == "avif":
        normalized = "AVIF"
    image.save(target, normalized, **save_kwargs)


def optimize(paths: list[Path], out_dir: Path, formats: list[str], max_width: int | None, quality: int) -> dict:
    Image, ImageOps = load_pillow()
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "atelier.image-manifest.v1",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "outputs": [],
    }

    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        original_bytes = path.stat().st_size
        with Image.open(path) as opened:
            image = ImageOps.exif_transpose(opened)
            width, height = image.size
            target_width = min(width, max_width) if max_width else width
            if target_width != width:
                ratio = target_width / width
                target_height = max(1, round(height * ratio))
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            else:
                target_height = height

            for fmt in formats:
                fmt = fmt.lower()
                target = output_path(out_dir, path, target_width, fmt)
                save_variant(image.copy(), target, fmt, quality)
                output_bytes = target.stat().st_size
                manifest["outputs"].append(
                    {
                        "source": str(path),
                        "output": str(target),
                        "format": fmt,
                        "width": target_width,
                        "height": target_height,
                        "quality": quality if fmt in {"jpeg", "webp", "avif"} else None,
                        "originalBytes": original_bytes,
                        "outputBytes": output_bytes,
                        "savingsPercent": round((1 - output_bytes / original_bytes) * 100, 2)
                        if original_bytes
                        else 0,
                    }
                )

    manifest_path = out_dir / "image-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", type=Path, nargs="+")
    parser.add_argument("--out", type=Path, default=Path("images"))
    parser.add_argument("--formats", nargs="+", default=["webp"], choices=["png", "jpeg", "webp", "avif"])
    parser.add_argument("--max-width", type=int)
    parser.add_argument("--quality", type=int, default=82)
    args = parser.parse_args()

    try:
        manifest = optimize(args.images, args.out, args.formats, args.max_width, args.quality)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
