#!/usr/bin/env python3
"""News Image 20261125 v3 — The World in One Day (Wednesday 25 November 2026).

Front page, 1024x1024, drawn fresh with Python PIL and DejaVu fonts only.
Layout follows the winning pattern of the 23/24 November editions:
13 illustrated stories (3 big leads + 10 small), each with an original
drawn scene and a certainty badge; stats strip; UTC ticker; region bar;
a real world map with numbered pins; an ALSO ON list with UTC times and
source codes (C = 2+ outlets, O = official, R = one outlet, CL = one side's
claim); and a DATE CHECK
box naming what was deliberately left out because it happened earlier.

Every story here happened, or was first reported, on Wednesday
25 November 2026 (UTC). Stories from 24 November or earlier are listed
in the DATE CHECK box, not shown as today's news.

Deterministic: re-running produces byte-identical output.
Usage: python3 draw_frontpage.py entry.png
"""
import math
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (31, 78, 121)
SEA = (215, 229, 234)
LAND = (232, 220, 192)
LAND_LINE = (180, 164, 130)
GREY = (110, 110, 108)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS_I = "DejaVuSans-Oblique.ttf"
SERIF_I = "DejaVuSerif-Italic.ttf"


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def badge(d, x, y, label):
    """Certainty badge: filled pill, returns width used."""
    fnt = font(SANS_B, 10)
    w = int(d.textlength(label, font=fnt)) + 12
    fill = {"CONFIRMED": (27, 94, 32), "OFFICIAL": (122, 96, 10),
            "REPORTED": (31, 78, 121), "CLAIM": (176, 92, 0),
            "ONGOING": (90, 40, 140)}.get(label, BLUE)
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    d.text((x + 6, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def num_badge(d, x, y, n, r=11, fs=13):
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    fnt = font(SANS_B, fs)
    d.text((x, y - 1), str(n), font=fnt, fill=(255, 255, 255), anchor="mm")


# ---------------------------------------------------------------- scenes
# Each scene draws an original flat illustration inside (x, y, w, h).

def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 52))
    for sx, sy in [(0.12, 0.18), (0.3, 0.1), (0.55, 0.22), (0.8, 0.12),
                   (0.9, 0.3), (0.2, 0.35), (0.65, 0.08)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2],
                  fill=(255, 255, 255))
    d.ellipse([x + w * 0.72, y + h * 0.12, x + w * 0.95, y + h * 0.32],
              fill=(235, 225, 200))
    cx = x + w * 0.45
    d.polygon([(cx, y + h * 0.08), (cx - w * 0.07, y + h * 0.62),
               (cx + w * 0.07, y + h * 0.62)], fill=(240, 240, 240))
    d.polygon([(cx, y + h * 0.08), (cx - w * 0.03, y + h * 0.22),
               (cx + w * 0.03, y + h * 0.22)], fill=RED)
    d.polygon([(cx - w * 0.07, y + h * 0.5), (cx - w * 0.13, y + h * 0.68),
               (cx - w * 0.07, y + h * 0.62)], fill=(200, 40, 40))
    d.polygon([(cx + w * 0.07, y + h * 0.5), (cx + w * 0.13, y + h * 0.68),
               (cx + w * 0.07, y + h * 0.62)], fill=(200, 40, 40))
    d.polygon([(cx - w * 0.05, y + h * 0.62), (cx, y + h * 0.95),
               (cx + w * 0.05, y + h * 0.62)], fill=(255, 170, 40))
    d.rectangle([x, y + h * 0.9, x + w, y + h], fill=(60, 60, 60))
    d.rectangle([x + w * 0.75, y + h * 0.55, x + w * 0.82, y + h * 0.9],
                fill=(120, 120, 120))


def scene_whitehouse(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 180, 210))
    d.ellipse([x + w * 0.78, y + h * 0.08, x + w * 0.95, y + h * 0.28],
              fill=(255, 240, 180))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(90, 140, 70))
    d.rectangle([x + w * 0.2, y + h * 0.42, x + w * 0.8, y + h * 0.8],
                fill=(245, 245, 240))
    d.pieslice([x + w * 0.42, y + h * 0.22, x + w * 0.58, y + h * 0.5],
               180, 360, fill=(245, 245, 240))
    for i in range(5):
        cx = x + w * (0.28 + i * 0.11)
        d.rectangle([cx - 3, y + h * 0.5, cx + 3, y + h * 0.8], fill=(200, 200, 190))
    d.rectangle([x + w * 0.48, y + h * 0.12, x + w * 0.49, y + h * 0.24],
                fill=(80, 80, 80))
    d.polygon([(x + w * 0.49, y + h * 0.12), (x + w * 0.49, y + h * 0.2),
               (x + w * 0.56, y + h * 0.16)], fill=(180, 40, 40))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 236, 222))
    d.line([x + w * 0.12, y + h * 0.15, x + w * 0.12, y + h * 0.85,
            x + w * 0.92, y + h * 0.85], fill=INK, width=2)
    bars = [0.18, 0.28, 0.34, 0.45, 0.52, 0.78]
    for i, b in enumerate(bars):
        bx = x + w * (0.18 + i * 0.13)
        d.rectangle([bx, y + h * (0.85 - b), bx + w * 0.09, y + h * 0.85],
                    fill=RED if i == len(bars) - 1 else (120, 120, 120))
    d.text((x + w * 0.14, y + h * 0.05), "700,000+", font=font(SANS_B, 15),
           fill=RED)


def scene_city_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 60))
    d.polygon([(x + w * 0.05, y + h), (x + w * 0.05, y + h * 0.4),
               (x + w * 0.3, y + h * 0.4), (x + w * 0.3, y + h)],
              fill=(25, 25, 40))
    d.polygon([(x + w * 0.35, y + h), (x + w * 0.35, y + h * 0.25),
               (x + w * 0.62, y + h * 0.25), (x + w * 0.62, y + h)],
              fill=(30, 30, 48))
    d.polygon([(x + w * 0.68, y + h), (x + w * 0.68, y + h * 0.5),
               (x + w * 0.95, y + h * 0.5), (x + w * 0.95, y + h)],
              fill=(25, 25, 40))
    for wx in (0.12, 0.2, 0.44, 0.53, 0.76, 0.86):
        d.rectangle([x + w * wx, y + h * 0.55, x + w * wx + 6, y + h * 0.62],
                    fill=(255, 220, 120))
    d.polygon([(x + w * 0.42, y + h * 0.75), (x + w * 0.48, y + h * 0.45),
               (x + w * 0.54, y + h * 0.75)], fill=(255, 140, 20))
    d.polygon([(x + w * 0.5, y + h * 0.75), (x + w * 0.55, y + h * 0.5),
               (x + w * 0.6, y + h * 0.75)], fill=(255, 200, 60))
    d.ellipse([x + w * 0.6, y + h * 0.12, x + w * 0.72, y + h * 0.28],
              fill=(120, 120, 130))
    d.ellipse([x + w * 0.7, y + h * 0.05, x + w * 0.84, y + h * 0.22],
              fill=(100, 100, 110))


def scene_rubble_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 185, 170))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.55), (x + w * 0.6, y + h)],
              fill=(140, 135, 120))
    d.polygon([(x + w * 0.45, y + h), (x + w * 0.7, y + h * 0.6),
               (x + w, y + h)], fill=(120, 115, 100))
    d.rectangle([x + w * 0.62, y + h * 0.12, x + w * 0.9, y + h * 0.42],
                fill=(0, 51, 153))
    for k in range(8):
        a = math.pi * (0.25 + k * 0.25)
        sx = x + w * 0.76 + 14 * math.cos(a)
        sy = y + h * 0.27 + 10 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 0))


def scene_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 215, 225))
    d.rectangle([x, y + h * 0.8, x + w, y + h], fill=(110, 150, 90))
    d.rectangle([x + w * 0.15, y + h * 0.55, x + w * 0.85, y + h * 0.8],
                fill=(235, 235, 230))
    d.pieslice([x + w * 0.4, y + h * 0.2, x + w * 0.6, y + h * 0.6],
               180, 360, fill=(235, 235, 230))
    d.rectangle([x + w * 0.495, y + h * 0.08, x + w * 0.505, y + h * 0.22],
                fill=(80, 80, 80))
    for i in range(6):
        cx = x + w * (0.22 + i * 0.096)
        d.rectangle([cx - 3, y + h * 0.6, cx + 3, y + h * 0.8], fill=(190, 190, 180))


def scene_sea_ships(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(170, 205, 225))
    d.ellipse([x + w * 0.8, y + h * 0.08, x + w * 0.93, y + h * 0.24],
              fill=(255, 235, 160))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(40, 110, 160))
    d.polygon([(x + w * 0.1, y + h * 0.62), (x + w * 0.42, y + h * 0.62),
               (x + w * 0.38, y + h * 0.8), (x + w * 0.14, y + h * 0.8)],
              fill=(70, 70, 80))
    d.rectangle([x + w * 0.22, y + h * 0.42, x + w * 0.24, y + h * 0.62],
                fill=(70, 70, 80))
    d.polygon([(x + w * 0.6, y + h * 0.68), (x + w * 0.88, y + h * 0.68),
               (x + w * 0.84, y + h * 0.82), (x + w * 0.64, y + h * 0.82)],
              fill=(90, 90, 100))
    for wy in (0.6, 0.72, 0.86):
        d.line([x + w * 0.05, y + h * wy, x + w * 0.95, y + h * wy],
               fill=(255, 255, 255), width=1)


def scene_server(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(25, 30, 45))
    for i in range(3):
        rx = x + w * (0.1 + i * 0.28)
        d.rectangle([rx, y + h * 0.12, rx + w * 0.22, y + h * 0.88],
                    fill=(60, 70, 90))
        for j in range(4):
            d.rectangle([rx + 4, y + h * (0.2 + j * 0.17),
                         rx + w * 0.22 - 4, y + h * (0.2 + j * 0.17) + 5],
                        fill=(40, 50, 65))
            d.ellipse([rx + 6, y + h * (0.2 + j * 0.17) + 1,
                       rx + 10, y + h * (0.2 + j * 0.17) + 5],
                      fill=(0, 220, 90) if (i + j) % 2 else (255, 60, 60))
    d.ellipse([x + w * 0.68, y + h * 0.35, x + w * 0.92, y + h * 0.72],
              outline=(255, 210, 0), width=4)
    d.rectangle([x + w * 0.76, y + h * 0.5, x + w * 0.84, y + h * 0.62],
                fill=(255, 210, 0))


def scene_port(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.6], fill=(180, 210, 225))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(50, 110, 150))
    d.polygon([(x + w * 0.15, y + h * 0.7), (x + w * 0.55, y + h * 0.7),
               (x + w * 0.5, y + h * 0.82), (x + w * 0.2, y + h * 0.82)],
              fill=(40, 40, 50))
    for i, c in enumerate([(200, 60, 60), (60, 120, 200), (220, 160, 40)]):
        d.rectangle([x + w * (0.12 + i * 0.2), y + h * 0.78,
                     x + w * (0.28 + i * 0.2), y + h * 0.92], fill=c)
    d.line([x + w * 0.62, y + h * 0.1, x + w * 0.62, y + h * 0.6],
           fill=(60, 60, 60), width=3)
    d.line([x + w * 0.62, y + h * 0.1, x + w * 0.95, y + h * 0.28],
           fill=(60, 60, 60), width=3)
    d.line([x + w * 0.95, y + h * 0.28, x + w * 0.95, y + h * 0.45],
           fill=(60, 60, 60), width=2)


def scene_envelope(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    d.rectangle([x + w * 0.18, y + h * 0.3, x + w * 0.82, y + h * 0.75],
                fill=(255, 255, 255), outline=(150, 150, 150))
    d.polygon([(x + w * 0.18, y + h * 0.3), (x + w * 0.5, y + h * 0.58),
               (x + w * 0.82, y + h * 0.3)], outline=(150, 150, 150))
    d.rectangle([x + w * 0.1, y + h * 0.12, x + w * 0.3, y + h * 0.24],
                fill=(180, 40, 40))
    d.rectangle([x + w * 0.7, y + h * 0.12, x + w * 0.9, y + h * 0.24],
                fill=(40, 80, 160))
    d.ellipse([x + w * 0.78, y + h * 0.15, x + w * 0.82, y + h * 0.21],
              fill=(255, 255, 255))


def scene_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 215))
    d.ellipse([x + w * 0.7, y + h * 0.1, x + w * 0.9, y + h * 0.32],
              fill=(255, 240, 180))
    d.line([x + w * 0.05, y + h * 0.75, x + w * 0.55, y + h * 0.3],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.5, y + h * 0.22, x + w * 0.62, y + h * 0.38],
              fill=(60, 60, 70))
    d.line([x + w * 0.42, y + h * 0.3, x + w * 0.7, y + h * 0.3],
           fill=(60, 60, 70), width=3)
    d.ellipse([x + w * 0.4, y + h * 0.26, x + w * 0.44, y + h * 0.34],
              fill=(40, 40, 50))
    d.ellipse([x + w * 0.68, y + h * 0.26, x + w * 0.72, y + h * 0.34],
              fill=(40, 40, 50))
    d.ellipse([x + w * 0.53, y + h * 0.55, x + w * 0.63, y + h * 0.7],
              fill=(255, 150, 40))


def scene_phone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 225, 215))
    d.rounded_rectangle([x + w * 0.32, y + h * 0.08, x + w * 0.68, y + h * 0.95],
                        radius=8, fill=(30, 30, 35))
    d.rectangle([x + w * 0.36, y + h * 0.16, x + w * 0.64, y + h * 0.85],
                fill=(220, 235, 245))
    d.rounded_rectangle([x + w * 0.38, y + h * 0.22, x + w * 0.6, y + h * 0.4],
                        radius=4, fill=(255, 255, 255))
    d.rounded_rectangle([x + w * 0.4, y + h * 0.48, x + w * 0.62, y + h * 0.66],
                        radius=4, fill=(180, 220, 255))
    d.ellipse([x + w * 0.12, y + h * 0.3, x + w * 0.22, y + h * 0.42],
              fill=(200, 60, 60))
    d.ellipse([x + w * 0.78, y + h * 0.55, x + w * 0.88, y + h * 0.67],
              fill=(200, 60, 60))


def scene_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(170, 200, 220))
    d.polygon([(x, y + h * 0.55), (x + w * 0.25, y + h * 0.15),
               (x + w * 0.5, y + h * 0.55)], fill=(120, 120, 130))
    d.polygon([(x + w * 0.3, y + h * 0.55), (x + w * 0.6, y + h * 0.05),
               (x + w * 0.9, y + h * 0.55)], fill=(90, 95, 105))
    d.polygon([(x + w * 0.55, y + h * 0.05), (x + w * 0.6, y + h * 0.05),
               (x + w * 0.66, y + h * 0.2), (x + w * 0.57, y + h * 0.18)],
              fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(240, 236, 222))
    d.line([(x + w * 0.05, y + h * 0.78), (x + w * 0.2, y + h * 0.78),
            (x + w * 0.28, y + h * 0.62), (x + w * 0.36, y + h * 0.92),
            (x + w * 0.44, y + h * 0.66), (x + w * 0.52, y + h * 0.86),
            (x + w * 0.6, y + h * 0.78), (x + w * 0.95, y + h * 0.78)],
           fill=RED, width=2)


SCENES = {"rocket": scene_rocket, "whitehouse": scene_whitehouse,
          "chart": scene_chart, "city_fire": scene_city_fire,
          "rubble_eu": scene_rubble_eu, "capitol": scene_capitol,
          "sea_ships": scene_sea_ships, "server": scene_server,
          "port": scene_port, "envelope": scene_envelope,
          "drone": scene_drone, "phone": scene_phone, "quake": scene_quake}

# ---------------------------------------------------------------- stories
# (n, place, certainty, label, headline, summary, source, scene)
LEADS = [
    (1, "JIUQUAN, CHINA", "CONFIRMED", "SHENZHOU-24",
     "Shenzhou-24 docks with first foreigner aboard",
     "Lifts off 00:18 UTC, docks 03:56 UTC. Zeeshan Ali is the first "
     "foreigner aboard.",
     "Reuters", "rocket"),
    (2, "WASHINGTON, US", "REPORTED", "TRUMP ON IRAN",
     "Trump: Iran war \u2018funded\u2019 through January",
     "Trump says the Iran war is \u2018funded\u2019 through January in a new "
     "interview, and hints at talks.",
     "NY Post", "whitehouse"),
    (3, "RUSSIA \u2013 UKRAINE", "REPORTED", "700,000+ DEAD",
     "700,000+ Russian soldiers killed, new analysis finds",
     "More than 700,000 Russian soldiers have been killed in the war, a new "
     "analysis finds, nearly five years in.",
     "RFE/RL", "chart"),
]

SMALL = [
    (4, "ODESA, UKRAINE", "REPORTED", "2 KILLED",
     "Odesa strike kills 2; Kyiv drone fire injures 2",
     "A Russian strike kills two; a Kyiv drone fire injures two more.",
     "Reuters", "city_fire"),
    (5, "KYIV, UKRAINE", "REPORTED", "3 KILLED",
     "Russian attacks kill 3; EU accuses Putin of stalling",
     "Russian attacks kill three; the EU accuses Putin of stalling.",
     "Al Jazeera", "rubble_eu"),
    (6, "WASHINGTON, US", "REPORTED", "TRUMP DEFENDS",
     "Trump: \u2018certainly not corrupt\u2019",
     "Trump defends himself: \u2018certainly not corrupt\u2019, he says.",
     "NY Post", "capitol"),
    (7, "KUALA LUMPUR", "REPORTED", "NO SEA CODE",
     "ASEAN\u2013China fail on South China Sea code",
     "ASEAN and China fail to agree a South China Sea code.",
     "Al Jazeera", "sea_ships"),
    (8, "VIRGINIA, US", "REPORTED", "CYBER BREACH",
     "CIA hit by cyber breach",
     "A breach exposes data on a CIA network; the DNI is also hit.",
     "CNN / Fox", "server"),
    (9, "YEMEN", "REPORTED", "REFINERY HIT",
     "Houthis hit Saudi refinery, Riyadh district",
     "Houthis say they hit Ras Tanura refinery and Riyadh's district.",
     "Reuters", "port"),
    (10, "WASHINGTON, US", "REPORTED", "KIM LETTERS",
     "Trump: Kim \u2018love letters\u2019 could restart",
     "Trump says his \u2018love letters\u2019 with Kim could restart.",
     "NY Post", "envelope"),
    (11, "UKRAINE", "REPORTED", "DRONE DOWNED",
     "Geran-5 interceptor downed",
     "A German-Ukrainian firm says an interceptor downed a Geran-5.",
     "Defence Express", "drone"),
    (12, "JERUSALEM, ISRAEL", "REPORTED", "1,542 CASES",
     "TikTok leads online abuse of women in Israel",
     "TikTok leads online abuse of women in Israel, 1,542 cases.",
     "Jerusalem Post", "phone"),
    (13, "MYANMAR", "REPORTED", "FAULT STUDY",
     "Myanmar quake fault study",
     "A Myanmar quake shows how fault history predicts the next slip.",
     "Phys.org", "quake"),
]

# (n, UTC time, headline, source code: C = 2+ outlets, O = official,
#  R = one outlet, CL = one side's claim)
ALSO_ON = [
    (14, "00:45", "Zelensky peace deal by Jan", "R"),
    (15, "00:45", "Iran sues US over school strike", "R"),
    (16, "04:00", "N. Korea expels Swiss envoy", "C"),
    (17, "06:12", "Trump weighs a second carrier", "R"),
    (18, "07:07", "Army to detonate 5 tons of lead azide", "R"),
    (19, "07:07", "Two Libyan soldiers die of wounds", "R"),
    (20, "02:12", "Ukraine hits two Rosneft refineries", "C"),
    (21, "07:18", "2,091 Russians killed in a day", "O"),
    (22, "09:18", "Russia hits power in 5 regions", "R"),
    (23, "13:18", "Ukraine hits air base, 5 planes lost", "C"),
    (24, "11:30", "RSF drones kill 19 in Sudan", "C"),
    (25, "06:29", "Solomons signs Australia pact", "C"),
    (26, "10:36", "Cartagena hostages freed", "C"),
    (27, "06:30", "KOSPI tumbles 6.2%", "C"),
]

STATS = [
    ("700,000+", "Russian soldiers killed, new analysis"),
    ("2", "killed in the Odesa strike"),
    ("3", "killed in Russian attacks"),
    ("1,542", "online abuse cases in Israel"),
    ("3", "taikonauts aboard Shenzhou-24"),
]

TICKER = [
    ("00:18", "Shenzhou-24 up"),
    ("00:52", "CIA breach"),
    ("01:01", "700,000+ dead"),
    ("01:06", "ASEAN code fails"),
    ("03:56", "Shenzhou-24 docks"),
]

# Turn A counts: 27 stories (19 v2 + 8 new); Turn B brings 36.
# Short names + 8pt bar labels: the 1-story segments are 27px wide.
REGIONS = [("EUROPE", 8, (31, 78, 121)), ("MIDDLE EAST", 4, (196, 110, 0)),
           ("ASIA-PACIFIC", 4, (16, 185, 129)),
           ("S-E ASIA", 2, (6, 182, 212)),
           ("S. ASIA", 0, (249, 115, 22)),
           ("AMERICAS", 6, (90, 40, 140)),
           ("LATAM", 1, (236, 72, 153)),
           ("AFRICA", 2, (40, 120, 60))]

DATE_CHECK = (
    "Left out, before Wednesday: Benghazi warship sinking (Sun 22) \u00b7 "
    "Hormuz tankers hit by mines (22\u201323 Nov) \u00b7 Nvidia +31.5% (Mon 23); "
    "Tuesday\u2019s \u22126% fade (Tue 24) \u00b7 Riyadh PIF tower, 11 wounded (Tue 24) "
    "\u00b7 Sarkozy trial, EU sanctions, $8.7bn to Ukraine (Mon\u2013Tue 24) \u00b7 Gaza "
    "Hamas chief killed, Sanofi $41bn, Baghdad oilfields, Nepal quake (Tue 24) "
    "\u00b7 FBI hack (Fri 20) \u00b7 Indonesia VP resigns (12 Nov) \u00b7 DR Congo "
    "pullback, Cartagena hostages, UK Houthi sanctions, Nigeria emir, Hegseth "
    "Patriots, BJP\u2013SAD alliance (Tue 24)."
)

# display offsets (px) for pins that would otherwise stack on the map
# (pins 1-13 only; ALSO ON items 14+ carry no map pin)
PIN_OFFSETS = {4: (-14, 10), 6: (18, -16), 10: (-18, 14), 8: (16, 14),
               11: (16, -8)}

# (lon, lat) for each numbered pin (1-13: the illustrated stories)
PINS = {1: (98.5, 40.9), 2: (-77.0, 39.0), 3: (37.6, 55.7),
        4: (30.7, 46.5), 5: (30.5, 50.4), 6: (-74.5, 41.5),
        7: (101.7, 3.1), 8: (-79.5, 37.5), 9: (42.9, 14.8),
        10: (-80.5, 35.5), 11: (33.0, 48.5), 12: (35.2, 31.8),
        13: (96.0, 21.0)}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 50), (-70, 42), (-80, 32), (-90, 20), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-140, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-40, 70), (-55, 76), (-65, 76)],
    [(-80, 10), (-70, 12), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-50, -30), (-60, -38), (-70, -50), (-75, -40),
     (-75, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (45, 0), (40, -10),
     (35, -25), (30, -35), (20, -35), (15, -25), (12, -5), (9, 4),
     (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (25, 65), (20, 70), (15, 70), (5, 60), (-5, 58), (-10, 54),
     (-10, 43)],
    [(30, 62), (40, 68), (60, 69), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (160, 55), (155, 50),
     (142, 45), (135, 40), (130, 35), (127, 33), (122, 30), (120, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 15), (75, 10), (72, 20), (65, 25), (60, 25), (55, 26),
     (50, 29), (48, 30), (45, 30), (40, 35), (35, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (136, -12), (132, -12),
     (126, -14), (122, -17), (118, -20)],
]


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SEA, outline=GREY)
    def proj(lon, lat):
        px = x0 + (lon + 170) / 360.0 * (x1 - x0)
        py = y0 + (75 - lat) / 130.0 * (y1 - y0)
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_LINE)
    for n, (lon, lat) in PINS.items():
        px, py = proj(lon, lat)
        ox, oy = PIN_OFFSETS.get(n, (0, 0))
        if (ox, oy) != (0, 0):
            d.line([px, py, px + ox, py + oy], fill=RED, width=1)
            px, py = px + ox, py + oy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=font(SANS_B, 10),
               fill=(255, 255, 255), anchor="mm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 14

    # masthead strip
    f_top = font(SANS_B, 13)
    d.text((mx, 8), "THE WORLD IN ONE DAY \u00b7 ONE PAGE",
           font=f_top, fill=RED)
    right = "27 STORIES \u00b7 8 REGIONS \u00b7 ALL FROM WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - mx, 8), right, font=f_top, fill=RED, anchor="ra")
    d.line([mx, 28, W - mx, 28], fill=INK, width=2)

    d.text((W // 2, 34), "Wednesday 25 November 2026",
           font=font(SERIF_B, 56), fill=INK, anchor="ma")
    d.text((W // 2, 94),
           "Shenzhou-24 docks with a Pakistani aboard \u25c6 Trump: Iran war "
           "\u2018funded\u2019 to January \u25c6 700,000 Russian dead",
           font=font(SERIF_I, 16), fill=RED, anchor="ma")
    d.line([mx, 114, W - mx, 114], fill=INK, width=1)

    # stats strip
    y = 118
    cell_w = (W - 2 * mx) / len(STATS)
    for i, (num, lab) in enumerate(STATS):
        cx = mx + cell_w * i + cell_w / 2
        d.text((cx, y), num, font=font(SERIF_B, 28), fill=INK, anchor="ma")
        d.text((cx, y + 33), lab, font=font(SANS, 11), fill=GREY, anchor="ma")
        if i:
            d.line([mx + cell_w * i, y + 4, mx + cell_w * i, y + 48],
                   fill=(200, 195, 180), width=1)

    # region bar (only regions with stories; two passes so a label that
    # overflows its narrow segment is never painted over by the next one)
    y = 172
    shown = [(n, c, col) for n, c, col in REGIONS if c]
    tot = sum(c for _, c, _ in shown)
    bx = mx
    segs = []
    for name, c, col in shown:
        seg = int((W - 2 * mx) * c / tot)
        d.rectangle([bx, y, bx + seg - 2, y + 18], fill=col)
        segs.append((bx, seg, name, c))
        bx += seg
    for bx, seg, name, c in segs:
        lab = f"{name} {c}"
        lw_ = d.textlength(lab, font=font(SANS_B, 8))
        lx_ = min(max(bx + seg / 2, mx + lw_ / 2), W - mx - lw_ / 2)
        d.text((lx_, y + 5), lab, font=font(SANS_B, 8),
               fill=(255, 255, 255), anchor="ma")

    # UTC ticker
    y = 196
    d.rectangle([mx, y, mx + 108, y + 18], fill=RED)
    d.text((mx + 54, y + 3), "THE DAY IN UTC", font=font(SANS_B, 10),
           fill=(255, 255, 255), anchor="ma")
    tick = "  \u00b7  ".join(f"{t} {s}" for t, s in TICKER)
    d.text((mx + 116, y + 2), tick, font=font(SANS_B, 11), fill=INK)

    # 3 big leads
    ly, lh = 218, 222
    lw = (W - 2 * mx - 16) / 3
    for i, (n, place, cert, label, head, summ, src, kind) in enumerate(LEADS):
        x = mx + i * (lw + 8)
        SCENES[kind](d, x, ly, lw, 104)
        d.rectangle([x, ly + 104 - 18, x + lw, ly + 104], fill=RED)
        d.text((x + 6, ly + 104 - 14), label, font=font(SANS_B, 11),
               fill=(255, 255, 255))
        num_badge(d, x + 16, ly + 122, n)
        d.text((x + 32, ly + 114), place, font=font(SANS_B, 11), fill=RED)
        badge(d, x + lw - 78, ly + 113, cert)
        hy = ly + 136
        hy = text_lines(d, x, hy, wrap(d, head, font(SERIF_B, 19), lw),
                        font(SERIF_B, 19), leading=22)
        text_lines(d, x, hy + 2, wrap(d, summ, font(SANS, 12), lw),
                   font(SANS, 12), leading=15)
        d.text((x, ly + lh - 12), f"({src})", font=font(SANS_I, 10),
               fill=GREY)

    # 10 small illustrated stories, 2 rows x 5
    sy, sh = 446, 140
    sw = (W - 2 * mx - 32) / 5
    for i, (n, place, cert, label, head, summ, src, kind) in enumerate(SMALL):
        row, col = divmod(i, 5)
        x = mx + col * (sw + 8)
        y0 = sy + row * (sh + 6)
        SCENES[kind](d, x, y0, sw, 50)
        d.rectangle([x, y0 + 50 - 14, x + sw, y0 + 50], fill=INK)
        d.text((x + 5, y0 + 50 - 11), label, font=font(SANS_B, 9),
               fill=(255, 255, 255))
        num_badge(d, x + 13, y0 + 64, n, r=10)
        d.text((x + 28, y0 + 56), place, font=font(SANS_B, 9), fill=RED)
        badge(d, x + sw - 74, y0 + 55, cert)
        hy = y0 + 76
        hy = text_lines(d, x, hy, wrap(d, head, font(SERIF_B, 13), sw),
                        font(SERIF_B, 13), leading=15)
        text_lines(d, x, hy + 1, wrap(d, summ, font(SANS, 10), sw),
                   font(SANS, 10), leading=12)
        d.text((x, y0 + sh - 10), f"({src})", font=font(SANS_I, 9),
               fill=GREY)

    # bottom: map + also on (two columns of ALSO ON, 12 rows each)
    by = 738
    d.text((mx, by), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=RED)
    d.text((mx + 172, by), "pins carry the story numbers",
           font=font(SANS_I, 11), fill=GREY)
    draw_map(d, mx, by + 20, 414, by + 172)

    ax = 430
    d.text((ax, by), "ALSO ON WEDNESDAY 25 NOVEMBER 2026",
           font=font(SANS_B, 13), fill=RED)
    ay0 = by + 24
    half = (len(ALSO_ON) + 1) // 2
    for j, (n, t, head, code) in enumerate(ALSO_ON):
        col, row = (0, j) if j < half else (1, j - half)
        cx = ax + col * 298
        ay = ay0 + row * 14
        num_badge(d, cx + 7, ay + 7, n, r=7, fs=9)
        d.text((cx + 20, ay), f"{t} {head} ({code})",
               font=font(SANS, 9), fill=INK)

    # DATE CHECK
    dy = 934
    d.rectangle([mx, dy, W - mx, dy + 56], outline=RED, width=2)
    d.rectangle([mx, dy, mx + 96, dy + 56], fill=RED)
    d.text((mx + 48, dy + 20), "DATE CHECK", font=font(SANS_B, 12),
           fill=(255, 255, 255), anchor="mm")
    text_lines(d, mx + 106, dy + 5,
               wrap(d, DATE_CHECK, font(SANS, 10.5), W - 2 * mx - 116),
               font(SANS, 10.5), leading=13)

    # footer legend
    d.text((mx, 1000),
           "REPORTED = carried by wires or officials \u00b7 CLAIM = one side\u2019s "
           "account \u00b7 ONGOING = still unfolding \u00b7 CONFIRMED = 2+ outlets",
           font=font(SANS, 9), fill=GREY)
    d.text((W - mx, 1000),
           "ALSO ON codes: C = 2+ outlets \u00b7 O = official \u00b7 R = one outlet "
           "\u00b7 CL = one side\u2019s claim",
           font=font(SANS, 9), fill=GREY, anchor="ra")

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out)
    print(f"wrote {out} {img.size}")


if __name__ == "__main__":
    main()
