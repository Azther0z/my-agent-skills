#!/usr/bin/env python3
"""Bootstrap a user-owned PyMuPDF environment and run a PDF tool."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


PINNED_DEPENDENCY = "PyMuPDF==1.28.2"
SUPPORTED_TOOLS = {"parse_pdf.py", "crop_pdf.py"}


def python_can_import(python: Path) -> bool:
    result = subprocess.run(
        [str(python), "-c", "import pymupdf"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def ensure_environment(python: Path, cache_dir: Path) -> None:
    if python.is_file() and python_can_import(python):
        return

    cache_dir.mkdir(parents=True, exist_ok=True)
    uv = shutil.which("uv")
    if uv:
        subprocess.run([uv, "venv", str(cache_dir / "venv")], check=True)
        subprocess.run(
            [uv, "pip", "install", "--python", str(python), PINNED_DEPENDENCY],
            check=True,
        )
        return

    subprocess.run([sys.executable, "-m", "venv", str(cache_dir / "venv")], check=True)
    subprocess.run([str(python), "-m", "pip", "install", PINNED_DEPENDENCY], check=True)


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in SUPPORTED_TOOLS:
        supported = "|".join(sorted(SUPPORTED_TOOLS))
        raise SystemExit(f"usage: run_tool.py {supported} [arguments...]")

    script_dir = Path(__file__).resolve().parent
    cache_root = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache").expanduser()
    cache_dir = cache_root / "my-agent-skills" / "my-parse-pdf"
    python = cache_dir / "venv" / "bin" / "python"
    ensure_environment(python, cache_dir)

    tool = script_dir / sys.argv[1]
    os.execv(str(python), [str(python), str(tool), *sys.argv[2:]])


if __name__ == "__main__":
    main()
