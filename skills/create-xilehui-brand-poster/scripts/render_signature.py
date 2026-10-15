#!/usr/bin/env python3
"""Reproduce the approved two-logo horizontal or stacked signature as a PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
SOURCES = {
    "som": "identity/som-triple-accreditation-lockup-color.png",
    "mem": "identity/mem25-anniversary-badge-color.png",
}
# Coordinates refer to visible alpha bounds, leaving every visible source pixel intact.
LAYOUTS = {
    "horizontal": {
        "canvas": (2400, 352),
        "placements": (("som", 120, 98, 1840), ("mem", 2080, 76, 200)),
    },
    "stacked": {
        "canvas": (1200, 356),
        "placements": (("som", 70, 50, 1060), ("mem", 542, 186, 116)),
    },
}
SURFACES = {"transparent": (0, 0, 0, 0), "cream": "#E7E0D3"}


def render(layout: str, surface: str) -> Image.Image:
    spec = LAYOUTS[layout]
    canvas = Image.new("RGBA", spec["canvas"], SURFACES[surface])
    for key, x, y, width in spec["placements"]:
        with Image.open(ASSET_DIR / SOURCES[key]) as source:
            rgba = source.convert("RGBA")
        bounds = rgba.getchannel("A").getbbox()
        if bounds is None:
            raise ValueError(f"Source has no visible pixels: {key}")
        sprite = rgba.crop(bounds)
        height = round(sprite.height * width / sprite.width)
        if x < 0 or y < 0 or x + width > canvas.width or y + height > canvas.height:
            raise ValueError(f"Placement exceeds canvas: {key}")
        sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
        canvas.alpha_composite(sprite, (x, y))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout", choices=LAYOUTS, required=True)
    parser.add_argument("--surface", choices=SURFACES, default="cream")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="Replace an existing output PNG.")
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output.is_relative_to(ASSET_DIR.resolve()):
        parser.error("Output must not overwrite or add to the locked asset library.")
    if output.suffix.lower() != ".png":
        parser.error("Output must have a .png extension.")
    if output.exists() and not args.force:
        parser.error("Output already exists; use --force to replace it.")
    canvas = render(args.layout, args.surface)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)
    print(f"Rendered {args.layout}/{args.surface}: {canvas.width}x{canvas.height} -> {output}")


if __name__ == "__main__":
    main()
