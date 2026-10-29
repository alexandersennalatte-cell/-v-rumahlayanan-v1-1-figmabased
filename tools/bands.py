"""Detect horizontal background-color bands in a full-page screenshot.

Used to align section boundaries between the current build and mock1.png.
"""
import sys
from PIL import Image

def hexs(c):
    return '#%02X%02X%02X' % c

def bands(path, probes=None):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    if probes is None:
        # probe x positions: left margin, center, right margin
        probes = [int(W * 0.03), W // 2, int(W * 0.97)]
    out = []
    for x in probes:
        runs = []
        prev = None; start = 0
        for y in range(H):
            c = im.getpixel((x, y))
            if prev is None:
                prev = c; start = y; continue
            if max(abs(a - b) for a, b in zip(c, prev)) > 6:
                if y - start >= 8:
                    runs.append((start, y, hexs(prev)))
                prev = c; start = y
        if H - start >= 8:
            runs.append((start, H, hexs(prev)))
        out.append((x, runs))
    return out

if __name__ == '__main__':
    for path in sys.argv[1:]:
        print(f"\n===== {path} =====")
        for x, runs in bands(path):
            print(f"  x={x}:")
            for s, e, c in runs:
                print(f"    {s:5d} .. {e:5d}  ({e-s:4d}px)  {c}")
