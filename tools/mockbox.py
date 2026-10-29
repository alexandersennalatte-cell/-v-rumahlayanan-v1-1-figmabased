"""Precise bbox measurement of mock header/hero elements."""
from PIL import Image

def d(a, b):
    return max(abs(x - y) for x, y in zip(a, b))

im = Image.open(r'K:\Newfolder\mock1.png').convert('RGB')
W, H = im.size

def bbox(x0, y0, x1, y1, pred, label):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(im.getpixel((x, y)))]
    if not pts:
        print(f'  {label}: none'); return
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f'  {label}: x {min(xs)}..{max(xs)} (w={max(xs)-min(xs)+1})  y {min(ys)}..{max(ys)} (h={max(ys)-min(ys)+1})')

print('MOCK header')
bbox(40, 40, 300, 135, lambda c: d(c, (6, 63, 48)) < 40, 'logo mark (green)')
bbox(300, 40, 700, 135, lambda c: d(c, (25, 60, 51)) < 60, 'logo text ink')
bbox(600, 40, 1400, 135, lambda c: d(c, (8, 102, 73)) < 70, 'nav green text')
bbox(1100, 40, 1400, 135, lambda c: max(c) - min(c) < 60 and sum(c) < 700, 'pengaduan btn area')
print('MOCK topbar')
bbox(40, 0, 400, 36, lambda c: min(c) > 180, 'topbar left text')
bbox(1000, 0, 1400, 36, lambda c: min(c) > 140, 'topbar right text')

print('MOCK hero')
bbox(40, 140, 760, 600, lambda c: d(c, (30, 58, 138)) > 40 and min(c) > 150, 'hero copy ink')
# eyebrow gold rule
bbox(40, 200, 760, 250, lambda c: d(c, (181, 150, 83)) < 60, 'eyebrow gold rule')
# search box white
bbox(40, 540, 760, 620, lambda c: min(c) > 235, 'search white box')
# buttons white (below search, y 700..790)
bbox(40, 690, 760, 800, lambda c: min(c) > 230, 'btn white')
# chips outlined
bbox(40, 620, 760, 690, lambda c: min(c) > 150 and d(c, (30, 58, 138)) > 40, 'chips text')
# photo
bbox(700, 140, 1440, 800, lambda c: d(c, (30, 58, 138)) > 30, 'photo+card region')
# blue button in search
bbox(40, 540, 760, 620, lambda c: d(c, (30, 58, 138)) < 20, 'search blue btn')
