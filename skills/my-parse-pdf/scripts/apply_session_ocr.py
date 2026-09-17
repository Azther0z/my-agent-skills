#!/usr/bin/env python3
"""Apply explicit in-session vision transcriptions to PDF derivatives."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--responses", required=True, type=Path)
    parser.add_argument("--response-dir", required=True, type=Path)
    return parser.parse_args()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def relative_path(path: Path, start: Path) -> str:
    try:
        return Path(os.path.relpath(path, start)).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    args = parse_args()
    markdown_path = args.markdown.expanduser().resolve()
    manifest_path = args.manifest.expanduser().resolve()
    responses_path = args.responses.expanduser().resolve()
    response_dir = args.response_dir.expanduser().resolve()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    response_doc = json.loads(responses_path.read_text(encoding="utf-8"))
    entries = response_doc.get("pages")
    if not isinstance(entries, list):
        raise SystemExit("responses file must contain a pages array")

    page_by_number = {int(page["page"]): page for page in manifest.get("pages", [])}
    pending = {
        number
        for number, page in page_by_number.items()
        if page.get("status") == "session_vision_pending"
    }
    seen: set[int] = set()
    markdown = markdown_path.read_text(encoding="utf-8")
    languages = manifest.get("languages", [])

    for entry in entries:
        if not isinstance(entry, dict):
            raise SystemExit("each response entry must be an object")
        try:
            number = int(entry["page"])
            text = entry["text"]
        except (KeyError, TypeError, ValueError) as error:
            raise SystemExit(f"invalid response entry: {entry!r}") from error
        if number in seen:
            raise SystemExit(f"duplicate response for page {number}")
        if number not in pending:
            raise SystemExit(f"page {number} is not pending session vision")
        if not isinstance(text, str) or not text.strip():
            raise SystemExit(f"page {number} needs a non-empty text transcription")
        seen.add(number)

        if "raw_response" not in entry:
            raise SystemExit(f"page {number} must include raw_response")
        raw_response = entry["raw_response"]
        sidecar = response_dir / f"page-{number:04d}.json"
        write_json(
            sidecar,
            {
                "schema_version": 1,
                "page": number,
                "backend": "in-session-vision",
                "languages": languages,
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "transcription": text,
                "raw_response": raw_response,
            },
        )

        page = page_by_number[number]
        page["status"] = "session_vision"
        page["ocr"] = {
            "backend": "in-session-vision",
            "response_path": relative_path(sidecar, manifest_path.parent),
            "text_chars": len(text),
        }
        page["image_path"] = page.get("image_path")

        pattern = re.compile(
            rf"(^## Page {number}\s*$)(.*?)(?=^## Page \d+\s*$|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        replacement = (
            f"## Page {number}\n"
            f"<!-- source page: {number} -->\n"
            "<!-- OCR via in-session vision; see the private response sidecar. -->\n\n"
            f"{text.rstrip()}\n\n"
        )
        markdown, count = pattern.subn(replacement, markdown, count=1)
        if count != 1:
            raise SystemExit(f"could not locate Markdown block for page {number}")

    manifest["pages"] = list(page_by_number.values())
    write_atomic(markdown_path, markdown)
    write_json(manifest_path, manifest)

    remaining = sum(
        page.get("status") == "session_vision_pending" for page in manifest["pages"]
    )
    print(json.dumps({"applied": len(seen), "remaining_pending": remaining}))
    return 2 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
