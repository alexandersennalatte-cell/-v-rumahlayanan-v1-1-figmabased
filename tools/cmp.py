"""Hero-region comparison: mock vs current."""
from PIL import Image

BLUE = (30, 58, 138)
CREAM = (247, 246, 238)

def load(p):
    return Image.open(p).convert('RGB')

def nb(c, bg, tol):
    return max(abs(a - b) for a, b in zip(c, bg)) > tol

def line_groups(im, x0, x1, y0, y1, bg, tol):
    groups, cur = [], None
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if nb(im.getpixel((x, y)), bg, tol)]
        if xs:
            if cur is None: cur = [y, y, min(xs), max(xs)]
            else:
                cur[1] = y
                cur[2] = min(cur[2], min(xs)); cur[3] = max(cur[3], max(xs))
        elif cur:
            groups.append(tuple(cur)); cur = None
    if cur: groups.append(tuple(cur))
    return groups

def report(path, label):
    im = load(path)
    W, H = im.size
    print(f'\n===== {label}  ({W}x{H}) =====')
    px0 = 760
    print('photo column profile (x>=%d):' % px0)
    for y in range(140, 840, 20):
        xs = [x for x in range(px0, W) if nb(im.getpixel((x, y)), BLUE, 26)]
        rng = f'x {min(xs)}..{max(xs)} (w={max(xs)-min(xs)+1})' if xs else 'none'
        print(f'   y {y}: {rng}')
    print('hero copy ink rows (x 60..760):')
    for g in line_groups(im, 60, 760, 140, 560, BLUE, 60):
        print(f'   y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})')
    print('header ink rows (x 40..1400, y 36..136):')
    for g in line_groups(im, 40, 1400, 36, 136, CREAM, 40):
        print(f'   y {g[0]}..{g[1]} (h={g[1]-g[0]+1})  x {g[2]}..{g[3]} (w={g[3]-g[2]+1})')

report(r'K:\Newfolder\mock1.png', 'MOCK')
report(r'K:\Newfolder\tools\shots\desktop.png', 'CUR')
