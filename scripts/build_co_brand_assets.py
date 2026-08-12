#!/usr/bin/env python3
"""Build normalized 喜乐会 co-brand assets from approved source masters."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


BURGUNDY = (74, 20, 32, 255)
CHAMPAGNE = (169, 151, 106, 255)
CREAM = (231, 224, 211, 255)


def contain(image: Image.Image, box: tuple[int, int]) -> Image.Image:
    layer = image.copy()
    layer.thumbnail(box, Image.Resampling.LANCZOS)
    return layer


def place(canvas: Image.Image, image: Image.Image, xy: tuple[int, int]) -> None:
    canvas.alpha_composite(image, xy)


def render_lockup(
    som: Image.Image,
    mem: Image.Image,
    output: Path,
    *,
    plate: bool,
) -> None:
    width, height = 2400, 360
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    if plate:
        draw.rounded_rectangle(
            (2, 2, width - 3, height - 3),
            radius=34,
            fill=CREAM,
            outline=CHAMPAGNE,
            width=3,
        )

    som_layer = contain(som, (1840, 190))
    mem_layer = contain(mem, (246, 246))
    som_x = 104
    som_y = (height - som_layer.height) // 2
    divider_x = 2026
    mem_x = 2090
    mem_y = (height - mem_layer.height) // 2

    place(canvas, som_layer, (som_x, som_y))
    draw.rounded_rectangle(
        (divider_x, 78, divider_x + 3, height - 78),
        radius=2,
        fill=(*CHAMPAGNE[:3], 185),
    )
    place(canvas, mem_layer, (mem_x, mem_y))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--som-psd", type=Path, required=True)
    parser.add_argument("--som-ai", type=Path, required=True)
    parser.add_argument("--mem-psd", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    for source in (args.som_psd, args.som_ai, args.mem_psd):
        if not source.is_file():
            raise FileNotFoundError(source)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    som = Image.open(args.som_psd).convert("RGBA")
    mem = Image.open(args.mem_psd).convert("RGBA")
    som.save(output_dir / "som-triple-accreditation-lockup-color.png", optimize=True)
    mem.save(output_dir / "mem25-anniversary-badge-color.png", optimize=True)

    render_lockup(
        som,
        mem,
        output_dir / "xilehui-publicity-signature-light.png",
        plate=False,
    )
    render_lockup(
        som,
        mem,
        output_dir / "xilehui-publicity-signature-dark.png",
        plate=True,
    )

    (output_dir / "masters").mkdir(exist_ok=True)
    for source, name in (
        (args.som_psd, "som-triple-accreditation-lockup-master.psd"),
        (args.som_ai, "som-triple-accreditation-lockup-master.ai"),
        (args.mem_psd, "mem25-anniversary-badge-master.psd"),
    ):
        destination = output_dir / "masters" / name
        destination.write_bytes(source.read_bytes())

    print(f"Built normalized co-brand assets in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
