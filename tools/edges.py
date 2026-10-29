"""Find the left/right content edges of a page region.

Scans rows within a y-range, finds columns containing pixels that differ
from the row's modal (background) colour, and reports the common bounds.
"""
import sys
from collections import Counter
from PIL import Image

def analyse(path, y0, y1, label):
    im = Image.open(path).convert('RGB')
    W = im.width
    lo, hi = W, -1
    for y in range(y0, min(y1, im.height)):
        row = [im.getpixel((x, y)) for x in range(W)]
        bg = Counter(row).most_common(1)[0][0]
        for x, c in enumerate(row):
            if max(abs(a - b) for a, b in zip(c, bg)) > 18:
                if x < lo: lo = x
                if x > hi: hi = x
    print(f"{label:34s} {path}")
    print(f"   content x: {lo} .. {hi}   (width {hi-lo+1})")
    return lo, hi

if __name__ == '__main__':
    analyse(r'K:\Newfolder\mock1.png', 60, 120, 'MOCK header row')
    analyse(r'K:\Newfolder\tools\shots\desktop.png', 60, 115, 'CUR header row')
    analyse(r'K:\Newfolder\mock1.png', 180, 300, 'MOCK hero title rows')
    analyse(r'K:\Newfolder\tools\shots\desktop.png', 180, 300, 'CUR hero title rows')
    analyse(r'K:\Newfolder\mock1.png', 60, 90, 'MOCK logo row')
    analyse(r'K:\Newfolder\tools\shots\desktop.png', 60, 100, 'CUR logo row')
