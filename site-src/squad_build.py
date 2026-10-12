# Страницы «Состав» (squad.html) и «Клуб» (club.html).
# Выполняется из build.py после matches_build.py: доступны head, nav_header, footer, SRC, style_end, OUT,
# а также PLAYED, UPCOMING, CLUBN из matches_build.py.
import datetime as _dt2, html as _h2, json as _j2

# ===== СОСТАВ =====
# Обновлять после каждого матча:
#   rpl = (игры, минуты, голы, передачи, ЖК, КК) — по Sports.ru (www.sports.ru/krasnodar/stat/)
#   cup = (игры, голы, передачи, ЖК)              — по протоколам матчей Кубка (rfs.ru)
# Голы с датами и соперниками берутся сами из PLAYED (matches_build.py) по полю «g» (часть имени автора гола).
# В списке только те, кто выходил на поле в РПЛ или Кубке; ушедших в аренду/проданных — убирать.
# Даты рождения и гражданство — Спорт Mail (sportmail.ru/team/547/players/).
SQUAD_UPDATED = '12 октября 2026 · РПЛ: 10 туров · Кубок: 3 тура'
SQUAD = [
 dict(n=1,  name='Станислав Агкацев',   pos='gk', bd='2002-01-09', c='Россия',     rpl=(10, 900, 0, 1, 1, 0), cup=(0, 0, 0, 0)),
 dict(n=16, name='Александр Корякин',   pos='gk', bd='2002-03-10', c='Россия',     rpl=(0, 0, 0, 0, 0, 0),    cup=(3, 0, 0, 0)),
 dict(n=3,  name='Витор Тормена',       pos='df', bd='1996-01-04', c='Бразилия',   rpl=(10, 890, 0, 0, 1, 1), cup=(2, 0, 0, 1), g='Тормена'),
 dict(n=5,  name='Жубал',               pos='df', bd='1993-08-29', c='Бразилия',   rpl=(10, 881, 3, 0, 3, 0), cup=(1, 0, 0, 0), g='Жубал'),
 dict(n=15, name='Лукас Оласа',         pos='df', bd='1994-07-21', c='Уругвай',    rpl=(10, 871, 1, 2, 2, 0), cup=(0, 0, 0, 0), g='Оласа'),
 dict(n=40, name='Илья Вахания',        pos='df', bd='2001-01-14', c='Россия',     rpl=(10, 767, 0, 1, 3, 0), cup=(2, 0, 0, 0)),
 dict(n=17, name='Валентин Пальцев',    pos='df', bd='2001-07-12', c='Россия',     rpl=(6, 137, 0, 0, 1, 0),  cup=(3, 0, 0, 0)),
 dict(n=59, name='Артём Хмарин',        pos='df', bd='2007-05-03', c='Россия',     rpl=(1, 8, 0, 0, 0, 0),    cup=(3, 0, 0, 0)),
 dict(n=98, name='Сергей Петров',       pos='df', bd='1991-01-02', c='Россия',     rpl=(3, 27, 0, 0, 0, 0),   cup=(0, 0, 0, 0)),
 dict(n=2,  name='Майсон Родригес',     pos='df', bd='2003-05-22', c='Уругвай',    rpl=(1, 7, 0, 0, 0, 0),    cup=(0, 0, 0, 0)),
 dict(n=11, name='Жоау Батчи',          pos='mf', bd='1998-05-01', c='Ангола',     rpl=(10, 787, 3, 1, 2, 0), cup=(3, 0, 0, 1), g='Батчи'),
 dict(n=53, name='Александр Черников',  pos='mf', bd='2000-02-01', c='Россия',     rpl=(10, 755, 0, 0, 3, 0), cup=(1, 0, 0, 0)),
 dict(n=8,  name='Дуглас Аугусто',      pos='mf', bd='1997-01-13', c='Бразилия',   rpl=(9, 705, 0, 1, 2, 0),  cup=(2, 0, 0, 0)),
 dict(n=18, name='Кристиан',            pos='mf', bd='2000-12-19', c='Бразилия',   rpl=(8, 553, 2, 2, 1, 0),  cup=(2, 0, 0, 0), g='Кристиан'),
 dict(n=23, name='Хуан Мануэль Боселли', pos='mf', bd='1999-11-09', c='Уругвай',   rpl=(8, 345, 2, 1, 0, 0),  cup=(2, 0, 0, 0), g='Боселли'),
 dict(n=88, name='Никита Кривцов',      pos='mf', bd='2002-08-18', c='Россия',     rpl=(4, 360, 3, 1, 1, 0),  cup=(2, 0, 0, 0), g='Кривцов', inj='травма'),
 dict(n=47, name='Даниил Уткин',        pos='mf', bd='1999-10-12', c='Россия',     rpl=(9, 343, 0, 0, 2, 0),  cup=(3, 1, 1, 0), g='Уткин'),
 dict(n=6,  name='Кевин Пина',          pos='mf', bd='1997-01-27', c='Кабо-Верде', rpl=(9, 280, 0, 1, 0, 0),  cup=(3, 0, 0, 0)),
 dict(n=21, name='Магомед Оздоев',      pos='mf', bd='1992-11-05', c='Россия',     rpl=(10, 179, 0, 0, 1, 0), cup=(3, 1, 0, 0), g='Оздоев'),
 dict(n=30, name='Степан Садчиков',     pos='mf', bd='2008-01-24', c='Россия',     rpl=(0, 0, 0, 0, 0, 0),    cup=(1, 0, 1, 0)),
 dict(n=60, name='Андрей Полевой',      pos='mf', bd='2008-07-02', c='Россия',     rpl=(0, 0, 0, 0, 0, 0),    cup=(1, 0, 0, 0)),
 dict(n=9,  name='Джон Кордоба',        pos='fw', bd='1993-05-11', c='Колумбия',   rpl=(6, 478, 2, 0, 3, 0),  cup=(0, 0, 0, 0), g='Кордоба'),
 dict(n=10, name='Дмитрий Воробьёв',    pos='fw', bd='1997-11-28', c='Россия',     rpl=(9, 598, 0, 2, 1, 0),  cup=(3, 0, 1, 1)),
 dict(n=70, name='Артём Дряхлов',       pos='fw', bd='2008-05-08', c='Россия',     rpl=(0, 0, 0, 0, 0, 0),    cup=(1, 0, 0, 1)),
 dict(n=74, name='Даниэль Амбарцумов',  pos='fw', bd='2008-03-07', c='Россия',     rpl=(0, 0, 0, 0, 0, 0),    cup=(1, 0, 0, 0)),
]
COACH = 'Мурад Мусаев'

_e = lambda s: _h2.escape(str(s), quote=True)
_MON = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
_TODAY = _dt2.date.today()

def _pl(n, a, b, c):
    return a if n % 10 == 1 and n % 100 != 11 else (b if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14 else c)

def _age(bd):
    b = _dt2.date.fromisoformat(bd)
    return _TODAY.year - b.year - ((_TODAY.month, _TODAY.day) < (b.month, b.day))

def _goals(key):
    out = []
    for m in PLAYED:
        for g in m.get('goals', []):
            if g[2] == 'k' and key in g[1]:
                d = _dt2.date.fromisoformat(m['d'])
                out.append(dict(d=f'{d.day} {_MON[d.month - 1]}', comp=m['comp'], opp=CLUBN[m['opp']],
                                where='дома' if m['home'] else 'в гостях', sc=f"{m['gf']}:{m['ga']}",
                                min=(g[0] + "'") if g[0] else '', pen='пенальти' in g[1], anchor='m-' + m['d']))
    return out

def _stat(v, w):
    return f'<span><b>{v}</b>{w}</span>'

def _card(p):
    rg, rm, rgl, ra, ry, rr = p['rpl']; cg, cgl, ca, cy = p['cup']
    a = _age(p['bd'])
    gk = p['pos'] == 'gk'
    cols = ['Игры', 'Мин'] + ([] if gk else ['Голы']) + ['Пасы', 'ЖК'] + (['КК'] if rr else [])
    def _row(lbl, cls, vals):
        return f'<tr><th scope="row"><i class="{cls}">{lbl}</i></th>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>'
    body = ''
    if rg:
        body += _row('РПЛ', 't-rpl', [rg, rm] + ([] if gk else [rgl]) + [ra, ry] + ([rr] if rr else []))
    if cg:
        body += _row('Кубок', 't-cup', [cg, '—'] + ([] if gk else [cgl]) + [ca, cy] + (['—'] if rr else []))
    rows = ('<table class="pl-t"><thead><tr><td></td>' + ''.join(f'<th scope="col">{c}</th>' for c in cols)
            + '</tr></thead><tbody>' + body + '</tbody></table>')
    gl = _goals(p['g']) if p.get('g') else []
    det = ''
    if gl:
        det = ('<details class="pl-g"><summary>Голы в сезоне — ' + str(len(gl)) + '</summary><ul>' + ''.join(
            f'<li><span class="mono">{x["d"]}</span><a href="matches.html#{x["anchor"]}">{x["comp"]} · {_e(x["opp"])}, {x["where"]} {x["sc"]}</a>'
            f'<b class="mono">{x["min"]}{" пен." if x["pen"] else ""}</b></li>' for x in gl) + '</ul></details>')
    inj = f' <span class="inj">{_e(p["inj"])}</span>' if p.get('inj') else ''
    return (f'<li class="pl" id="p{p["n"]}"><div class="pl-n">{p["n"]}</div><div class="pl-b"><h3>{_e(p["name"])}{inj}</h3>'
            f'<div class="pl-m">{_e(p["c"])} · {a} {_pl(a, "год", "года", "лет")}</div>{rows}{det}</div></li>')

_POS = [('gk', 'Вратари'), ('df', 'Защитники'), ('mf', 'Полузащитники'), ('fw', 'Нападающие')]
def _sortkey(p):
    return (-(p['rpl'][0] + p['cup'][0]), -p['rpl'][1], p['n'])
_groups = ''.join(
    f'<h2 class="grp">{t} <span>{sum(1 for p in SQUAD if p["pos"] == k)}</span></h2><ul class="pls">'
    + ''.join(_card(p) for p in sorted([p for p in SQUAD if p['pos'] == k], key=_sortkey)) + '</ul>'
    for k, t in _POS)
_lead_data = [dict(n=p['name'], id=p['n'], rg=p['rpl'][0], rgl=p['rpl'][2], ra=p['rpl'][3],
                   cg=p['cup'][0], cgl=p['cup'][1], ca=p['cup'][2]) for p in SQUAD]

SQUAD_CSS = r'''
.nav a[aria-current="page"] { background: var(--turf-2); }
main.sq { display: block; padding-block: 8px 56px; }
.sq-head { padding-block: 28px 4px; display: grid; gap: 10px; }
.sq-head h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(28px, 5vw, 44px); letter-spacing: -.01em; line-height: 1.1; }
.sq-head p { margin: 0; color: var(--muted); max-width: 70ch; }
.sq-upd { font-family: var(--font-mono); font-size: 12px; color: var(--muted); }
.lead-box { margin-top: 18px; background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px 16px; }
.lead-top { display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; justify-content: space-between; }
.lead-top h2 { font-family: var(--font-display); font-size: 18px; margin: 0; }
.lds { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px 24px; margin-top: 12px; }
.ld h3 { font-family: var(--font-mono); font-size: 11px; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); margin: 0 0 6px; }
.ld ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 5px; }
.ld li { display: flex; justify-content: space-between; gap: 8px; font-size: 14px; }
.ld li a { text-decoration: none; }
.ld li a:hover { color: var(--accent); }
.ld li b { font-family: var(--font-display); font-variant-numeric: tabular-nums; }
.ld .none { color: var(--muted); font-size: 13px; }
.grp { font-family: var(--font-display); font-weight: 800; font-size: clamp(26px, 4.5vw, 34px); margin: 36px 0 12px; display: flex; align-items: baseline; gap: 8px; }
.grp span { font-family: var(--font-mono); font-size: 15px; color: var(--muted); }
.pls { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; }
.pl { display: grid; grid-template-columns: 50px minmax(0, 1fr); gap: 12px; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px; align-items: start; scroll-margin-top: 120px; }
.pl:target { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
.pl-n { font-family: var(--font-display); font-weight: 900; font-size: 28px; color: var(--accent); text-align: center; line-height: 1.1; }
.pl h3 { margin: 0; font-size: 16px; }
.pl-m { color: var(--muted); font-size: 13px; margin-bottom: 4px; }
.pl-t { width: 100%; border-collapse: collapse; margin-top: 6px; }
.pl-t thead th { font-family: var(--font-mono); font-size: 10px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--muted); text-align: center; padding: 0 0 3px; }
.pl-t thead td { width: 52px; }
.pl-t td, .pl-t thead th { padding-inline: 3px; }
.pl-t tbody th { text-align: left; padding: 4px 0; }
.pl-t td { text-align: center; font-family: var(--font-display); font-weight: 700; font-size: 15px; font-variant-numeric: tabular-nums; padding: 4px 0; }
.pl-t tbody tr + tr { border-top: 1px solid var(--line); }
.pl-t i { font-style: normal; font-family: var(--font-mono); font-size: 10px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; border-radius: 4px; padding: 1px 5px; min-width: 46px; text-align: center; }
.t-rpl { background: var(--accent-soft); color: var(--accent); }
.t-cup { background: var(--signal); color: var(--on-signal); }
.pl-g { margin-top: 8px; font-size: 13px; }
.pl-g summary { cursor: pointer; color: var(--accent); font-weight: 700; }
.pl-g ul { list-style: none; margin: 6px 0 0; padding: 0; display: grid; gap: 3px; }
.pl-g li { display: grid; grid-template-columns: 48px minmax(0, 1fr) auto; gap: 8px; }
.pl-g a { text-decoration: none; }
.pl-g a:hover { text-decoration: underline; }
.pl-g .mono { font-family: var(--font-mono); font-size: 12px; color: var(--muted); }
.pl-g li b { color: var(--ink); }
.sq-note { color: var(--muted); font-size: 13px; margin-top: 22px; border-top: 1px solid var(--line); padding-top: 12px; }
.sq-note a { color: var(--accent); }
@media (max-width: 700px) {
  .lds { grid-template-columns: minmax(0, 1fr); }
  .pls { grid-template-columns: minmax(0, 1fr); }
  .pl { grid-template-columns: 38px minmax(0, 1fr); gap: 10px; }
  .pl-n { font-size: 24px; }
}
'''

SQUAD_JS = r'''
(function () {
  var D = __DATA__;
  var box = document.getElementById('ldBox'), mode = 'all';
  var CAT = [['Голы', 'gl'], ['Передачи', 'a'], ['Матчи', 'g']];
  function val(p, k) { return mode === 'rpl' ? p['r' + k] : mode === 'cup' ? p['c' + k] : p['r' + k] + p['c' + k]; }
  function esc(t) { var e = document.createElement('div'); e.textContent = t; return e.innerHTML; }
  function render() {
    box.innerHTML = CAT.map(function (c) {
      var top = D.filter(function (p) { return val(p, c[1]) > 0; }).sort(function (a, b) { return val(b, c[1]) - val(a, c[1]); }).slice(0, 4);
      return '<div class="ld"><h3>' + c[0] + '</h3>' + (top.length ? '<ol>' + top.map(function (p) {
        return '<li><a href="#p' + p.id + '">' + esc(p.n) + '</a><b>' + val(p, c[1]) + '</b></li>';
      }).join('') + '</ol>' : '<p class="none">Пока никого</p>') + '</div>';
    }).join('');
  }
  document.querySelectorAll('.lead-top .chip').forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.getAttribute('data-m');
      document.querySelectorAll('.lead-top .chip').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      render();
    });
  });
  render();
})();
'''.replace('__DATA__', _j2.dumps(_lead_data, ensure_ascii=False))

squad_main = f'''<main class="wrap sq" id="top">
  <div class="sq-head">
    <h1>Состав «Краснодара» 2026/27</h1>
    <p>Игроки, которые выходили на поле в сезоне 2026/27. Статистика каждого приведена отдельно по РПЛ и Кубку России. Главный тренер — {COACH}.</p>
    <p>Чтобы посмотреть голы игрока по матчам, откройте «Голы в сезоне» в его карточке.</p>
    <span class="sq-upd">Обновлено: {SQUAD_UPDATED}</span>
  </div>
  <section class="lead-box" aria-labelledby="ld-h">
    <div class="lead-top"><h2 id="ld-h">Лидеры сезона</h2>
      <div class="chips" role="group" aria-label="Турнир">
        <button class="chip" type="button" data-m="all" aria-pressed="true">Все турниры</button>
        <button class="chip" type="button" data-m="rpl" aria-pressed="false">РПЛ</button>
        <button class="chip" type="button" data-m="cup" aria-pressed="false">Кубок</button>
      </div>
    </div>
    <div class="lds" id="ldBox"></div>
  </section>
  {_groups}
  <p class="sq-note">Статистика РПЛ — <a href="https://www.sports.ru/krasnodar/stat/" target="_blank" rel="noopener">Sports.ru</a>; Кубок — протоколы матчей на <a href="https://www.rfs.ru/" target="_blank" rel="noopener">сайте РФС</a>; даты рождения и гражданство — <a href="https://sportmail.ru/team/547/players/" target="_blank" rel="noopener">Спорт Mail</a>. В Кубке учитываются выходы на поле, голы, передачи и карточки в основное и дополнительное время, без серий пенальти.</p>
</main>
'''
squad_page = (head('Состав «Краснодара» 2026/27 — Быки News', 'Состав ФК «Краснодар» в сезоне 2026/27: номера, возраст и статистика каждого игрока в РПЛ и Кубке России — игры, голы, передачи.', 'squad.html')
              + '<title>Состав «Краснодара» 2026/27 — Быки News</title>\n'
              + SRC[SRC.index('<style>'):style_end].replace('</style>', SQUAD_CSS + '</style>')
              + '\n</head>\n<body>\n' + nav_header('squad') + '\n\n' + squad_main + '\n' + footer + '\n\n<script>' + SQUAD_JS + '</script>\n</body>\n</html>\n')
(OUT / 'squad.html').write_text(squad_page, encoding='utf-8')

# ===== КЛУБ =====
_WD = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
_next = []
for _u in UPCOMING[:3]:
    _d = _dt2.date.fromisoformat(_u[0])
    _t = _u[1].rstrip('*')
    _next.append(f'<li><b>{_d.day} {_MON[_d.month - 1]}, {_WD[_d.weekday()]}' + (f', {_t}' if _t else '') + ('*' if _u[1].endswith('*') else '')
                 + f'</b> — «{_e(CLUBN[_u[4]])}», {_u[2]}, ' + ('Ozon Арена' if _u[5] else 'в гостях') + '</li>')

CLUB_CSS = r'''
.nav a[aria-current="page"] { background: var(--turf-2); }
main.cl { display: block; padding-block: 8px 56px; }
.cl-head { padding-block: 28px 4px; display: grid; gap: 10px; }
.cl-head h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(28px, 5vw, 44px); letter-spacing: -.01em; line-height: 1.1; }
.cl-head p { margin: 0; color: var(--muted); max-width: 70ch; }
.cl .kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }
.cl .kpi { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 14px; color: var(--ink); }
.cl .kpi b { font-family: var(--font-display); font-weight: 900; font-size: 24px; display: block; line-height: 1.15; }
.cl .kpi span { color: var(--muted); font-size: 13px; }
.cl .kpi.gold { background: var(--signal); border-color: var(--signal); color: var(--on-signal); }
.cl .kpi.gold span { color: var(--on-signal); }
.cblocks { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; margin-top: 14px; }
.cb { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 16px 18px; min-width: 0; }
.cb h2 { font-family: var(--font-display); font-size: 19px; margin: 0 0 10px; }
.cb ul { margin: 0; padding-left: 18px; display: grid; gap: 7px; }
.cb p { margin: 0 0 8px; }
.tline { list-style: none; padding: 0 !important; }
.tline li { display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: 10px; }
.tline li > b { font-family: var(--font-mono); font-size: 13px; color: var(--accent); padding-top: 2px; }
.cl .btn { display: inline-block; margin-top: 10px; background: var(--accent); color: #fff; text-decoration: none; font-weight: 700; border-radius: 999px; padding: 8px 14px; font-size: 14px; }
.cl .muted { color: var(--muted); font-size: 13px; }
.cl-note { color: var(--muted); font-size: 13px; margin-top: 22px; border-top: 1px solid var(--line); padding-top: 12px; }
.cl-note a { color: var(--accent); }
@media (max-width: 760px) {
  .cblocks { grid-template-columns: minmax(0, 1fr); }
  .cl .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .cl .kpi b { font-size: 19px; }
}
'''
club_main = f'''<main class="wrap cl" id="top">
  <div class="cl-head">
    <h1>Клуб и болельщикам</h1>
    <p>Коротко о «Краснодаре», стадионе Ozon Арена и о том, как попасть на матч.</p>
  </div>
  <div class="kpis">
    <div class="kpi gold"><b>2024/25</b><span>чемпион России — первый титул в истории</span></div>
    <div class="kpi"><b>2008</b><span>год основания, 22 февраля</span></div>
    <div class="kpi"><b>2-е место</b><span>в РПЛ 2025/26</span></div>
    <div class="kpi"><b>3 финала</b><span>Кубка России: 2014, 2023, 2026</span></div>
  </div>
  <div class="cblocks">
    <section class="cb"><h2>История в датах</h2><ul class="tline">
      <li><b>2008</b><span>Сергей Галицкий основал клуб 22 февраля</span></li>
      <li><b>2011</b><span>Дебют в Премьер-лиге. С тех пор «Краснодар» не покидал высший дивизион</span></li>
      <li><b>2016</b><span>9 октября открыт собственный стадион — матчем Россия — Коста-Рика</span></li>
      <li><b>2024</b><span>В марте в клуб вернулся Мурад Мусаев — он тренирует команду второй раз</span></li>
      <li><b>2025</b><span>24 мая — победа над «Динамо» в последнем туре и первое чемпионство</span></li>
      <li><b>2026</b><span>Серебро РПЛ и финал Кубка со «Спартаком»: 1:1, в серии пенальти 3:4</span></li>
    </ul></section>
    <section class="cb"><h2>Стадион — Ozon Арена</h2>
      <p>Так стадион «Краснодар» называется с 1 мая 2025 года. Вмещает больше 33 тысяч зрителей. Внутри — панорамный экран площадью 4700 м², снаружи — медиафасад по всему периметру.</p>
      <p>Адрес: Краснодар, ул. Разведчика Леонова, 1. Рядом — парк Галицкого площадью 22 гектара. В дни матчей ходят шаттлы от крупных транспортных узлов.</p>
      <a class="btn" href="https://2gis.ru/krasnodar/firm/70000001025023333" target="_blank" rel="noopener">Маршрут в 2ГИС ↗</a></section>
    <section class="cb"><h2>Билеты</h2><ul>
      <li>Официально: <b>ticket.fckrasnodar.ru</b>, приложение клуба, кассы стадиона; также «Яндекс Афиша» и Кассир.ру.</li>
      <li>На кубковые матчи с октября нужен <b>Fan ID</b> — без него онлайн-покупка недоступна.</li>
      <li>Перепроданные билеты клуб аннулирует — покупайте только в официальных точках.</li>
      <li>Владельцы абонементов проходят по QR-коду из «Госуслуг».</li>
    </ul></section>
    <section class="cb"><h2>Ближайшие матчи</h2><ul>{''.join(_next)}</ul>
      <p class="muted" style="margin-top:8px">* время предварительное</p>
      <a class="btn" href="matches.html">Все матчи →</a></section>
  </div>
  <p class="cl-note">Источники: <a href="https://www.euro-football.ru/article/29/1005917172_chempionskiy_titul_rpl__pervyiy_trofey_krasnodara_v_klubnoy_istorii" target="_blank" rel="noopener">Евро-Футбол</a> (история, чемпионство), <a href="https://kuban.aif.ru/sport/-krasnodar-v-borbe-za-kubok-rossii-put-k-finalu-sezona-2025-2026" target="_blank" rel="noopener">АиФ-Кубань</a> (финал Кубка 2026), <a href="https://www.livesport.ru/football/2026/05/17/rpl_results/" target="_blank" rel="noopener">Livesport</a> (итоги РПЛ 2025/26), <a href="https://www.vedomosti.ru/sport/football/articles/2024/03/30/1028958-vozvraschenie" target="_blank" rel="noopener">Ведомости</a> (возвращение Мусаева), <a href="https://www.putevka.com/krasnodar/krasnodar/sight/stadion-krasnodar" target="_blank" rel="noopener">Putevka</a> (стадион), <a href="https://fckrasnodar.ru/fan/news/object/?object_id=154135" target="_blank" rel="noopener">официальный сайт клуба</a> (билеты).</p>
</main>
'''
club_page = (head('Клуб «Краснодар»: история, стадион, билеты — Быки News', 'ФК «Краснодар»: история клуба и трофеи, стадион Ozon Арена — адрес и как добраться, где купить билеты и что нужно для прохода.', 'club.html')
             + '<title>Клуб «Краснодар»: история, стадион, билеты — Быки News</title>\n'
             + SRC[SRC.index('<style>'):style_end].replace('</style>', CLUB_CSS + '</style>')
             + '\n</head>\n<body>\n' + nav_header('club') + '\n\n' + club_main + '\n' + footer + '\n</body>\n</html>\n')
(OUT / 'club.html').write_text(club_page, encoding='utf-8')
print('squad', len(squad_page), 'players', len(SQUAD), '| club', len(club_page))
