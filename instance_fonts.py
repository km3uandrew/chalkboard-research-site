"""Build-time font instancing for the render image.

cairosvg renders text through cairo's "toy" font API: numeric font-weight >= 550
selects the family's Bold face (which fontconfig resolves from a variable font as
wght 700), and anything below 550 selects Regular. Intermediate weights are
unreachable by font-weight alone, so the wordmark weight (Jost wght 600) is baked
here into a static instance registered under its own family name, "Jost W600",
and referenced by that family name with normal weight in the SVG sources.

The instanced font is generated inside the Docker image at build time and never
committed to the repo (the repo is publicly served, and redistributing a renamed
modified font would raise OFL Reserved Font Name questions).
"""
from fontTools import ttLib
from fontTools.varLib.instancer import instantiateVariableFont

f = ttLib.TTFont("/tmp/Jost.ttf")
instantiateVariableFont(f, {"wght": 600}, inplace=True)
for rec in f["name"].names:
    if rec.nameID in (1, 16, 4):
        rec.string = "Jost W600"
    elif rec.nameID in (2, 17):
        rec.string = "Regular"
    elif rec.nameID == 6:
        rec.string = "Jost-W600"
f["OS/2"].usWeightClass = 400
f.save("/usr/local/share/fonts/chalkboard/Jost-W600.ttf")
print("wrote /usr/local/share/fonts/chalkboard/Jost-W600.ttf")
