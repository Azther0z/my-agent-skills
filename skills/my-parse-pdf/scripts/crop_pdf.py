#!/usr/bin/env python3
"""Render a reproducible crop from one PDF page."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

try:
    import pymupdf
except ModuleNotFoundError:
    raise SystemExit("PyMuPDF is missing; run scripts/run_crop.sh instead.")


def parse_rect(value: str) -> tuple[float, float, float, float]:
    parts = [item for item in re.split(r"[ ,]+", value.strip()) if item]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "--rect must contain x0,y0,x1,y1 in PDF points"
        )
    try:
        values = tuple(float(item) for item in parts)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--rect values must be numbers") from error
    if values[2] <= values[0] or values[3] <= values[1]:
        raise argparse.ArgumentTypeError("--rect must have positive width and height")
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--page", required=True, type=int)
    parser.add_argument("--rect", required=True, type=parse_rect)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--dpi", default=300, type=int)
    parser.add_argument("--padding", default=0.0, type=float)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    source = args.input.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_file():
        raise SystemExit(f"input PDF not found: {source}")
    if args.page < 1:
        raise SystemExit("--page must be 1 or greater")
    if args.dpi < 72 or args.dpi > 600:
        raise SystemExit("--dpi must be between 72 and 600")
    if args.padding < 0:
        raise SystemExit("--padding must not be negative")
    if output.exists() and not args.force:
        raise SystemExit("output exists; pass --force to replace it")

    with pymupdf.open(source) as document:
        if args.page > document.page_count:
            raise SystemExit(
                f"--page {args.page} is outside the document ({document.page_count} pages)"
            )
        page = document[args.page - 1]
        x0, y0, x1, y1 = args.rect
        requested = pymupdf.Rect(
            x0 - args.padding,
            y0 - args.padding,
            x1 + args.padding,
            y1 + args.padding,
        )
        clipped = requested & page.rect
        if clipped.width <= 0 or clipped.height <= 0:
            raise SystemExit("--rect does not intersect the requested page")
        pixmap = page.get_pixmap(dpi=args.dpi, clip=clipped, alpha=False)
        output.parent.mkdir(parents=True, exist_ok=True)
        pixmap.save(str(output))

    result = {
        "page": args.page,
        "requested_rect": [round(value, 2) for value in requested],
        "clipped_rect": [round(value, 2) for value in clipped],
        "dpi": args.dpi,
        "output": output.as_posix(),
        "width_pixels": pixmap.width,
        "height_pixels": pixmap.height,
        "sha256": sha256(output),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
