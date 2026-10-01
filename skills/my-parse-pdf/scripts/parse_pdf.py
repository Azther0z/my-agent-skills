#!/usr/bin/env python3
"""Extract PDF text and generate visual evidence for every page."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    import pymupdf
except ModuleNotFoundError:
    print(
        "PyMuPDF is missing; run scripts/run_tool.py parse_pdf.py instead.",
        file=sys.stderr,
    )
    raise SystemExit(1)


SCHEMA_VERSION = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--languages", default="en,th")
    parser.add_argument("--dpi", default=200, type=int)
    parser.add_argument("--min-text-chars", default=24, type=int)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def relative_path(path: Path, start: Path) -> str:
    try:
        return Path(os.path.relpath(path, start)).as_posix()
    except ValueError:
        return path.as_posix()


def is_usable(text: str, minimum: int) -> bool:
    return len(" ".join(text.split())) >= minimum


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def rect_values(rect: Any) -> list[float]:
    return [round(float(value), 2) for value in (rect.x0, rect.y0, rect.x1, rect.y1)]


def safe_extension(value: object) -> str:
    extension = str(value or "png").lower().lstrip(".")
    if not extension.isalnum() or len(extension) > 5:
        return "png"
    return extension


def build_markdown(source: Path, pages: list[dict[str, object]]) -> str:
    lines = [
        "---",
        "type: raw",
        f"source: {yaml_string(source.name)}",
        f"collected: {date.today().isoformat()}",
        "published: null",
        "---",
        "",
        f"# {source.name}",
        "",
        "<!-- Deterministic draft: complete the direct visual review before publishing. -->",
        "",
    ]
    for page in pages:
        number = int(page["page"])
        lines.extend([f"## Page {number}", f"<!-- source page: {number} -->"])
        text = str(page["text"]).rstrip()
        if text:
            lines.extend(["", text])
        else:
            lines.extend(
                [
                    "",
                    "[No usable embedded text. Inspect the source page render and add a direct visual transcription or an explicit gap.]",
                ]
            )

        visual_candidate = bool(page["visual_candidate"])
        if visual_candidate or not text:
            rendered_page = str(page["rendered_page"])
            lines.extend(
                [
                    "",
                    "### Source visual evidence",
                    f"![Source page {number}]({rendered_page})",
                ]
            )
            for index, image in enumerate(page["images"], start=1):
                if not isinstance(image, dict) or not image.get("path"):
                    continue
                lines.append(
                    f"![Embedded source image {number}.{index}]({image['path']})"
                )
            lines.extend(
                [
                    "",
                    "<!-- Complete the direct visual review. Add source crops, labeled reconstructions, or explicit gap markers as needed. -->",
                ]
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def page_text_blocks(page: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        page_dict = page.get_text("dict", sort=True)
    except TypeError:
        page_dict = page.get_text("dict")

    blocks: list[dict[str, Any]] = []
    for block in page_dict.get("blocks", []):
        if block.get("type") != 0:
            continue
        text = str(block.get("text", "")).strip()
        bbox = block.get("bbox")
        if not bbox or not text:
            continue
        blocks.append(
            {
                "bbox": [round(float(value), 2) for value in bbox],
                "chars": len(text),
            }
        )
    return page_dict, blocks


def extract_image_blocks(
    page_dict: dict[str, Any], page_number: int, image_dir: Path, output_dir: Path
) -> list[dict[str, Any]]:
    image_dir.mkdir(parents=True, exist_ok=True)
    images: list[dict[str, Any]] = []
    image_index = 0
    for block in page_dict.get("blocks", []):
        if block.get("type") != 1:
            continue
        image_index += 1
        raw_image = block.get("image")
        bbox = block.get("bbox")
        item: dict[str, Any] = {
            "index": image_index,
            "bbox": [round(float(value), 2) for value in bbox]
            if bbox
            else None,
            "width": block.get("width"),
            "height": block.get("height"),
            "ext": safe_extension(block.get("ext")),
            "path": None,
        }
        if isinstance(raw_image, (bytes, bytearray)) and raw_image:
            extension = safe_extension(block.get("ext"))
            asset = image_dir / (
                f"page-{page_number:04d}-image-{image_index:02d}.{extension}"
            )
            asset.write_bytes(bytes(raw_image))
            item["path"] = relative_path(asset, output_dir)
            item["sha256"] = sha256_bytes(bytes(raw_image))
            item["bytes"] = len(raw_image)
        images.append(item)
    return images


def drawing_inventory(page: Any) -> dict[str, Any]:
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []
    bboxes: list[dict[str, Any]] = []
    item_count = 0
    for drawing in drawings:
        rect = drawing.get("rect")
        items = drawing.get("items") or []
        item_count += len(items)
        if rect:
            bboxes.append(
                {
                    "bbox": rect_values(rect),
                    "items": len(items),
                    "type": drawing.get("type"),
                }
            )
    return {
        "count": len(drawings),
        "items": item_count,
        "bboxes": bboxes,
    }


def page_record(
    page: Any,
    page_number: int,
    output_dir: Path,
    pages_dir: Path,
    embedded_dir: Path,
    minimum: int,
    dpi: int,
) -> dict[str, Any]:
    text = page.get_text("text", sort=True).strip()
    page_dict, text_blocks = page_text_blocks(page)
    images = extract_image_blocks(page_dict, page_number, embedded_dir, output_dir)
    drawings = drawing_inventory(page)

    rendered = pages_dir / f"page-{page_number:04d}.png"
    page.get_pixmap(dpi=dpi, alpha=False).save(str(rendered))

    reasons: list[str] = []
    if not is_usable(text, minimum):
        reasons.append("no_usable_embedded_text")
    if images:
        reasons.append("embedded_images")
    if drawings["count"]:
        reasons.append("vector_drawings")

    return {
        "page": page_number,
        "status": "embedded_text" if is_usable(text, minimum) else "visual_only",
        "agent_review": {
            "status": "required",
            "method": None,
            "artifacts": [],
            "gaps": [],
        },
        "rotation": int(page.rotation),
        "dimensions": {
            "width": round(float(page.rect.width), 2),
            "height": round(float(page.rect.height), 2),
            "unit": "pt",
        },
        "embedded_text_chars": len(text),
        "text_blocks": text_blocks,
        "rendered_page": relative_path(rendered, output_dir),
        "images": images,
        "drawings": drawings,
        "visual_candidate": bool(reasons),
        "visual_reasons": reasons,
        "text": text,
    }


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    markdown_path = output_dir / f"{source.name}.md"
    manifest_path = output_dir / f"{source.name}.manifest.json"

    if not source.is_file():
        raise SystemExit(f"input PDF not found: {source}")
    if args.dpi < 72 or args.dpi > 600:
        raise SystemExit("--dpi must be between 72 and 600")
    if args.min_text_chars < 0:
        raise SystemExit("--min-text-chars must not be negative")
    if not args.force and (markdown_path.exists() or manifest_path.exists()):
        raise SystemExit("derivatives exist; pass --force to replace them")

    output_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = output_dir / "assets" / "pages"
    embedded_dir = output_dir / "assets" / "embedded"
    pages_dir.mkdir(parents=True, exist_ok=True)
    embedded_dir.mkdir(parents=True, exist_ok=True)
    languages = [item.strip() for item in args.languages.split(",") if item.strip()]
    if not languages:
        raise SystemExit("--languages must contain at least one language")

    pages: list[dict[str, Any]] = []
    page_count: int | None = None
    version = getattr(pymupdf, "VersionBind", None)
    manifest: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "name": source.name,
            "sha256": sha256(source),
            "size_bytes": source.stat().st_size,
        },
        "languages": languages,
        "renderer": {
            "library": "PyMuPDF",
            "version": version,
            "dpi": args.dpi,
            "min_text_chars": args.min_text_chars,
            "page_assets": "assets/pages",
            "embedded_assets": "assets/embedded",
        },
        "page_count": page_count,
        "pages": [],
        "errors": [],
    }

    try:
        with pymupdf.open(source) as document:
            page_count = document.page_count
            for page_number, page in enumerate(document, start=1):
                pages.append(
                    page_record(
                        page,
                        page_number,
                        output_dir,
                        pages_dir,
                        embedded_dir,
                        args.min_text_chars,
                        args.dpi,
                    )
                )
    except Exception as error:
        manifest["page_count"] = page_count
        manifest["pages"] = [
            {key: value for key, value in page.items() if key != "text"}
            for page in pages
        ]
        manifest["errors"] = [
            {"type": type(error).__name__, "message": str(error) or "unreadable PDF"}
        ]
        write_json(manifest_path, manifest)
        print(
            json.dumps(
                {"manifest": manifest_path.as_posix(), "error": str(error)},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1

    manifest["page_count"] = page_count
    manifest["pages"] = [
        {key: value for key, value in page.items() if key != "text"}
        for page in pages
    ]
    markdown_path.write_text(
        build_markdown(source, pages), encoding="utf-8"
    )
    write_json(manifest_path, manifest)

    print(
        json.dumps(
            {
                "markdown": markdown_path.as_posix(),
                "manifest": manifest_path.as_posix(),
                "pages": page_count,
                "visual_review_required": page_count,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
