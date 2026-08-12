#!/usr/bin/env python3
"""List, verify, and tint the locked 喜乐会 brand assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageChops, ImageOps


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_DIR = SKILL_DIR / "assets"
MANIFEST_PATH = ASSET_DIR / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def list_assets(_: argparse.Namespace) -> int:
    manifest = load_manifest()
    for relative, meta in manifest["files"].items():
        print(
            f"{relative}\t{meta['width']}x{meta['height']}\t"
            f"{meta['mode']}\t{meta['sha256']}"
        )
    return 0


def verify_assets(_: argparse.Namespace) -> int:
    manifest = load_manifest()
    errors: list[str] = []
    for relative, expected in manifest["files"].items():
        path = ASSET_DIR / relative
        if not path.is_file():
            errors.append(f"missing: {relative}")
            continue
        actual_hash = sha256(path)
        if actual_hash != expected["sha256"]:
            errors.append(
                f"hash mismatch: {relative}\n"
                f"  expected {expected['sha256']}\n  actual   {actual_hash}"
            )
            continue
        try:
            with Image.open(path) as image:
                if list(image.size) != [expected["width"], expected["height"]]:
                    errors.append(
                        f"size mismatch: {relative}: {image.size} != "
                        f"({expected['width']}, {expected['height']})"
                    )
                if image.mode != expected["mode"]:
                    errors.append(
                        f"mode mismatch: {relative}: {image.mode} != {expected['mode']}"
                    )
        except Exception as exc:  # pragma: no cover - diagnostic path
            errors.append(f"unreadable image: {relative}: {exc}")

    locked_sources = {
        "som-triple-accreditation-psd": (
            ASSET_DIR / "identity" / "masters" / "som-triple-accreditation-lockup-master.psd"
        ),
        "som-triple-accreditation-ai": (
            ASSET_DIR / "identity" / "masters" / "som-triple-accreditation-lockup-master.ai"
        ),
        "mem25-anniversary-psd": (
            ASSET_DIR / "identity" / "masters" / "mem25-anniversary-badge-master.psd"
        ),
    }
    verified_sources = 0
    for source_name, source_path in locked_sources.items():
        expected_hash = manifest.get("sources", {}).get(source_name)
        if expected_hash is None:
            errors.append(f"missing source hash in manifest: {source_name}")
            continue
        if not source_path.is_file():
            errors.append(f"missing source master: {source_path.relative_to(ASSET_DIR)}")
            continue
        verified_sources += 1
        actual_hash = sha256(source_path)
        if actual_hash != expected_hash:
            errors.append(
                f"source hash mismatch: {source_path.relative_to(ASSET_DIR)}\n"
                f"  expected {expected_hash}\n  actual   {actual_hash}"
            )

    if errors:
        print("Brand asset verification FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Brand asset verification passed: {len(manifest['files'])} image files, "
        f"{verified_sources} source masters"
    )
    return 0


def parse_hex_color(value: str) -> tuple[int, int, int]:
    raw = value.strip().lstrip("#")
    if len(raw) != 6:
        raise argparse.ArgumentTypeError("color must be a six-digit hex value")
    try:
        return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("invalid hex color") from exc


def flattened(image: Image.Image):
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()


def tint_asset(args: argparse.Namespace) -> int:
    source = Path(args.input).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if source == output:
        raise ValueError("output must not overwrite the locked source asset")
    if not source.is_file():
        raise FileNotFoundError(source)
    if output.exists() and not args.force:
        raise FileExistsError(f"output already exists; pass --force to replace it: {output}")

    with Image.open(source) as original:
        rgba = original.convert("RGBA")
        source_alpha = rgba.getchannel("A")
        luminance = ImageOps.grayscale(rgba.convert("RGB"))
        if args.polarity == "auto":
            width, height = luminance.size
            border = list(flattened(luminance.crop((0, 0, width, 1))))
            border += list(flattened(luminance.crop((0, height - 1, width, height))))
            border += list(flattened(luminance.crop((0, 0, 1, height))))
            border += list(flattened(luminance.crop((width - 1, 0, width, height))))
            border_mean = sum(border) / max(len(border), 1)
            polarity = "light-on-dark" if border_mean < 128 else "dark-on-light"
        else:
            polarity = args.polarity
        ink = luminance if polarity == "light-on-dark" else ImageOps.invert(luminance)

        if args.min_ink:
            cutoff = args.min_ink
            ink = ink.point(
                lambda value: 0
                if value <= cutoff
                else round((value - cutoff) * 255 / (255 - cutoff))
            )

        alpha = ImageChops.multiply(ink, source_alpha)
        opacity = max(0.0, min(1.0, args.opacity))
        alpha = alpha.point(lambda value: round(value * opacity))

        layer = Image.new("RGBA", rgba.size, (*args.color, 255))
        layer.putalpha(alpha)
        output.parent.mkdir(parents=True, exist_ok=True)
        layer.save(output)

    print(
        f"Tinted without resizing: {source} -> {output} "
        f"({layer.size[0]}x{layer.size[1]}, {polarity})"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list locked assets and hashes")
    list_parser.set_defaults(func=list_assets)

    verify_parser = subparsers.add_parser("verify", help="verify hashes and dimensions")
    verify_parser.set_defaults(func=verify_assets)

    tint_parser = subparsers.add_parser(
        "tint", help="create a transparent monochrome line layer without resizing"
    )
    tint_parser.add_argument("input")
    tint_parser.add_argument("output")
    tint_parser.add_argument("--color", type=parse_hex_color, default="#A9976A")
    tint_parser.add_argument("--opacity", type=float, default=1.0)
    tint_parser.add_argument("--force", action="store_true")
    tint_parser.add_argument(
        "--polarity",
        choices=("auto", "dark-on-light", "light-on-dark"),
        default="auto",
        help="select whether the linework is darker or lighter than its background",
    )
    tint_parser.add_argument(
        "--min-ink",
        type=int,
        default=3,
        choices=range(0, 255),
        metavar="0-254",
        help="remove near-white background noise while preserving line geometry",
    )
    tint_parser.set_defaults(func=tint_asset)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
