#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

from PIL import Image
import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "create-xilehui-brand-poster"


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_skill_metadata() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter is missing")
    metadata = yaml.safe_load(match.group(1))
    if set(metadata) != {"name", "description"}:
        fail(f"Unexpected SKILL.md fields: {sorted(metadata)}")
    if metadata["name"] != "create-xilehui-brand-poster":
        fail("Skill name does not match its directory")

    interface = yaml.safe_load((SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    prompt = interface["interface"]["default_prompt"]
    if "$create-xilehui-brand-poster" not in prompt:
        fail("openai.yaml default_prompt must mention the skill")


def check_assets() -> None:
    manifest_path = SKILL / "assets" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative, expected in manifest["files"].items():
        path = SKILL / "assets" / relative
        if not path.is_file():
            fail(f"Missing asset: {relative}")
        if sha256(path) != expected["sha256"]:
            fail(f"Asset hash mismatch: {relative}")
        with Image.open(path) as image:
            if list(image.size) != [expected["width"], expected["height"]]:
                fail(f"Asset dimensions mismatch: {relative}")
            if image.mode != expected["mode"]:
                fail(f"Asset mode mismatch: {relative}")

    for source_name, expected_hash in manifest.get("sources", {}).items():
        source_path = {
            "som-triple-accreditation-psd": SKILL / "assets" / "identity" / "masters" / "som-triple-accreditation-lockup-master.psd",
            "som-triple-accreditation-ai": SKILL / "assets" / "identity" / "masters" / "som-triple-accreditation-lockup-master.ai",
            "mem25-anniversary-psd": SKILL / "assets" / "identity" / "masters" / "mem25-anniversary-badge-master.psd",
        }.get(source_name)
        if source_path is None:
            continue
        if not source_path.is_file():
            fail(f"Missing source master: {source_path.relative_to(SKILL)}")
        if sha256(source_path) != expected_hash:
            fail(f"Source master hash mismatch: {source_path.relative_to(SKILL)}")


def check_copywriting_knowledge() -> None:
    path = SKILL / "references" / "copywriting-library.md"
    if not path.is_file():
        fail("Copywriting knowledge base is missing")

    text = path.read_text(encoding="utf-8")
    required = (
        "281a2d71d92e67d166ec07c916b2b09bf83e05388ef5f45fcbda9b05352a2023",
        "39f4cc1538f69ccf3fb579804b2cd572d77666b25c0f07756d958a6b542e4aaa",
        "## 推文文案原文",
        "## 邀请函文案原文",
        "香格里拉酒店",
        "具体时段和地点列为待确认",
        "current-campaign.md",
    )
    for phrase in required:
        if phrase not in text:
            fail(f"Copywriting knowledge base omits required provenance or guardrail: {phrase}")

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    if "references/copywriting-library.md" not in skill_text:
        fail("SKILL.md does not route copywriting tasks to the knowledge base")


def check_portability() -> None:
    forbidden = (
        "/" + "Users" + "/",
        "/var/" + "folders" + "/",
        "Documents" + "/MEM",
    )
    suffixes = {".md", ".py", ".sh", ".yaml", ".yml", ".json", ".html", ".css", ".js"}
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if (
            not path.is_file()
            or path.suffix.lower() not in suffixes
            or ".git" in path.parts
            or ".venv" in path.parts
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for token in forbidden:
            if token.lower() in text.lower():
                findings.append(f"{path.relative_to(ROOT)}: {token}")
    if findings:
        fail("Non-portable or forbidden references:\n" + "\n".join(findings))


def check_required_files() -> None:
    required = [
        ROOT / "AGENTS.md",
        ROOT / "install.sh",
        ROOT / "README.md",
        ROOT / "ASSET-LICENSE.md",
        SKILL / "references" / "creative-routing.md",
        SKILL / "references" / "aesthetic-acceptance.md",
        SKILL / "references" / "copywriting-library.md",
        SKILL / "references" / "signature-lockup.md",
        SKILL / "scripts" / "brand_assets.py",
        SKILL / "scripts" / "palette_audit.py",
        ROOT / "scripts" / "build_co_brand_assets.py",
        ROOT / "docs" / "index.html",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))


def main() -> int:
    checks = [
        check_skill_metadata,
        check_assets,
        check_copywriting_knowledge,
        check_portability,
        check_required_files,
    ]
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print("Package validation passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
