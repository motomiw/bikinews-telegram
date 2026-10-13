# Отдельная страница для каждого пересказа из «Главного» (<slug>-<id>.html) — чтобы поисковики находили новости по отдельности.
# Выполняется из build.py: доступны items, head, nav_header, footer, SRC, style_end, OUT.
import html as _hn, json as _jn, datetime as _dn

_e = lambda s: _hn.escape(str(s), quote=True)
_MONG = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
_MSK = _dn.timezone(_dn.timedelta(hours=3))

NP_CSS = r'''
.nav a[aria-current="page"] { background: var(--turf-2); }
main.na { display: block; padding-block: 8px 56px; }
.na-crumbs { font-size: 14px; color: var(--muted); padding-top: 24px; display: flex; gap: 6px; flex-wrap: wrap; }
.na-crumbs a { color: var(--accent); text-decoration: none; }
.na-crumbs a:hover { text-decoration: underline; }
.na-art { max-width: 72ch; padding-block: 10px 8px; }
.na-meta { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; font-family: var(--font-mono); font-size: 12px; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; color: var(--muted); margin: 14px 0 10px; }
.na-meta .tag { background: var(--signal); color: var(--on-signal); padding: 2px 7px; border-radius: 4px; }
.na-art h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(26px, 4.6vw, 40px); line-height: 1.15; letter-spacing: -.01em; margin: 0 0 18px; text-wrap: balance; }
.na-art p { font-size: 18px; line-height: 1.65; margin: 0 0 16px; }
.na-src { display: inline-block; margin-top: 6px; font-weight: 700; color: var(--accent); text-decoration: none; border-bottom: 1px solid currentColor; }
.na-more { margin-top: 40px; border-top: 2px solid var(--ink); padding-top: 16px; max-width: 72ch; }
.na-more h2 { font-family: var(--font-display); font-size: 22px; margin: 0 0 10px; }
.na-more ul { list-style: none; margin: 0; padding: 0; }
.na-more li { border-bottom: 1px solid var(--line); padding: 10px 0; display: grid; grid-template-columns: 92px minmax(0, 1fr); gap: 12px; }
.na-more time { font-family: var(--font-mono); font-size: 12px; color: var(--muted); padding-top: 3px; }
.na-more a { text-decoration: none; font-weight: 600; }
.na-more a:hover { color: var(--accent); text-decoration: underline; }
.na-all { display: inline-block; margin-top: 16px; font-weight: 700; color: var(--accent); }
@media (max-width: 600px) { .na-art p { font-size: 17px; } .na-more li { grid-template-columns: minmax(0, 1fr); gap: 2px; } }
'''

def _date(it, with_time=True):
    d = _dn.datetime.fromtimestamp(it['ts'], _MSK)
    s = f'{d.day} {_MONG[d.month - 1]} {d.year}'
    return s + (f', {d:%H:%M}' if with_time and not it.get('notime') else '')

_style = SRC[SRC.index('<style>'):style_end].replace('</style>', NP_CSS + '</style>')
for _i, it in enumerate(items):
    title = it['title']
    desc = (it['paras'][0] if it['paras'] else title)
    desc = desc if len(desc) <= 160 else desc[:157].rsplit(' ', 1)[0] + '…'
    iso = _dn.datetime.fromtimestamp(it['ts'], _MSK).isoformat()
    ld = _jn.dumps({'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': title[:110],
                    'datePublished': iso, 'dateModified': iso, 'inLanguage': 'ru',
                    'mainEntityOfPage': 'https://bikinews.ru/' + it['page'],
                    'image': ['https://bikinews.ru/og-image.jpg'],
                    'author': {'@type': 'Organization', 'name': 'Быки News', 'url': 'https://bikinews.ru/'},
                    'publisher': {'@type': 'Organization', 'name': 'Быки News', 'url': 'https://bikinews.ru/'},
                    'isBasedOn': it['url'], 'about': 'ФК «Краснодар»'}, ensure_ascii=False)
    others = [o for o in items if o is not it][:6]
    more = ''.join(f'<li><time>{_e(_date(o, False))}</time><a href="{_e(o["page"])}">{_e(o["title"])}</a></li>' for o in others)
    page_main = f'''<main class="wrap na" id="top">
  <nav class="na-crumbs" aria-label="Навигация"><a href="./">Главная</a><span>›</span><a href="news.html">Новости ФК «Краснодар»</a></nav>
  <article class="na-art">
    <div class="na-meta"><span class="tag">{_e(it["tag"])}</span><time datetime="{iso}">{_e(_date(it))}</time></div>
    <h1>{_e(title)}</h1>
    {''.join(f'<p>{_e(p)}</p>' for p in it['paras'])}
    <a class="na-src" href="{_e(it["url"])}" target="_blank" rel="noopener">Источник: {_e(it["source"])} ↗</a>
  </article>
  <section class="na-more" aria-labelledby="more-h"><h2 id="more-h">Другие новости «Краснодара»</h2><ul>{more}</ul>
    <a class="na-all" href="news.html">Все новости →</a></section>
</main>
'''
    page = (head(_e(title) + ' — ФК «Краснодар» | Быки News', _e(desc), it['page'])
            .replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
            + f'<title>{_e(title)} — ФК «Краснодар» | Быки News</title>\n'
            + f'<script type="application/ld+json">{ld}</script>\n'
            + _style + '\n</head>\n<body>\n' + nav_header('news') + '\n\n' + page_main + '\n' + footer + '\n</body>\n</html>\n')
    (OUT / it['page']).write_text(page, encoding='utf-8')

# на главной заголовки пересказов в «Главном» ведут на их страницы
_idx = (OUT / 'index.html').read_text(encoding='utf-8')
for it in items:
    _h3 = '<h3>' + _hn.escape(it['title'], quote=False) + '</h3>'
    if _h3 in _idx:
        _idx = _idx.replace(_h3, f'<h3><a class="nl" href="{_e(it["page"])}">{_hn.escape(it["title"], quote=False)}</a></h3>', 1)
_idx = _idx.replace('</style>', '.feed h3 a.nl { color: inherit; text-decoration: none; } .feed h3 a.nl:hover { color: var(--accent); text-decoration: underline; text-underline-offset: 3px; }\n</style>', 1)
(OUT / 'index.html').write_text(_idx, encoding='utf-8')
print('news pages', len(items))
