#!/usr/bin/env python3
"""Copy an explicit, safe allowlist into an approved static artifact root."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ALLOWED_SUFFIXES = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".md"}
PRIVATE_PARTS = {".git", ".ok", ".claude", ".codex", ".opencode", "raw", "scratchpad"}
PRIVATE_WORDS = ("manifest", "response", "ocr", "secret", "credential")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--files", required=True, nargs="+")
    parser.add_argument("--publish", action="store_true", help="confirm the explicit publish action")
    return parser.parse_args()


def safe_relative(relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise SystemExit(f"unsafe relative path: {relative}")
    if any(part.startswith(".") for part in path.parts):
        raise SystemExit(f"hidden path is not publishable: {relative}")
    return path


def safe_source(root: Path, relative: str) -> Path:
    relative_path = safe_relative(relative)
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root):
        raise SystemExit(f"file escapes source root: {relative}")
    if not candidate.is_file():
        raise SystemExit(f"source file not found: {relative}")
    original = root / relative_path
    if original.is_symlink():
        raise SystemExit(f"symlinks are not publishable: {relative}")
    if any(part in PRIVATE_PARTS for part in relative_path.parts):
        raise SystemExit(f"private path is not publishable: {relative}")
    lowered = candidate.name.lower()
    if any(word in lowered for word in PRIVATE_WORDS):
        raise SystemExit(f"private-looking filename is not publishable: {relative}")
    if candidate.suffix.lower() not in ALLOWED_SUFFIXES:
        raise SystemExit(f"file type is not publishable: {relative}")
    return candidate


def main() -> int:
    args = parse_args()
    if not args.publish:
        raise SystemExit("refusing to publish without --publish")
    source = args.source.expanduser().resolve()
    target = args.target.expanduser().resolve()
    if not source.is_dir():
        raise SystemExit(f"source directory not found: {source}")

    copied: list[str] = []
    for relative in args.files:
        candidate = safe_source(source, relative)
        relative_path = safe_relative(relative)
        destination = (target / relative_path).resolve(strict=False)
        if not destination.is_relative_to(target):
            raise SystemExit(f"target path escapes target root: {relative}")
        if (target / relative_path).is_symlink():
            raise SystemExit(f"target symlinks are not publishable: {relative}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate, destination)
        copied.append(relative)
    print(json.dumps({"target": target.as_posix(), "copied": copied}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
