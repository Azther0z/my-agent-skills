#!/usr/bin/env python3
"""Extract embedded PDF text and render pages that need session vision."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import date
from pathlib import Path

try:
    import pymupdf
except ModuleNotFoundError:
    print("PyMuPDF is missing; run scripts/run_parser.sh instead.", file=sys.stderr)
    raise SystemExit(1)


PENDING_EXIT = 2
SCHEMA_VERSION = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--session-dir", type=Path)
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


def build_markdown(source: Path, pages: list[dict[str, object]], output_dir: Path) -> str:
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
    ]
    for page in pages:
        number = int(page["page"])
        lines.extend([f"## Page {number}", f"<!-- source page: {number} -->"])
        if page["status"] == "embedded_text":
            text = str(page["text"]).rstrip()
            lines.extend(["", text if text else "[empty page]"])
        else:
            image = str(page["image_path"])
            lines.extend(
                [
                    "",
                    f"<!-- OCR_PENDING page={number} image={json.dumps(image)} -->",
                    "[OCR pending: transcribe this rendered page with the session vision handoff.]",
                ]
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    source = args.input.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    session_dir = (
        args.session_dir.expanduser().resolve()
        if args.session_dir
        else output_dir.parent / ".pdf-parser" / source.name
    )
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
    session_dir.mkdir(parents=True, exist_ok=True)
    languages = [item.strip() for item in args.languages.split(",") if item.strip()]
    if not languages:
        raise SystemExit("--languages must contain at least one language")

    pages: list[dict[str, object]] = []
    version = getattr(pymupdf, "VersionBind", None)
    page_count: int | None = None
    manifest = {
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
        },
        "page_count": page_count,
        "pages": [
            {key: value for key, value in page.items() if key != "text"}
            for page in pages
        ],
        "errors": [],
    }

    try:
        with pymupdf.open(source) as document:
            page_count = document.page_count
            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text", sort=True).strip()
                if is_usable(text, args.min_text_chars):
                    pages.append(
                        {
                            "page": page_number,
                            "status": "embedded_text",
                            "text": text,
                            "embedded_text_chars": len(text),
                            "image_path": None,
                            "ocr": None,
                        }
                    )
                    continue

                image_path = session_dir / f"page-{page_number:04d}.png"
                page.get_pixmap(dpi=args.dpi, alpha=False).save(str(image_path))
                pages.append(
                    {
                        "page": page_number,
                        "status": "session_vision_pending",
                        "text": "",
                        "embedded_text_chars": len(text),
                        "image_path": relative_path(image_path, output_dir),
                        "ocr": None,
                    }
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
        print(json.dumps({"manifest": manifest_path.as_posix(), "error": str(error)}), file=sys.stderr)
        return 1

    manifest["page_count"] = page_count
    manifest["pages"] = [
        {key: value for key, value in page.items() if key != "text"}
        for page in pages
    ]
    markdown_path.write_text(build_markdown(source, pages, output_dir), encoding="utf-8")
    write_json(manifest_path, manifest)

    pending = sum(page["status"] == "session_vision_pending" for page in pages)
    print(
        json.dumps(
            {
                "markdown": markdown_path.as_posix(),
                "manifest": manifest_path.as_posix(),
                "pages": page_count,
                "pending_session_vision": pending,
            },
            ensure_ascii=False,
        )
    )
    return PENDING_EXIT if pending else 0


if __name__ == "__main__":
    raise SystemExit(main())
