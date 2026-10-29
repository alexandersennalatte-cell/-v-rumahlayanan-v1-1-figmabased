"""Crop an arbitrary rect from a PNG and upscale it for close inspection."""
import sys
from PIL import Image, ImageDraw

def zoom(src, out, x0, y0, x1, y1, scale=1.0, label=None, grid=0):
    im = Image.open(src).convert('RGB').crop((x0, y0, x1, y1))
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    if grid:
        for gx in range(x0 - x0 % grid, x1, grid):
            X = (gx - x0) * scale
            d.line([(X, 0), (X, im.height)], fill=(255, 0, 255), width=1)
            d.text((X + 2, 2), str(gx), fill=(255, 0, 255))
        for gy in range(y0 - y0 % grid, y1, grid):
            Y = (gy - y0) * scale
            d.line([(0, Y), (im.width, Y)], fill=(0, 200, 255), width=1)
            d.text((2, Y + 2), str(gy), fill=(0, 200, 255))
    if label:
        d.rectangle([0, 0, 460, 26], fill=(0, 0, 0))
        d.text((8, 7), label, fill=(255, 255, 255))
    im.save(out)
    print(f"{out}  {im.width}x{im.height}  (src x {x0}..{x1} y {y0}..{y1})")

if __name__ == "__main__":
    a = sys.argv
    zoom(a[1], a[2], int(a[3]), int(a[4]), int(a[5]), int(a[6]),
         float(a[7]) if len(a) > 7 else 1.0,
         a[8] if len(a) > 8 else None,
         int(a[9]) if len(a) > 9 else 0)
