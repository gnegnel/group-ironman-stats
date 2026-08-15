"""Rebuild the card chrome, icon sheet and 9-slice frame from the wiki's
capture of the in-game skills tab (oldschool.runescape.wiki Skills_tab.png).

Everything structural is the sprite's own pixels. Only two things are
synthesised: the stone noise that used to sit under the icons and level
numbers, and the extra bars stacked above and below the grid -- both are
built by resampling the sprite, so the whole card stays one material."""

import random
from collections import deque, Counter
from PIL import Image

SRC = Image.open('Skills_tab.png').convert('RGB')
px = SRC.load()
W, H = SRC.size
STONE = {(61,61,59),(68,68,65),(73,73,69),(77,77,73),(82,82,77),(85,85,81),(89,90,85),(98,99,93)}
YELLOW = (255,255,0)
TW, TH, PX, PY, SX, SY = 60, 29, 63, 30, 9, 9
ICONW = 33
origin = lambda i: (SX + PX*(i % 3), SY + PY*(i // 3))

# Positions showing bare stone (or a level digit) in at least one tile are
# tile interior; positions black in every tile are the engraved diagonal.
# Whatever is left is chrome -- bevel, chamfer, border -- and is identical
# in all 24 tiles, so it survives untouched.
interior, slash = set(), set()
for ry in range(TH):
    for rx in range(TW):
        cols = [px[ox+rx, oy+ry] for ox, oy in map(origin, range(24))]
        if any(c in STONE or c == YELLOW for c in cols): interior.add((rx, ry))
        if all(sum(c) < 30 for c in cols): slash.add((rx, ry))

# --- cleaned tile grid ---------------------------------------------------
# The stone is per-pixel random noise over a fixed eight-colour ramp, so it
# is redrawn from the sprite's own measured frequencies. Copying the literal
# pixels across instead prints one patch into all 24 tiles and leaves a
# visible ghost of whichever icon used to cover it.
tally = Counter(px[ox+rx, oy+ry] for ox, oy in map(origin, range(24))
                for (rx, ry) in interior if px[ox+rx, oy+ry] in STONE)
ramp, weights = zip(*tally.items())
rng = random.Random(20130222)

clean = SRC.copy(); c = clean.load()
for i in range(24):
    ox, oy = origin(i)
    for (rx, ry) in interior:
        c[ox+rx, oy+ry] = (0,0,0) if (rx, ry) in slash else rng.choices(ramp, weights)[0]
    for (rx, ry) in slash:
        c[ox+rx, oy+ry] = (0, 0, 0)
for y in range(249, 266):
    for x in range(W):
        if c[x, y] == YELLOW: c[x, y] = (0, 0, 0)

# --- card = frame + name bar + grid + total bar + footer bar -------------
# Each strip is lifted wholesale out of the cleaned sprite, so the added
# bars are literally the total-level bar repeated.
TOP, BAR, DIV, GRID, BOTTOM = (0,9), (249,266), (248,249), (9,249), (266,275)
STACK = [TOP, BAR, DIV, GRID, BAR, DIV, BAR, BOTTOM]
CARDH = sum(b-a for a, b in STACK)
card = Image.new('RGB', (W, CARDH))
y = 0
offsets = []
for a, b in STACK:
    card.paste(clean.crop((0, a, W, b)), (0, y))
    offsets.append((a, y, b-a)); y += b-a

GRID_Y = next(dy for sa, dy, n in offsets if sa == GRID[0])
BAR_Y  = [dy for sa, dy, n in offsets if sa == BAR[0]]
card.save('skills-card.png')

# --- icon sheet ----------------------------------------------------------
sheet = Image.new('RGBA', (ICONW, TH*24), (0,0,0,0)); s = sheet.load()
for i in range(24):
    ox, oy = origin(i)
    box = [p for p in interior if p[0] < ICONW]
    solid = {p for p in box if px[ox+p[0], oy+p[1]] not in STONE
             and px[ox+p[0], oy+p[1]] != YELLOW}
    # Grey icon pixels can land exactly on a stone colour, so flood the
    # background inward from the edges and keep whatever it cannot reach.
    bg, q = set(), deque()
    for p in box:
        if p in solid: continue
        if p[0] in (0, ICONW-1) or p[1] in (0, TH-1) or (p[0]+1, p[1]) not in interior:
            bg.add(p); q.append(p)
    while q:
        x0, y0 = q.popleft()
        for n in ((x0+1,y0),(x0-1,y0),(x0,y0+1),(x0,y0-1)):
            if n in interior and n[0] < ICONW and n not in bg and n not in solid:
                bg.add(n); q.append(n)
    for p in box:
        if p not in bg: s[p[0], TH*i + p[1]] = px[ox+p[0], oy+p[1]] + (255,)
sheet.save('skill-icons.png')

# --- 9-slice frame for the auxiliary panels ------------------------------
E = 9
frame = Image.new('RGB', (E*3, E*3))
mid_x, mid_y = 100, 150
for i, sx0 in enumerate((0, mid_x, W-E)):
    for j, sy0 in enumerate((0, mid_y, H-E)):
        frame.paste(clean.crop((sx0, sy0, sx0+E, sy0+E)), (i*E, j*E))
for x in range(E, E*2):                      # black interior, chat-box style
    for y2 in range(E, E*2): frame.putpixel((x, y2), (0, 0, 0))
frame.save('osrs-frame.png')

print('card %dx%d  grid_y=%d  bars=%s' % (W, CARDH, GRID_Y, BAR_Y))
print('tile origin x = 9 + 63*col, y = %d + 30*row' % GRID_Y)
