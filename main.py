#!/usr/bin/env python3
"""Draw the front page of 19 November 2026's world news.

A single self-contained program: it draws the whole poster with Pillow
from the story data embedded below, writes it to entry.png in the output
directory, and uses no network, no randomness and no clock, so every run
produces identical bytes.

Run:  python3 main.py
      MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette: newspaper front page -------------------------------------
PAPER = (247, 243, 234, 255)      # warm off-white
INK = (22, 26, 34, 255)          # near-black
RED = (178, 34, 34, 255)         # headline accent
NAVY = (27, 48, 84, 255)         # header band
GOLD = (198, 148, 52, 255)       # thin rule
LIGHT = (233, 227, 214, 255)     # panel fill
MID = (120, 124, 132, 255)       # secondary text
WHITE = (255, 255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_KICK = font("DejaVuSans-Bold.ttf", 21)
F_DATE = font("DejaVuSans-Bold.ttf", 66)
F_SUB = font("DejaVuSans.ttf", 24)
F_HERO_KICK = font("DejaVuSans-Bold.ttf", 20)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_HERO_SUB = font("DejaVuSans.ttf", 25)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 22)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# --- story data: (kicker, headline, subline, icon key) ------------------
HERO = (
    "SHENZHEN  ·  APEC SIDELINES",
    "Trump, Xi and Putin meet in Shenzhen",
    "Three leaders issue a \u201cpeace declaration\u201d on nuclear risks",
    "summit",
)

STORIES = [
    (
        "THE HAGUE  ·  UN COURT",
        "UN court: Myanmar committed genocide",
        "First ruling of its kind, over the 2017 Rohingya crackdown",
        "scales",
    ),
    (
        "GAZA  ·  MIDDLE EAST",
        "Israel ends first major Gaza raid since truce",
        "Tanks pull back past the \u201cYellow Line\u201d; about 6,000 fled",
        "tank",
    ),
    (
        "RIYADH  ·  SAUDI ARABIA",
        "Houthi missile hits Riyadh\u2019s tallest tower",
        "Saudi wealth fund\u2019s PIF Tower damaged in a new attack",
        "tower",
    ),
    (
        "CRIMEA  ·  RUSSIA\u2013UKRAINE WAR",
        "Ukraine strikes Crimean Bridge again",
        "Russia says it was the third attack on the bridge this week",
        "bridge",
    ),
    (
        "INDIA  ·  BAY OF BENGAL",
        "Cyclone Akvan nears India\u2019s east coast",
        "50,000 evacuated; landfall due Friday near Gopalpur",
        "cyclone",
    ),
    (
        "HORN OF AFRICA",
        "Ethiopia and Eritrea on the brink of war",
        "Troops mass at the border as clashes flare near Badme",
        "flags",
    ),
]

ICON_COLORS = {
    "summit": (178, 34, 34, 255),
    "scales": (27, 48, 84, 255),
    "tank": (74, 94, 58, 255),
    "tower": (120, 72, 20, 255),
    "bridge": (40, 90, 120, 255),
    "cyclone": (30, 110, 130, 255),
    "flags": (150, 40, 60, 255),
}


def draw_icon(draw, kind, cx, cy, r):
    """Simple flat pictogram centred at (cx, cy) inside radius r."""
    c = ICON_COLORS[kind]
    d = draw
    if kind == "summit":
        # three overlapping circles: the three leaders' flags
        cols = [(178, 34, 34, 255), (200, 40, 40, 255), (27, 48, 84, 255)]
        offs = [(-r * 0.55, r * 0.25), (0, -r * 0.45), (r * 0.55, r * 0.25)]
        for (ox, oy), col in zip(offs, cols):
            d.ellipse([cx + ox - r * 0.42, cy + oy - r * 0.42,
                       cx + ox + r * 0.42, cy + oy + r * 0.42],
                      fill=col, outline=WHITE, width=3)
    elif kind == "scales":
        d.line([cx, cy - r, cx, cy + r * 0.8], fill=c, width=6)
        d.line([cx - r * 0.9, cy - r * 0.55, cx + r * 0.9, cy - r * 0.55],
               fill=c, width=6)
        for s in (-1, 1):
            x0 = cx + s * r * 0.9
            d.line([x0, cy - r * 0.55, x0, cy + r * 0.1], fill=c, width=3)
            d.polygon([(x0 - r * 0.45, cy + r * 0.1), (x0 + r * 0.45, cy + r * 0.1),
                       (x0, cy + r * 0.75)], fill=c)
        d.rectangle([cx - r * 0.55, cy + r * 0.8, cx + r * 0.55, cy + r * 0.95],
                    fill=c)
    elif kind == "tank":
        d.rectangle([cx - r, cy - r * 0.15, cx + r * 0.75, cy + r * 0.35],
                    fill=c)
        d.ellipse([cx - r * 0.25, cy - r * 0.55, cx + r * 0.25, cy - r * 0.05],
                  fill=c)
        d.line([cx + r * 0.2, cy - r * 0.3, cx + r * 1.15, cy - r * 0.45],
               fill=c, width=7)
        for i in range(5):
            x = cx - r + i * r * 0.42
            d.ellipse([x, cy + r * 0.35, x + r * 0.34, cy + r * 0.69],
                      fill=c)
    elif kind == "tower":
        d.rectangle([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                    fill=c)
        for row in range(5):
            y = cy - r * 0.75 + row * r * 0.36
            for col in range(3):
                x = cx - r * 0.32 + col * r * 0.32
                d.rectangle([x, y, x + r * 0.18, y + r * 0.18], fill=GOLD)
        # crack of damage near the top
        d.line([cx + r * 0.45, cy - r * 0.9, cx + r * 0.15, cy - r * 0.55,
                cx + r * 0.45, cy - r * 0.3], fill=WHITE, width=4)
    elif kind == "bridge":
        d.line([cx - r, cy + r * 0.5, cx + r, cy + r * 0.5], fill=c, width=7)
        d.arc([cx - r, cy - r * 0.6, cx + r, cy + r * 0.9], start=180, end=360,
              fill=c, width=7)
        for s in (-0.7, -0.35, 0, 0.35, 0.7):
            x = cx + s * r
            top = cy - r * 0.55 + abs(s) * r * 0.5
            d.line([x, top, x, cy + r * 0.5], fill=c, width=4)
    elif kind == "cyclone":
        for i, rr in enumerate([r, r * 0.72, r * 0.46, r * 0.22]):
            start = 200 + i * 95
            d.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=start,
                  end=start + 250, fill=c, width=7)
    elif kind == "flags":
        d.line([cx - r * 0.55, cy - r, cx - r * 0.55, cy + r], fill=c, width=5)
        d.line([cx + r * 0.55, cy - r, cx + r * 0.55, cy + r], fill=c, width=5)
        d.polygon([(cx - r * 0.55, cy - r), (cx + r * 0.15, cy - r),
                   (cx - r * 0.05, cy - r * 0.45), (cx - r * 0.55, cy - r * 0.45)],
                  fill=(178, 34, 34, 255))
        d.polygon([(cx + r * 0.55, cy - r), (cx - r * 0.15, cy - r),
                   (cx + r * 0.05, cy - r * 0.45), (cx + r * 0.55, cy - r * 0.45)],
                  fill=(27, 48, 84, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 158], fill=NAVY)
    d.rectangle([0, 158, W, 164], fill=GOLD)
    kick = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(kick, font=F_KICK)) / 2, 16), kick,
           font=F_KICK, fill=GOLD)
    date = "19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 44), date,
           font=F_DATE, fill=WHITE)
    sub = "Thursday  \u00b7  Seven stories from around the globe"
    d.text(((W - d.textlength(sub, font=F_SUB)) / 2, 122), sub,
           font=F_SUB, fill=(210, 216, 228, 255))

    # --- hero story -----------------------------------------------------
    hx, hy, hw, hh = 24, 182, W - 48, 196
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=LIGHT, outline=INK, width=2)
    d.rectangle([hx, hy, hx + 10, hy + hh], fill=RED)
    draw_icon(d, HERO[3], hx + 88, hy + hh // 2, 52)
    tx = hx + 158
    d.text((tx, hy + 16), HERO[0], font=F_HERO_KICK, fill=RED)
    head_lines = wrap(d, HERO[1], F_HERO_HEAD, hw - 158 - 24)
    draw_lines(d, tx, hy + 44, head_lines, F_HERO_HEAD, INK, 48)
    sub_lines = wrap(d, HERO[2], F_HERO_SUB, hw - 158 - 24)
    draw_lines(d, tx, hy + 146, sub_lines, F_HERO_SUB, MID, 30)

    # --- six story panels, 2 columns x 3 rows ---------------------------
    gx, gy = 24, 396
    pw, ph = (W - 48 - 20) // 2, 186
    gap = 20
    for i, (kicker, head, body, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (pw + gap)
        y = gy + row * (ph + 14)
        d.rectangle([x, y, x + pw, y + ph], fill=LIGHT, outline=INK, width=2)
        d.rectangle([x, y, x + pw, y + 5], fill=ICON_COLORS[icon])
        draw_icon(d, icon, x + 52, y + 62, 34)
        tx = x + 96
        d.text((tx, y + 14), kicker, font=F_KICKER, fill=RED)
        head_lines = wrap(d, head, F_HEAD, pw - 96 - 16)
        y2 = draw_lines(d, tx, y + 42, head_lines, F_HEAD, INK, 35)
        body_lines = wrap(d, body, F_BODY, pw - 96 - 16)
        draw_lines(d, tx, y2 + 4, body_lines, F_BODY, MID, 27)

    # --- footer ---------------------------------------------------------
    fy = 988
    foot = ("Sources: Reuters, AFP, DPA, The Japan Times, The Hindu, NYT  "
            "\u00b7  Drawn with Python + Pillow")
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, fy), foot,
           font=F_FOOT, fill=MID)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    os.makedirs(out_dir, exist_ok=True)
    img = build()
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
