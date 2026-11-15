"""Генерация заглушек скриншотов для публичного репозитория BioFlow.

Запуск:  python make_placeholders.py
Результат: docs/screenshots/*.png (1080x1920) — тёмная тема приложения.
Позже эти файлы заменяются настоящими скриншотами с теми же именами.
"""

import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "screenshots")

BG_TOP = (26, 19, 16)
BG_BOTTOM = (14, 11, 10)
PEACH = (255, 179, 167)
CORAL = (255, 138, 128)
MUTED = (150, 143, 140)

FONT_DIR = r"C:\Windows\Fonts"
FONT_REG = os.path.join(FONT_DIR, "segoeui.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def gradient_bg():
    img = Image.new("RGB", (W, H), BG_BOTTOM)
    small = Image.new("RGB", (W // 4, H // 4))
    d = ImageDraw.Draw(small)
    for y in range(small.height):
        t = y / max(1, small.height - 1)
        c = tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (small.width, y)], fill=c)
    return small.resize((W, H), Image.LANCZOS)


def glow(img, cx, cy, radius, color, strength=0.5):
    layer = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = radius // 4
    steps = 42
    for i in range(steps, 0, -1):
        t = i / steps
        rr = int(r * t)
        alpha = int(255 * strength * (1 - t) ** 2 / steps * 7)
        d.ellipse([cx // 4 - rr, cy // 4 - rr, cx // 4 + rr, cy // 4 + rr],
                  fill=color + (min(255, alpha),))
    layer = layer.filter(ImageFilter.GaussianBlur(radius=18))
    layer = layer.resize((W, H), Image.LANCZOS)
    img.alpha_composite(layer)


def card(draw, box, radius=34, fill=(255, 255, 255, 12), outline=(255, 255, 255, 26)):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=2)


def bar(draw, box, color=(255, 255, 255, 26), radius=14):
    draw.rounded_rectangle(box, radius=radius, fill=color)


def circle(draw, cx, cy, r, fill, outline=None, width=3):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=width)


def layout_dashboard(d):
    card(d, [150, 240, 930, 720], radius=48)
    circle(d, 540, 400, 92, fill=(255, 179, 167, 30), outline=(255, 179, 167, 120), width=6)
    bar(d, [380, 520, 700, 556], (255, 255, 255, 60))
    for i, x in enumerate((140, 460, 780)):
        card(d, [x, 780, x + 280, 1060], radius=40)
        bar(d, [x + 40, 830, x + 240, 846], (255, 255, 255, 46))
        bar(d, [x + 40, 900, x + 170, 960], (255, 179, 167, 90), radius=18)
    card(d, [150, 1120, 930, 1420], radius=40)
    bar(d, [190, 1170, 620, 1206], (255, 255, 255, 40))
    bar(d, [190, 1250, 700, 1370], (255, 255, 255, 22), radius=20)


def layout_biometrics(d):
    card(d, [150, 220, 930, 520], radius=44)
    bar(d, [200, 290, 520, 326], (255, 255, 255, 52))
    bar(d, [200, 370, 780, 470], (255, 179, 167, 70), radius=22)
    card(d, [150, 580, 930, 980], radius=44)
    for i in range(10):
        x = 200 + i * 68
        circle(d, x, 700, 24, fill=(255, 179, 167, 40), outline=(255, 179, 167, 90))
    bar(d, [200, 820, 700, 856], (255, 255, 255, 40))
    card(d, [150, 1040, 930, 1300], radius=44)
    bar(d, [200, 1110, 520, 1146], (255, 255, 255, 52))
    bar(d, [200, 1190, 760, 1250], (255, 255, 255, 24), radius=20)


def layout_journal(d):
    card(d, [150, 220, 930, 700], radius=44)
    bar(d, [200, 290, 640, 326], (255, 255, 255, 52))
    for i in range(4):
        y = 380 + i * 76
        bar(d, [200, y, 860 - i * 90, y + 34], (255, 255, 255, 22), radius=16)
    card(d, [150, 760, 930, 1240], radius=44)
    bar(d, [200, 830, 560, 866], (255, 255, 255, 52))
    for i in range(3):
        y = 920 + i * 92
        circle(d, 228, y + 18, 22, fill=(255, 179, 167, 60))
        bar(d, [280, y + 4, 840 - i * 120, y + 38], (255, 255, 255, 22), radius=16)
    card(d, [150, 1300, 930, 1500], radius=40)
    bar(d, [420, 1380, 660, 1420], (255, 179, 167, 110), radius=20)


def layout_stats(d):
    card(d, [150, 240, 930, 560], radius=44)
    bar(d, [200, 300, 480, 336], (255, 255, 255, 52))
    card(d, [150, 620, 930, 1240], radius=44)
    pts = [(230, 1100), (390, 980), (550, 900), (710, 960), (860, 880)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(255, 120, 110, 220), width=8)
    for (x, y) in pts:
        circle(d, x, y, 16, fill=(255, 120, 110, 255))
    card(d, [150, 1300, 930, 1520], radius=40)
    bar(d, [200, 1360, 520, 1396], (255, 255, 255, 52))
    bar(d, [200, 1430, 780, 1462], (255, 255, 255, 24), radius=16)


def layout_settings(d):
    card(d, [150, 240, 930, 520], radius=44)
    bar(d, [200, 300, 520, 336], (255, 255, 255, 52))
    bar(d, [200, 380, 700, 430], (255, 255, 255, 22), radius=16)
    card(d, [150, 580, 930, 1040], radius=44)
    for i in range(3):
        y = 650 + i * 130
        bar(d, [200, y, 620, y + 40], (255, 255, 255, 44))
        circle(d, 840, y + 18, 26, fill=(255, 179, 167, 45), outline=(255, 179, 167, 120))
    card(d, [150, 1100, 930, 1360], radius=44)
    bar(d, [200, 1160, 560, 1196], (255, 255, 255, 52))
    bar(d, [200, 1240, 720, 1272], (255, 255, 255, 22), radius=16)


SCREENS = [
    ("01-dashboard", "Главный экран", "серия дней, вода, привычки, быстрые действия", layout_dashboard),
    ("02-biometrics", "Биометрия", "сон, самочувствие, вода, тренировка", layout_biometrics),
    ("03-journal", "Дневник «7 минут»", "утро, вечер, благодарности, рефлексия", layout_journal),
    ("04-stats", "Статистика", "аналитика, связи показателей, история", layout_stats),
    ("05-settings", "Настройки", "профиль, нормы, темы, данные", layout_settings),
]


def make(name, title, subtitle, layout):
    img = gradient_bg().convert("RGBA")
    glow(img, 540, 380, 900, PEACH, 0.30)
    glow(img, 180, 1500, 800, CORAL, 0.18)

    d = ImageDraw.Draw(img, "RGBA")
    layout(d)

    # подпись
    f_title = font(FONT_BOLD, 62)
    f_sub = font(FONT_REG, 34)
    f_hint = font(FONT_REG, 30)

    tw = d.textbbox((0, 0), title, font=f_title)[2]
    d.text(((W - tw) / 2, 1590), title, font=f_title, fill=(245, 240, 238, 255))

    sw = d.textbbox((0, 0), subtitle, font=f_sub)[2]
    d.text(((W - sw) / 2, 1672), subtitle, font=f_sub, fill=MUTED + (230,))

    hint = "место для скриншота"
    hw = d.textbbox((0, 0), hint, font=f_hint)[2]
    d.text(((W - hw) / 2, 1740), hint, font=f_hint, fill=(140, 130, 126, 220))

    # рамка-подсказка «сюда положить файл»
    d.rounded_rectangle([60, 120, W - 60, H - 120], radius=48,
                        outline=(255, 255, 255, 22), width=3)

    path = os.path.join(OUT, name + ".png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    print("saved", path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for args in SCREENS:
        make(*args)
    print("готово")
