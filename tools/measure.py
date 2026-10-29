"""Measure text line bands and ink extents inside a region.

Used to compare type sizes between the current build and mock1.png.
"""
import sys
from collections import Counter
from PIL import Image

def text_bands(path, x0, x1, y0, y1, bg=None, thresh=40):
    im = Image.open(path).convert('RGB')
    rows = []
    for y in range(y0, min(y1, im.height)):
        cnt = 0
        for x in range(x0, min(x1, im.width)):
            c = im.getpixel((x, y))
            if bg is None:
                # treat "ink" as dark-ish pixels (works for light backgrounds)
                if sum(c) < 560:
                    cnt += 1
            else:
                if max(abs(a - b) for a, b in zip(c, bg)) > thresh:
                    cnt += 1
        rows.append((y, cnt))
    bands = []
    cur = None
    for y, cnt in rows:
        if cnt > 0:
            if cur is None: cur = [y, y, cnt]
            else:
                cur[1] = y; cur[2] = max(cur[2], cnt)
        else:
            if cur: bands.append(tuple(cur)); cur = None
    if cur: bands.append(tuple(cur))
    return bands

def ink_box(path, x0, x1, y0, y1, bg):
    im = Image.open(path).convert('RGB')
    lo, hi = 10**9, -1
    for y in range(y0, min(y1, im.height)):
        for x in range(x0, min(x1, im.width)):
            c = im.getpixel((x, y))
            if max(abs(a - b) for a, b in zip(c, bg)) > 40:
                lo = min(lo, x); hi = max(hi, x)
    return lo, hi

if __name__ == '__main__':
    CUR = r'K:\Newfolder\tools\shots\desktop.png'
    MOCK = r'K:\Newfolder\mock1.png'
    BLUE = (30, 58, 138)
    CREAM = (247, 246, 238)

    print('--- MOCK hero title (light on blue), x 80..660 ---')
    for b in text_bands(MOCK, 80, 660, 150, 480, bg=BLUE):
        print('   y', b[0], '..', b[1], ' h=', b[1]-b[0]+1)
    print('--- CUR hero title (light on blue), x 104..640 ---')
    for b in text_bands(CUR, 104, 640, 150, 500, bg=BLUE):
        print('   y', b[0], '..', b[1], ' h=', b[1]-b[0]+1)
