"""Crop a PNG into labelled horizontal bands for visual comparison."""
import sys, os
from PIL import Image, ImageDraw

def band(src, out, y0, y1, scale=1.0, label=None):
    im = Image.open(src)
    im = im.crop((0, y0, im.width, min(y1, im.height)))
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    if label:
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 460, 26], fill=(0, 0, 0))
        d.text((8, 7), label, fill=(255, 255, 255))
    im.save(out)
    print(f"{out}  {im.width}x{im.height}  (src y {y0}..{y1})")

if __name__ == "__main__":
    src = sys.argv[1]; out = sys.argv[2]
    y0 = int(sys.argv[3]); y1 = int(sys.argv[4])
    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
    label = sys.argv[6] if len(sys.argv) > 6 else None
    band(src, out, y0, y1, scale, label)
