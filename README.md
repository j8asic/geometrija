# Ship Geometry

A small [Quarto book](https://quarto.org/docs/books/) for first-year Naval Architecture students at FESB, University of Split. Course author: Josip Bašić. Teaching language: English, matching the supplied hull-modelling notes.

**Website after deployment:** https://j8asic.github.io/geometrija/

## What is included

- A first-ever Rhino practical: interface, viewports, selection, coordinates, snaps, layers, Gumball and a dimensioned pontoon model.
- A hull-modelling practical adapted and extended from `source/curvenote.tex`: calibrate a drawing, trace and position sections, build rails and surfaces, mirror and inspect the result.
- Original synthetic practice drawing and CSV offsets, generated without third-party Python packages. Students do not need Python or Git to use the published downloads.
- Links to McNeel documentation and externally hosted illustrations, plus both FESB videos supplied by the lecturer.

## One-time GitHub Pages setup

Before merging the initial PR, open **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**. Do not select a branch and do not add GitHub's example Jekyll workflow. This repository already contains the workflow.

Then merge the PR. **Every push to `main` builds and publishes** the book. Pushes to other branches and pull requests build and validate it but do not replace the student website. In Actions, a successful build also has a downloadable `book-preview` artifact. A manual `workflow_dispatch` run is available after the workflow reaches `main`.

No personal access token, extra GitHub App, publishing branch, npm project, R installation or LaTeX installation is required. Deployment uses GitHub's built-in token with Pages and OpenID Connect permissions confined to the deployment job. If a `github-pages` environment requires approval, approve it or change that environment's policy deliberately.

The connector used to prepare this PR does not expose repository Pages administration. Committing a workflow alone does not enable Pages; the setting above is required. See [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Edit and preview

Install [Quarto 1.10.18](https://quarto.org/docs/download/) and Python 3. The `python` command should refer to Python 3 (on systems using only `python3`, provide the equivalent command or adjust `pre-render` in `_quarto.yml`).

```sh
quarto preview
```

For the same validation used in CI:

```sh
quarto render --to html
python scripts/check_site.py _book
```

The pre-render script creates the PNG, SVG and offsets CSV from `downloads/practice-stations.csv`. Generated files and `_book/` are not committed. The workflow pins Quarto for reproducibility; update its version together with this README after testing.

### Add an exercise

Copy `_templates/exercise.qmd` into `exercises/`, edit its contents, and add the file to `book.chapters` in `_quarto.yml`. Relative links to another `.qmd` file become HTML links during rendering. Put downloadable source data in `downloads/`. Browser printing is styled; PDF compilation is intentionally not part of this simple HTML site.

### Course maintenance

`docs/instructor-notes.md` records lesson timing, the important corrections to the original notes, and suggested classroom checks. `resources.qmd` records media provenance and reference links. Third-party images are linked from McNeel rather than copied into this repository; the lessons remain usable from the text if those hosts are unavailable. FESB videos use YouTube's privacy-enhanced player with ordinary watch links as a fallback. No analytics are configured.

The CI checker validates local page/asset links and local fragment targets, image alternative text, video titles and required downloads. It does not claim to test Rhino itself or continuously validate external websites.

## Rights and provenance

The original supplied TeX is retained in `source/curvenote.tex`, with its author and date intact. Its Curvenote support files were not supplied, so it is an archival source, not a standalone TeX build target. The Quarto version does not need them.

No new blanket licence is imposed on the lecturer's material by this initial PR. Third-party documentation, illustrations and videos remain subject to their respective owners' terms. The synthetic body plan is newly created teaching data, not a real vessel, a certified design or a published experimental dataset.
