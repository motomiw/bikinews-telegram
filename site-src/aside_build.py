# Боковая колонка для страниц новостей и статей: ближайший матч и фрагмент таблицы РПЛ.
# Выполняется из build.py после matches_build.py (нужны UPCOMING, CLUBN, MON_G, WD) и до news_pages_build.py / article_build.py.
import ast as _asd, datetime as _dtd, html as _hd, re as _red

_tbl_src = SRC[SRC.index('var table = ') + len('var table = '):]
_TABLE = _asd.literal_eval(_tbl_src[:_tbl_src.index('];') + 1])     # [клуб, И, В, Н, П, забито, пропущено, очки]
_SD_TOP = 8

ASIDE_CSS = r'''
.na-grid { display: grid; grid-template-columns: minmax(0, 72ch) minmax(280px, 340px); gap: 56px; align-items: start; }
.na-main { min-width: 0; }
.na-side { position: sticky; top: 88px; display: grid; gap: 20px; padding-top: 18px; }
.sd-box { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; }
.sd-box h2 { margin: 0 0 12px; font-family: var(--font-display); font-size: 16px; font-weight: 800; }
.sd-teams { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 8px; text-align: center; }
.sd-teams img { width: 44px; height: 44px; display: block; margin: 0 auto 6px; }
.sd-teams b { display: block; font-size: 14px; line-height: 1.2; }
.sd-time { font-family: var(--font-display); font-weight: 800; font-size: 24px; }
.sd-meta { margin: 12px 0 0; font-size: 14px; color: var(--muted); }
.sd-link { display: inline-block; margin-top: 12px; font-weight: 700; font-size: 14px; color: var(--accent); }
.sd-tbl { width: 100%; border-collapse: collapse; font-size: 14px; }
.sd-tbl th { font-family: var(--font-mono); font-size: 12px; font-weight: 700; color: var(--muted); text-align: right; padding: 0 0 6px; }
.sd-tbl th:nth-child(-n+2) { text-align: left; }
.sd-tbl td { padding: 7px 0; border-top: 1px solid var(--line); text-align: right; font-variant-numeric: tabular-nums; }
.sd-tbl td:first-child { width: 26px; text-align: left; color: var(--muted); }
.sd-tbl td:nth-child(2) { text-align: left; }
.sd-tbl td:nth-child(2) span { display: inline-flex; align-items: center; gap: 8px; }
.sd-tbl img { width: 20px; height: 20px; }
.sd-tbl tr.us td { font-weight: 800; background: var(--accent-soft); }
.sd-tbl tr.us td:first-child { padding-left: 6px; color: var(--ink); }
.sd-tbl tr.us td:last-child { padding-right: 6px; }
@media (max-width: 960px) { .na-grid { grid-template-columns: minmax(0, 72ch); gap: 8px; } .na-side { position: static; padding-top: 28px; } }
'''


def aside_html():
    today = _dtd.datetime.now(_dtd.timezone(_dtd.timedelta(hours=3))).date()
    nxt = next((m for m in UPCOMING if _dtd.date.fromisoformat(m[0]) >= today), None)
    out = ['<aside class="na-side" aria-label="Матч и таблица">']
    if nxt:
        d, t, comp, rnd, opp, home = nxt
        day = _dtd.date.fromisoformat(d)
        a, b = ('krasnodar', opp) if home else (opp, 'krasnodar')
        when = f'{WD[day.weekday()]}, {day.day} {MON_G[day.month - 1]}'
        out.append(
            f'<section class="sd-box" aria-labelledby="sd-m"><h2 id="sd-m">Ближайший матч</h2>'
            f'<div class="sd-teams"><div><img src="logos/{a}.svg" alt="" width="44" height="44" loading="lazy"><b>{_hd.escape(CLUBN[a])}</b></div>'
            f'<div class="sd-time">{_hd.escape(t.rstrip("*")) if t else "—"}</div>'
            f'<div><img src="logos/{b}.svg" alt="" width="44" height="44" loading="lazy"><b>{_hd.escape(CLUBN[b])}</b></div></div>'
            f'<p class="sd-meta">{_hd.escape(when)} · {"РПЛ" if comp == "РПЛ" else "Кубок России"}, {_hd.escape(rnd)}<br>'
            f'{"Дома, «Ozon Арена»" if home else "В гостях"} · время московское</p>'
            f'<a class="sd-link" href="matches.html">Все матчи →</a></section>')
    rows = ''.join(
        f'<tr{" class=us" if r[0] == "krasnodar" else ""}><td>{i}</td><td><span><img src="logos/{r[0]}.svg" alt="" width="20" height="20" loading="lazy">{_hd.escape(CLUBN[r[0]])}</span></td><td>{r[1]}</td><td>{r[7]}</td></tr>'
        for i, r in enumerate(_TABLE[:_SD_TOP], 1))
    out.append(
        '<section class="sd-box" aria-labelledby="sd-t"><h2 id="sd-t">Таблица РПЛ</h2>'
        f'<table class="sd-tbl"><thead><tr><th>#</th><th>Клуб</th><th>И</th><th>О</th></tr></thead><tbody>{rows}</tbody></table>'
        '<a class="sd-link" href="./#table">Вся таблица →</a></section>')
    out.append('</aside>')
    return ''.join(out)
