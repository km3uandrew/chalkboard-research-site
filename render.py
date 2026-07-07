"""Renders all brand PNGs from SVG sources in _source/.
Run via Docker: docker run --rm -v "$(pwd):/work" chalkboard-render
"""

import io
import os
import struct
import zlib

import cairosvg
from PIL import Image, ImageChops

SRC = os.path.join(os.path.dirname(__file__), "_source")
OUT = os.path.dirname(__file__)


def set_dpi(path, dpi=144):
    with open(path, "rb") as f:
        data = f.read()
    ppm = int(dpi / 0.0254)
    phys = struct.pack(">IIB", ppm, ppm, 1)
    crc = zlib.crc32(b"pHYs" + phys) & 0xFFFFFFFF
    chunk = struct.pack(">I", 9) + b"pHYs" + phys + struct.pack(">I", crc)
    with open(path, "wb") as f:
        f.write(data[:33] + chunk + data[33:])


def render(svg, output, *, width, height, dpi=144, src=None, supersample=1):
    """Render SVG to PNG. supersample>1 renders at that multiple then downsamples with LANCZOS."""
    out_path = os.path.join(OUT, output)
    if supersample > 1:
        buf = io.BytesIO()
        cairosvg.svg2png(
            url=os.path.join(src or SRC, svg),
            write_to=buf,
            output_width=width * supersample,
            output_height=height * supersample,
        )
        buf.seek(0)
        Image.open(buf).convert("RGB").resize((width, height), Image.LANCZOS).save(out_path)
    else:
        cairosvg.svg2png(
            url=os.path.join(src or SRC, svg),
            write_to=out_path,
            output_width=width,
            output_height=height,
        )
    set_dpi(out_path, dpi=dpi)
    print(f"{output}: {os.path.getsize(out_path):,} bytes")


def render_signature_logo():
    """Render at scale=1 (700×96), crop to content + 19px right padding → 548×96.
    Also emit a 2× version (1096×192, supersampled from 4×) for high-DPI email
    clients — display it at width=548 in the signature HTML."""
    buf = io.BytesIO()
    cairosvg.svg2png(url=os.path.join(SRC, "signature-logo.svg"), write_to=buf, scale=1)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.crop((0, 0, 548, img.height))
    out_path = os.path.join(OUT, "signature", "signature-logo.png")
    img.save(out_path)
    set_dpi(out_path, dpi=72)
    print(f"signature/signature-logo.png: {os.path.getsize(out_path):,} bytes")

    buf = io.BytesIO()
    cairosvg.svg2png(url=os.path.join(SRC, "signature-logo.svg"), write_to=buf, scale=4)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")
    img = img.crop((0, 0, 548 * 4, img.height)).resize((548 * 2, 96 * 2), Image.LANCZOS)
    out_path = os.path.join(OUT, "signature", "signature-logo-2x.png")
    img.save(out_path)
    set_dpi(out_path, dpi=144)
    print(f"signature/signature-logo-2x.png: {os.path.getsize(out_path):,} bytes")


def render_deck_assets():
    """Transparent-background assets for slide decks and handouts, in deck/.
    Light backgrounds only (strokes and text are #2b2b2b).

    - mark-2x.png: tight-cropped three-box mark from deck/mark.svg
    - lockup.pdf: vector lockup (fonts embedded by cairo; Keynote/PowerPoint take PDF)
    - lockup-2x.png: 1096x192 transparent raster lockup

    The lockup renders from _source/signature-logo.svg with the white
    background rect stripped and the canvas narrowed to the 548-unit crop,
    so there is one source of truth for the lockup geometry."""
    deck = os.path.join(OUT, "deck")

    out_path = os.path.join(deck, "mark-2x.png")
    cairosvg.svg2png(url=os.path.join(deck, "mark.svg"), write_to=out_path, scale=6)
    set_dpi(out_path, dpi=144)
    print(f"deck/mark-2x.png: {os.path.getsize(out_path):,} bytes")

    with open(os.path.join(SRC, "signature-logo.svg")) as f:
        svg = f.read()
    svg = svg.replace('<rect width="700" height="96" fill="white"/>', "")
    svg = svg.replace('width="700" height="96" viewBox="0 0 700 96"',
                      'width="548" height="96" viewBox="0 0 548 96"')

    out_path = os.path.join(deck, "lockup.pdf")
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=out_path)
    print(f"deck/lockup.pdf: {os.path.getsize(out_path):,} bytes")

    buf = io.BytesIO()
    cairosvg.svg2png(bytestring=svg.encode(), write_to=buf, scale=4)
    buf.seek(0)
    img = Image.open(buf).convert("RGBA").resize((548 * 2, 96 * 2), Image.LANCZOS)
    out_path = os.path.join(deck, "lockup-2x.png")
    img.save(out_path)
    set_dpi(out_path, dpi=144)
    print(f"deck/lockup-2x.png: {os.path.getsize(out_path):,} bytes")


def render_favicon_ico():
    """Render favicon at 16px and 32px and combine into a .ico file."""
    sizes = [16, 32]
    frames = []
    for size in sizes:
        buf = io.BytesIO()
        cairosvg.svg2png(url=os.path.join(OUT, "favicon.svg"), write_to=buf, output_width=size, output_height=size)
        buf.seek(0)
        frames.append(Image.open(buf).convert("RGBA"))
    out_path = os.path.join(OUT, "favicon.ico")
    frames[0].save(out_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=frames[1:])
    print(f"favicon.ico: {os.path.getsize(out_path):,} bytes")


if __name__ == "__main__":
    render("og-image.svg",          "web/og-image-v2.png",                 width=1200, height=630,  dpi=144, supersample=2)
    render("linkedin-banner.svg",   "linkedin/linkedin-banner.png",        width=1128, height=191,  dpi=144, supersample=2)
    render("linkedin-logo-sq.svg",  "linkedin/linkedin-logo-3box-300.png", width=300,  height=300,  dpi=144, supersample=2)
    render("favicon.svg",           "apple-touch-icon.png",       width=180,  height=180,  dpi=144, src=OUT)
    render_signature_logo()
    render_deck_assets()
    render_favicon_ico()
    print("Done.")
