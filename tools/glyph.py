"""Measure cap-height (H) and line positions of the hero title."""
from PIL import Image

def is_text(c):
    return c[0] > 140 and c[1] > 140 and c[2] > 160

def glyph_box(im, x0, x1, y0, y1):
    minx, miny, maxx, maxy = None, None, None, None
    for y in range(y0, y1):
        for x in range(x0, x1):
            if is_text(im.getpixel((x, y))):
                if minx is None:
                    minx, maxx, miny, maxy = x, x, y, y
                else:
                    minx = min(minx, x); maxx = max(maxx, x)
                    miny = min(miny, y); maxy = max(maxy, y)
    return (minx, miny, maxx, maxy)

def report(path, label, H_x0, H_x1, L1_y0, L1_y1):
    im = Image.open(path).convert('RGB')
    print(f'\n===== {label} =====')
    b = glyph_box(im, H_x0, H_x1, L1_y0, L1_y1)
    print(f'  H glyph: x {b[0]}..{b[2]} y {b[1]}..{b[3]} cap={b[3]-b[1]+1} w={b[2]-b[0]+1}')
    b2 = glyph_box(im, H_x0, 700, L1_y0, L1_y1)
    print(f'  line1:   x {b2[0]}..{b2[2]} (w={b2[2]-b2[0]+1}) y {b2[1]}..{b2[3]}')

report(r'K:\Newfolder\mock1.png', 'MOCK', 82, 118, 250, 350)
report(r'K:\Newfolder\tools\shots\desktop.png', 'CUR', 104, 140, 210, 310)
