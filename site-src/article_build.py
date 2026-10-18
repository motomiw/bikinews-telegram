# Длинные авторские статьи Быки News (не пересказы). Каждая — своя страница <slug>.html.
# Выполняется из build.py после news_pages_build.py: доступны head, nav_header, footer, SRC, style_end, OUT, NP_CSS.
# Чтобы статья попала в «Главное» (и в Telegram), в bykinews.html добавляется обычный <li> со ссылкой
# https://bikinews.ru/<slug>.html — build.py узнаёт свою ссылку и ведёт заголовок сразу на статью.
import html as _ha, json as _ja

ARTICLES = [{
    'slug': 'krasnodar-bez-pobed-chto-slomalos-razbor.html',
    'title': '«Краснодар» без побед: что сломалось и как это чинить',
    'desc': 'Разбор спада «Краснодара»: пять причин с цифрами, что делать до зимы, кого искать в трансферное окно и стоит ли менять Мусаева.',
    'tag': 'Разбор',
    'date_iso': '2026-10-19T01:20:00+03:00',
    'date_txt': '19 октября 2026',
    'read': '6 минут',
    'body': '''
<p class="ar-lead">Шесть матчей без побед, пятое место и слухи об отставке Мусаева. Разбираемся спокойно: где правда, где шум и что можно исправить.</p>

<aside class="ar-box" aria-label="Коротко">
  <h2>Коротко</h2>
  <ul>
    <li><b>Это не обвал, а пробуксовка.</b> В РПЛ одно поражение, до первого места — 3 очка.</li>
    <li><b>Некому создавать моменты.</b> Ушёл Сперцян, травмирован Кривцов.</li>
    <li><b>Кордоба на пределе</b> и играет без поддержки.</li>
    <li><b>Оборона и Агкацев</b> перестали спасать.</li>
    <li><b>Менять тренера рано.</b> Нужны схема без «десятки» и точечные покупки зимой.</li>
  </ul>
</aside>

<h2>Цифры спада</h2>
<ul class="ar-score">
  <li><span>«Крылья Советов»</span><b class="mono">2:2</b></li>
  <li><span>«Акрон»</span><b class="mono">1:1</b></li>
  <li><span>«Оренбург»</span><b class="mono">0:0</b></li>
  <li><span>«Зенит»</span><b class="mono">2:3</b></li>
  <li><span>«Факел», Кубок</span><b class="mono">0:2</b></li>
  <li><span>«Локомотив»</span><b class="mono">3:3</b></li>
</ul>
<p>Сейчас Быки <b>пятые</b>: 22 очка, мячи 19:13. У лидера, московского «Динамо», — 25.</p>
<p>Пять туров РПЛ подряд без побед у «Краснодара» — всего второй раз за десять лет.</p>

<h2>1. Некому создавать моменты</h2>
<p>Летом в «Аль-Ахли» ушёл <b>Эдуард Сперцян</b> — капитан и мозг атаки. В прошлом чемпионате у него 13 голов и 16 передач.</p>
<p>Сначала его роль взял <b>Никита Кривцов</b>, и команда выиграла шесть матчей подряд. Потом Кривцов тяжело травмировался — и замены ему не нашлось.</p>
<p>Под нападающим пробовали Уткина, Кристиана и Воробьёва. Не сработал никто. Уткин бьёт больше трёх раз за матч, но создаёт для партнёров меньше одного момента.</p>

<h2>2. Кордоба на пределе</h2>
<ul>
  <li>33 года, после травмы на ЧМ-2026 — без нормальной предсезонки.</li>
  <li>7 матчей РПЛ из 11 и 3 гола.</li>
  <li>Последние 6 туров — все 90 минут: менять некем.</li>
  <li>Выигрывает около 41% единоборств на земле и 28% — в воздухе.</li>
</ul>
<p>Без партнёра под собой Джону приходится воевать в одиночку. Но характер на месте — гол «Локомотиву» это показал.</p>

<h2>3. Оборона и вратарь перестали спасать</h2>
<ul>
  <li><b>Ушёл Виктор Са.</b> Кристиан чаще отбирает мяч, но хуже держит позицию — соперники атакуют через его фланг.</li>
  <li><b>Диего Коста — в аренде в ПАОК.</b> Тормена и Жубал допустили по 4 ошибки, приведшие к голам (данные «РУСТАТ»).</li>
</ul>
<div class="ar-tbl"><table>
  <caption>Станислав Агкацев по сезонам</caption>
  <thead><tr><th>Показатель</th><th>24/25</th><th>25/26</th><th>26/27</th></tr></thead>
  <tbody>
    <tr><td>Пропущено за матч</td><td>0,77</td><td>0,77</td><td class="bad">1,18</td></tr>
    <tr><td>Отражено ударов</td><td>78%</td><td>71%</td><td class="bad">68%</td></tr>
    <tr><td>Предотвращённые голы</td><td>+10,3</td><td>+3,9</td><td class="bad">−2,3</td></tr>
  </tbody>
</table></div>
<p>По отдельности ни оборона, ни вратарь не провальные. Просто они перестали страховать друг друга.</p>

<h2>4. Короткая скамейка</h2>
<p>Игроков в заявке хватает, равноценных замен — нет. Выпал один Кривцов — и пустует «десятка». Нет сменщика Кордобе — и он играет на износ.</p>

<h2>5. Раздевалка: правда и шум</h2>
<ul>
  <li><b>Мусаев</b> после «Факела»: «Проблема глобальная: она внутри там».</li>
  <li><b>Кривцов</b> публично усомнился, что капитаном должен быть иностранец. Повязку летом отдали Кордобе.</li>
  <li><b>«Сила Спорта»</b> пишет, что Галицкий недоволен и клуб обсуждает отставку тренера. Официально это не подтверждено.</li>
  <li><b>«Спорт-Экспресс»</b> по своим источникам: раскола на группировки нет.</li>
</ul>
<p class="ar-note"><b>Наш взгляд.</b> Плохая игра портит атмосферу, а не наоборот. Но после ухода Сперцяна в команде пока нет признанного лидера.</p>

<h2>Что делать до зимней паузы</h2>
<ol>
  <li><b>Схема без «десятки».</b> Создавать моменты вдвоём-втроём: «восьмёрки» и вингеры, смещающиеся в центр.</li>
  <li><b>Второй нападающий</b> рядом с Кордобой, чтобы он не воевал один.</li>
  <li><b>Давать Кордобе отдыхать.</b> Концовки — Воробьёву.</li>
  <li><b>Закрыть фланг:</b> дисциплинированный крайний и подстраховка опорника.</li>
  <li><b>Постоянная пара центральных защитников</b> и меньше риска у своих ворот.</li>
  <li><b>Поддержать Агкацева,</b> а не менять в панике.</li>
  <li><b>Закрыть тему капитанства</b> внутри команды, без интервью.</li>
  <li><b>Стандарты</b> — самый быстрый источник голов, когда игра не идёт.</li>
</ol>

<h2>Кого искать зимой</h2>
<ul>
  <li><b>Созидающий атакующий полузащитник</b> — приоритет №1.</li>
  <li>Быстрый центральный защитник.</li>
  <li>Вингер, который умеет работать назад.</li>
  <li>Нападающий-сменщик Кордобе.</li>
  <li>А Кривцова — не торопить с возвращением.</li>
</ul>

<h2>Менять ли Мусаева?</h2>
<p><b>Рано.</b> Он выиграл чемпионство-2024/25, а в прошлом сезоне уступил «Зениту» всего два очка. Сейчас проблемы прежде всего кадровые.</p>
<p>Вопросы к ротации и заменам справедливы. Но увольнение при отставании в три очка скорее добавит хаоса, чем решит что-то.</p>

<h2>Итог</h2>
<p>У «Краснодара» кризис креатива и глубины состава, а не всего сразу. Отставание минимальное, характер есть. Первый шанс развернуть серию — <b>24 октября дома с «Балтикой»</b>.</p>

<section class="ar-src" aria-labelledby="src-h">
  <h2 id="src-h">Источники</h2>
  <ul>
    <li><a href="https://www.sovsport.ru/football/articles/krah-vratarya-dyra-posle-krivczova-kordoba-ne-tot-pochemu-krasnodar-povalilsya" target="_blank" rel="noopener">«Советский спорт»: почему «Краснодар» повалился ↗</a></li>
    <li><a href="https://www.sport-express.net/football/rfpl/reviews/krasnodar-v-sezone-2026-27-rezultaty-i-prichiny-problem-shansy-na-chempionstvo-2463828/" target="_blank" rel="noopener">«Спорт-Экспресс»: чёрная серия «Краснодара» ↗</a></li>
    <li><a href="https://kuban24.tv/item/musaev-zayavil-chto-u-fk-krasnodar-est-globalnaya-problema-vnutri-kluba" target="_blank" rel="noopener">«Кубань 24»: Мусаев о проблеме внутри клуба ↗</a></li>
    <li><a href="https://legalbet.ru/news/62020161-425477-krasnodar-mozhet-uvolit-musaeva-iz-za-pyati-matche/" target="_blank" rel="noopener">Legalbet: «Краснодар» может уволить Мусаева ↗</a></li>
    <li><a href="https://sport.rambler.ru/football/57245318-bubnov-nazval-prichiny-spada-krasnodara/" target="_blank" rel="noopener">«Рамблер/спорт»: Бубнов о причинах спада ↗</a></li>
    <li><a href="https://sportandbets.com/novosti/genich-zashchitil-krasnodar-posle-serii-bez-pobed-globalnykh-treshchin-ya-ne-vizhu.html" target="_blank" rel="noopener">SportandBets: Генич защитил «Краснодар» ↗</a></li>
    <li><a href="https://www.sports.ru/football/tournament/rfpl/" target="_blank" rel="noopener">Sports.ru: таблица РПЛ 2026/27 ↗</a></li>
  </ul>
</section>
''',
}]

AR_CSS = r'''
.ar-art { max-width: 68ch; }
.ar-art .ar-lead { font-size: 20px; line-height: 1.55; color: var(--muted); }
.ar-art h2 { font-family: var(--font-display); font-weight: 800; font-size: clamp(21px, 3.2vw, 26px); line-height: 1.2; margin: 34px 0 12px; }
.ar-art ul, .ar-art ol { margin: 0 0 16px; padding-left: 1.3em; font-size: 18px; line-height: 1.6; }
.ar-art li { margin-bottom: 8px; }
.ar-art li::marker { color: var(--accent); font-weight: 700; }
.ar-box { background: var(--accent-soft); border-left: 4px solid var(--accent); border-radius: 10px; padding: 16px 20px 6px; margin: 22px 0 8px; }
.ar-box h2 { margin: 0 0 10px; font-size: 18px; text-transform: uppercase; letter-spacing: .06em; font-family: var(--font-mono); }
.ar-art .ar-score { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 8px; }
.ar-score li { display: flex; justify-content: space-between; align-items: center; gap: 10px; border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; margin: 0; font-size: 16px; }
.ar-score b { font-size: 18px; }
.ar-tbl { overflow-x: auto; margin: 6px 0 16px; }
.ar-tbl table { border-collapse: collapse; width: 100%; font-size: 16px; }
.ar-tbl caption { text-align: left; font-weight: 700; padding-bottom: 8px; }
.ar-tbl th, .ar-tbl td { padding: 9px 10px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }
.ar-tbl th:first-child, .ar-tbl td:first-child { text-align: left; white-space: normal; }
.ar-tbl thead th { font-family: var(--font-mono); font-size: 13px; color: var(--muted); border-bottom: 2px solid var(--ink); }
.ar-tbl td.bad { font-weight: 800; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 3px; }
.ar-note { border: 2px solid var(--signal); border-radius: 10px; padding: 12px 16px; }
.ar-src { margin-top: 36px; border-top: 2px solid var(--ink); padding-top: 6px; }
.ar-src h2 { margin-top: 12px; font-size: 20px; }
.ar-src ul { font-size: 15px; }
.ar-src a { color: var(--accent); }
@media (max-width: 600px) { .ar-art .ar-lead { font-size: 18px; } .ar-art ul, .ar-art ol { font-size: 17px; } .ar-box { padding-inline: 16px; } }
'''

_ae = lambda s: _ha.escape(str(s), quote=True)
_ar_style = SRC[SRC.index('<style>'):style_end].replace('</style>', NP_CSS + AR_CSS + '</style>')
for _a in ARTICLES:
    _ld = _ja.dumps({'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': _a['title'][:110],
                     'description': _a['desc'], 'datePublished': _a['date_iso'], 'dateModified': _a['date_iso'],
                     'inLanguage': 'ru', 'mainEntityOfPage': 'https://bikinews.ru/' + _a['slug'],
                     'image': ['https://bikinews.ru/og-image.jpg'],
                     'author': {'@type': 'Organization', 'name': 'Быки News', 'url': 'https://bikinews.ru/'},
                     'publisher': {'@type': 'Organization', 'name': 'Быки News', 'url': 'https://bikinews.ru/'},
                     'about': 'ФК «Краснодар»'}, ensure_ascii=False)
    _main = f'''<main class="wrap na" id="top">
  <nav class="na-crumbs" aria-label="Навигация"><a href="./">Главная</a><span>›</span><a href="news.html">Новости ФК «Краснодар»</a></nav>
  <article class="na-art ar-art">
    <div class="na-meta"><span class="tag">{_ae(_a["tag"])}</span><time datetime="{_a["date_iso"]}">{_ae(_a["date_txt"])}</time><span>· {_ae(_a["read"])} чтения</span></div>
    <h1>{_ae(_a["title"])}</h1>
    {_a["body"]}
  </article>
  <p><a class="na-all" href="news.html">Все новости «Краснодара» →</a></p>
</main>
'''
    _page = (head(_ae(_a['title']) + ' | Быки News', _ae(_a['desc']), _a['slug'])
             .replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
             + f'<title>{_ae(_a["title"])} | Быки News</title>\n'
             + f'<script type="application/ld+json">{_ld}</script>\n'
             + _ar_style + '\n</head>\n<body>\n' + nav_header('news') + '\n\n' + _main + '\n' + footer + '\n</body>\n</html>\n')
    (OUT / _a['slug']).write_text(_page, encoding='utf-8')

# в «Главном» на главной ссылка «Источник: Быки News» у своей статьи → «Читать статью полностью»
_idx = (OUT / 'index.html').read_text(encoding='utf-8')
for _a in ARTICLES:
    _idx = re.sub(r'<a class="src" href="https://bikinews\.ru/' + re.escape(_a['slug']) + r'"[^>]*>.*?</a>',
                  f'<a class="src" href="{_a["slug"]}">Читать статью полностью →</a>', _idx, flags=re.S)
(OUT / 'index.html').write_text(_idx, encoding='utf-8')
print('articles', len(ARTICLES))
