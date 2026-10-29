"""Geometry of hero blocks in mock vs current."""
from PIL import Image

BLUE = (30, 58, 138)
CREAM = (247, 246, 238)

def d(a, b): return max(abs(x - y) for x, y in zip(a, b))

def bbox_where(im, pred, x0, x1, y0, y1):
    minx, miny, maxx, maxy = None, None, None, None
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(im.getpixel((x, y))):
                if minx is None: minx = maxx = x; miny = maxy = y
                else:
                    minx = min(minx, x); maxx = max(maxx, x)
                    miny = min(miny, y); maxy = max(maxy, y)
    return (minx, miny, maxx, maxy) if minx is not None else None

def is_white(c): return c[0] > 238 and c[1] > 238 and c[2] > 238

def analyse(path, label):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    print(f'\n===== {label} {W}x{H} =====')
    # photo: non-blue region in right half
    ph = bbox_where(im, lambda c: d(c, BLUE) > 30, 700, W, 140, 900)
    print(f'  photo bbox      x {ph[0]}..{ph[2]} (w={ph[2]-ph[0]+1})  y {ph[1]}..{ph[3]} (h={ph[3]-ph[1]+1})')
    # white search box: white run on a row that has one
    for y in [520, 540, 560, 580, 600]:
        row = [x for x in range(40, 700) if is_white(im.getpixel((x, y)))]
        if row:
            # longest contiguous run
            runs, s = [], row[0]
            for a, b in zip(row, row[1:]):
                if b - a > 3: runs.append((s, a)); s = b
            runs.append((s, row[-1]))
            runs.sort(key=lambda r: r[1] - r[0])
            if runs[-1][1] - runs[-1][0] > 60:
                print(f'  search row y={y}: white run x {runs[-1][0]}..{runs[-1][1]} (w={runs[-1][1]-runs[-1][0]+1})')
                break
    # white card inside photo region
    for y in [660, 690, 700]:
        row = [x for x in range(700, W) if is_white(im.getpixel((x, y)))]
        if row:
            runs, s = [], row[0]
            for a, b in zip(row, row[1:]):
                if b - a > 3: runs.append((s, a)); s = b
            runs.append((s, row[-1]))
            runs.sort(key=lambda r: r[1] - r[0])
            if runs[-1][1] - runs[-1][0] > 80:
                print(f'  card row y={y}: white run x {runs[-1][0]}..{runs[-1][1]} (w={runs[-1][1]-runs[-1][0]+1})')
                break
    # hero bottom: last blue row before cream
    bot = None
    for y in range(140, 1000):
        if is_white(im.getpixel((720, y))) or d(im.getpixel((720, y)), CREAM) < 12:
            bot = y; break
    print(f'  hero bottom ~ y={bot}')

analyse(r'K:\Newfolder\mock1.png', 'MOCK')
analyse(r'K:\Newfolder\tools\shots\desktop.png', 'CUR')
