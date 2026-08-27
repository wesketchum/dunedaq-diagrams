# Diagrams

This repo stores draw.io diagrams as editable sources under [`src/`](../src),
with rendered previews auto-generated into [`auto-images/`](../auto-images)
by CI. **Never hand-edit `auto-images/`** — it's regenerated on every PR that
touches `src/**/*.drawio` (and on every push to `main`) and any manual
changes will be overwritten.

Each `.drawio` source holds exactly **one page**. draw.io's own export only
renders a file's active/first page, so a multi-page file silently drops every
other page from its render — if you need several views of the same subject,
save them as separate single-page `.drawio` files rather than extra pages of
one file.

## Index

| Diagram | Preview | Edit |
|---|---|---|
| HD Fiber Plant | ![HD Fiber Plant](../auto-images/DUNE_Detector_Fiber_Plant-v3-HD_Fiber_Plant.svg) | [Open in draw.io](https://app.diagrams.net/#Hwesketchum%2Fdunedaq-diagrams%2Fmain%2Fsrc%2FDUNE_Detector_Fiber_Plant-v3-HD_Fiber_Plant.drawio) |
| VD Fiber Plant | ![VD Fiber Plant](../auto-images/DUNE_Detector_Fiber_Plant-v3-VD_Fiber_Plant.svg) | [Open in draw.io](https://app.diagrams.net/#Hwesketchum%2Fdunedaq-diagrams%2Fmain%2Fsrc%2FDUNE_Detector_Fiber_Plant-v3-VD_Fiber_Plant.drawio) |
| VD Fiber Plant, Detector Top Readout | ![VD Fiber Plant, Detector Top Readout](../auto-images/DUNE_Detector_Fiber_Plant-v3-VD_Fiber_Plant_Detector_Top_Readout.svg) | [Open in draw.io](https://app.diagrams.net/#Hwesketchum%2Fdunedaq-diagrams%2Fmain%2Fsrc%2FDUNE_Detector_Fiber_Plant-v3-VD_Fiber_Plant_Detector_Top_Readout.drawio) |

> These three used to be pages of one `DUNE_Detector_Fiber_Plant-v3.drawio`
> file; they were split into one `.drawio` per page (see note above) so each
> one actually gets rendered.
>
> The previews above won't render until the first PR touching these files (or
> a push to `main`) has run the `Sync diagram renders` workflow and committed
> the matching files under `auto-images/`.

## Adding a new diagram

1. Add a single-page `.drawio` file anywhere under `src/` (subfolders are
   fine — the render mirrors whatever structure you use).
2. Open a PR. The `Sync diagram renders` workflow renders it to a matching
   path under `auto-images/` and pushes that render onto your PR branch, so
   the rendered image shows up in the PR diff for review.
3. Add a row to the table above, pointing the preview at the new
   `auto-images/...svg` path and the edit link at the new `src/...drawio` path.

## Editing an existing diagram

Click the **Edit** link in the table — it opens the diagram directly from
this repo in [app.diagrams.net](https://app.diagrams.net) (GitHub OAuth on
first use). The link format is `#H<owner>%2F<repo>%2F<branch>%2F<path>`
(slashes percent-encoded as `%2F`), which loads the file straight from this
repo and saves commits back to that same path.

Prefer editing from a branch and opening a PR, so the rendered SVG shows up
in the PR diff for review before it reaches `main`. If you do save directly
to `main`, the push-triggered run of `Sync diagram renders` will still keep
`auto-images/` in sync automatically — you just won't get a PR to review the
rendered result against.

Alternatively, use the [draw.io VS Code extension](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)
to edit `.drawio` files locally.

## Fork PRs

The render workflow can't push commits onto a fork's branch (the default
`GITHUB_TOKEN` doesn't have write access there), so it skips auto-commit for
PRs from forks. If this repo starts taking outside contributions, that job
should be replaced with a check-only variant for fork PRs: render into a
scratch directory, diff against the committed `auto-images/`, and fail the
check if they don't match — pushing the regeneration step back onto the
contributor instead of the bot.
