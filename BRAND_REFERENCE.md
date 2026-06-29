# Chalkboard Research — Brand & Technical Reference

This document is the source of truth for all brand assets. It is intended as a
briefing document for Claude Code or any future session continuing this work.

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
The mark geometry is embedded directly in each asset SVG in `_source/`.

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

**Left boxplot — pink (#CC79A7), stroke-width 1.96:**
- Top whisker vertical: x=19.6, y1=14, y2=24.22
- Top whisker cap: x1=9.8, x2=29.4, y=14
- Median: x1=7, x2=32.2, y=42
- Bottom whisker vertical: x=19.6, y1=65.38, y2=78.4
- Bottom whisker cap: x1=9.8, x2=29.4, y=78.4
- IQR rect: x=7, y=25.2, width=25.2, height=39.2

**Center boxplot — blue (#56B4E9), stroke-width 2.1:**
- Top whisker vertical: x=56, y1=5.6, y2=18.55
- Top whisker cap: x1=43.4, x2=68.6, y=5.6
- Median: x1=40.6, x2=71.4, y=43.4
- Bottom whisker vertical: x=56, y1=73.85, y2=88.2
- Bottom whisker cap: x1=43.4, x2=68.6, y=88.2
- IQR rect: x=40.6, y=19.6, width=30.8, height=53.2

**Right boxplot — green (#009E73), stroke-width 1.96:**
- Top whisker vertical: x=92.4, y1=16.8, y2=27.02
- Top whisker cap: x1=82.6, x2=102.2, y=16.8
- Median: x1=79.8, x2=105, y=46.2
- Bottom whisker vertical: x=92.4, y1=62.58, y2=75.6
- Bottom whisker cap: x1=82.6, x2=102.2, y=75.6
- IQR rect: x=79.8, y=28, width=25.2, height=33.6

---

## Asset Inventory

All files live in the GitHub repo root unless noted. SVG sources are in `_source/`.

### Web assets (served at chalkboard-research.com)

| File | Dimensions | Purpose |
|------|-----------|---------|
| `index.html` | — | Landing page |
| `favicon.svg` | 32×32 viewBox | Browser tab icon (SVG, modern browsers) |
| `favicon.ico` | 16+32px | Browser tab icon (legacy fallback) |
| `apple-touch-icon.png` | 180×180px | iOS home screen icon |
| `og-image.png` | 1200×630px | Open Graph / link preview image |
| `signature-logo.png` | 548×96px | Gmail signature image (hosted for URL insert); wordmark only, no tagline |

### LinkedIn assets (upload manually)

| File | Dimensions | Purpose |
|------|-----------|---------|
| `linkedin-logo-3box-300.png` | 300×300px | Company Page profile/logo slot |
| `linkedin-banner.png` | 1128×191px | Company Page cover/banner image |

### SVG sources (_source/ folder)

| File | Purpose |
|------|---------|
| `og-image.svg` | Source for og-image.png |
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
| og-image.png | og-image.svg | 1200×630 | 144 DPI |
| linkedin-banner.png | linkedin-banner.svg | 1128×191 | 144 DPI |
| linkedin-logo-3box-300.png | linkedin-logo-sq.svg | 300×300 | 144 DPI |
| signature-logo.png | signature-logo.svg | 548×96 | render at scale=1 (700×96), crop to (0,0,548,96); 72 DPI. Uses `font-weight="600"` — requires Pango in the Docker image to take effect |
| apple-touch-icon.png | favicon.svg | 180×180 | 144 DPI |
| favicon.ico | favicon.svg | 16+32px | Pillow ICO format |

---

## Open Issues / Active Threads

- **Gmail signature:** signature-logo.png (548×96) is hosted at chalkboard-research.com/signature-logo.png. Insert via Gmail Settings → Signature → image icon → URL. Sizing behavior is inconsistent across Gmail contexts; this is a known Gmail limitation.
- **LinkedIn OG cache:** if og-image.png is updated, run LinkedIn Post Inspector (linkedin.com/post-inspector) to force a re-scrape. If cache persists, rename file to og-image-v2.png and update og:image meta tags in index.html.
- **LinkedIn mobile banner overlap:** banner wordmark starts at x=420 to clear the square logo overlay on mobile. May need further adjustment if LinkedIn changes its mobile layout.
- **Dark mode:** index.html does not implement prefers-color-scheme. White background is intentional; page will look the same in dark mode browsers.

---

## Infrastructure

- **Domain:** chalkboard-research.com (Cloudflare DNS)
- **Hosting:** Cloudflare Pages, connected to GitHub repo km3uandrew/chalkboard-research-site
- **Deploy:** automatic on push to main branch
- **Email:** kary@chalkboard-research.com via Cloudflare Email Routing → Gmail
- **SSL:** Cloudflare-managed, confirmed active
