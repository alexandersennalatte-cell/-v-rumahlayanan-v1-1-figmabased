"""Row ink profile (count + x-extent) for a region - reveals baselines."""
import sys
from PIL import Image

def profile(path, x0, x1, y0, y1, bg, tol=60, label=''):
    im = Image.open(path).convert('RGB')
    print(f'--- {label} ---')
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1)
              if max(abs(a - b) for a, b in zip(im.getpixel((x, y)), bg)) > tol]
        if xs:
            print(f'  y={y:4d} n={len(xs):4d}  x {min(xs)}..{max(xs)}')

if __name__ == '__main__':
    MOCK = r'K:\Newfolder\mock1.png'
    profile(MOCK, 70, 700, 215, 260, (30, 58, 138), label='MOCK eyebrow')
    profile(MOCK, 70, 700, 262, 430, (30, 58, 138), label='MOCK title')
