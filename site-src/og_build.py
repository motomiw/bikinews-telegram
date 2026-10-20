# Картинки-превью (1200×630) для ссылок в Telegram, MAX, соцсетях и поисковиках: у каждой новости и статьи своя.
# Выполняется из build.py до news_pages_build.py и article_build.py; даёт make_og(page, title, tag, date_txt) → имя файла для og:image.
# Если Pillow нет, сборка не ломается: везде остаётся общая картинка og-image.jpg.
try:
    from PIL import Image, ImageDraw, ImageFont
    _PIL = True
except Exception:   # noqa: BLE001
    _PIL = False

_OG_DIR = OUT / 'og'
_BG, _YEL, _INK, _MUTED = (15, 59, 36), (228, 173, 29), (240, 247, 242), (154, 187, 166)
_FONTS = ROOT / 'static' / 'fonts'
_og_n = 0


def _wrap(draw, text, font, width):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def make_og(page, title, tag, date_txt):
    global _og_n
    default = 'og-image.jpg'
    if not _PIL:
        return default
    try:
        _OG_DIR.mkdir(parents=True, exist_ok=True)
        name = 'og/' + page.rsplit('.', 1)[0] + '.jpg'
        W, H = 1200, 630
        im = Image.new('RGB', (W, H), _BG)
        d = ImageDraw.Draw(im)
        d.rectangle((0, H - 14, W, H), fill=_YEL)
        logo = Image.open(ROOT / 'assets' / 'og-logo.png').convert('RGB')
        lw = 330
        logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
        im.paste(logo, (W - lw - 36, 120))
        # метка раздела
        f_tag = ImageFont.truetype(str(_FONTS / 'Unbounded.woff'), 26)
        tg = tag.upper()
        tw = d.textlength(tg, font=f_tag)
        d.rounded_rectangle((64, 60, 64 + tw + 36, 60 + 52), radius=8, fill=_YEL)
        d.text((64 + 18, 60 + 26), tg, font=f_tag, fill=_BG, anchor='lm')
        d.text((64 + tw + 36 + 22, 60 + 26), date_txt, font=ImageFont.truetype(str(_FONTS / 'GolosText.woff'), 28), fill=_MUTED, anchor='lm')
        # заголовок: подбираем размер, чтобы влез в 5 строк
        box_w, top, bottom = 740, 150, 540
        for size in (56, 52, 48, 44, 40, 36):
            f = ImageFont.truetype(str(_FONTS / 'Unbounded.woff'), size)
            lines = _wrap(d, title, f, box_w)
            lh = round(size * 1.28)
            if len(lines) * lh <= bottom - top:
                break
        else:
            maxl = (bottom - top) // lh
            lines = lines[:maxl]
            lines[-1] = lines[-1].rstrip(' ,.:;—-') + '…'
        y = top
        for ln in lines:
            d.text((64, y), ln, font=f, fill=_INK)
            y += lh
        # подпись
        f_s = ImageFont.truetype(str(_FONTS / 'GolosText.woff'), 30)
        f_b = ImageFont.truetype(str(_FONTS / 'Unbounded.woff'), 28)
        d.text((64, H - 52), 'Быки News', font=f_b, fill=_YEL, anchor='lm')
        d.text((64 + d.textlength('Быки News', font=f_b) + 26, H - 52), 'bikinews.ru · новости ФК «Краснодар»', font=f_s, fill=_MUTED, anchor='lm')
        im.save(OUT / name, 'JPEG', quality=80, optimize=True, subsampling=2)
        _og_n += 1
        return name
    except Exception as ex:   # noqa: BLE001
        print('og: не удалось', page, ex)
        return default
