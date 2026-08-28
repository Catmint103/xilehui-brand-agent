#!/usr/bin/env python3
"""Render a configurable Xilehui header/footer overlay with exact assets and text."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = SKILL_ROOT / "assets" / "default-config.json"
VALID_SCENARIOS = {"general", "peripheral-promo", "culture-shirt-promo"}
FUNDRAISING_SCENARIOS = {"peripheral-promo", "culture-shirt-promo"}
FUNDRAISING_NOTICE = "本品销售结余全部纳入本届活动经费"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_value(raw: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def set_dot_path(data: dict[str, Any], dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    target: Any = data
    for part in parts[:-1]:
        if not isinstance(target, dict) or part not in target:
            raise KeyError(f"Unknown configuration key: {dotted_key}")
        target = target[part]
    if not isinstance(target, dict) or parts[-1] not in target:
        raise KeyError(f"Unknown configuration key: {dotted_key}")
    target[parts[-1]] = value


def apply_overrides(config: dict[str, Any], overrides: list[str]) -> None:
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"Override must use key=value: {item}")
        key, raw = item.split("=", 1)
        set_dot_path(config, key.strip(), parse_value(raw.strip()))


def apply_scenario_rules(config: dict[str, Any]) -> None:
    scenario = str(config.get("scenario", "general"))
    if scenario not in VALID_SCENARIOS:
        raise ValueError(
            f"Unknown scenario '{scenario}'. Available: {sorted(VALID_SCENARIOS)}"
        )
    if scenario in FUNDRAISING_SCENARIOS:
        config["text"]["footer_line_2"]["content"] = FUNDRAISING_NOTICE


def validate_output_prefix(raw: Any) -> str:
    if not isinstance(raw, str):
        raise ValueError("output.prefix must be a string.")
    prefix = raw
    if (
        not prefix
        or prefix in {".", ".."}
        or "/" in prefix
        or "\\" in prefix
        or Path(prefix).is_absolute()
    ):
        raise ValueError("output.prefix must be a plain file-name prefix without path separators.")
    return prefix


def resolve_path(raw: str, config_dir: Path) -> Path:
    path = Path(raw).expanduser()
    candidates = [path] if path.is_absolute() else [config_dir / path, SKILL_ROOT / path]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    raise FileNotFoundError(f"Asset or font not found: {raw}")


def resolve_font(config: dict[str, Any], font_key: str, size: int, config_dir: Path) -> ImageFont.FreeTypeFont:
    candidates = config.get("fonts", {}).get(font_key)
    if isinstance(candidates, str):
        candidates = [candidates]
    if not candidates:
        raise ValueError(f"No font candidates configured for: {font_key}")
    for candidate in candidates:
        if isinstance(candidate, str):
            raw = candidate
            index = 0
        elif isinstance(candidate, dict):
            raw = candidate.get("path")
            index = candidate.get("index", 0)
            if not isinstance(raw, str) or not raw:
                raise ValueError(f"Font candidate for '{font_key}' must include a non-empty path.")
            if not isinstance(index, int) or index < 0:
                raise ValueError(f"Font candidate index for '{font_key}' must be a non-negative integer.")
        else:
            raise ValueError(f"Font candidate for '{font_key}' must be a path or an object.")
        try:
            path = resolve_path(raw, config_dir)
            return ImageFont.truetype(str(path), size=size, index=index)
        except (FileNotFoundError, OSError):
            continue
    raise FileNotFoundError(
        f"No usable font found for '{font_key}'. Add a local .ttf or .ttc path under fonts.{font_key}."
    )


def crop_alpha(image: Image.Image, pad: int = 0) -> Image.Image:
    rgba = image.convert("RGBA")
    box = rgba.getbbox()
    if not box:
        return rgba
    left, top, right, bottom = box
    return rgba.crop(
        (
            max(0, left - pad),
            max(0, top - pad),
            min(rgba.width, right + pad),
            min(rgba.height, bottom + pad),
        )
    )


def white_to_alpha(image: Image.Image, threshold: int = 246) -> Image.Image:
    rgba = image.convert("RGBA")
    red, green, blue, original_alpha = rgba.split()
    minimum = ImageChops.darker(ImageChops.darker(red, green), blue)
    alpha = minimum.point(lambda value: 0 if value >= threshold else min(255, max(0, (threshold - value) * 16)))
    rgba.putalpha(ImageChops.darker(alpha, original_alpha))
    return crop_alpha(rgba, 8)


def tint_image(image: Image.Image, color: str) -> Image.Image:
    ImageColor.getrgb(color)
    tinted = Image.new("RGBA", image.size, color)
    tinted.putalpha(image.getchannel("A"))
    return tinted


def contain(image: Image.Image, box: list[int]) -> tuple[Image.Image, tuple[int, int]]:
    x, y, width, height = [int(value) for value in box]
    if width <= 0 or height <= 0:
        raise ValueError(f"Asset box must have positive size: {box}")
    scale = min(width / image.width, height / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    resized = image.resize(size, Image.Resampling.LANCZOS)
    return resized, (x + (width - size[0]) // 2, y + (height - size[1]) // 2)


def load_asset(asset_config: dict[str, Any], config_dir: Path) -> Image.Image:
    custom_path = asset_config.get("custom_path")
    if custom_path:
        raw_path = custom_path
    else:
        variant = asset_config.get("variant")
        variants = asset_config.get("variants", {})
        if variant not in variants:
            raise ValueError(f"Unknown asset variant '{variant}'. Available: {sorted(variants)}")
        raw_path = variants[variant]
    image = Image.open(resolve_path(raw_path, config_dir)).convert("RGBA")
    image = white_to_alpha(image) if asset_config.get("remove_white", False) else crop_alpha(image)
    tint = asset_config.get("tint")
    return tint_image(image, tint) if tint else image


def paste_asset(canvas: Image.Image, asset_config: dict[str, Any], config_dir: Path) -> None:
    if not asset_config.get("visible", True):
        return
    image = load_asset(asset_config, config_dir)
    resized, position = contain(image, asset_config["box"])
    canvas.alpha_composite(resized, position)


def color_value(config: dict[str, Any], raw: str) -> str:
    value = config.get("colors", {}).get(raw, raw)
    ImageColor.getrgb(value)
    return value


def tracked_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, tracking: float) -> float:
    return sum(draw.textlength(character, font=font) for character in text) + tracking * max(0, len(text) - 1)


def draw_tracked(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    tracking: float,
) -> None:
    cursor = x
    for character in text:
        draw.text((cursor, y), character, font=font, fill=fill)
        cursor += draw.textlength(character, font=font) + tracking


def draw_text_block(canvas: Image.Image, config: dict[str, Any], block: dict[str, Any], config_dir: Path) -> None:
    content = str(block.get("content", ""))
    if not content:
        return
    draw = ImageDraw.Draw(canvas)
    font = resolve_font(config, block["font"], int(block["size"]), config_dir)
    tracking = float(block.get("tracking", 0))
    x = float(block["x"])
    if block.get("align", "left") == "center":
        x -= tracked_width(draw, content, font, tracking) / 2
    draw_tracked(draw, x, float(block["y"]), content, font, color_value(config, block["color"]), tracking)


def draw_divider(canvas: Image.Image, config: dict[str, Any], divider: dict[str, Any]) -> None:
    if divider.get("visible", True):
        ImageDraw.Draw(canvas).line(
            tuple(int(value) for value in divider["xy"]),
            fill=color_value(config, divider["color"]),
            width=int(divider["width"]),
        )


def validate_config(config: dict[str, Any]) -> None:
    canvas = config["canvas"]
    width = int(canvas["width"])
    height = int(canvas["height"])
    header_height = int(canvas["header_height"])
    footer_height = int(canvas["footer_height"])
    if min(width, height, header_height, footer_height) <= 0:
        raise ValueError("Canvas dimensions must be positive.")
    if header_height + footer_height >= height:
        raise ValueError("Header and footer must leave a non-empty transparent middle region.")


def render(config: dict[str, Any], config_dir: Path, output_dir: Path) -> list[Path]:
    config = copy.deepcopy(config)
    apply_scenario_rules(config)
    prefix = validate_output_prefix(
        config.get("output", {}).get("prefix", "xilehui-header-footer")
    )
    validate_config(config)
    canvas = config["canvas"]
    width = int(canvas["width"])
    height = int(canvas["height"])
    header_height = int(canvas["header_height"])
    footer_height = int(canvas["footer_height"])
    background = color_value(config, "background")

    header = Image.new("RGBA", (width, header_height), background)
    footer = Image.new("RGBA", (width, footer_height), background)
    paste_asset(header, config["assets"]["seal"], config_dir)
    paste_asset(header, config["assets"]["logo"], config_dir)

    for key in ("organization", "event", "english"):
        draw_text_block(header, config, config["text"][key], config_dir)
    for key in ("footer_line_1", "footer_line_2"):
        draw_text_block(footer, config, config["text"][key], config_dir)
    draw_divider(header, config, config["dividers"]["header"])
    draw_divider(footer, config, config["dividers"]["footer"])

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    overlay.alpha_composite(header, (0, 0))
    overlay.alpha_composite(footer, (0, height - footer_height))

    alpha = overlay.getchannel("A")
    if alpha.crop((0, header_height, width, height - footer_height)).getextrema() != (0, 0):
        raise RuntimeError("Transparent middle validation failed.")
    if alpha.crop((0, 0, width, header_height)).getextrema() != (255, 255):
        raise RuntimeError("Opaque header validation failed.")
    if alpha.crop((0, height - footer_height, width, height)).getextrema() != (255, 255):
        raise RuntimeError("Opaque footer validation failed.")

    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        output_dir / f"{prefix}-header.png",
        output_dir / f"{prefix}-footer.png",
        output_dir / f"{prefix}-overlay.png",
        output_dir / f"{prefix}-effective-config.json",
    ]
    header.save(paths[0])
    footer.save(paths[1])
    overlay.save(paths[2])
    with paths[3].open("w", encoding="utf-8") as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="Custom JSON configuration. Defaults to the packaged config.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for generated PNG and effective config files.")
    parser.add_argument("--set", dest="overrides", action="append", default=[], help="Override a dotted key with key=value; repeat as needed.")
    args = parser.parse_args()

    config_path = (args.config or DEFAULT_CONFIG).expanduser().resolve()
    config = copy.deepcopy(load_json(config_path))
    apply_overrides(config, args.overrides)
    paths = render(config, config_path.parent, args.output_dir.expanduser().resolve())
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
