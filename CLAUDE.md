# Chalkboard Research — Brand & Technical Reference

This document is the source of truth for all brand assets and the working conventions
for this repo. It is loaded automatically by Claude Code at the start of every session.

## Working conventions

- **Everything committed here is published.** Cloudflare Pages serves the whole repo,
  so every committed file is publicly downloadable at chalkboard-research.com/<path>.
  Client content, client document builders, and private tooling never go in this repo —
  they live in chalkboard-core (private) or the client's own repo.
- **Render assets:** `docker run --rm -v "$(pwd):/work" chalkboard-render` from the repo root.
  Docker Desktop must be running. One-time build: `docker build -t chalkboard-render .`
- **Git:** commit locally, then ask before pushing to remote. Site auto-deploys on push via Cloudflare Pages.
- **Python (macOS fallback only):** `/opt/homebrew/bin/python3.9` has cairosvg/Pillow/fonttools.
  Do not use `/usr/bin/python3` (macOS system Python, missing packages). Docker is preferred for all renders.
- **og-image versioning:** if LinkedIn caches a stale og-image, increment the filename
  (og-image-v2.png → og-image-v3.png) and update the reference in index.html, render.py, and this file.

---

## Business

**Name:** Chalkboard Research LLC  
**Service mark:** Chalkboard Research℠ (in use since June 2026; Wayback Machine snapshot on file)  
**Tagline:** Drawing Insights from Your Data  
**Owner:** Kary Myers, PhD  
**Email:** kary@chalkboard-research.com  
**Location:** Santa Fe, New Mexico  
**Website:** https://chalkboard-research.com  
**GitHub repo:** km3uandrew/chalkboard-research-site (Cloudflare Pages, auto-deploys on push to main)

---

## Brand Colors

| Name    | Hex       | Use |
|---------|-----------|-----|
| Blue    | `#56B4E9` | Center boxplot IQR outline; accent |
| Pink    | `#CC79A7` | Left boxplot IQR outline |
| Green   | `#009E73` | Right boxplot IQR outline; email link color |
| Charcoal| `#2b2b2b` | Wordmark, name, whiskers, medians |
| Readable gray | `#4a4a4a` | Body text, tagline, secondary text in rendered images |
| Background | `#ffffff` | White — all assets use white background |

These are colorblind-friendly (Wong palette).

---

## Typography

### Web (index.html)
- **Headlines / wordmark:** Josefin Sans SemiBold (weight 600), all-caps, letter-spacing 0.1em
- **Tagline:** Josefin Sans Regular (weight 400), all-caps, letter-spacing 0.18em, padding-left 5px (optical compensation for round left edge of "C" in wordmark above vs straight "D" in tagline)
- **Body text:** Lora Regular (weight 400), 18px, line-height 1.75
- **Name (Kary Myers, PhD):** Josefin Sans SemiBold, 15px, all-caps
- **Contact / location:** Josefin Sans, 15px / 14px, all-caps
- **Footer (LLC line):** 11px, color `#c0c0c0`
- Google Fonts import: Josefin Sans (300, 400, 600) + Lora (400)

### Rendered images (cairosvg)
All rendering is done via Docker — see the Rendering Pipeline section. Font handling is
managed inside the Docker image; no local font installation is required.

---

## Logo: The Boxplot Mark

The logo is three boxplots (Concept 2: colored IQR outlines, charcoal whiskers and median).
The mark geometry is embedded directly in each asset SVG in `_source/`, the inline SVG in
`index.html`, and `deck/mark.svg`.

**Cross-repo duplicate:** the lockup geometry (mark + divider + wordmark, from
`_source/signature-logo.svg`) is also duplicated as vector-drawing code in
`draw_lockup()` in chalkboard-core's `pdf/chalkboard_pdf.py` (private repo, reportlab
client documents). If the mark or lockup geometry changes here, update that function
to match.

### Design rules (hard-won):
1. **Drawing order:** all whisker lines and median lines draw BEFORE the rect (box outline),
   so the box stroke renders on top, cleanly covering line endpoints.
2. **Uniform stroke widths:** all elements (whiskers, medians, box outlines) use the same
   stroke width per boxplot. No heavier medians or thicker boxes.
3. **Median reach:** median x-coordinates match the box's nominal edges exactly
   (e.g. left box: x1=7, x2=32.2). The box stroke's half-width covers the endpoints.
   Do NOT extend beyond nominal edges (overcorrection) or pull in (too short).
4. **Whisker length:** top whisker ends at (box_top - half_stroke_width) so it doesn't
   enter the box interior. Bottom whisker starts at (box_bottom + half_stroke_width).
5. **No fill** on any box — stroke only, fill="none".
6. **Optical alignment:** tagline "DRAWING INSIGHTS FROM YOUR DATA" is nudged 2-3px right
   relative to "CHALKBOARD RESEARCH" to compensate for the round left edge of "C" vs "D".

### Master logo coordinates (112×95 viewBox):

Pixel-snapped 2026-07-07: every stroke-width is 2 and every centerline/edge coordinate
is an integer, so strokes land exactly on pixel boundaries at 1× (and any integer
scale). Box widths are even so the whisker centerline is an integer at the box center.
Do not reintroduce fractional coordinates or stroke widths.

**Left boxplot — pink (#CC79A7), stroke-width 2:**
- Top whisker vertical: x=20, y1=14, y2=24
- Top whisker cap: x1=10, x2=30, y=14
- Median: x1=7, x2=33, y=42
- Bottom whisker vertical: x=20, y1=65, y2=78
- Bottom whisker cap: x1=10, x2=30, y=78
- IQR rect: x=7, y=25, width=26, height=39

**Center boxplot — blue (#56B4E9), stroke-width 2:**
- Top whisker vertical: x=56, y1=6, y2=19
- Top whisker cap: x1=43, x2=69, y=6
- Median: x1=41, x2=71, y=43
- Bottom whisker vertical: x=56, y1=74, y2=88
- Bottom whisker cap: x1=43, x2=69, y=88
- IQR rect: x=41, y=20, width=30, height=53

**Right boxplot — green (#009E73), stroke-width 2:**
- Top whisker vertical: x=92, y1=17, y2=27
- Top whisker cap: x1=82, x2=102, y=17
- Median: x1=79, x2=105, y=46
- Bottom whisker vertical: x=92, y1=63, y2=76
- Bottom whisker cap: x1=82, x2=102, y=76
- IQR rect: x=79, y=28, width=26, height=34

(The signature-logo lockup uses its own slightly different integer geometry —
see `_source/signature-logo.svg` — with the same design rules.)

---

## Asset Inventory

Assets are organized by use: `web/` (site images), `linkedin/`, `signature/`, `deck/`,
with SVG sources in `_source/`. The whole repo is served by Cloudflare Pages, so every
file has a URL at its repo path. `index.html` and the favicon trio stay at the repo
root — browsers and iOS request `/favicon.ico` and `/apple-touch-icon.png` at the root
path by convention, often ignoring the HTML link tags.

### Web assets (served at chalkboard-research.com)

| File | Dimensions | Purpose |
|------|-----------|---------|
| `index.html` | — | Landing page |
| `favicon.svg` | 32×32 viewBox | Browser tab icon (SVG, modern browsers); root by convention |
| `favicon.ico` | 16+32px | Browser tab icon (legacy fallback); root by convention |
| `apple-touch-icon.png` | 180×180px | iOS home screen icon; root by convention |
| `web/og-image-v2.png` | 1200×630px | Open Graph / link preview image |

### Signature assets (signature/ folder)

| File | Dimensions | Purpose |
|------|-----------|---------|
| `signature/signature-logo.png` | 548×96px | Email signature image, 1× legacy; wordmark only, no tagline |
| `signature/signature-logo-2x.png` | 1096×192px | Email signature image for high-DPI displays — the one referenced in the Proton Mail signature |
| `signature/email_signature.html` | — | The signature HTML pasted into Proton Mail's editor (HTML mode); logo linked to the site at width 400 |

### Deck assets (deck/ folder, transparent backgrounds)

For slide decks and handouts. Light backgrounds only — strokes and text are `#2b2b2b`,
and the lockup's divider line (`#d0d0d0`) washes out on mid-tone fills.

**Using these assets from other sessions:** prefer the vector files (`mark.svg`,
`lockup.pdf`) where the tool accepts them; use the transparent 2× PNGs otherwise.
Claude Code sessions on this machine read them from this repo directly
(`~/Chalkboard Research/Brand and First Use Info/chalkboard-research-site/deck/`).
Sessions without filesystem access (e.g. Claude Chat) fetch the public URLs — the
whole repo is served by Cloudflare Pages:
`https://chalkboard-research.com/deck/mark.svg`, `.../deck/lockup.pdf`,
`.../deck/mark-2x.png`, `.../deck/lockup-2x.png`. When prompting a session that
cannot read this file, restate the constraint: transparent background, charcoal
`#2b2b2b` strokes and text, light slide backgrounds only.

| File | Dimensions | Purpose |
|------|-----------|---------|
| `deck/mark.svg` | 106×90 viewBox | Tight-cropped three-box mark, vector (insert directly into Keynote/PowerPoint/Google Slides) |
| `deck/mark-2x.png` | 636×540px | Raster fallback for the mark |
| `deck/lockup.pdf` | 548×96pt | Vector lockup with fonts embedded (SVG text would require Josefin Sans installed, so the vector lockup ships as PDF) |
| `deck/lockup-2x.png` | 1096×192px | Raster fallback for the lockup |

### LinkedIn assets (upload manually)

| File | Dimensions | Purpose |
|------|-----------|---------|
| `linkedin/linkedin-logo-3box-300.png` | 300×300px | Company Page profile/logo slot |
| `linkedin/linkedin-banner.png` | 1128×191px | Company Page cover/banner image |

### SVG sources (_source/ folder)

| File | Purpose |
|------|---------|
| `og-image.svg` | Source for og-image-v2.png |
| `linkedin-banner.svg` | Source for linkedin-banner.png |
| `linkedin-logo-sq.svg` | Source for linkedin-logo-3box-300.png |
| `signature-logo.svg` | Source for signature-logo.png |
| `favicon.svg` | Served directly; also source for favicon.ico and apple-touch-icon.png |

---

## Rendering Pipeline

All PNGs are rendered from SVG sources using cairosvg via Docker. Docker provides a
Linux/FreeType rendering environment that matches the environment where the original
assets were produced, avoiding macOS CoreText font weight discrepancies.

### Rendering environment

All assets are rendered via Docker (Linux + Pango/FreeType), which matches the Ubuntu 24
environment where the original assets were produced. This is the only supported render path —
macOS/CoreText produces lighter font weight and should not be used.

**One-time setup:**
```bash
cd "Brand and First Use Info/chalkboard-research-site"
docker build -t chalkboard-render .
```

**Re-render all assets** (from the repo root):
```bash
docker run --rm -v "$(pwd):/work" chalkboard-render
```

The image is reused on every subsequent run. Only rebuild if `Dockerfile` changes.

Key details of the rendering environment:
- cairosvg with Pango support (`libpango`, `pangocffi`, `pangocairocffi`) — required for
  `font-weight="600"` to be passed through correctly; without Pango, numeric weights are ignored
- Variable fonts installed directly to `/usr/local/share/fonts/` — Pango resolves weight 600
  from the variable font axis; no static instance extraction needed
- `signature-logo.svg` uses `font-family="Josefin Sans"` `font-weight="600"` — do not change
  to `font-family="Josefin Sans SemiBold"` or add stroke compensation; those were macOS workarounds

### Per-asset render settings

| Asset | SVG source | Output dimensions | Notes |
|-------|-----------|------------------|-------|
| web/og-image-v2.png | og-image.svg | 1200×630 | 144 DPI |
| linkedin/linkedin-banner.png | linkedin-banner.svg | 1128×191 | 144 DPI |
| linkedin/linkedin-logo-3box-300.png | linkedin-logo-sq.svg | 300×300 | 144 DPI |
| signature/signature-logo.png | signature-logo.svg | 548×96 | render at scale=1 (700×96), crop to (0,0,548,96); 72 DPI. Uses `font-weight="600"` — requires Pango in the Docker image to take effect |
| signature/signature-logo-2x.png | signature-logo.svg | 1096×192 | supersampled from a 4× render; 144 DPI |
| deck/mark-2x.png | deck/mark.svg | 636×540 | transparent; scale=6 |
| deck/lockup.pdf | signature-logo.svg | 548×96pt | white rect stripped and canvas narrowed at render time (see render_deck_assets) |
| deck/lockup-2x.png | signature-logo.svg | 1096×192 | transparent; supersampled from 4×; same source transform as lockup.pdf |
| apple-touch-icon.png | favicon.svg | 180×180 | 144 DPI |
| favicon.ico | favicon.svg | 16+32px | Pillow ICO format |

---

## Open Issues / Active Threads

- **Gmail signature:** signature-logo.png (548×96) is hosted at chalkboard-research.com/signature-logo.png. Insert via Gmail Settings → Signature → image icon → URL. Sizing behavior is inconsistent across Gmail contexts; this is a known Gmail limitation.
- **LinkedIn OG cache:** if og-image-v2.png is updated, run LinkedIn Post Inspector (linkedin.com/post-inspector) to force a re-scrape. If cache persists, rename to og-image-v3.png (incrementing the version) and update the og:image meta tags in index.html, render.py, and CLAUDE.md.
- **LinkedIn mobile banner overlap:** banner wordmark starts at x=420 to clear the square logo overlay on mobile. May need further adjustment if LinkedIn changes its mobile layout.
- **Dark mode:** index.html does not implement prefers-color-scheme. White background is intentional; page will look the same in dark mode browsers.

---

## Infrastructure

- **Domain:** chalkboard-research.com (Cloudflare DNS)
- **Hosting:** Cloudflare Pages, connected to GitHub repo km3uandrew/chalkboard-research-site
- **Deploy:** automatic on push to main branch
- **Email:** kary@chalkboard-research.com via Cloudflare Email Routing → Gmail
- **SSL:** Cloudflare-managed, confirmed active
