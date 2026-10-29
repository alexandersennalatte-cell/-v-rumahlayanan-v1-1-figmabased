"""Measure hero geometry: photo bounding box, copy column, title lines."""
import sys
from PIL import Image

def nonbg_cols(im, y0, y1, bg, tol=26):
    cols = []
    for x in range(im.width):
        for y in range(y0, min(y1, im.height)):
            c = im.getpixel((x, y))
            if max(abs(a - b) for a, b in zip(c, bg)) > tol:
                cols.append(x); break
    return cols

def runs(xs, gap=6):
    if not xs: return []
    out = []; s = p = xs[0]
    for x in xs[1:]:
        if x - p > gap:
            out.append((s, p)); s = x
        p = x
    out.append((s, p))
    return out

def analyze(path, label, y0, y1, bg):
    im = Image.open(path).convert('RGB')
    print(f"=== {label}  hero band y {y0}..{y1} ===")
    for y in range(y0, y1, 25):
        cols = nonbg_cols(im, y, y + 2, bg)
        rr = [r for r in runs(cols, gap=40) if r[1] - r[0] > 20]
        print(f"  y={y}: " + " | ".join(f"{a}..{b}({b-a+1})" for a, b in rr))

def band_rows(path, y0, y1, x0, x1, bg, tol=26):
    im = Image.open(path).convert('RGB')
    out = []
    for y in range(y0, y1):
        hit = False
        for x in range(x0, x1):
            c = im.getpixel((x, y))
            if max(abs(a - b) for a, b in zip(c, bg)) > tol:
                hit = True; break
        out.append(hit)
    # group
    res = []; cur = None
    for i, h in enumerate(out):
        if h and cur is None: cur = i
        elif not h and cur is not None:
            res.append((y0 + cur, y0 + i - 1)); cur = None
    if cur is not None: res.append((y0 + cur, y0 + len(out) - 1))
    return res

if __name__ == '__main__':
    analyze(r'K:\Newfolder\mock1.png', 'MOCK', 140, 805, (30, 58, 138))
    print()
    analyze(r'K:\Newfolder\tools\shots\desktop.png', 'CUR', 130, 860, (30, 58, 138))
    print('\nMOCK title row bands (x 80..740):',
          band_rows(r'K:\Newfolder\mock1.png', 140, 420, 80, 740, (30, 58, 138)))
    print('CUR  title row bands (x 100..760):',
          band_rows(r'K:\Newfolder\tools\shots\desktop.png', 130, 430, 100, 760, (30, 58, 138)))
