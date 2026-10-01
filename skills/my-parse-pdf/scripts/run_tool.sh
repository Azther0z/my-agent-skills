#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
entrypoint=${1:-}
if test -z "$entrypoint"; then
    echo "usage: run_tool.sh parse_pdf.py|crop_pdf.py [arguments...]" >&2
    exit 2
fi
shift

case "$entrypoint" in
    parse_pdf.py|crop_pdf.py) ;;
    *)
        echo "unsupported parser tool: $entrypoint" >&2
        exit 2
        ;;
esac

cache_dir="${XDG_CACHE_HOME:-$HOME/.cache}/my-agent-skills/my-parse-pdf"
venv="$cache_dir/venv"

if test ! -x "$venv/bin/python" || ! "$venv/bin/python" -c 'import pymupdf' >/dev/null 2>&1; then
    mkdir -p "$cache_dir"
    if command -v uv >/dev/null 2>&1; then
        uv venv "$venv"
        uv pip install --python "$venv/bin/python" 'PyMuPDF==1.28.2'
    else
        python3 -m venv "$venv"
        "$venv/bin/python" -m pip install 'PyMuPDF==1.28.2'
    fi
fi

exec "$venv/bin/python" "$script_dir/$entrypoint" "$@"
