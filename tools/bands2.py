"""Section boundaries via background colour transitions down a column."""
from PIL import Image

def bands(path, label, x=700):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    print(f'=== {label} (h={H}) ===')
    prev = None
    start = 0
    for y in range(H):
        c = im.getpixel((x, y))
        if c != prev:
            if prev is not None and y - start > 10:
                print(f'   y {start}..{y-1} (h={y-start})  {prev}')
            prev = c; start = y
    print(f'   y {start}..{H-1} (h={H-start})  {prev}')

if __name__ == '__main__':
    bands(r'K:\Newfolder\mock1.png', 'MOCK x=700')
    bands(r'K:\Newfolder\tools\shots\desktop.png', 'CUR x=700')
