#!/usr/bin/env python3
"""Audit a poster against the locked 喜乐会 six-color palette."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys

from PIL import Image


PALETTE = {
    "burgundy": (0x4A, 0x14, 0x20),
    "wine": (0x7A, 0x2E, 0x3D),
    "champagne-gold": (0xA9, 0x97, 0x6A),
    "blue-gray": (0x4F, 0x62, 0x72),
    "stone-beige": (0xE7, 0xE0, 0xD3),
    "charcoal": (0x2E, 0x2A, 0x26),
}


def distance(left: tuple[int, int, int], right: tuple[int, int, int]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def nearest_brand_color(pixel: tuple[int, int, int]) -> tuple[str, float]:
    choices = [(name, distance(pixel, rgb)) for name, rgb in PALETTE.items()]
    return min(choices, key=lambda item: item[1])


def audit(args: argparse.Namespace) -> int:
    source = Path(args.image).expanduser().resolve()
    with Image.open(source) as image:
        rgba = image.convert("RGBA")
        rgba.thumbnail((args.max_side, args.max_side), Image.Resampling.LANCZOS)
        data = (
            rgba.get_flattened_data()
            if hasattr(rgba, "get_flattened_data")
            else rgba.getdata()
        )
        pixels = [
            rgb[:3]
            for rgb in data
            if rgb[3] >= args.min_alpha
        ]

    if not pixels:
        raise ValueError("image has no visible pixels")

    counts: Counter[str] = Counter()
    close_counts: Counter[str] = Counter()
    total_distance = 0.0
    close = 0
    for pixel in pixels:
        name, gap = nearest_brand_color(pixel)
        counts[name] += 1
        total_distance += gap
        if gap <= args.tolerance:
            close += 1
            close_counts[name] += 1

    total = len(pixels)
    near_white_ratio = sum(
        1 for red, green, blue in pixels if red >= 245 and green >= 245 and blue >= 245
    ) / total
    close_ratio = close / total
    close_denominator = max(close, 1)
    shares = {
        name: close_counts[name] / close_denominator for name in PALETTE
    }
    red_share = shares["burgundy"] + shares["wine"]

    checks = {
        "palette_affinity": close_ratio >= args.min_affinity,
        "gold_is_accent": shares["champagne-gold"] <= 0.25,
        "blue_gray_is_minor": shares["blue-gray"] <= 0.12,
        "pure_white_is_limited": near_white_ratio <= (0.18 if args.mode == "dark" else 0.25),
    }
    if args.mode == "dark":
        checks["dark_primary_balance"] = red_share + shares["charcoal"] >= 0.58
    else:
        checks["light_primary_balance"] = shares["stone-beige"] >= 0.42

    report = {
        "image": str(source),
        "mode": args.mode,
        "sampled_pixels": total,
        "tolerance": args.tolerance,
        "palette_affinity": round(close_ratio, 4),
        "mean_rgb_distance": round(total_distance / total, 2),
        "near_white_ratio": round(near_white_ratio, 4),
        "brand_shares_within_tolerance": {
            name: round(value, 4) for name, value in shares.items()
        },
        "checks": checks,
        "passed": all(checks.values()),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Palette affinity: {close_ratio:.1%}")
        print(f"Mean RGB distance: {report['mean_rgb_distance']}")
        for name, share in shares.items():
            print(f"- {name}: {share:.1%}")
        for name, passed in checks.items():
            print(f"{'PASS' if passed else 'WARN'} {name}")
        print("RESULT:", "PASS" if report["passed"] else "REVIEW REQUIRED")

    if args.strict and not report["passed"]:
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    parser.add_argument("--mode", choices=("dark", "light"), default="dark")
    parser.add_argument("--tolerance", type=float, default=72.0)
    parser.add_argument("--min-affinity", type=float, default=0.72)
    parser.add_argument("--max-side", type=int, default=800)
    parser.add_argument("--min-alpha", type=int, default=16)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero when a check warns"
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(audit(build_parser().parse_args()))
