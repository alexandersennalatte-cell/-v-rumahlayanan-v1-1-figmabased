"""Sample colors at key coordinates from two images and report differences."""
import sys
from PIL import Image

def px(im, x, y):
    return im.convert('RGB').getpixel((x, y))

def hexs(c):
    return '#%02X%02X%02X' % c

CUR = Image.open(r'K:\Newfolder\tools\shots\desktop.png')
MOCK = Image.open(r'K:\Newfolder\mock1.png')

POINTS = [
    ('topbar bg',        700, 12),
    ('topbar text',      1150, 12),
    ('header bg',        700, 60),
    ('hero bg',          60, 200),
    ('hero bg right',    1400, 400),
    ('nav active green', 735, 78),
    ('logo mark',        117, 78),
    ('search btn blue',  650, 618),
    ('cream body',       700, 830),
    ('h2 green text',    35, 300),
    ('eyebrow gold',     30, 190),
    ('card white',       300, 435),
    ('card border',      30, 430),
    ('section bg',       700, 1500),
    ('gold band',        700, 5010),
    ('green box',        200, 5100),
    ('footer green',     700, 6700),
]

print(f"{'point':20s} {'CURRENT':>9s} {'MOCK':>9s}  match")
for name, x, y in POINTS:
    a = px(CUR, x, y); b = px(MOCK, x, y)
    d = sum(abs(p - q) for p, q in zip(a, b))
    print(f"{name:20s} {hexs(a):>9s} {hexs(b):>9s}  {'OK' if d < 24 else f'DIFF({d})'}")
