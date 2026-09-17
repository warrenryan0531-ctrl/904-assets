#!/usr/bin/env python3
"""Render a 904 Digital Media branded quote/tip card from a JSON spec.

Spec (instagram/cards/<name>.json):
  {"label": "TIP OF THE DAY", "lines": ["..", ".."], "footer": "904 Digital Media  ·  Jacksonville, FL"}
Output: instagram/<name>.png (1080x1080, electric blue #0057FF, white Poppins)
"""
import json, sys, os, urllib.request
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/tmp/fonts"
POPPINS = {
    "Bold": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
    "Medium": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Medium.ttf",
}

def font(weight, size):
    os.makedirs(FONT_DIR, exist_ok=True)
    p = os.path.join(FONT_DIR, f"Poppins-{weight}.ttf")
    if not os.path.exists(p):
        urllib.request.urlretrieve(POPPINS[weight], p)
    return ImageFont.truetype(p, size)

def render(spec_path):
    spec = json.load(open(spec_path))
    name = os.path.splitext(os.path.basename(spec_path))[0]
    W = H = 1080
    img = Image.new("RGB", (W, H), "#0057FF")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 14], fill="white")
    d.ellipse([820, -220, 1300, 260], outline="white", width=6)
    d.rectangle([88, 880, 200, 892], fill="white")
    d.text((88, 120), spec.get("label", "TIP OF THE DAY"), font=font("Medium", 30), fill="white")
    lines = spec["lines"]
    size = 78 if len(lines) <= 5 else 66
    big = font("Bold", size)
    step = int(size * 1.2)
    y = 250
    for l in lines:
        d.text((88, y), l, font=big, fill="white")
        y += step
    d.text((88, 915), spec.get("footer", "904 Digital Media  ·  Jacksonville, FL"),
           font=font("Medium", 32), fill="white")
    out = os.path.join("instagram", f"{name}.png")
    img.save(out, optimize=True)
    print(f"rendered {out} ({os.path.getsize(out)} bytes)")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        render(p)
