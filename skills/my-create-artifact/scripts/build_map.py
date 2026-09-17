#!/usr/bin/env python3
"""Render declarative learning-map JSON into the bundled standalone template."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


DATA_MARKER = "__STUDY_MAP_DATA__"
TITLE_MARKER = "__STUDY_MAP_TITLE__"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def load_data(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit("map data must be a JSON object")
    if not isinstance(value.get("title"), str) or not value["title"].strip():
        raise SystemExit("map data needs a non-empty title")
    levels = value.get("levels")
    nodes = value.get("nodes")
    edges = value.get("edges", [])
    if not isinstance(levels, list) or not levels:
        raise SystemExit("map data needs a non-empty levels array")
    if not isinstance(nodes, list):
        raise SystemExit("map data needs a nodes array")
    if not isinstance(edges, list):
        raise SystemExit("map data edges must be an array")

    level_ids: set[str] = set()
    for level in levels:
        if not isinstance(level, dict) or not isinstance(level.get("id"), str):
            raise SystemExit("each level needs a string id")
        if level["id"] in level_ids:
            raise SystemExit(f"duplicate level id: {level['id']}")
        level_ids.add(level["id"])

    node_ids: set[str] = set()
    for node in nodes:
        if not isinstance(node, dict):
            raise SystemExit("each node must be an object")
        for key in ("id", "label", "level"):
            if not isinstance(node.get(key), str) or not node[key].strip():
                raise SystemExit(f"each node needs a non-empty string {key}")
        if node["id"] in node_ids:
            raise SystemExit(f"duplicate node id: {node['id']}")
        if node["level"] not in level_ids:
            raise SystemExit(f"node {node['id']} uses unknown level {node['level']}")
        node_ids.add(node["id"])

    for edge in edges:
        if not isinstance(edge, dict) or edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            raise SystemExit(f"edge references an unknown node: {edge!r}")

    return value


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent.parent
    template_path = (
        args.template.expanduser().resolve()
        if args.template
        else script_dir / "assets" / "study-map.html"
    )
    data_path = args.data.expanduser().resolve()
    output_path = args.output.expanduser().resolve()
    if output_path.exists() and not args.force:
        raise SystemExit("output exists; pass --force to replace it")

    data = load_data(data_path)
    template = template_path.read_text(encoding="utf-8")
    if DATA_MARKER not in template or TITLE_MARKER not in template:
        raise SystemExit("template is missing a required placeholder")

    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    serialized = (
        serialized.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    title = html.escape(str(data["title"]), quote=True)
    rendered = template.replace(TITLE_MARKER, title).replace(DATA_MARKER, serialized)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(json.dumps({"output": output_path.as_posix(), "nodes": len(data["nodes"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
