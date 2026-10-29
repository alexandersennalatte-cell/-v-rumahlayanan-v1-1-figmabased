"""Locate the hero photo (non-blue region) inside the blue hero band."""
from PIL import Image

BLUE = (30, 58, 138)

def photo_box(path, y, label):
    im = Image.open(path).convert('RGB')
    xs = []
    for x in range(im.width):
        c = im.getpixel((x, y))
        if max(abs(a - b) for a, b in zip(c, BLUE)) > 25:
            xs.append(x)
    # find contiguous runs
    if not xs:
        print(label, 'none'); return
    runs = []
    s = p = xs[0]
    for x in xs[1:]:
        if x != p + 1:
            runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    print(label, [(a, b, b - a + 1) for a, b in runs if b - a > 5] if runs else 'none')

if __name__ == '__main__':
    import sys
    for y in (200, 300, 500, 700, 800):
        photo_box(r'K:\Newfolder\mock1.png', y, f'MOCK y={y}:')
    for y in (200, 300, 500, 700, 850):
        photo_box(r'K:\Newfolder\tools\shots\desktop.png', y, f'CUR  y={y}:')
