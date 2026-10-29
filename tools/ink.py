"""Precise ink row/column extents for a region."""
import sys
from PIL import Image

def rows(path, x0, x1, y0, y1, bg, tol=40):
    im = Image.open(path).convert('RGB')
    res = []
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1)
              if max(abs(a - b) for a, b in zip(im.getpixel((x, y)), bg)) > tol]
        res.append((y, (min(xs), max(xs), len(xs)) if xs else None))
    groups = []
    cur = None
    for y, r in res:
        if r and cur is None: cur = [y, y, r[0], r[1]]
        elif r:
            cur[1] = y; cur[2] = min(cur[2], r[0]); cur[3] = max(cur[3], r[1])
        elif cur:
            groups.append(tuple(cur)); cur = None
    if cur: groups.append(tuple(cur))
    return groups

if __name__ == '__main__':
    MOCK = r'K:\Newfolder\mock1.png'
    BLUE = (30, 58, 138)
    print('MOCK hero copy rows (x 70..700):')
    for g in rows(MOCK, 70, 700, 140, 820, BLUE):
        print(f"   y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})")
    CREAM = (247, 246, 238)
    print('\nMOCK header rows (x 60..1380):')
    for g in rows(MOCK, 60, 1380, 36, 136, CREAM):
        print(f"   y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})")
    print('\nMOCK topbar rows (x 60..1380):')
    for g in rows(MOCK, 60, 1380, 0, 36, (30, 58, 138)):
        print(f"   y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})")
