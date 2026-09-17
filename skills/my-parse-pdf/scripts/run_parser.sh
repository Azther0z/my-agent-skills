#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/my-agent-skills/my-parse-pdf"
venv="$cache_dir/venv"

if test ! -x "$venv/bin/python"; then
  mkdir -p "$cache_dir"
  if command -v uv >/dev/null 2>&1; then
    uv venv "$venv"
    uv pip install --python "$venv/bin/python" 'PyMuPDF==1.28.2'
  else
    python3 -m venv "$venv"
    "$venv/bin/python" -m pip install 'PyMuPDF==1.28.2'
  fi
fi

exec "$venv/bin/python" "$script_dir/parse_pdf.py" "$@"
