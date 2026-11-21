#!/usr/bin/env python3
"""draw_news.py: draw the 21 November 2026 front page (1024x1024 PNG).

This is the drawing script for news-image-20261121. It renders
entry.png with PIL from the bundled DejaVu fonts. Run it locally to
(regenerate) entry.png; the graded entrypoint is main.py, which only
copies the already-rendered entry.png into the grader's output folder
(the grader image has no Pillow, so the entrypoint must not import it).

Writes entry.png next to this script by default, or into
MAKEFUN_OUTPUT_DIR when that variable is set.
"""
import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", HERE)) / "entry.png"

# ---- palette -------------------------------------------------------
NAVY = (18, 38, 74)
RED = (178, 24, 33)
DARKRED = (140, 16, 24)
GREY = (88, 92, 99)
LIGHT = (236, 236, 234)
PAPER = (250, 248, 244)
MAP_BG = (232, 236, 238)
LAND = (196, 198, 186)
LAND_EDGE = (150, 154, 140)
INK = (30, 30, 32)

# ---- fonts (bundled DejaVu, so rendering is identical anywhere) ----
def font(name, size):
    return ImageFont.truetype(str(HERE / "fonts" / name), size)

F_TITLE = font("DejaVuSerif-Bold.ttf", 52)
F_SUB = font("DejaVuSans.ttf", 16)
F_DATE = font("DejaVuSans-Bold.ttf", 31)
F_KICK = font("DejaVuSans-Bold.ttf", 14)
F_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_DECK = font("DejaVuSans.ttf", 14)
F_SEC = font("DejaVuSans-Bold.ttf", 15)
F_BAR_NAME = font("DejaVuSans-Bold.ttf", 10)
F_BAR_NUM = font("DejaVuSans-Bold.ttf", 15)
F_NUM = font("DejaVuSans-Bold.ttf", 21)
F_NUMCAP = font("DejaVuSans.ttf", 10)
F_BRIEF_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 13)
F_MAP_LBL = font("DejaVuSans-Bold.ttf", 11)
F_OCEAN = font("DejaVuSans.ttf", 13)

# ---- the news ------------------------------------------------------
# 3 leads + 45 briefs = 48 stories, 7 regions.
LEADS = [
    ("COP31 OVERTIME",
     "COP31 SPILLS INTO OVERTIME",
     "Draft drops fossil fuels; ~200 nations deadlocked in Antalya."),
    ("SAUDI MISSILES",
     "3 HOUTHI MISSILES DOWNED OVER RIYADH",
     "Three ballistic missiles intercepted early Saturday, days "
     "after the PIF tower was hit."),
    ("PERU QUAKE",
     "6.7 QUAKE SHAKES PERU'S ANDES",
     "Junin tremor felt in Lima; no deaths reported, but landslides "
     "hit the hillsides."),
]

# (region, text) -- order is the reading order down the three columns.
BRIEFS = [
    ("N. AMERICA", "S&P 500 falls 3.7% into correction"),
    ("N. AMERICA", "Nasdaq sheds 5.3%, erasing its 2026 gains"),
    ("N. AMERICA", "Nvidia craters 14%, worst day in two years"),
    ("N. AMERICA", "Anthropic slides 9% a day after record IPO"),
    ("N. AMERICA", "Trump: Iran deal \u201cnot acceptable to me\u201d"),
    ("N. AMERICA", "Trump warns of \u201ctremendous tax\u201d on AI centres"),
    ("N. AMERICA", "US sanctions Iranian oil-revenue “trustees”"),
    ("N. AMERICA", "Washington Spirit reach NWSL final"),
    ("LATIN AMERICA", "Salvadoran troops in Haiti hit by explosives"),
    ("LATIN AMERICA", "Brazil's Bovespa falls 0.7% in global rout"),
    ("LATIN AMERICA", "Lula's first Brazilian state visit to Manila"),
    ("EUROPE", "Russia hits Ukraine with 400+ drones, 110 missiles"),
    ("EUROPE", "Russian missiles land in Poland; Tusk warns"),
    ("EUROPE", "Spain heads to a Nov 29 election; right gains"),
    ("EUROPE", "Estonia to close border crossings with Russia"),
    ("EUROPE", "Alcaraz beats Cobolli to stay unbeaten at ATP Finals"),
    ("EUROPE", "BepiColombo reaches Mercury orbit after eight years"),
    ("AFRICA", "Boat carrying funeral mourners capsizes in Nigeria"),
    ("AFRICA", "Tanzania's Lissu convicted of sedition"),
    ("AFRICA", "Somalia orders UAE ambassador to leave in 72 hours"),
    ("AFRICA", "South Sudan shifts its first election to February 2027"),
    ("AFRICA", "DRC's Tshisekedi signs bill extending tenure limit"),
    ("AFRICA", "UN: drones killed 1,600+ people in Sudan this year"),
    ("M. EAST", "Iran Guard says it downed a US MQ-9 over Hormuz"),
    ("M. EAST", "Iran FM: US naval blockade must end for oil exports"),
    ("M. EAST", "Tanker hit near Oman; two more hit mines"),
    ("M. EAST", "Iraqi forces enter Kataeb Hezbollah stronghold"),
    ("M. EAST", "Israeli strikes kill Palestinians in Gaza"),
    ("M. EAST", "US missile strike hits near Iran's Qeshm Island"),
    ("ASIA", "ICJ: Myanmar guilty of genocide against Rohingya"),
    ("ASIA", "Saudi Arabia and Japan agree an oil stockpile deal"),
    ("ASIA", "Nepal PM Balendra Shah to make his first India visit"),
    ("ASIA", "Quad business forum set for early 2027, Rubio says"),
    ("ASIA", "Trump defends his Putin and Xi ties after Shenzhen"),
    ("ASIA", "Nikkei tanks 5.1%; Kospi \u22125.5% and Taiex \u22126.2%"),
    ("ASIA", "Gold slides to a 14-month low near $3,514"),
    ("ASIA", "Bitcoin slips below $58,200 in the sell-off"),
    ("ASIA", "Leapmotor Q3 profit plunges 73% on record sales"),
    ("ASIA", "27 Chinese firms announce share buybacks in a day"),
    ("ASIA", "Chinese banks warn clients over precious-metals risk"),
    ("ASIA", "Choi Min-jeong advances at short-track World Tour"),
    ("ASIA", "Malaysia sets record with 11,007 diabetes screenings"),
    ("OCEANIA", "Australia crush NZ 34\u201310 to win Women's RLWC"),
    ("OCEANIA", "Kangaroos edge Kiwis 24\u201322 in RLWC men's opener"),
    ("OCEANIA", "Australia, Canada, NZ urge Russia to ceasefire"),
]

REGIONS = ["N. AMERICA", "LATIN AM.", "EUROPE", "AFRICA",
           "M. EAST", "ASIA", "OCEANIA"]
REGION_COUNTS = {"N. AMERICA": 8, "LATIN AM.": 4, "EUROPE": 7,
                 "AFRICA": 6, "M. EAST": 7, "ASIA": 13, "OCEANIA": 3}

NUMBERS = [
    ("6.7", "Peru quake"),
    ("510", "fired at Ukraine"),
    ("\u22125.3%", "Nasdaq plunge"),
    ("3", "downed over Riyadh"),
    ("~200", "nations at COP31"),
    ("34\u201310", "RLWC final score"),
]

# ---- simplified world map (hand-drawn lon/lat polygons) ------------
CONTINENTS = [
    # North America
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 57),
     (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
     (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
     (-79, 9), (-81, 13), (-84, 16), (-87, 21), (-90, 21), (-91, 19),
     (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 26), (-80, 32),
     (-76, 35), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
     (-55, 47), (-60, 52), (-65, 55), (-68, 58), (-72, 62), (-78, 62),
     (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70),
     (-155, 71), (-165, 68)],
    # Greenland
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70),
     (-20, 74), (-25, 76), (-35, 77), (-50, 76), (-58, 74), (-60, 70)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-73, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32),
     (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
     (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
     (-72, 12), (-77, 8)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (37, 22),
     (39, 18), (43, 12), (48, 11), (51, 10), (46, 5), (42, 0), (40, -5),
     (40, -10), (36, -18), (33, -26), (28, -33), (20, -35), (17, -32),
     (15, -27), (12, -18), (13, -12), (9, -1), (9, 4), (-8, 4), (-13, 8),
     (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
     (0, 50), (3, 51), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60),
     (5, 62), (12, 65), (18, 69), (25, 71), (32, 70), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 70), (170, 67),
     (178, 65), (170, 60), (162, 58), (158, 52), (150, 59), (142, 55),
     (140, 50), (135, 43), (130, 42), (127, 40), (122, 38), (120, 32),
     (122, 28), (118, 25), (110, 20), (108, 18), (105, 10), (103, 8),
     (100, 8), (98, 10), (95, 16), (92, 21), (89, 22), (86, 20), (80, 15),
     (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26),
     (56, 27), (52, 28), (50, 29), (48, 30), (44, 29), (40, 32), (36, 36),
     (30, 36), (27, 37), (23, 36), (19, 40), (15, 44), (12, 44), (8, 44),
     (3, 43), (0, 40), (-2, 37), (-6, 36)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
     (141, 42), (143, 44), (145, 44), (142, 42), (140, 38), (138, 35),
     (135, 33), (131, 32)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (176, -38), (178, -37),
     (174, -41), (170, -44)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (46, -24), (44, -25),
     (43, -20)],
    # Indonesia islands (rough blobs)
    [(95, 5), (98, 3), (100, 0), (98, -3), (95, 0)],
    [(105, -6), (110, -7), (114, -8), (112, -9), (106, -8)],
    [(120, -1), (125, 0), (128, -2), (124, -4), (120, -3)],
    [(132, -2), (136, -3), (138, -5), (134, -6), (131, -4)],
]

# (label, lon, lat, dx, dy, anchor) -- label offset from the dot.
HOTSPOTS = [
    ("Antalya", 30.7, 36.9, -8, -16, "right"),
    ("Riyadh", 46.7, 24.6, -52, 8, "left"),
    ("Junin", -76.0, -11.0, 8, -4, "left"),
    ("Kyiv", 30.5, 50.5, 6, -14, "left"),
    ("Nowa Deba", 21.8, 50.4, -62, 10, "left"),
    ("The Hague", 4.3, 52.1, -70, -14, "left"),
    ("Gaza", 34.5, 31.5, 6, 6, "left"),
    ("Hormuz", 56.5, 26.5, 8, -4, "left"),
    ("Washington", -77.0, 38.9, -78, 6, "left"),
    ("New York", -74.0, 40.7, 6, -16, "left"),
    ("Madrid", -3.7, 40.4, -48, 8, "left"),
    ("Dar es Salaam", 39.3, -6.8, 8, -4, "left"),
    ("Bayelsa", 6.3, 4.8, -52, 10, "left"),
    ("Tokyo", 139.7, 35.7, 6, -4, "left"),
    ("Sydney", 151.2, -33.9, 6, -4, "left"),
    ("Shenzhen", 114.1, 22.5, -60, 10, "left"),
]

# ---- helpers -------------------------------------------------------
def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    draw.text(((x0 + x1 - draw.textlength(text, font=fnt)) / 2, y),
              text, font=fnt, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 26                      # side margin
    CW = W - 2 * MX              # content width

    # ---- masthead --------------------------------------------------
    d.rectangle([0, 0, W, 6], fill=RED)
    centre(d, 14, "THE WORLD IN ONE DAY", F_TITLE, NAVY)
    centre(d, 76, "48 stories from seven regions, in one picture",
           F_SUB, GREY)

    # ---- date band -------------------------------------------------
    d.rectangle([0, 102, W, 150], fill=RED)
    centre(d, 112, "SATURDAY  21  NOVEMBER  2026", F_DATE, (255, 255, 255))

    # ---- three leads ----------------------------------------------
    col_w = (CW - 2 * 24) // 3
    lead_y = 164
    for i, (kick, head, deck) in enumerate(LEADS):
        x = MX + i * (col_w + 24)
        d.rectangle([x, lead_y, x + col_w, lead_y + 3], fill=RED)
        d.text((x, lead_y + 10), kick, font=F_KICK, fill=RED)
        y = lead_y + 30
        for ln in wrap(d, head, F_HEAD, col_w):
            d.text((x, y), ln, font=F_HEAD, fill=NAVY)
            y += 24
        y += 2
        for ln in wrap(d, deck, F_DECK, col_w):
            d.text((x, y), ln, font=F_DECK, fill=(60, 60, 64))
            y += 17
    d.line([MX, 286, MX + CW, 286], fill=(200, 200, 198), width=1)

    # ---- world map -------------------------------------------------
    map_x0, map_y0, map_w, map_h = MX, 292, CW, 138
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                fill=MAP_BG, outline=(190, 194, 196), width=1)

    def proj(lon, lat):
        px = map_x0 + (lon + 180.0) / 360.0 * map_w
        py = map_y0 + (75.0 - lat) / 130.0 * map_h
        return px, py

    # graticule
    for lon in range(-150, 181, 30):
        x, _ = proj(lon, 0)
        d.line([x, map_y0, x, map_y0 + map_h], fill=(210, 215, 218), width=1)
    for lat in range(-30, 76, 30):
        _, y = proj(0, lat)
        d.line([map_x0, y, map_x0 + map_w, y], fill=(210, 215, 218), width=1)
    # land
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # ocean labels
    for label, fx, fy in (("PACIFIC", 0.10, 0.80), ("ATLANTIC", 0.44, 0.82),
                          ("INDIAN", 0.70, 0.82)):
        d.text((map_x0 + fx * map_w, map_y0 + fy * map_h), label,
               font=F_OCEAN, fill=(150, 156, 160))
    # hotspots
    for label, lon, lat, dx, dy, _anchor in HOTSPOTS:
        px, py = proj(lon, lat)
        lx, ly = px + dx, py + dy
        d.text((lx + 1, ly), label, font=F_MAP_LBL, fill=(255, 255, 255))
        d.text((lx - 1, ly), label, font=F_MAP_LBL, fill=(255, 255, 255))
        d.text((lx, ly + 1), label, font=F_MAP_LBL, fill=(255, 255, 255))
        d.text((lx, ly - 1), label, font=F_MAP_LBL, fill=(255, 255, 255))
        d.text((lx, ly), label, font=F_MAP_LBL, fill=NAVY)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=1)

    # ---- stories by region ----------------------------------------
    bar_y = 440
    d.text((MX, bar_y), "STORIES BY REGION", font=F_SEC, fill=NAVY)
    total = "48 IN ALL"
    d.text((MX + CW - d.textlength(total, font=F_SEC), bar_y), total,
           font=F_SEC, fill=RED)
    seg_y, seg_h = 462, 34
    x = MX
    for name in REGIONS:
        w = CW * REGION_COUNTS[name] / 48
        d.rectangle([x, seg_y, x + w - 2, seg_y + seg_h], fill=LIGHT,
                    outline=(205, 205, 202), width=1)
        d.rectangle([x, seg_y, x + w - 2, seg_y + 3], fill=RED)
        d.text((x + 6, seg_y + 6), name, font=F_BAR_NAME, fill=GREY)
        d.text((x + 6, seg_y + 18), str(REGION_COUNTS[name]),
               font=F_BAR_NUM, fill=NAVY)
        x += w

    # ---- day in numbers -------------------------------------------
    num_y = 508
    d.text((MX, num_y), "THE DAY IN NUMBERS", font=F_SEC, fill=NAVY)
    box_y, box_h = 530, 48
    bw = CW / 6
    for i, (val, cap) in enumerate(NUMBERS):
        x = MX + i * bw
        if i:
            d.line([x, box_y + 4, x, box_y + box_h - 4],
                   fill=(205, 205, 202), width=1)
        centre(d, box_y, val, F_NUM, RED, x + 4, x + bw - 4)
        centre(d, box_y + 27, cap, F_NUMCAP, GREY, x + 4, x + bw - 4)

    # ---- the day in brief -----------------------------------------
    brief_y = 586
    d.rectangle([0, brief_y, W, brief_y + 28], fill=NAVY)
    d.text((MX, brief_y + 5), "THE DAY IN BRIEF  \u2014  45 MORE STORIES",
           font=F_BRIEF_HEAD, fill=(255, 255, 255))
    rows_y = brief_y + 36
    row_h = 25.0
    col_w2 = (CW - 2 * 20) // 3
    for idx, (_region, text) in enumerate(BRIEFS):
        col = idx // 15
        row = idx % 15
        x = MX + col * (col_w2 + 20)
        y = rows_y + row * row_h
        d.rectangle([x, y + 3, x + 8, y + 11], fill=RED)
        lines = wrap(d, text, F_BRIEF, col_w2 - 14)[:2]
        ty = y
        for ln in lines:
            d.text((x + 14, ty), ln, font=F_BRIEF, fill=INK)
            ty += 12

    # ---- footer ----------------------------------------------------
    centre(d, 1002,
           "Every story above was reported on Saturday 21 November 2026.",
           F_FOOT, GREY)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
