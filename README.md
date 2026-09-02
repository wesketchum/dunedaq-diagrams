# dunedaq-diagrams

draw.io diagrams for DUNE DAQ, stored so they're viewable and diffable
directly on GitHub.

See [`docs/README.md`](docs/README.md) for the diagram index (previews +
edit links) and instructions for adding or editing diagrams.

## Local scripts

CI runs these on every push/PR touching `src/**/*.drawio`, but they can also
be run locally:

- `scripts/render-images.sh` renders `src/**/*.drawio` into the mirrored
  `auto-images/**/*.svg` tree. Requires the
  [draw.io desktop](https://github.com/jgraph/drawio-desktop) CLI on `PATH`
  (`brew install --cask drawio` on macOS; see the "Install draw.io desktop
  CLI" step in `.github/workflows/sync-diagrams.yml` for the Linux
  equivalent). Run with `--all` to render everything, or with specific
  `.drawio` paths to render just those.
- `scripts/generate-index.py` regenerates `docs/diagram-index.md`. Requires
  only python3.
