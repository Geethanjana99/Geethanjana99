# Geethanjana / GitHub Profile Setup

## Publish the profile

Create or open the **public** repository named `Geethanjana99` under the GitHub account `Geethanjana99`. GitHub displays the root `README.md` of that matching-name public repository on the account's profile.

Extract this package and copy its **contents** into that repository. Do not place the entire `geethanjana-profile` folder inside the repository: `README.md` and `assets/` must be at the repository root.

The minimum files needed for the visual profile are:

```text
README.md
assets/
```

Commit them to the repository's default branch. The profile artwork does not need a build step, npm, Vercel, an API key, or an external image service.

For a local Git workflow, clone the profile repository first, copy the package's contents into that clone, then run:

```bash
git add .
git commit -m "Create visual developer and VR profile"
git push
```

Git authentication is handled by the account holder's normal GitHub setup. This package does not contain credentials and has not been published to the account.

## Preview before publishing

Open `preview.html` in a browser for the animated dark preview, or `preview-light.html` for the light-theme preview. Keep the HTML file beside the `assets` folder.

These are local approximations of GitHub's Markdown styling, not screenshots from the live GitHub profile. The profile content, images, native links, and disclosure sections are drawn from the same `README.md`. Check the final profile on GitHub after publishing because its sanitization, spacing, and caching can differ.

After editing `README.md`, regenerate the included browser previews with:

```bash
python -m pip install markdown-it-py beautifulsoup4
python scripts/build_preview.py
```

The profile intentionally uses native Markdown, supported HTML elements, and image assets. It does not attempt to run CSS application layouts, JavaScript, WebGL, or a real VR application inside the README. GitHub sanitizes README HTML, including scripts and inline styles.

## Animation and accessibility

The desktop profile uses two small four-second GIF loops:

| Asset | Motion |
| --- | --- |
| `assets/hero.gif` | Subtle orbiting particles, a floating VR headset, and terminal-cursor variation. |
| `assets/vr-lab.gif` | Slow decorative packets moving between networking icons and a VR headset. |

No flashing or rapid colour cycling is used. The orbit and network animation are decorative, not live telemetry or a running research simulation.

Each animated image has a static SVG alternative. The `<picture>` sources prefer a static image for reduced-motion preferences and use specially composed mobile SVGs at narrow viewport sizes. This depends on the viewer's browser and GitHub's handling of `<picture>`; the static README is the deterministic no-motion option.

For an entirely static profile, copy the contents of `README-static.md` over `README.md`. Keep the static file at the repository root while editing so its relative asset paths remain correct.

Key profile information is also present as selectable Markdown text or descriptive alternative text; project contributions are in expandable native `<details>` sections.

## Optional public GitHub statistics

The profile starts with a designed "Explore the repositories" navigation card. It does **not** contain made-up statistics or an uninitialized broken image.

An optional workflow can replace that same local card with a dated public GitHub snapshot. It is manual-only by default; uploading this package does not turn on scheduled refreshes.

To use it, include these files in the repository:

```text
.github/workflows/profile-stats.yml
scripts/refresh_stats.py
assets/github-activity.svg
```

In GitHub, open **Actions**, select **Refresh public profile stats**, and choose **Run workflow**. The workflow file must be on the default branch. The workflow requests `contents: write` so it can commit the generated SVG; repository or organization settings and branch protections can still prevent those commits. Where applicable, allow the workflow to write to this repository or use the manual method below.

The workflow uses GitHub's automatically supplied, scoped `GITHUB_TOKEN`. No personal access token needs to be pasted into a README or committed to the repository.

The generated card displays:

- Original public repositories owned by the account, excluding forks and including archived original repositories.
- Stars summed across those repositories, plus the account's public follower count.
- The top six primary languages by repository count. Each repository counts once under its primary language. This is **not** a byte-percentage, proficiency, or contribution-volume chart.

The refresh script uses only Python's standard library. It paginates repository results, deduplicates records, escapes SVG text, retries transient errors, and keeps the previous artwork intact if fetching fails. The displayed timestamp identifies the snapshot; it is not continuously live.

To opt into daily refreshes later, uncomment the `schedule` lines in `.github/workflows/profile-stats.yml`. The supplied example is 06:23 UTC. Scheduled workflows can be delayed and, for public repositories, can be disabled after 60 days of inactivity.

For a manual local refresh:

```bash
python scripts/refresh_stats.py --username Geethanjana99
```

Without a token, public API requests are subject to GitHub's unauthenticated rate limit. A locally configured `GITHUB_TOKEN` environment variable can be used when needed; never commit the token. Commit the updated `assets/github-activity.svg` afterward.

The statistics transformations and error-preservation behavior were tested offline. The optional workflow has not been run against this account or tested in its repository settings.

## Edit the content

Use `README.md` for normal writing changes. The supplied profile details have been preserved without adding projects, certification dates, private repository links, employers, or research outcomes that were not provided.

Before publishing, the account holder should check the undergraduate status and the 2022–2026 education range, confirm the listed credentials and project descriptions, and confirm that employer-related work can be publicly described. The supplied portfolio, LinkedIn, and email links are used as provided.

Project visuals are **conceptual illustrations**, not screenshots of TrueMarke, WayPoint, or CareSync. Add actual product screenshots only when available and permitted. Direct project repository links were not supplied, so none were invented.

## Customize the artwork

All graphics are editable SVGs. Technology tiles use original line illustrations and text monograms; they are not a bundled official-logo library. SVG text uses system font fallbacks. No font files are included or required for display.

Edit an individual SVG directly, or edit the palette, labels, and drawing functions in `scripts/build_art.py` and regenerate:

```bash
python scripts/build_art.py
```

Regenerating SVGs requires only Python 3.10 or later. To also regenerate the two GIFs:

```bash
python -m pip install Pillow CairoSVG
python scripts/build_art.py --animate
```

CairoSVG may require the Cairo native library on the operating system. This is only relevant when rebuilding the optional GIFs; it is not needed to use the shipped assets. Never run the artwork generator over unreviewed edits, because it replaces generated static SVG files. It deliberately preserves `assets/github-activity.svg` once that file exists.

The dark palette is defined at the top of `scripts/build_art.py`:

| Role | Colour |
| --- | --- |
| Background | `#080D18` |
| Panels | `#101929` |
| Borders | `#22344A` |
| Main text | `#EDF5FF` |
| Secondary text | `#93A8C1` |
| Cyan accent | `#66E3F1` |
| Violet accent | `#AA9AFF` |
| Soft green accent | `#A0E5B0` |

## Files included

```text
README.md                         Animated profile, ready to publish
README-static.md                  Static alternative
SETUP.md                          This guide
preview.html                      Local dark browser preview
preview-light.html                Local light browser preview
assets/                           All local profile imagery
  hero.gif / hero.svg              Animated cover and still version
  vr-lab.gif / vr-lab.svg          Animated research art and still version
  project-*.svg                   Three conceptual project illustrations
  stack-*.svg                     Five technology boards
  academic.svg                    Academic highlight panel
  developer-console.svg           Developer configuration illustration
  principles.svg                  Engineering principles panel
  github-activity.svg              Navigation card / optional generated stats
  link-*.svg                      Clickable link-button graphics
  footer.svg                      Closing banner
  sections/                       Nine numbered section banners
  mobile/                         Mobile-specific SVG compositions
  icons/                          Reusable developer and VR line icons
scripts/
  build_art.py                    Rebuild SVGs and optionally GIFs
  build_preview.py                Rebuild the local HTML previews
  refresh_stats.py                Generate a public GitHub statistics card
  test_stats.py                   Offline tests for stats processing
.github/workflows/
  profile-stats.yml               Optional manual statistics refresh
```

## Reference documentation

GitHub profile README setup:
https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

GitHub's markup sanitization:
https://github.com/github/markup

Native expandable sections:
https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections

GitHub Actions workflow syntax and permissions:
https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions
https://docs.github.com/actions/reference/authentication-in-a-workflow

Manual and scheduled workflow behavior:
https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows

Public user and repository REST endpoints:
https://docs.github.com/en/rest/users/users
https://docs.github.com/en/rest/repos/repos

The supplied workflow pins the official `actions/checkout` v7.0.1 commit:
https://github.com/actions/checkout/tree/3d3c42e5aac5ba805825da76410c181273ba90b1
