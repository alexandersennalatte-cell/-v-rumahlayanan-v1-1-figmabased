"""Precise mock vs current hero measurements."""
from PIL import Image

def load(p):
    return Image.open(p).convert('RGB')

def dist(a, b):
    return max(abs(x - y) for x, y in zip(a, b))

def bands_col(im, x, y0, y1, tol=3):
    print(f'  column x={x}:')
    prev = None; start = y0
    for y in range(y0, y1):
        c = im.getpixel((x, y))
        if prev is None:
            prev = c; start = y; continue
        if dist(c, prev) > tol:
            print(f'    y {start}..{y-1} (h={y-start})  {prev}')
            prev = c; start = y
    print(f'    y {start}..{y1-1} (h={y1-start})  {prev}')

def ink_groups(im, x0, x1, y0, y1, bg, tol):
    groups, cur = [], None
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if dist(im.getpixel((x, y)), bg) > tol]
        if xs:
            if cur is None:
                cur = [y, y, min(xs), max(xs)]
            else:
                cur[1] = y; cur[2] = min(cur[2], min(xs)); cur[3] = max(cur[3], max(xs))
        elif cur:
            groups.append(tuple(cur)); cur = None
    if cur: groups.append(tuple(cur))
    return groups

def col_ink(im, y, x0, x1, bg, tol):
    xs = [x for x in range(x0, x1) if dist(im.getpixel((x, y)), bg) > tol]
    if not xs: return None
    runs, s = [], xs[0]
    for a, b in zip(xs, xs[1:]):
        if b - a > 14:
            runs.append((s, a)); s = b
    runs.append((s, xs[-1]))
    return runs

BLUE = (30, 58, 138)
CREAM = (247, 246, 238)

def analyse(path, label):
    im = load(path)
    W, H = im.size
    print(f'\n########## {label}  {W}x{H} ##########')
    bands_col(im, 10, 0, 200)
    bands_col(im, 700, 0, 200)
    print('  header ink rows (x 40..1400, y 0..140, bg cream):')
    for g in ink_groups(im, 40, 1400, 0, 140, CREAM, 40):
        print(f'    y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})')
    print('  title ink groups (x 40..760, y 140..600, bg blue):')
    for g in ink_groups(im, 40, 760, 140, 600, BLUE, 60):
        print(f'    y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})')
    for g in ink_groups(im, 40, 760, 140, 600, BLUE, 60):
        if g[1] - g[0] < 40: continue
        y = (g[0] + g[1]) // 2
        print(f'    line y{g[0]}..{g[1]} runs: {col_ink(im, y, 40, 760, BLUE, 60)}')
    print('  photo bbox (right side):')
    def row_photo(y):
        xs = [x for x in range(700, W) if dist(im.getpixel((x, y)), BLUE) > 26]
        return (min(xs), max(xs)) if xs else None
    top = None
    for y in range(140, 900):
        r = row_photo(y)
        if r and top is None: top = y
        if not r and top is not None:
            print(f'    photo rows {top}..{y-1}  (h={y-top})')
            break
    print('  search box / card bands:')
    bands_col(im, 200, 400, 800, 40)
    bands_col(im, 1100, 400, 800, 40)

analyse(r'K:\Newfolder\mock1.png', 'MOCK')
analyse(r'K:\Newfolder\tools\shots\desktop.png', 'CUR')
