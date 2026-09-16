"""Pre-process screenshots for device composites (run with any Python that has Pillow).
- home-hero_clean: paint over the bottom "Trusted by..." strip with the page background.
- demo chat crops: pad to a fixed phone-screen aspect with the chat's own background colour.
"""
from PIL import Image
from pathlib import Path
HERE = Path(__file__).resolve().parent
SHOTS = HERE.parent.parent / 'assets' / 'screenshots'
WORK = HERE / 'work'; WORK.mkdir(exist_ok=True)

im = Image.open(SHOTS / 'home-hero_clean.png').convert('RGB')
W, H = im.size
bg = im.getpixel((40, H - 60))
im.paste(bg, (0, int(H * 0.955), W, H))
im.save(WORK / 'home-hero_clean_nofooter.png')

for m in ['home_clean_mobile.png']:
    Image.open(SHOTS / m).convert('RGB').save(WORK / m)

SCREEN_RATIO = 826 / 412  # h / w of the screen area below the faux status bar
for f in sorted((SHOTS / 'crops').glob('demo-step-*_chat-mobile.png')):
    c = Image.open(f).convert('RGB')
    w, h = c.size
    # trim the site's own bezel: 8 css px (x3) on each side and bottom rounded corner zone
    b = 3 * 8
    c = c.crop((b, 0, w - b, h - b))
    w, h = c.size
    fill = c.getpixel((w // 2, h - 30))
    head = c.getpixel((w // 2, 12))
    # paint the site's own rounded-corner bezel pixels (top corners -> header colour, bottom -> chat colour)
    px = c.load(); r = 150
    def near(a, b2, tol=40): return sum(abs(x - y) for x, y in zip(a, b2)) < tol
    for (x0, y0, col) in [(0, 0, head), (w - r, 0, head), (0, h - r, fill), (w - r, h - r, fill)]:
        for yy in range(y0, y0 + r):
            for xx in range(x0, x0 + r):
                p0 = px[xx, yy]
                if not near(p0, col) and sum(p0) < sum(col) + 30 and abs(p0[0] - p0[2]) < 12:
                    px[xx, yy] = col
    target_h = int(w * SCREEN_RATIO)
    out = Image.new('RGB', (w, max(target_h, h)), fill)
    out.paste(c, (0, 0))
    out.save(WORK / f.name.replace('_chat-mobile', '_phone'))
    print(f.name, (w, h), '->', out.size, 'fill', fill)
