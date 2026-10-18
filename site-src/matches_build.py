# Страница «Матчи» (выполняется из build.py: доступны head, nav_header, footer, SRC, style_end, OUT)
import datetime as _dt, html as _h

CLUBN = {'krasnodar': 'Краснодар', 'rubin': 'Рубин', 'fakel': 'Факел', 'akhmat': 'Ахмат', 'spartak': 'Спартак',
         'dynamo': 'Динамо', 'dynamo-mkh': 'Динамо Мх', 'rostov': 'Ростов', 'krylia': 'Крылья Советов', 'akron': 'Акрон',
         'orenburg': 'Оренбург', 'zenit': 'Зенит', 'lokomotiv': 'Локомотив', 'baltika': 'Балтика', 'rodina': 'Родина', 'cska': 'ЦСКА'}
HOME_STADIUM = 'Ozon Арена, Краснодар'

# ---- Сыгранные матчи сезона 2026/27 (время московское) ----
# goals: (минута или None, автор, 'k' — Краснодар / 'o' — соперник, ассистент или '')
# stats: показатель -> (Краснодар, соперник)
PLAYED = [
 dict(d='2026-07-26', t='19:30', comp='РПЛ', rnd='1 тур', opp='rubin', home=False, gf=3, ga=1, stad='«Ак Барс Арена», Казань', ref='Артём Чистяков', att=18866,
      goals=[('12', 'Мирлинд Даку', 'o', 'Ставер'), ('45+6', 'Хуан Мануэль Боселли', 'k', ''), ('53', 'Никита Кривцов', 'k', 'Боселли'), ('90+4', 'Кристиан', 'k', '')],
      reds=[('18', 'Илья Рожков', 'o')], stats={'Владение, %': (72, 28), 'xG': (2.76, 0.61), 'Удары': (19, 5)}),
 dict(d='2026-08-02', t='18:15', comp='РПЛ', rnd='2 тур', opp='fakel', home=True, gf=3, ga=2, ref='Станислав Матвеев', att=30953,
      goals=[('5', 'Жубал', 'k', 'Оласа'), ('28', 'Никита Кривцов', 'k', 'Кристиан'), ('59', 'Никита Кривцов', 'k', 'Батчи'), ('85', 'Максим Туришев', 'o', 'Гиоргобиани'), ('88', 'Алексей Сутормин', 'o', 'Пуси')],
      note='На 51-й минуте Аксель Гнапи («Факел») не реализовал пенальти.', stats={'Владение, %': (56, 44), 'xG': (1.36, 2.30), 'Удары': (11, 13)}),
 dict(d='2026-08-05', t='20:45', comp='Кубок', rnd='группа B, 1 тур', opp='akhmat', home=True, gf=1, ga=1, pens='5:4', att=20017,
      goals=[('66', 'Даниил Уткин (пенальти)', 'k', ''), ('90+5', 'Максим Самородов', 'o', '')], stats={}),
 dict(d='2026-08-09', t='20:00', comp='РПЛ', rnd='3 тур', opp='spartak', home=False, gf=2, ga=1, stad='«Лукойл Арена», Москва', ref='Кирилл Левников', att=38846,
      goals=[('3', 'Манфред Угальде', 'o', 'Маркиньос'), ('6', 'Лукас Оласа', 'k', 'Дуглас Аугусто'), ('11', 'Жоау Батчи', 'k', 'Кривцов')],
      stats={'Владение, %': (37, 63), 'xG': (0.99, 1.06), 'Удары': (16, 16)}),
 dict(d='2026-08-15', t='20:45', comp='РПЛ', rnd='4 тур', opp='akhmat', home=True, gf=1, ga=0, ref='Сергей Карасёв', att=29365,
      goals=[('5', 'Кристиан', 'k', 'Воробьёв')], stats={'Владение, %': (58, 42), 'xG': (1.00, 1.03), 'Удары': (17, 9)}),
 dict(d='2026-08-19', t='20:45', comp='Кубок', rnd='группа B, 2 тур', opp='dynamo', home=False, gf=1, ga=0, stad='«ВТБ Арена», Москва', ref='Никита Новиков', att=23332,
      goals=[('44', 'Казбек Мукаилов', 'k', '')], stats={}),
 dict(d='2026-08-23', t='17:30', comp='РПЛ', rnd='5 тур', opp='dynamo-mkh', home=False, gf=1, ga=0, stad='«Анжи Арена», Каспийск', ref='Василий Казарцев', att=9792,
      goals=[('80', 'Жубал', 'k', 'Кевин Пина')], stats={'Владение, %': (58, 42), 'xG': (0.54, 0.88), 'Удары': (10, 10)}),
 dict(d='2026-08-29', t='17:30', comp='РПЛ', rnd='6 тур', opp='rostov', home=True, gf=1, ga=0, ref='Никита Новиков', att=33083,
      goals=[('19', 'Жубал', 'k', 'Кристиан')], stats={'Владение, %': (55, 45), 'xG': (0.81, 0.88), 'Удары': (13, 13)}),
 dict(d='2026-09-01', t='18:00', comp='Кубок', rnd='группа B, 3 тур', opp='fakel', home=False, gf=1, ga=1, pens='4:3', stad='стадион «Факел», Воронеж', ref='Игорь Капленков',
      goals=[('59', 'Антон Ковалёв', 'o', ''), ('60', 'Магомед Оздоев', 'k', '')],
      stats={'Удары': (9, 13), 'Удары в створ': (6, 6), 'Угловые': (6, 3), 'Фолы': (7, 11), 'Жёлтые карточки': (1, 1)}),
 dict(d='2026-09-05', t='14:00', comp='РПЛ', rnd='7 тур', opp='krylia', home=False, gf=2, ga=2, ht='2:0', stad='«Солидарность Самара Арена», Самара', ref='Инал Танашев', att=12175,
      goals=[('3', 'Джон Кордоба', 'k', 'Воробьёв'), ('17', 'Жоау Батчи', 'k', 'Оласа'), ('55', 'Амар Рахманович', 'o', 'Олейников'), ('79', 'Амар Рахманович', 'o', 'Олейников')],
      stats={'Владение, %': (56, 44), 'xG': (1.93, 1.27), 'Удары': (14, 11), 'Удары в створ': (7, 5), 'Угловые': (2, 0), 'Фолы': (18, 21), 'Офсайды': (7, 2), 'Жёлтые карточки': (1, 2)}),
 dict(d='2026-09-13', t='19:30', comp='РПЛ', rnd='8 тур', opp='akron', home=True, gf=1, ga=1, ref='Василий Казарцев', att=30463,
      goals=[('13', 'Константин Марадишвили', 'o', 'Бардыбахин'), ('88', 'Хуан Мануэль Боселли', 'k', '')],
      stats={'Владение, %': (69, 31), 'xG': (1.40, 0.33), 'Удары': (21, 8)}),
 dict(d='2026-09-17', t='16:15', comp='РПЛ', rnd='9 тур', opp='orenburg', home=False, gf=0, ga=0, stad='«Газовик», Оренбург', ref='Кирилл Левников', att=4635,
      goals=[], stats={'Владение, %': (60, 40), 'xG': (1.38, 0.89), 'Удары': (16, 17)}),
 dict(d='2026-10-10', t='19:30', comp='РПЛ', rnd='10 тур', opp='zenit', home=True, gf=2, ga=3, ht='0:2', ref='Инал Танашев', att=35055,
      goals=[('40', 'Максим Глушенков', 'o', ''), ('45+4', 'Максим Глушенков', 'o', ''), ('53', 'Александр Соболев', 'o', 'Педро'), ('55', 'Жоау Батчи', 'k', ''), ('71', 'Джон Кордоба', 'k', 'Вахания')],
      reds=[('80', 'Витор Тормена', 'k')],
      stats={'Владение, %': (55, 45), 'xG': (2.29, 1.08), 'Удары': (14, 15), 'Удары в створ': (6, 7), 'Угловые': (3, 3), 'Фолы': (21, 11), 'Офсайды': (4, 0), 'Жёлтые карточки': (4, 3)}),
 dict(d='2026-10-13', t='20:45', comp='Кубок', rnd='группа B, 4 тур', opp='fakel', home=True, gf=0, ga=2, ht='0:0', ref='Матвей Заика',
      goals=[('69', 'Абдула Багамаев', 'o', ''), ('81', 'Максим Турищев', 'o', '')],
      note='В первом тайме Валентин Пальцев не реализовал пенальти — удар отразил Игорь Обухов.',
      stats={'Владение, %': (68, 32), 'Удары': (19, 11), 'Удары в створ': (6, 7), 'Угловые': (5, 3), 'Фолы': (12, 15), 'Жёлтые карточки': (0, 4)}),
 dict(d='2026-10-17', t='19:30', comp='РПЛ', rnd='11 тур', opp='lokomotiv', home=False, gf=3, ga=3, stad='«РЖД Арена», Москва', ref='Никита Новиков',
      goals=[('5', 'Жоау Батчи', 'k', ''), ('16', 'Николай Титков', 'o', ''), ('71', 'Александр Руденко', 'o', 'Ненахов'), ('78', 'Александр Коваленко', 'o', ''),
             ('86', 'Лукас Оласа', 'k', ''), ('90+1', 'Джон Кордоба', 'k', 'Батчи')],
      note='«Краснодар» отыгрался со счёта 1:3. На 36-й минуте Ньямси, уже имевший жёлтую карточку, сбил Кордобу подкатом, но второго предупреждения не получил.',
      stats={}),
]

# ---- Предстоящие: время 'X' — подтверждено, 'X*' — предварительное, '' — не назначено ----
UPCOMING = [
 ('2026-10-24', '19:30*', 'РПЛ', '12 тур', 'baltika', True),
 ('2026-10-27', '20:30*', 'Кубок', 'группа B, 5 тур', 'dynamo', True),
 ('2026-10-31', '19:45*', 'РПЛ', '13 тур', 'rodina', False),
 ('2026-11-07', '19:30*', 'РПЛ', '14 тур', 'cska', True),
 ('2026-11-22', '14:00*', 'РПЛ', '15 тур', 'dynamo', False),
 ('2026-11-25', '18:00*', 'Кубок', 'группа B, 6 тур', 'akhmat', False),
 ('2026-11-29', '15:15*', 'РПЛ', '16 тур', 'rostov', False),
 ('2026-12-06', '19:30*', 'РПЛ', '17 тур', 'rubin', True),
 ('2027-02-27', '', 'РПЛ', '18 тур', 'spartak', True),
 ('2027-03-06', '', 'РПЛ', '19 тур', 'krylia', True),
 ('2027-03-13', '', 'РПЛ', '20 тур', 'baltika', False),
 ('2027-03-20', '', 'РПЛ', '21 тур', 'dynamo', True),
 ('2027-04-03', '', 'РПЛ', '22 тур', 'cska', False),
 ('2027-04-10', '', 'РПЛ', '23 тур', 'rodina', True),
 ('2027-04-17', '', 'РПЛ', '24 тур', 'akron', False),
 ('2027-04-24', '', 'РПЛ', '25 тур', 'dynamo-mkh', True),
 ('2027-05-01', '', 'РПЛ', '26 тур', 'zenit', False),
 ('2027-05-08', '', 'РПЛ', '27 тур', 'orenburg', True),
 ('2027-05-15', '', 'РПЛ', '28 тур', 'akhmat', False),
 ('2027-05-22', '', 'РПЛ', '29 тур', 'fakel', False),
 ('2027-05-29', '', 'РПЛ', '30 тур', 'lokomotiv', True),
]

MON_G = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
MON_S = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
WD = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
e = _h.escape


def dparts(d):
    x = _dt.date.fromisoformat(d)
    return x.day, MON_S[x.month - 1], WD[x.weekday()], x


def logo(slug):
    return f'<img class="lg" src="logos/{slug}.svg" alt="" width="24" height="24" loading="lazy">'


def teams(opp, home):
    a, b = ('krasnodar', opp) if home else (opp, 'krasnodar')
    return a, b


def fmt_num(v):
    return (('%.2f' % v).replace('.', ',')) if isinstance(v, float) else str(v)


def stat_rows(st):
    out = []
    for label, (k, o) in st.items():
        tot = (k + o) or 1
        kp = round(100 * k / tot)
        out.append(f'<div class="sr"><span class="sv mono">{fmt_num(k)}</span><div class="sb"><span class="sl">{e(label)}</span>'
                   f'<div class="bar" role="img" aria-label="{e(label)}: Краснодар {fmt_num(k)}, соперник {fmt_num(o)}"><i class="bk" style="width:{kp}%"></i><i class="bo" style="width:{100 - kp}%"></i></div></div>'
                   f'<span class="sv mono o">{fmt_num(o)}</span></div>')
    return ''.join(out)


played_html = []
W = D = L = GF = GA = 0
for m in reversed(PLAYED):
    day, mon, wd, _ = dparts(m['d'])
    a, b = teams(m['opp'], m['home'])
    sa, sb = (m['gf'], m['ga']) if m['home'] else (m['ga'], m['gf'])
    res = 'w' if m['gf'] > m['ga'] else ('l' if m['gf'] < m['ga'] else 'd')
    if m.get('pens'):
        res_note = 'победа по пенальти ' + m['pens']
    else:
        res_note = {'w': 'Победа', 'd': 'Ничья', 'l': 'Поражение'}[res]
    W += res == 'w'; D += res == 'd'; L += res == 'l'; GF += m['gf']; GA += m['ga']
    opp_n = CLUBN[m['opp']]
    meta = [m.get('stad') or HOME_STADIUM]
    if m.get('ref'): meta.append('судья — ' + m['ref'])
    if m.get('att'): meta.append('зрителей — ' + f"{m['att']:,}".replace(',', ' '))
    if m.get('ht'): meta.append('первый тайм — ' + m['ht'])
    ev = []
    for mn, who, side, ast in m['goals']:
        ev.append(f'<li class="{side}"><span class="mn mono">{(mn + "′") if mn else "—"}</span><span class="ic" aria-hidden="true">⚽</span>'
                  f'<span><b>{e(who)}</b>{(" <small>пас: " + e(ast) + "</small>") if ast else ""}<small class="tm">{"Краснодар" if side == "k" else e(opp_n)}</small></span></li>')
    for mn, who, side in m.get('reds', []):
        ev.append(f'<li class="{side} red"><span class="mn mono">{mn}′</span><span class="ic rc" aria-hidden="true"></span>'
                  f'<span><b>{e(who)}</b> <small>красная карточка</small><small class="tm">{"Краснодар" if side == "k" else e(opp_n)}</small></span></li>')
    ev_html = ('<ol class="ev">' + ''.join(ev) + '</ol>') if ev else '<p class="none">Голов не было.</p>'
    if m.get('pens'):
        ev_html += f'<p class="pen">Серия пенальти: «Краснодар» выиграл {m["pens"]}.</p>'
    if m.get('note'):
        ev_html += f'<p class="pen">{e(m["note"])}</p>'
    st_html = (('<div class="stats"><div class="sh"><span>Краснодар</span><span>' + e(opp_n) + '</span></div>' + stat_rows(m['stats']) + '</div>')
               if m['stats'] else '<p class="none">Подробная статистика по этому матчу не публиковалась.</p>')
    played_html.append(f'''<details class="mt rs-{res}" id="m-{m['d']}" data-comp="{m['comp']}">
  <summary><span class="dt"><b>{day} {mon}</b>{wd} · {m['t']}</span>
    <span class="tm2"><span class="pair">{logo(a)}{logo(b)}</span><span class="nm"><b>{CLUBN[a]} — {CLUBN[b]}</b><small><span class="cp {'cup' if m['comp'] == 'Кубок' else ''}">{m['comp']}</span> {m['rnd']} · {'дома' if m['home'] else 'в гостях'}</small></span></span>
    <span class="scr mono">{sa}:{sb}<span class="res {res}" title="{res_note}">{'ВНП'['wdl'.index(res)]}</span></span>
    <span class="chev" aria-hidden="true"></span></summary>
  <div class="mb">
    <p class="meta">{' · '.join(e(x) for x in meta)}</p>
    <div class="cols"><div><h3>События</h3>{ev_html}</div><div><h3>Статистика</h3>{st_html}</div></div>
  </div>
</details>''')

played_by_opp = {}
for m in PLAYED:
    played_by_opp.setdefault(m['opp'], []).append(m)

up_html = []
today = _dt.date(2026, 10, 11)
for i, (d, t, comp, rnd, opp, home) in enumerate(UPCOMING):
    day, mon, wd, x = dparts(d)
    a, b = teams(opp, home)
    if t.endswith('*'):
        tcell = f'<span class="mono">{t[:-1]}</span><small>предварительно</small>'
    elif t:
        tcell = f'<span class="mono">{t}</span><small>подтверждено</small>'
    else:
        tcell = '<small class="tbd">время уточняется</small>'
    prev = played_by_opp.get(opp, [])
    prev_html = ''
    if prev:
        prev_html = '<p class="meta">В этом сезоне уже играли: ' + '; '.join(
            f'<a href="#m-{p["d"]}">{dparts(p["d"])[0]} {dparts(p["d"])[1]}, {p["comp"]} — {(p["gf"] if p["home"] else p["ga"])}:{(p["ga"] if p["home"] else p["gf"])}'
            + (f' (пен. {p["pens"]})' if p.get('pens') else '') + '</a>' for p in prev) + '</p>'
    spring = x.year == 2027
    up_html.append(f'''<details class="mt up{' nx' if i == 0 else ''}" id="m-{d}" data-comp="{comp}">
  <summary><span class="dt"><b>{day} {mon}</b>{wd}{' · ' + ('ближайший' if i == 0 else '') if i == 0 else ''}</span>
    <span class="tm2"><span class="pair">{logo(a)}{logo(b)}</span><span class="nm"><b>{CLUBN[a]} — {CLUBN[b]}</b><small><span class="cp {'cup' if comp == 'Кубок' else ''}">{comp}</span> {rnd} · {'дома' if home else 'в гостях'}</small></span></span>
    <span class="tc">{tcell}</span><span class="chev" aria-hidden="true"></span></summary>
  <div class="mb">
    <p class="meta">{'Стадион: ' + HOME_STADIUM if home else 'Выездной матч'} · {'дата по календарю РПЛ, может сдвинуться' if spring else 'время московское'}</p>
    {prev_html or '<p class="meta">В этом сезоне с этим соперником ещё не играли.</p>'}
  </div>
</details>''')

MATCH_CSS = r'''
main.mp { display: block; padding-block: 8px 56px; }
.mp-head { padding-block: 28px 4px; display: grid; gap: 10px; }
.mp-head h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(28px, 5vw, 44px); letter-spacing: -.01em; line-height: 1.1; }
.mp-head p { margin: 0; color: var(--muted); max-width: 70ch; }
.sum { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }
.sum div { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 10px 14px; min-width: 92px; }
.sum b { font-family: var(--font-display); font-size: 24px; display: block; line-height: 1.1; }
.sum small { color: var(--muted); font-size: 12px; }
.mp-tools { display: flex; gap: 8px; flex-wrap: wrap; padding-block: 18px 4px; }
.mp h2.sec { font-family: var(--font-display); font-weight: 700; font-size: clamp(20px, 3vw, 26px); margin: 26px 0 8px; }
.mt { border-bottom: 1px solid var(--line); }
.mt:first-of-type { border-top: 1px solid var(--line); }
.mt summary { list-style: none; cursor: pointer; display: grid; grid-template-columns: 82px minmax(0, 1fr) auto 18px; gap: 12px; align-items: center; padding: 12px 6px; border-radius: 8px; }
.mt summary::-webkit-details-marker { display: none; }
.mt summary:hover { background: var(--soft); }
.mt summary:focus-visible { outline: 3px solid var(--signal); outline-offset: 2px; }
.mt .dt { font-size: 12px; color: var(--muted); line-height: 1.3; }
.mt .dt b { display: block; color: var(--ink); font-size: 15px; }
.tm2 { display: flex; align-items: center; gap: 10px; min-width: 0; }
.pair { display: inline-flex; gap: 4px; flex: none; }
.lg { width: 24px; height: 24px; object-fit: contain; display: block; }
.nm { min-width: 0; }
.nm b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nm small { color: var(--muted); font-size: 12px; }
.cp { font-family: var(--font-mono); font-size: 10px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; color: var(--accent); }
.cp.cup { color: var(--ink); background: var(--signal); padding: 0 5px; border-radius: 4px; color: var(--on-signal); }
.scr { display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 700; }
.tc { text-align: right; display: grid; justify-items: end; line-height: 1.2; }
.tc .mono { font-size: 16px; font-weight: 700; }
.tc small { color: var(--muted); font-size: 11px; }
.tc .tbd { font-size: 12px; }
.chev { width: 10px; height: 10px; border-right: 2px solid var(--muted); border-bottom: 2px solid var(--muted); transform: rotate(45deg); margin-top: -4px; transition: transform .15s; }
.mt[open] .chev { transform: rotate(225deg); margin-top: 4px; }
.mt.nx summary { background: var(--accent-soft); }
:root { --loss-bg: #FBE3DC; --draw-bg: #FBF0C9; --draw-line: #C99A06; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --loss-bg: #3A1D14; --draw-bg: #33290C; --draw-line: #EDBE3E; } }
:root[data-theme="dark"] { --loss-bg: #3A1D14; --draw-bg: #33290C; --draw-line: #EDBE3E; }
.mt.rs-l > summary { background: var(--loss-bg); box-shadow: inset 4px 0 0 var(--loss); }
.mt.rs-d > summary { background: var(--draw-bg); box-shadow: inset 4px 0 0 var(--draw-line); }
.mt.rs-l > summary, .mt.rs-d > summary { padding-left: 12px; margin-block: 2px; }
.mt.rs-l > summary:hover, .mt.rs-d > summary:hover { filter: brightness(.97); }

.mb { padding: 4px 6px 20px; }
.mb .meta { color: var(--muted); font-size: 14px; margin: 0 0 12px; }
.mb .meta a { color: var(--accent); }
.cols { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 24px; }
.mb h3 { font-family: var(--font-mono); font-size: 12px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.ev { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
.ev li { display: grid; grid-template-columns: 44px 22px minmax(0, 1fr); gap: 6px; align-items: start; }
.ev .mn { color: var(--muted); font-size: 13px; padding-top: 2px; }
.ev b { font-weight: 600; }
.ev small { color: var(--muted); font-size: 13px; }
.ev .tm { display: block; font-size: 12px; }
.ev li.k b { color: var(--accent); }
.ev .rc { width: 11px; height: 15px; background: var(--loss); border-radius: 2px; margin-top: 3px; }
.none, .pen { color: var(--muted); font-size: 14px; margin: 8px 0 0; }
.stats { display: grid; gap: 10px; }
.stats .sh { display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; color: var(--muted); }
.sr { display: grid; grid-template-columns: 44px minmax(0, 1fr) 44px; gap: 8px; align-items: end; }
.sv { font-size: 14px; font-weight: 700; }
.sv.o { text-align: right; color: var(--muted); }
.sb { display: grid; gap: 4px; }
.sl { font-size: 12px; color: var(--muted); text-align: center; }
.bar { display: flex; height: 8px; border-radius: 4px; overflow: hidden; gap: 2px; }
.bar .bk { background: var(--accent); }
.bar .bo { background: var(--line); }
.mp-note { color: var(--muted); font-size: 13px; margin-top: 18px; }
@media (max-width: 700px) {
  .cols { grid-template-columns: minmax(0, 1fr); }
  .mt summary { grid-template-columns: 54px minmax(0, 1fr) auto 12px; gap: 8px; padding-inline: 2px; }
  .pair .lg { width: 20px; height: 20px; }
  .scr { font-size: 16px; gap: 6px; }
  .nm b { white-space: normal; line-height: 1.25; }
}
'''

MATCH_JS = r'''
(function () {
  var chips = document.querySelectorAll('.mp-tools .chip'), items = document.querySelectorAll('.mt');
  chips.forEach(function (c) { c.addEventListener('click', function () {
    var f = c.getAttribute('data-f');
    chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
    items.forEach(function (m) { m.hidden = !(f === 'all' || m.getAttribute('data-comp') === f); });
  }); });
  function openHash() {
    var t = location.hash && document.getElementById(location.hash.slice(1));
    if (t && t.tagName === 'DETAILS') { t.open = true; t.hidden = false; setTimeout(function () { t.scrollIntoView({ block: 'start' }); }, 30); }
  }
  window.addEventListener('hashchange', openHash); openHash();
})();
'''

n = len(PLAYED)
main_m = f'''<main class="wrap mp" id="top">
  <div class="mp-head">
    <h1>Матчи ФК «Краснодар» 2026/27</h1>
    <p>Все игры сезона в РПЛ и Кубке России. Нажмите на матч, чтобы увидеть голы, удаления и статистику. Время московское.</p>
    <div class="sum">
      <div><b>{n}</b><small>сыграно</small></div>
      <div><b>{W}–{D}–{L}</b><small>В–Н–П в осн. время</small></div>
      <div><b>{GF}:{GA}</b><small>мячи</small></div>
      <div><b>{len(UPCOMING)}</b><small>впереди</small></div>
    </div>
  </div>
  <div class="mp-tools chips" role="group" aria-label="Турнир">
    <button class="chip" type="button" data-f="all" aria-pressed="true">Все</button>
    <button class="chip" type="button" data-f="РПЛ" aria-pressed="false">РПЛ</button>
    <button class="chip" type="button" data-f="Кубок" aria-pressed="false">Кубок России</button>
  </div>
  <h2 class="sec">Ближайшие матчи</h2>
  {''.join(up_html)}
  <h2 class="sec">Сыгранные матчи</h2>
  {''.join(played_html)}
  <p class="mp-note">Время с пометкой «предварительно» может измениться: РПЛ утверждает его за несколько недель до тура. Статистика: FotMob, «Спорт Mail», официальный сайт ФК «Краснодар».</p>
</main>
'''
matches = (head('ФК «Краснодар»: календарь и результаты матчей 2026/27 — Быки News', 'Календарь и результаты ФК «Краснодар» в сезоне 2026/27: время матчей, голы и статистика каждой игры.', 'matches.html')
           + '<title>ФК «Краснодар»: календарь и результаты матчей 2026/27 — Быки News</title>\n'
           + SRC[SRC.index('<style>'):style_end].replace('</style>', MATCH_CSS + '</style>')
           + '\n</head>\n<body>\n' + nav_header('matches') + '\n\n' + main_m + '\n' + footer + '\n\n<script>' + MATCH_JS + '</script>\n</body>\n</html>\n')
(OUT / 'matches.html').write_text(matches, encoding='utf-8')
print('matches', len(matches), 'played', n, 'W-D-L', W, D, L, GF, GA)
