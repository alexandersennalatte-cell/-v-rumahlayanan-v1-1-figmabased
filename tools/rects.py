"""Find white-ish rectangles (search box) and photo x-bbox in mock vs current."""
from PIL import Image

BLUE = (30, 58, 138)

def d(a, b):
    return max(abs(x - y) for x, y in zip(a, b))

def white_rows(im, x0, x1, y0, y1):
    res = []
    for y in range(y0, y1):
        cnt = sum(1 for x in range(x0, x1) if min(im.getpixel((x, y))) > 235)
        res.append(cnt)
    return res

def report(path, label, y0, y1):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    print(f'\n===== {label} {W}x{H} =====')
    # search box white band: count near-white pixels across x 100..680
    for y in range(y0, y1):
        cnt = sum(1 for x in range(100, 680)
                  if min(im.getpixel((x, y))) > 240 and d(im.getpixel((x, y)), (255, 255, 255)) < 12)
        if cnt > 300:
            print(f'  white band y={y} count={cnt}')
    # photo bbox by scanning for non-blue in right half
    print('  photo rows:')
    top = None
    for y in range(140, H):
        xs = [x for x in range(700, W) if d(im.getpixel((x, y)), BLUE) > 30]
        if xs and top is None:
            top = y; print(f'    top={y} first xs {min(xs)}..{max(xs)}')
        if not xs and top is not None:
            print(f'    bottom={y-1} h={y-top}')
            break
    # horizontal extent of photo at several rows
    for y in (220, 300, 400, 500, 600, 700, 740):
        xs = [x for x in range(700, W) if d(im.getpixel((x, y)), BLUE) > 30]
        print(f'    row {y}: {min(xs) if xs else None}..{max(xs) if xs else None}')
    # hero bottom: last blue row in column x=10
    last = None
    for y in range(140, H):
        if d(im.getpixel((10, y)), BLUE) < 12:
            last = y; break
    print(f'  hero blue ends at y={last}')

report(r'K:\Newfolder\mock1.png', 'MOCK', 480, 700)
report(r'K:\Newfolder\tools\shots\desktop.png', 'CUR', 500, 760)
