"""Precise geometry probe: ink boxes for specific regions of a page image."""
import sys
from PIL import Image

def hexs(c): return '#%02X%02X%02X' % c

def ink_cols(im, x0, x1, y0, y1, bg, thresh=30):
    cols = []
    for x in range(x0, min(x1, im.width)):
        for y in range(y0, min(y1, im.height)):
            c = im.getpixel((x, y))
            if max(abs(a - b) for a, b in zip(c, bg)) > thresh:
                cols.append(x); break
    return (min(cols), max(cols)) if cols else (None, None)

def ink_rows(im, x0, x1, y0, y1, bg, thresh=30):
    rows = []
    for y in range(y0, min(y1, im.height)):
        for x in range(x0, min(x1, im.width)):
            c = im.getpixel((x, y))
            if max(abs(a - b) for a, b in zip(c, bg)) > thresh:
                rows.append(y); break
    return (min(rows), max(rows)) if rows else (None, None)

def probe(path, name, x0, x1, y0, y1, bg):
    im = Image.open(path).convert('RGB')
    cx0, cx1 = ink_cols(im, x0, x1, y0, y1, bg)
    ry0, ry1 = ink_rows(im, x0, x1, y0, y1, bg)
    print(f"{name:30s} x {cx0}..{cx1} (w {None if cx0 is None else cx1-cx0+1})   y {ry0}..{ry1} (h {None if ry0 is None else ry1-ry0+1})")

if __name__ == '__main__':
    MOCK = r'K:\Newfolder\mock1.png'
    CUR = r'K:\Newfolder\tools\shots\desktop.png'
    BLUE = (30, 58, 138); CREAM = (247, 246, 238); SAGE = (232, 238, 229)
    GOLD = (240, 232, 211); GREEN = (6, 63, 48); WHITE = (255, 255, 255)

    print('== MOCK ==')
    probe(MOCK, 'logo mark',        80, 130, 40, 135, CREAM)
    probe(MOCK, 'logo title text', 135, 320, 40, 135, CREAM)
    probe(MOCK, 'nav Beranda',      740, 830, 55, 100, CREAM)
    probe(MOCK, 'nav cta',        1220, 1360, 40, 135, CREAM)
    probe(MOCK, 'hero title L1',    80, 700, 250, 345, BLUE)
    probe(MOCK, 'hero title L2',    80, 700, 345, 425, BLUE)
    probe(MOCK, 'hero lead',        80, 620, 435, 530, BLUE)
    probe(MOCK, 'hero search',      80, 700, 540, 620, BLUE)
    probe(MOCK, 'hero photo',      700, 1400, 150, 810, BLUE)

    print('== CUR ==')
    probe(CUR, 'logo mark',       100, 150, 40, 125, CREAM)
    probe(CUR, 'logo title text', 155, 340, 40, 125, CREAM)
    probe(CUR, 'nav Beranda',     700, 790, 55, 100, CREAM)
    probe(CUR, 'nav cta',        1200, 1340, 40, 125, CREAM)
    probe(CUR, 'hero title L1',   100, 660, 225, 305, BLUE)
    probe(CUR, 'hero title L2',   100, 660, 305, 380, BLUE)
    probe(CUR, 'hero title L3',   100, 660, 380, 460, BLUE)
    probe(CUR, 'hero lead',       100, 620, 470, 560, BLUE)
    probe(CUR, 'hero search',     100, 700, 580, 660, BLUE)
    probe(CUR, 'hero photo',      700, 1400, 150, 870, BLUE)
