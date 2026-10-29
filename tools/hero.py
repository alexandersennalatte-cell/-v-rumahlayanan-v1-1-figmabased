"""Photo arch bounding box in mock + current."""
from PIL import Image

def photo_box(path, label, y0=136, y1=780):
    im = Image.open(path).convert('RGB')
    BLUE = (30, 58, 138)
    def nb(c, tol=26):
        return max(abs(a - b) for a, b in zip(c, BLUE)) > tol
    top = None
    for y in range(y0, y1):
        if any(nb(im.getpixel((x, y))) for x in range(700, 1440)):
            top = y; break
    bot = None
    for y in range(y1 - 1, y0, -1):
        if any(nb(im.getpixel((x, y))) for x in range(700, 1440)):
            bot = y; break
    best = (0, 0, 0)
    for y in range(top, bot + 1):
        xs = [x for x in range(600, 1440) if nb(im.getpixel((x, y)))]
        if xs and len(xs) > best[0]:
            best = (len(xs), min(xs), max(xs))
    print(f'{label}: photo top={top} bottom={bot} widest={best[1]}..{best[2]} '
          f'(w={best[2]-best[1]+1}) h={bot-top+1}')

photo_box(r'K:\Newfolder\mock1.png', 'MOCK')
photo_box(r'K:\Newfolder\tools\shots\desktop.png', 'CUR ')
