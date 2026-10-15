#!/usr/bin/env python3
"""Export current SOM and 25MEM identity assets from approved source masters.

The alumni association logo and old three-party lockups are retired. This
builder exports only the two current standalone identities; their layout is
chosen in the requesting material rather than reusing a retired lockup.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


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
    retired = (
        "som-alumni-association-lockup-color.png",
        "xilehui-publicity-signature-light.png",
        "xilehui-publicity-signature-dark.png",
        "masters/som-alumni-association-lockup-source.jpg",
    )
    if any((output_dir / name).exists() for name in retired):
        raise ValueError("Output contains retired identity assets; use a clean output directory.")

    output_dir.mkdir(parents=True, exist_ok=True)
    for source, name in (
        (args.som_psd, "som-triple-accreditation-lockup-color.png"),
        (args.mem_psd, "mem25-anniversary-badge-color.png"),
    ):
        with Image.open(source) as image:
            image.convert("RGBA").save(output_dir / name, optimize=True)

    (output_dir / "masters").mkdir(exist_ok=True)
    for source, name in (
        (args.som_psd, "som-triple-accreditation-lockup-master.psd"),
        (args.som_ai, "som-triple-accreditation-lockup-master.ai"),
        (args.mem_psd, "mem25-anniversary-badge-master.psd"),
    ):
        destination = output_dir / "masters" / name
        if source.resolve() != destination.resolve():
            destination.write_bytes(source.read_bytes())

    print(f"Exported current standalone identity assets in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
