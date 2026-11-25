#!/usr/bin/env python3
"""
build_image.py — draws entry.png for the make.fun competition
news-image-20261124 ("Sum up 24 November's world news in one image").

The picture is a classic, elegant broadsheet front page in the old
style: ivory paper, black ink, hairline rules, a display-serif
masthead and not a single photograph — the day told in type alone.
Drawn entirely with Pillow primitives plus Pillow-rendered text, so
the result is fully reproducible: run this script and it rewrites
entry.png next to itself.

Every story below was reported on Tuesday 24 November 2026 and was
checked against at least two independent reports before it was drawn:

  * Hormuz — Iran rules out talks until its seven conditions are met;
    the Revolutionary Guard says three tankers struck naval mines and
    burned in the strait (TBS News / AP / Reuters, 24 Nov).
  * Zaporizhzhia — Russian glide-bomb attack kills 2 civilians and
    wounds 48, four of them children (AP / 112.ua, 24 Nov); Kyiv's
    naval drones struck a Russian warship at Benghazi, Libya (AP).
  * The Hague — fourteen countries affirm the ICJ ruling that Myanmar
    committed genocide against the Rohingya; Britain adds sanctions
    (Horizon / News Media House, 24 Nov).
  * Markets — Nvidia's board reinstates Jensen Huang as CEO; the
    shares leap 31%, the S&P 500 rises 4.73% to 7,237.17 and the
    Nasdaq 6.51% to 24,089.56 (AP / Xinhua / Le Monde, 24 Nov).
  * Briefs — Oxfam on Gaza; Shenzhou-24 crew unveiled with Pakistan's
    Muhammad Zeeshan Ali, first foreign astronaut to Tiangong
    (Reuters / Xinhua); Nepal magnitude 5.6 quake in Taplejung
    (Nepal NEMRC via Xinhua / EMSC); Guterres urges an AI-risk
    framework (UN News); North Korea orders the Swiss office in
    Pyongyang closed (AP); Hanoi hot-pot blast kills six (AP).
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
PAPER = (246, 240, 226)      # ivory newsprint
INK = (22, 20, 17)           # warm black ink
GRAY = (96, 90, 80)          # faded ink for furniture
ACCENT = (122, 28, 32)       # deep oxblood, used sparingly

W = H = 1024
MARGIN = 40
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

# ------------------------------------------------------------------ fonts ---
NOTO = "/usr/share/fonts/truetype/noto/"
DISPLAY_BLACK = NOTO + "NotoSerifDisplay-Black.ttf"
DISPLAY_BOLD = NOTO + "NotoSerifDisplay-Bold.ttf"
SERIF = NOTO + "NotoSerif-Regular.ttf"
SERIF_BOLD = NOTO + "NotoSerif-Bold.ttf"
SERIF_ITALIC = NOTO + "NotoSerif-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text_w(s, fnt):
    return d.textlength(s, font=fnt)


def centered(s, fnt, y, fill=INK, tracking=0):
    if tracking:
        total = sum(text_w(ch, fnt) for ch in s) + tracking * (len(s) - 1)
        x = (W - total) / 2
        for ch in s:
            d.text((x, y), ch, font=fnt, fill=fill)
            x += text_w(ch, fnt) + tracking
        return total
    w = text_w(s, fnt)
    d.text(((W - w) / 2, y), s, font=fnt, fill=fill)
    return w


def wrap(s, fnt, width):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if text_w(trial, fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def block(s, fnt, x, y, width, leading, fill=INK, align="left"):
    for line in wrap(s, fnt, width):
        if align == "center":
            d.text((x + (width - text_w(line, fnt)) / 2, y), line, font=fnt, fill=fill)
        else:
            d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(y, thick=2, thin=1, gap=3, x0=MARGIN, x1=RIGHT):
    d.line([(x0, y), (x1, y)], fill=INK, width=thick)
    d.line([(x0, y + thick + gap), (x1, y + thick + gap)], fill=INK, width=thin)
    return y + thick + gap + thin


def ornament(y):
    cx = W // 2
    d.line([(MARGIN, y + 4), (cx - 26, y + 4)], fill=GRAY, width=1)
    d.line([(cx + 26, y + 4), (RIGHT, y + 4)], fill=GRAY, width=1)
    d.polygon([(cx, y - 2), (cx + 7, y + 4), (cx, y + 10), (cx - 7, y + 4)], fill=INK)
    return y + 13


def kicker(s, y, x=MARGIN, width=CONTENT_W):
    f = F(SERIF_BOLD, 14)
    block(s, f, x, y, width, 18, fill=ACCENT,
          align="center" if width == CONTENT_W else "left")
    return y + 22


# ================================================================ masthead ===
y = 22
f_small = F(SERIF, 13)
d.text((MARGIN, y), "VOL. I — No. 24", font=f_small, fill=GRAY)
r = "ONE PAGE · THE WHOLE DAY"
d.text((RIGHT - text_w(r, f_small), y), r, font=f_small, fill=GRAY)
y += 22

centered("The World in One Day", F(DISPLAY_BLACK, 68), y)
y += 88
y = rule(y, thick=3, thin=1, gap=4)
y += 7
f_date = F(SERIF_BOLD, 16)
d.text((MARGIN, y), "LATE EDITION", font=f_date, fill=INK)
centered("TUESDAY, 24 NOVEMBER 2026", f_date, y, tracking=2)
r = "EST. MMXXVI"
d.text((RIGHT - text_w(r, f_date), y), r, font=f_date, fill=INK)
y += 24
y = rule(y, thick=1, thin=3, gap=4)

# ================================================================== lead ====
y += 13
y = kicker("THE GULF · THE STRAIT OF HORMUZ", y)
f_head = F(DISPLAY_BLACK, 52)
centered("HORMUZ ON A KNIFE-EDGE", f_head, y)
y += 62
f_deck = F(SERIF_ITALIC, 19)
y = block("Iran says three oil tankers struck mines and burned in the "
          "strait; Tehran will not talk until its seven conditions are met",
          f_deck, MARGIN + 100, y, CONTENT_W - 200, 25, align="center")
y += 7

f_body = F(SERIF, 14)
lead = ("TEHRAN — Iran's chief negotiator, Mohammad Bagher Qalibaf, said "
        "Tehran would not negotiate with Washington “until Iran's seven "
        "conditions are met” — among them, state media say, an end to the "
        "American naval blockade of Iranian ports, the easing of sanctions "
        "and the release of frozen assets. The Revolutionary Guard said "
        "three tankers under American escort struck naval mines and were "
        "“engulfed in flames”; the claim was not independently confirmed. "
        "Washington rejected the terms and kept its carriers near the "
        "strait, where the threat level stands at “severe”.")
col_w = (CONTENT_W - 2 * 22) // 3
lines = wrap(lead, f_body, col_w)
per = (len(lines) + 2) // 3
for i in range(3):
    yy = y
    for line in lines[i * per:(i + 1) * per]:
        d.text((MARGIN + i * (col_w + 22), yy), line, font=f_body, fill=INK)
        yy += 20
y += per * 20 + 4
y = ornament(y)

# ============================================================ second row ====
y += 6
half = (CONTENT_W - 32) // 2
x2 = MARGIN + half + 32

yy = kicker("UKRAINE", y, x=MARGIN, width=half)
y_left = block("Glide Bombs Kill Two, Wound 48 in Zaporizhzhia",
               F(DISPLAY_BOLD, 26), MARGIN, yy, half, 31)
y_left = block("KYIV — A Russian nighttime glide-bomb attack destroyed a "
               "house and tore into a five-storey apartment block, killing "
               "two civilians and wounding 48, four of them children. Kyiv "
               "meanwhile explained its unprecedented strike in Libya, "
               "where Ukrainian naval drones hit a Russian warship docked "
               "at Benghazi.",
               f_body, MARGIN, y_left + 3, half, 20)

yy = kicker("THE HAGUE · MYANMAR", y, x=x2, width=half)
y_right = block("Fourteen Nations Affirm the Rohingya Genocide Ruling",
                F(DISPLAY_BOLD, 26), x2, yy, half, 31)
y_right = block("THE HAGUE — Fourteen countries, among them Britain, "
                "Spain, Canada and Australia, affirmed the International "
                "Court of Justice's ruling that Myanmar committed genocide "
                "against the Rohingya. London added fresh sanctions on "
                "senior figures of Myanmar's military.",
                f_body, x2, y_right + 3, half, 20)
d.line([(MARGIN + half + 16, y), (MARGIN + half + 16, max(y_left, y_right))],
       fill=GRAY, width=1)
y = max(y_left, y_right) + 6
y = ornament(y)

# ================================================================ markets ====
y += 6
y = kicker("MARKETS · NEW YORK", y)
centered("Huang Returns, and Wall Street Roars Back", F(DISPLAY_BOLD, 29), y)
y += 38
y = block("Nvidia's board reinstated Jensen Huang as chief executive, "
          "eleven days after his resignation, and the chipmaker leapt 31 "
          "per cent — the largest one-day gain in market value on record, "
          "recovering half of last week's plunge.",
          f_body, MARGIN + 70, y, CONTENT_W - 140, 20, align="center")
f_fig = F(SERIF_BOLD, 16)
centered("NVIDIA +31%    ·    S&P 500 +4.73% — 7,237.17    ·    "
         "NASDAQ +6.51% — 24,089.56    ·    DOW +3.01%",
         f_fig, y + 1, fill=ACCENT)
y += 28
y = ornament(y)

# ================================================================= briefs ====
y += 6
centered("IN BRIEF", F(SERIF_BOLD, 15), y, tracking=4)
y += 22
briefs = [
    ("GAZA — ", "Oxfam describes a territory transformed into a “toxic "
     "land” by the war; Israeli strikes killed at least eight people "
     "on Tuesday."),
    ("SPACE — ", "China named the Shenzhou-24 crew: Pakistan's "
     "Muhammad Zeeshan Ali, first foreigner to visit the "
     "Tiangong station."),
    ("NEPAL — ", "A magnitude 5.6 earthquake struck Taplejung, near "
     "the Tibet border, at 7.17 in the morning; no casualties were "
     "reported."),
    ("UNITED NATIONS — ", "Secretary-General Guterres urged a global "
     "framework to govern the risks of artificial intelligence "
     "within a year."),
    ("KOREA — ", "North Korea demanded that Switzerland close its new "
     "diplomatic office in Pyongyang and send its envoy home."),
    ("VIETNAM — ", "An explosion at a hot-pot restaurant in Hanoi "
     "killed six people and injured more than a dozen others."),
]
col_w = (CONTENT_W - 2 * 22) // 3
f_brief = F(SERIF, 13)
for i, group in enumerate([briefs[0:2], briefs[2:4], briefs[4:6]]):
    yy = y
    x = MARGIN + i * (col_w + 22)
    for head, rest in group:
        for line in wrap(head + rest, f_brief, col_w):
            d.text((x, yy), line, font=f_brief, fill=INK)
            yy += 17
        yy += 8

# ================================================================ footer ====
y = H - 52
y = rule(y, thick=3, thin=1, gap=4)
y += 8
centered("All stories reported on Tuesday, 24 November 2026 · "
         "Set in a single page · The World in One Day",
         F(SERIF_ITALIC, 13), y, fill=GRAY)

img.save("/home/hatch/workspace/makefun/news-image-20261124-repo/entry.png")
print("saved entry.png", img.size)
