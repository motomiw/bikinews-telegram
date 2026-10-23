#!/usr/bin/env python3
"""Сборка сайта bikinews.ru из мастер-файла bykinews.html.

Делает:
  site/index.html        — главная (обёртка мастера)
  site/news.html         — страница «Новости»: наши пересказы + архив автоленты
  site/data/glavnoe.json — пересказы из блока «Главное» (для страницы новостей)
"""
import base64, html, json, re, time, calendar
from pathlib import Path

import os, shutil
ROOT = Path(__file__).resolve().parent
SRC = (ROOT / 'bykinews.html').read_text(encoding='utf-8')
OUT = Path(os.environ.get('BIKINEWS_OUT', ROOT.parent / 'dist'))
(OUT / 'data').mkdir(parents=True, exist_ok=True)
FAV = base64.b64encode((ROOT / 'assets/favicon-32.png').read_bytes()).decode()
YEAR = 2026


def head(title, desc, path='', img='og-image.jpg'):
    url = 'https://bikinews.ru/' + path
    og = ('<meta property="og:type" content="website">\n'
          '<meta property="og:site_name" content="Быки News">\n'
          '<meta property="og:locale" content="ru_RU">\n'
          f'<meta property="og:url" content="{url}">\n'
          f'<meta property="og:title" content="{title}">\n'
          f'<meta property="og:description" content="{desc}">\n'
          f'<meta property="og:image" content="https://bikinews.ru/{img}">\n'
          '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
          '<meta property="og:image:alt" content="Быки News — новости ФК «Краснодар»">\n'
          '<meta name="twitter:card" content="summary_large_image">\n'
          f'<meta name="twitter:image" content="https://bikinews.ru/{img}">\n'
          f'<link rel="canonical" href="{url}">\n')
    return ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n' + og +
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<meta name="description" content="{desc}">\n'
            # значок — обычными файлами из корня (Яндекс не берёт data:-ссылки, поэтому в выдаче был «глобус»)
            '<link rel="icon" href="/favicon.ico" sizes="any">\n'
            '<link rel="icon" type="image/png" sizes="180x180" href="/apple-touch-icon.png">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="alternate" type="application/rss+xml" title="Быки News" href="https://bikinews.ru/rss.xml">\n'
            '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}'
            'html.app .site-head .nav>a,html.app .site-head .nav::before{display:none!important}'
            'html.app .site-head .wrap{flex-wrap:nowrap!important;justify-content:space-between!important;min-height:56px;padding-block:6px!important}'
            'html.app .site-head .logo{flex-basis:auto!important}html.app .site-head .nav{margin-left:auto;flex-basis:auto!important}</style>\n'
            # в приложении Быки News для Android разделы — в нижней панели приложения, ссылки шапки прячем
            '<script>if(/BikinewsApp\\//.test(navigator.userAgent))document.documentElement.classList.add("app")</script>\n')


# ---------- главная ----------
style_end = SRC.index('</style>') + len('</style>')
INDEX_TITLE = 'ФК «Краснодар»: новости, матчи, таблица РПЛ — Быки News'
INDEX_DESC = ('Новости ФК «Краснодар» каждый день: анонсы и итоги матчей, заявления Мусаева и игроков, '
              'таблица РПЛ, состав, бомбардиры и календарь сезона 2026/27.')
INDEX_LD = ('<script type="application/ld+json">' + json.dumps({
    '@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Быки News',
    'alternateName': 'bikinews.ru', 'url': 'https://bikinews.ru/', 'inLanguage': 'ru',
    'description': INDEX_DESC}, ensure_ascii=False) + '</script>\n')
# <title> в мастере короткий («Быки News») — для поисковиков ставим полный
index_src_head = re.sub(r'<title>.*?</title>', '<title>' + INDEX_TITLE + '</title>', SRC[:style_end], count=1, flags=re.S)
index = (head(INDEX_TITLE, INDEX_DESC) + INDEX_LD
         + index_src_head + '\n</head>\n<body>\n' + SRC[style_end:].lstrip('\n') + '</body>\n</html>\n')
(OUT / 'index.html').write_text(index, encoding='utf-8')

# ---------- «Главное» → JSON ----------
MON = {'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4, 'мая': 5, 'июн': 6, 'июл': 7, 'авг': 8, 'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12}
feed_html = SRC[SRC.index('<ul class="feed">'):SRC.index('</ul>', SRC.index('<ul class="feed">'))]
items = []
for n, li in enumerate(re.findall(r'<li><article>(.*?)</article></li>', feed_html, flags=re.S)):
    t = re.sub(r'<[^>]+>', ' ', re.search(r'<time[^>]*>(.*?)</time>', li, flags=re.S).group(1))
    m = re.search(r'(\d{1,2})\s+([а-я]{3})', t)
    hm = re.search(r'(\d{1,2}):(\d{2})', t)
    day, mon = int(m.group(1)), MON[m.group(2)]
    hh, mm = (int(hm.group(1)), int(hm.group(2))) if hm else (12, 0)
    ts = calendar.timegm((YEAR, mon, day, hh, mm, 0)) - 3 * 3600   # время московское
    a = re.search(r'<a class="src" href="([^"]+)"[^>]*>(.*?)</a>', li, flags=re.S)
    items.append({
        'id': 'n' + __import__('hashlib').sha1((html.unescape(re.search(r'<a class="src" href="([^"]+)"', li).group(1)) + '|' + html.unescape(re.search(r'<h3>(.*?)</h3>', li, flags=re.S).group(1))).encode()).hexdigest()[:8],
        'ts': ts, 'notime': not hm,
        'tag': html.unescape(re.search(r'<span class="tag">(.*?)</span>', li).group(1)),
        'title': html.unescape(re.search(r'<h3>(.*?)</h3>', li, flags=re.S).group(1)),
        'paras': [html.unescape(re.sub(r'<[^>]+>', '', p)) for p in re.findall(r'<p>(.*?)</p>', li, flags=re.S)],
        'url': html.unescape(a.group(1)),
        'source': html.unescape(re.sub(r'^Источник:\s*|\s*↗$', '', a.group(2)).strip()),
    })
# у каждого пересказа своя страница: <транслит заголовка>-<id>.html
_TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя', ['a','b','v','g','d','e','e','zh','z','i','y','k','l','m','n','o','p','r','s','t','u','f','h','ts','ch','sh','sch','','y','','e','yu','ya']))
def news_slug(title, nid):
    t = ''.join(_TR.get(c, c) for c in title.lower())
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    t = t[:60].rsplit('-', 1)[0] if len(t) > 60 else t
    return (t + '-' if t else '') + nid + '.html'
for _it in items:
    _it['page'] = news_slug(_it['title'], _it['id'])
    if _it['url'].startswith('https://bikinews.ru/'):   # своя статья (article_build.py): заголовок ведёт прямо на неё
        _it['page'] = _it['url'][len('https://bikinews.ru/'):]; _it['article'] = True
from email.utils import formatdate as _fd
_rss = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>',
        '<title>Быки News — новости ФК «Краснодар»</title>', '<link>https://bikinews.ru/</link>',
        '<atom:link href="https://bikinews.ru/rss.xml" rel="self" type="application/rss+xml"/>',
        '<description>Главные новости ФК «Краснодар» каждый день — Быки News.</description>', '<language>ru</language>']
for _it in items[:30]:
    _link = 'https://bikinews.ru/' + _it['page']
    _desc = (_it['paras'][0] if _it['paras'] else '') + ' Источник: ' + _it['source'] + '.'
    _rss.append('<item><title>' + html.escape(_it['title']) + '</title><link>' + _link + '</link><guid isPermaLink="false">bikinews-' + _it['id'] + '</guid>'
                + '<pubDate>' + _fd(_it['ts']) + '</pubDate><description>' + html.escape(_desc) + '</description></item>')
_rss.append('</channel></rss>')
(OUT / 'rss.xml').write_text('\n'.join(_rss), encoding='utf-8')
(OUT / 'data/glavnoe.json').write_text(json.dumps({'updated': int(time.time()), 'items': items}, ensure_ascii=False, indent=1), encoding='utf-8')

# ---------- страница «Новости» ----------
header = SRC[SRC.index('<header class="site-head">'):SRC.index('</header>') + len('</header>')]
header = header.replace('href="#top"', 'href="./"')
HEADER_BASE = header
TG_LINK = re.search(r'<a class="cta tg".*?</a>\s*<a class="mx".*?</a>\s*<button class="a11y-btn".*?</button>', SRC, flags=re.S).group(0)
def nav_header(cur):
    items = [('./', 'Главная', ''), ('matches.html', 'Матчи', 'matches'), ('./#table', 'Таблица', ''), ('squad.html', 'Состав', 'squad'), ('news.html', 'Новости', 'news'), ('club.html', 'Клуб', 'club')]
    nav = '<nav class="nav" aria-label="Разделы">\n' + ''.join(
        f'      <a href="{h}"' + (' class="home"' if t == 'Главная' else '') + (' aria-current="page"' if k == cur else '') + f'>{t}</a>\n' for h, t, k in items) + '      ' + TG_LINK + '\n    </nav>'
    return re.sub(r'<nav class="nav".*?</nav>', nav, HEADER_BASE, flags=re.S)
header = nav_header('news')
footer = SRC[SRC.index('<footer class="foot">'):SRC.index('</footer>') + len('</footer>')]

NEWS_CSS = r'''
/* страница новостей */
.nav a[aria-current="page"] { background: var(--turf-2); }
main.np { display: block; padding-block: 8px 56px; }
.np-head { padding-block: 28px 4px; display: grid; gap: 10px; }
.np-head h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(28px, 5vw, 44px); letter-spacing: -.01em; line-height: 1.1; }
.np-head p { margin: 0; color: var(--muted); max-width: 70ch; }
.np-head .np-lead { color: var(--ink); font-size: clamp(17px, 2.2vw, 20px); line-height: 1.5; max-width: 62ch; }
.np-kinds { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin: 8px 0 0; }
.np-kinds > div { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; }
.np-kinds dt { font-weight: 700; font-size: 15px; margin: 0 0 4px; }
.np-kinds dd { margin: 0; color: var(--muted); font-size: 14px; line-height: 1.45; }
.np-head .np-upd { font-size: 13px; }
.np-head .np-upd:has(#npUpd:empty) { display: none; }
@media (max-width: 720px) { .np-kinds { grid-template-columns: minmax(0, 1fr); gap: 6px; } .np-kinds > div { padding: 10px 14px; } .np-kinds dd { font-size: 13px; } }
.np-tools { display: flex; flex-wrap: wrap; gap: 12px 16px; align-items: center; padding-block: 16px 8px; position: sticky; top: 64px; z-index: 5; background: var(--bg); }
.np-search { flex: 1 1 220px; max-width: 360px; font: 16px var(--font-body); color: var(--ink); background: var(--surface); border: 1.5px solid var(--line); border-radius: 999px; padding: 9px 16px; }
.np-search:focus { outline: none; border-color: var(--accent); }
.np-count { color: var(--muted); font-size: 13px; }
.np-day { font-family: var(--font-mono); font-size: 13px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); padding: 26px 0 8px; border-bottom: 2px solid var(--ink); }
.np-list { list-style: none; margin: 0; padding: 0; }
.np-list > li { border-bottom: 1px solid var(--line); }
.np-item { display: grid; grid-template-columns: 64px minmax(0, 1fr); gap: 16px; padding: 16px 0; }
.np-item time { color: var(--muted); font-size: 13px; padding-top: 3px; }
.np-body { min-width: 0; display: grid; gap: 6px; justify-items: start; }
.np-meta { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--accent); display: flex; gap: 10px; flex-wrap: wrap; }
.np-meta .own { background: var(--signal); color: var(--on-signal); padding: 1px 6px; border-radius: 4px; }
.np-meta .src-name { color: var(--muted); }
.np-item h3 { font-size: 18px; font-weight: 700; line-height: 1.3; }
.np-item h3 a { text-decoration: none; }
.np-item h3 a:hover { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }
.np-item p { margin: 0; line-height: 1.6; max-width: 70ch; }
.np-item p + p { color: var(--muted); }
.np-item .ext { color: var(--muted); font-size: 15px; }
.np-item .src { font-size: 14px; font-weight: 600; color: var(--accent); text-decoration: none; border-bottom: 1px solid currentColor; }
.np-item.own-item h3 { font-size: 20px; }
.np-empty { padding: 40px 0; color: var(--muted); }
.np-more { display: block; margin: 24px auto 8px; }
.np-item:target { background: var(--accent-soft); border-radius: 8px; padding-inline: 10px; margin-inline: -10px; }
@media (max-width: 600px) {
  .np-tools { top: 0; position: static; }
  .np-item { grid-template-columns: minmax(0, 1fr); gap: 4px; }
  .np-item h3, .np-item.own-item h3 { font-size: 18px; }
}
'''

NEWS_JS = r'''
(function () {
  'use strict';
  var PAGE = 40, shown = PAGE, filter = 'all', query = '', all = [];
  var MONTHS_G = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
  var WD = ['воскресенье','понедельник','вторник','среда','четверг','пятница','суббота'];
  function msk(ts) {
    var f = new Intl.DateTimeFormat('ru-RU', { timeZone: 'Europe/Moscow', year: 'numeric', month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit', weekday: 'long', hour12: false });
    var o = {}; f.formatToParts(new Date(ts * 1000)).forEach(function (p) { o[p.type] = p.value; }); return o;
  }
  function esc(t) { var e = document.createElement('div'); e.textContent = String(t == null ? '' : t); return e.innerHTML.replace(/"/g, '&quot;'); }
  // один и тот же сюжет, пересказанный разными словами: сравниваем смысловые слова (основы по 5 букв и числа)
  var STOP = { красн: 1, матч: 1, клуб: 1, команд: 1, рпл: 1, сезон: 1, тур: 1, игра: 1, игры: 1, после: 1, перед: 1, быков: 1, быки: 1, быкам: 1, сообщ: 1, стало: 1, этом: 1, этого: 1, также: 1, котор: 1, чтобы: 1, читат: 1, дальш: 1, прес: 1 };
  function toks(t) {
    var out = [];
    String(t).toLowerCase().replace(/ё/g, 'е').replace(/[^a-zа-я0-9 ]+/g, ' ').split(/\s+/).forEach(function (w) {
      if (!w) return;
      var k = /^[0-9]+$/.test(w) ? (w.length >= 2 ? w : '') : (w.length > 3 ? w.slice(0, 5) : '');
      if (k && !STOP[k] && out.indexOf(k) === -1) out.push(k);
    });
    return out;
  }
  function body(n) { return n.title + ' ' + (n.paras ? n.paras.join(' ') : (n.text || '')); }
  function sameStory(n, m) {
    if (Math.abs(n.ts - m.ts) > 24 * 3600) return false;
    var a = toks(n.title), b = toks(m.title);
    if (!a.length || !b.length) return false;
    // заголовки почти совпадают
    var c = a.filter(function (w) { return b.indexOf(w) !== -1; }).length;
    if (c >= 3 && c / Math.min(a.length, b.length) >= 0.6) return true;
    // заголовок одного укладывается в текст другого (например, наш пересказ и заметка издания)
    var bb = toks(body(m)), aa = toks(body(n));
    var ca = a.filter(function (w) { return bb.indexOf(w) !== -1; }).length;
    var cb = b.filter(function (w) { return aa.indexOf(w) !== -1; }).length;
    if ((ca >= 4 && ca / a.length >= 0.6) || (cb >= 4 && cb / b.length >= 0.6)) return true;
    // одно событие разными словами («голкипер стал мастером спорта» / «вратарь получил звание»): много общих смысловых слов в заголовках и текстах
    if (Math.abs(n.ts - m.ts) <= 12 * 3600) {
      var shared = aa.filter(function (w) { return bb.indexOf(w) !== -1; }).length;
      if (shared >= 5 && shared / Math.min(aa.length, bb.length) >= 0.35) return true;
    }
    return false;
  }
  function dedupNews(list) {
    var kept = [];
    list.forEach(function (n) {
      if (!kept.some(function (k) { return sameStory(n, k); })) kept.push(n);
    });
    return kept;
  }
  // Только новости о «Краснодаре»: news.php тащит и чужие (голы «Зенита» и т. п.).
  // Пропускаем материал, если «Краснодар», Быки, тренер или игрок клуба есть в заголовке, либо это сайт клуба.
  var KRD_RE = /краснодар|(^|[^а-яё])бык(и|ов|ам|ами|ах)?([^а-яё]|$)|мусаев|галицк|ozon арен|озон арен|кордоб|агкацев|батчи|жубал|оласа|тормен|вахани|пальцев|хмарин|черников|аугусто|боселли|кривцов|уткин|оздоев|воробь[её]в|корякин|буркин|садчиков/i;
  function aboutKrd(n) {
    if (String(n.source || '').indexOf('ФК') === 0) return true;
    var t = String(n.title || '').toLowerCase().replace(/ё/g, 'е').replace(/воробьев/g, 'воробьёв');
    // «Мусаев» без других признаков «Краснодара» в материале о «Зените» — это игрок «Зенита», не наш тренер
    if (/зенит/.test(t) && !KRD_RE.test(t.replace(/мусаев[а-я]*/g, ''))) return false;
    return KRD_RE.test(t);
  }
  function kind(n) { return n.own ? 'own' : (n.source.indexOf('ФК') === 0 ? 'club' : 'media'); }
  function getJSON(u) { return fetch(u + '?t=' + Date.now(), { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); }

  Promise.all([getJSON('data/glavnoe.json'), getJSON('data/archive.json'), getJSON('data/news.json')]).then(function (res) {
    var g = res[0] && res[0].items || [], seen = {};
    g.forEach(function (n) { n.own = true; seen[n.url] = 1; all.push(n); });
    [res[1], res[2]].forEach(function (d) {
      (d && d.items || []).filter(aboutKrd).forEach(function (n) { if (!seen[n.url]) { seen[n.url] = 1; all.push(n); } });
    });
    var own = all.filter(function (n) { return n.own; }), ext = all.filter(function (n) { return !n.own; });
    ext.sort(function (a, b) { return a.ts - b.ts; });
    // у издания и у нас один сюжет — оставляем наш пересказ, заметку издания не дублируем
    ext = dedupNews(ext).filter(function (n) { return !own.some(function (o) { return sameStory(n, o); }); });
    all = own.concat(ext);
    all.sort(function (a, b) { return b.ts - a.ts; });
    var upd = Math.max(res[1] ? res[1].updated || 0 : 0, res[2] ? res[2].updated || 0 : 0);
    if (upd) { var u = msk(upd); document.getElementById('npUpd').textContent = 'Лента изданий обновлена ' + (+u.day) + ' ' + MONTHS_G[+u.month - 1] + ' в ' + u.hour + ':' + u.minute + '.'; }
    render();
    if (location.hash) { var t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
  });

  function match(n) {
    if (filter !== 'all' && kind(n) !== filter) return false;
    if (!query) return true;
    var hay = (n.title + ' ' + (n.text || '') + ' ' + (n.paras || []).join(' ') + ' ' + n.source).toLowerCase();
    return query.split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
  }

  function item(n) {
    var d = msk(n.ts), time = n.notime ? '' : d.hour + ':' + d.minute;
    if (n.own) {
      return '<li><article class="np-item own-item" id="' + esc(n.id) + '"><time class="mono">' + time + '</time><div class="np-body">' +
        '<div class="np-meta"><span class="own">Быки News</span><span>' + esc(n.tag) + '</span></div>' +
        '<h3>' + (n.page ? '<a href="' + esc(n.page) + '">' + esc(n.title) + '</a>' : esc(n.title)) + '</h3>' + n.paras.map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('') +
        '<a class="src" href="' + esc(n.url) + '" target="_blank" rel="noopener">Источник: ' + esc(n.source) + ' ↗</a></div></article></li>';
    }
    return '<li><article class="np-item"><time class="mono">' + time + '</time><div class="np-body">' +
      '<div class="np-meta"><span class="src-name">' + esc(n.source) + '</span></div>' +
      '<h3><a href="' + esc(n.url) + '" target="_blank" rel="noopener">' + esc(n.title) + ' <span class="ext">↗</span></a></h3>' +
      (n.text ? '<p>' + esc(n.text).replace(/([а-яё0-9»)])([А-ЯЁ])/g, '$1. $2').replace(/\s*(Читать (?:дальше|далее)\S*)/gi, ' <b>$1</b>') + '</p>' : '') + '</div></article></li>';
  }

  function render() {
    var list = all.filter(match), out = [], lastDay = '';
    list.slice(0, shown).forEach(function (n) {
      var d = msk(n.ts), key = d.year + d.month + d.day;
      if (key !== lastDay) {
        if (lastDay) out.push('</ul>');
        out.push('<h2 class="np-day">' + (+d.day) + ' ' + MONTHS_G[+d.month - 1] + ', ' + d.weekday + '</h2><ul class="np-list">');
        lastDay = key;
      }
      out.push(item(n));
    });
    if (lastDay) out.push('</ul>');
    document.getElementById('npFeed').innerHTML = out.length ? out.join('') :
      '<p class="np-empty">' + (all.length ? 'Ничего не нашлось — попробуйте другое слово или фильтр.' : 'Новости загружаются…') + '</p>';
    document.getElementById('npCount').textContent = list.length ? 'Новостей: ' + list.length : '';
    document.getElementById('npMore').hidden = list.length <= shown;
  }

  document.querySelectorAll('.np-tools .chip').forEach(function (c) {
    c.addEventListener('click', function () {
      filter = c.getAttribute('data-f'); shown = PAGE;
      document.querySelectorAll('.np-tools .chip').forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      render();
    });
  });
  var timer;
  document.getElementById('npSearch').addEventListener('input', function (e) {
    clearTimeout(timer); timer = setTimeout(function () { query = e.target.value.trim().toLowerCase(); shown = PAGE; render(); }, 150);
  });
  document.getElementById('npMore').addEventListener('click', function () { shown += PAGE; render(); });
})();
'''

main = '''<main class="wrap np" id="top">
  <div class="np-head">
    <h1>Новости ФК «Краснодар»</h1>
    <p class="np-lead">Всё, что происходит вокруг клуба: матчи и турнирная борьба, состав и травмы, слова тренера и игроков. Коротко, понятным языком и всегда со ссылкой на первоисточник.</p>
    <dl class="np-kinds">
      <div><dt>От редакции</dt><dd>Главное за день в двух абзацах, своими словами и со ссылкой на источник.</dd></div>
      <div><dt>Сайт клуба</dt><dd>Официальные сообщения ФК «Краснодар» без изменений.</dd></div>
      <div><dt>Издания</dt><dd>Заголовки профильных СМИ. Полный текст — на сайте источника.</dd></div>
    </dl>
    <p class="np-upd"><span id="npUpd"></span></p>
  </div>
  <div class="np-tools">
    <div class="chips" role="group" aria-label="Какие новости показать">
      <button class="chip" type="button" data-f="all" aria-pressed="true">Все</button>
      <button class="chip" type="button" data-f="own" aria-pressed="false">От редакции</button>
      <button class="chip" type="button" data-f="club" aria-pressed="false">Сайт клуба</button>
      <button class="chip" type="button" data-f="media" aria-pressed="false">Издания</button>
    </div>
    <input class="np-search" id="npSearch" type="search" placeholder="Поиск: Кордоба, Кубок, травма…" aria-label="Поиск по новостям">
    <span class="np-count" id="npCount"></span>
  </div>
  <div id="npFeed"><p class="np-empty">Новости загружаются…</p></div>
  <button class="more np-more" id="npMore" type="button" hidden>Показать ещё</button>
</main>
'''
news = (head('Новости ФК «Краснодар» сегодня — Быки News', 'Свежие новости ФК «Краснодар»: матчи и составы, травмы и трансферы, заявления тренера и игроков, решения РПЛ и КДК. Лента обновляется каждый день.', 'news.html')
        + '<title>Новости ФК «Краснодар» сегодня — Быки News</title>\n'
        + SRC[SRC.index('<style>'):style_end].replace('</style>', NEWS_CSS + '</style>')
        + '\n</head>\n<body>\n' + header + '\n\n' + main + '\n' + footer + '\n\n<script>' + NEWS_JS + '</script>\n</body>\n</html>\n')
(OUT / 'news.html').write_text(news, encoding='utf-8')
print('index', len(index), 'news', len(news), 'glavnoe', len(items))

exec(open(ROOT / 'max_build.py', encoding='utf-8').read())
exec(open(ROOT / 'matches_build.py', encoding='utf-8').read())
exec(open(ROOT / 'squad_build.py', encoding='utf-8').read())
exec(open(ROOT / 'aside_build.py', encoding='utf-8').read())
exec(open(ROOT / 'og_build.py', encoding='utf-8').read())
exec(open(ROOT / 'news_pages_build.py', encoding='utf-8').read())
exec(open(ROOT / 'article_build.py', encoding='utf-8').read())
exec(open(ROOT / 'privacy_build.py', encoding='utf-8').read())

# статические файлы (шрифты, логотипы, иконки, robots, sitemap, .htaccess)
shutil.copytree(ROOT / 'static', OUT, dirs_exist_ok=True)

# sitemap с сегодняшней датой
import datetime as _d
_today = _d.date.today().isoformat()
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>https://bikinews.ru/{p}</loc><lastmod>{_today}</lastmod><changefreq>{c}</changefreq><priority>{pr}</priority></url>\n'
              for p, c, pr in [('', 'hourly', '1.0'), ('news.html', 'hourly', '0.9'), ('matches.html', 'daily', '0.9'), ('squad.html', 'weekly', '0.8'), ('club.html', 'monthly', '0.6'), ('privacy.html', 'yearly', '0.2')] + [(it['page'], 'monthly', '0.7') for it in items])
    + '</urlset>\n', encoding='utf-8')
print('dist ->', OUT)
