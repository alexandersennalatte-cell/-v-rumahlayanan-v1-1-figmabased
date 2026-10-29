"""Isolate each header element's ink box by scanning narrow x windows."""
from PIL import Image

CREAM = (247, 246, 238)

def cols_of_ink(path, y0, y1, bg, thresh=30):
    im = Image.open(path).convert('RGB')
    out = []
    for x in range(im.width):
        for y in range(y0, min(y1, im.height)):
            c = im.getpixel((x, y))
            if max(abs(a - b) for a, b in zip(c, bg)) > thresh:
                out.append(x); break
    return out

def runs(xs, gap=8):
    if not xs: return []
    res = []; s = p = xs[0]
    for x in xs[1:]:
        if x - p > gap:
            res.append((s, p, p - s + 1)); s = x
        p = x
    res.append((s, p, p - s + 1))
    return res

MOCK = r'K:\Newfolder\mock1.png'
CUR = r'K:\Newfolder\tools\shots\desktop.png'

for label, path in (('MOCK', MOCK), ('CUR', CUR)):
    print(f'--- {label} header ---')
    for y0, y1 in [(55, 88), (88, 118)]:
        cols = cols_of_ink(path, y0, y1, CREAM)
        rr = runs(cols, gap=16)
        print(f'   rows {y0}..{y1}: ' + ', '.join(f'{a}..{b}({c})' for a, b, c in rr))
