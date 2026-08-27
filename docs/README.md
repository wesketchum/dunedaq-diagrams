# Diagrams

This repo stores draw.io diagrams as editable sources under [`src/`](../src),
with rendered previews auto-generated into [`auto-images/`](../auto-images)
by CI. **Never hand-edit `auto-images/`** — it's regenerated on every PR that
touches `src/**/*.drawio` and any manual changes will be overwritten.

## Index

| Diagram | Preview | Edit |
|---|---|---|
| DUNE Detector Fiber Plant v3 | ![DUNE Detector Fiber Plant v3](../auto-images/DUNE_Detector_Fiber_Plant-v3.svg) | [Open in draw.io](https://app.diagrams.net/#Hgithub/wesketchum/dunedaq-diagrams/blob/main/src/DUNE_Detector_Fiber_Plant-v3.drawio) |

> The preview above won't render until the first PR touching
> `src/DUNE_Detector_Fiber_Plant-v3.drawio` has run the `Sync diagram renders`
> workflow and committed `auto-images/DUNE_Detector_Fiber_Plant-v3.svg`.

## Adding a new diagram

1. Add the `.drawio` file anywhere under `src/` (subfolders are fine — the
   render mirrors whatever structure you use).
2. Open a PR. The `Sync diagram renders` workflow renders it to a matching
   path under `auto-images/` and pushes that render onto your PR branch, so
   the rendered image shows up in the PR diff for review.
3. Add a row to the table above, pointing the preview at the new
   `auto-images/...svg` path and the edit link at the new `src/...drawio` path.

## Editing an existing diagram

Click the **Edit** link in the table — it opens the diagram directly from
this repo in [app.diagrams.net](https://app.diagrams.net) (GitHub OAuth on
first use) and saves commit straight back to the same path on `main`. Editing
that way should generally happen via a branch/PR rather than direct pushes to
`main`, so the render workflow gets a chance to run.

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
