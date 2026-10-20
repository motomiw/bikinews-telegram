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
}, {
    'slug': 'tri-matcha-za-vosem-dnej-krasnodar-ishchet-pobedu.html',
    'title': 'Три матча за восемь дней: «Краснодар» ищет победу',
    'desc': '«Балтика», «Динамо» в Кубке и «Родина»: что стоит на кону у Быков в ближайшие восемь дней, где команда теряла очки и что говорят Мусаев и эксперты.',
    'tag': 'Разбор',
    'date_iso': '2026-10-20T16:00:00+03:00',
    'date_txt': '20 октября 2026',
    'read': '4 минуты',
    'body': '''
<p class="ar-lead">С 29 августа «Краснодар» не выигрывал в основное время. Пять ничьих и два поражения подряд, пятое место в таблице и разговоры об отставке тренера. Ближайшие восемь дней покажут, насколько всё серьёзно.</p>

<p>После 11 туров у Быков 22 очка: шесть побед, четыре ничьи и одно поражение, мячи 19:13. До лидера, московского «Динамо», три очка, до «Зенита» два. Первые пять команд уместились в три очка, поэтому любая серия сейчас двигает клуб по таблице сильнее, чем обычно.</p>

<ul class="ar-score">
  <li><span>24 окт, «Балтика»</span><b class="mono">19:30</b></li>
  <li><span>27 окт, «Динамо», Кубок</span><b class="mono">20:30</b></li>
  <li><span>31 окт, «Родина», гости</span><b class="mono">19:45</b></li>
</ul>

<h2>Ничья, которая не успокоила</h2>
<p>Матч с «Локомотивом» (3:3) показал команду целиком. Быки открыли счёт на пятой минуте, потом пропустили три мяча и к 78-й проигрывали 1:3. Лукас Оласа на 86-й и Джон Кордоба на 90+1-й спасли очко, но Мурад Мусаев после игры говорил совсем не о характере.</p>

<p>«Не понравились лёгкие голы, которые мы пропускаем. Такого не было три сезона. Это непозволительно», — сказал тренер. Про атаку он отозвался мягче: моменты есть, надо убирать простые ошибки.</p>

<p>Дело не только в обороне. Эдуард Сперцян ушёл летом, Никита Кривцов, который должен был его заменить, в этом году уже не сыграет. Мусаев надеется, что тот вернётся к тренировкам в январе. Андрей Тихонов в интервью Metaratings причину видит в глубине состава, а не в тренере: без двух человек, «которые делали разницу», по его словам, никакая команда не покажет прежний футбол.</p>

<h2>Три соперника, три разных вопроса</h2>
<p><b>«Балтика»</b> стоит седьмой, у неё 13 очков и 12 пропущенных мячей в 11 турах. На выходных калининградцы сыграли 0:0 с «Ростовом», так что лёгкого матча не будет. Для «Краснодара» это, прежде всего, проверка дома: с «Оренбургом» в гостях и с «Акроном» у себя Быки очки уже теряли.</p>

<p>Матч с «Акроном» (1:1) наглядный пример. Владение 69%, 21 удар против восьми, xG 1,40 против 0,33. Гости забили первыми, на 13-й минуте, и Хуану Мануэлю Боселли пришлось спасать очко на 88-й.</p>

<p><b>«Динамо»</b> в Кубке России — единственный из трёх соперников, которого «Краснодар» уже обыгрывал в этом сезоне. 19 августа в Москве Казбек Мукаилов забил на 44-й минуте, и этого хватило для победы 1:0. Сейчас «Динамо» возглавляет РПЛ, и встреча в группе B снова пройдёт на «Ozon Арене». В кубковой группе после неё останется один матч, с «Ахматом» 25 ноября. А 22 ноября Быки сыграют с «Динамо» уже в чемпионате, в гостях.</p>

<p><b>«Родина»</b> идёт последней: шесть очков и 27 пропущенных мячей, больше, чем у любой другой команды. Но и она в понедельник не сдалась, сравняв счёт с «Оренбургом» на 90-й минуте (2:2). Поездка в Химки выглядит лёгкой только на бумаге: с «Акроном» и «Оренбургом» тоже так казалось.</p>

<h2>Что на кону</h2>
<p>Победы в обоих чемпионатных матчах дадут 28 очков. Это больше, чем сейчас у «Динамо». Что наберут остальные, предсказать нельзя, но к ноябрю Быки подходили бы в числе лидеров, а не в роли догоняющих. Если же серия продолжится, разговоры вокруг команды и Мусаева станут громче независимо от места в таблице.</p>

<p>Следующая точка после этих трёх матчей — 7 ноября, дома с ЦСКА. У армейцев сейчас столько же очков, сколько у «Краснодара».</p>

<section class="ar-src" aria-labelledby="src-h">
  <h2 id="src-h">Источники</h2>
  <ul>
    <li><a href="https://www.euro-football.ru/article/29/1006383228_musaev__o_nichey_s_lokomotivom_ne_ponravilis_legkie_golyi" target="_blank" rel="noopener">«Евро-Футбол»: Мусаев о ничьей с «Локомотивом» ↗</a></li>
    <li><a href="https://sport-express.ru/football/rfpl/news/trener-krasnodara-murad-musaev-kommentariy-o-niche-v-matche-s-lokomotivom-17-oktyabrya-2026-2464229" target="_blank" rel="noopener">«Спорт-Экспресс»: комментарий Мусаева после матча ↗</a></li>
    <li><a href="https://metaratings.ru/news/tikhonov-s-krasnodarom-chto-to-tvoritsya-neladnoe-delo-v-glubine-sostava-663602/" target="_blank" rel="noopener">Metaratings: Тихонов о «Краснодаре» ↗</a></li>
    <li><a href="https://www.sovsport.ru/football/news/trener-krasnodara-musaev-podtverdil-chto-krivczov-bolshe-ne-sygraet-v-etom-godu" target="_blank" rel="noopener">«Советский спорт»: Мусаев о Кривцове ↗</a></li>
    <li><a href="https://news.mail.ru/society/72676561/" target="_blank" rel="noopener">«Новости Mail»: Мусаев о возвращении Кривцова ↗</a></li>
    <li><a href="https://www.sport-express.ru/football/rfpl/news/rodina-orenburg-schet-i-rezultat-machta-11-tura-rpl-19-oktyabrya-2026-2464875/" target="_blank" rel="noopener">«Спорт-Экспресс»: «Родина» — «Оренбург» 2:2 ↗</a></li>
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
