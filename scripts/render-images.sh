#!/usr/bin/env bash
# Renders src/**/*.drawio into a mirrored auto-images/**/*.svg tree using the
# draw.io desktop CLI, stamps each render with its provenance, and removes
# any auto-images/ renders whose source .drawio no longer exists.
#
# Usage:
#   scripts/render-images.sh --all              render every src/**/*.drawio
#   scripts/render-images.sh file1.drawio ...    render only these (repo-relative paths)
#   scripts/render-images.sh                     render nothing, just run orphan cleanup
#
# Requires the `drawio` desktop CLI on PATH (or $DRAWIO_BIN pointing at it):
# macOS: brew install --cask drawio
# Linux: install the matching drawio-desktop .deb release + xvfb, see
#        .github/workflows/sync-diagrams.yml for the pinned version.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

DRAWIO_BIN="${DRAWIO_BIN:-drawio}"
SRC_DIR="src"
OUT_DIR="auto-images"

files=()
if [ "${1:-}" = "--all" ]; then
  while IFS= read -r f; do
    files+=("$f")
  done < <(find "$SRC_DIR" -type f -name '*.drawio' | sort)
else
  files=("$@")
fi

if [ "${#files[@]}" -gt 0 ]; then
  if ! command -v "$DRAWIO_BIN" >/dev/null 2>&1; then
    echo "error: '$DRAWIO_BIN' not found on PATH." >&2
    echo "  macOS: brew install --cask drawio" >&2
    echo "  Linux: install the pinned drawio-desktop .deb (see .github/workflows/sync-diagrams.yml)" >&2
    exit 1
  fi

  commit_sha="$(git rev-parse HEAD)"
  rendered_at="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

  for src_file in "${files[@]}"; do
    rel="${src_file#"$SRC_DIR"/}"
    dest="$OUT_DIR/${rel%.drawio}.svg"
    mkdir -p "$(dirname "$dest")"

    echo "Rendering $src_file -> $dest"
    if command -v xvfb-run >/dev/null 2>&1; then
      xvfb-run -a "$DRAWIO_BIN" -x -f svg -t -o "$dest" "$src_file"
    else
      "$DRAWIO_BIN" -x -f svg -t -o "$dest" "$src_file"
    fi

    comment="<!-- rendered from ${src_file} at commit ${commit_sha} on ${rendered_at} -->"
    tmp="$(mktemp)"
    { head -n 2 "$dest"; echo "$comment"; tail -n +3 "$dest"; } > "$tmp"
    mv "$tmp" "$dest"
  done
fi

# Orphan cleanup always runs: a deleted .drawio file has no "changed" render
# to trigger, but its stale auto-images/ render still needs to go.
if [ -d "$OUT_DIR" ]; then
  while IFS= read -r f; do
    rel="${f#"$OUT_DIR"/}"
    src_equiv="$SRC_DIR/${rel%.svg}.drawio"
    if [ ! -f "$src_equiv" ]; then
      echo "Removing orphaned render: $f (no matching $src_equiv)"
      rm "$f"
    fi
  done < <(find "$OUT_DIR" -type f -name '*.svg')
  find "$OUT_DIR" -mindepth 1 -type d -empty -delete
fi
