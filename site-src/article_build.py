# Длинные авторские статьи Быки News (не пересказы). Каждая — своя страница <slug>.html.
# Выполняется из build.py после news_pages_build.py: доступны head, nav_header, footer, SRC, style_end, OUT, NP_CSS.
# Чтобы статья попала в «Главное» (и в Telegram), в bykinews.html добавляется обычный <li> со ссылкой
# https://bikinews.ru/<slug>.html — build.py узнаёт свою ссылку и ведёт заголовок сразу на статью.
import html as _ha, json as _ja

ARTICLES = [{
    'slug': 'krasnodar-bez-pobed-chto-slomalos-razbor.html',
    'title': 'Почему после шести стартовых побед «Краснодар» стал терять очки',
    'desc': 'За семь официальных матчей команда пять раз сыграла вничью и дважды уступила в основное время. В центре поля пришлось искать замену травмированному Кривцову, а у Кордобы почти не осталось передышки. В разборе собрали цифры по атаке, обороне и игре Агкацева.',
    'tag': 'Разбор',
    'date_iso': '2026-10-19T01:20:00+03:00',
    'date_txt': '19 октября 2026',
    'read': '5 минут',
    'body': '''
<p class="ar-lead">Семь матчей подряд «Краснодар» не выигрывает за 90 минут. При этом до первого места всего три очка. Где команда, начавшая чемпионат с шести побед, потеряла прежнее преимущество?</p>

<h2>Серия в цифрах</h2>
<ul class="ar-score">
  <li><span>«Факел», Кубок</span><b class="mono">1:1</b></li>
  <li><span>«Крылья Советов»</span><b class="mono">2:2</b></li>
  <li><span>«Акрон»</span><b class="mono">1:1</b></li>
  <li><span>«Оренбург»</span><b class="mono">0:0</b></li>
  <li><span>«Зенит»</span><b class="mono">2:3</b></li>
  <li><span>«Факел», Кубок</span><b class="mono">0:2</b></li>
  <li><span>«Локомотив»</span><b class="mono">3:3</b></li>
</ul>
<p>В Воронеже краснодарцы одолели «Факел» по пенальти (4:3). Но в чемпионате за пять туров набрали всего четыре очка. После 11 матчей у них 22 очка и мячи 19:13, у лидирующего московского «Динамо» 25 очков.</p>

<h2>Некому создавать моменты</h2>
<p>За прошлый чемпионат Эдуард Сперцян забил 13 голов и сделал 16 результативных передач. После его перехода в «Аль-Ахли» между линиями удачно открывался Никита Кривцов. Команда выиграла шесть туров подряд, но затем потеряла и его из-за травмы.</p>
<p>Под Кордобой выходят Уткин, Кристиан и Воробьёв. У каждого свои привычки. Уткин, например, за матч больше трёх раз бьёт сам, а под удар партнёра выводит в среднем реже одного раза.</p>

<h2>Кордоба играет на износ</h2>
<p>У Кордобы три гола в семи играх чемпионата. После травмы на чемпионате мира он пропустил часть подготовки, но последние шесть туров отыграл целиком. В воздухе колумбиец выигрывает около 28% единоборств, на земле около 41%. Тем ценнее его гол «Локомотиву» в добавленное время.</p>

<h2>Оборона и вратарь перестали выручать друг друга</h2>
<p>После ухода Виктора Са на фланге чаще играет Кристиан. За его спиной остаётся пространство, которое приходится закрывать центральным защитникам. После аренды Диего Косты в ПАОК выбор там сократился. По подсчётам «РУСТАТ», у Тормены и Жубала по четыре ошибки, после которых команда пропустила.</p>
<div class="ar-tbl"><table>
  <caption>Станислав Агкацев по сезонам</caption>
  <thead><tr><th>Показатель</th><th>24/25</th><th>25/26</th><th>26/27</th></tr></thead>
  <tbody>
    <tr><td>Пропущено за матч</td><td>0,77</td><td>0,77</td><td class="bad">1,18</td></tr>
    <tr><td>Отражено ударов</td><td>78%</td><td>71%</td><td class="bad">68%</td></tr>
    <tr><td>Предотвращённые голы</td><td>+10,3</td><td>+3,9</td><td class="bad">−2,3</td></tr>
  </tbody>
</table></div>
<p>Агкацев в двух предыдущих чемпионатах пропускал в среднем по 0,77 мяча за игру. Теперь показатель вырос до 1,18. Сократилась и доля отражённых ударов, с 71% в прошлом сезоне до 68% в нынешнем.</p>
<p>Мусаеву трудно давать отдых основным игрокам. Подмена нужна сразу на двух позициях. Кривцов лечится, а Кордоба остаётся на поле даже в тех концовках, где пригодился бы свежий нападающий.</p>

<h2>Что происходит в раздевалке</h2>
<p>После кубкового поражения от «Факела» Мусаев заговорил о внутренней проблеме команды. Кривцов отдельно высказался о выборе иностранца капитаном. Публикации о возможной отставке тренера клуб не подтверждал. По сведениям «Спорт-Экспресса», раскола среди игроков нет.</p>
<p class="ar-note"><b>Мнение редакции.</b> О разногласиях со стороны судить трудно. На поле заметнее другое: после травмы Кривцова партнёрам всё сложнее доставлять мяч Кордобе.</p>

<h2>Что можно сделать до зимней паузы</h2>
<p>До зимы можно попробовать чаще сводить в центре крайнего и одного из центральных полузащитников. Тогда короткая передача к штрафной не будет зависеть от одного разыгрывающего. Воробьёв может забирать у Кордобы часть минут в концовках. Защитникам важно договориться, кто страхует фланг при подключениях.</p>
<p>Если зимой появится возможность усилить одну позицию, больше всего команде пригодился бы полузащитник с последним пасом. Кривцов тогда смог бы возвращаться в удобном для него темпе.</p>

<h2>Менять ли Мусаева</h2>
<p>За два предыдущих сезона команда Мусаева выиграла чемпионство и взяла серебро, отстав от «Зенита» на два очка. Сейчас до первого места три очка. При таком разрыве у тренера есть время попробовать другие сочетания игроков.</p>
<p>Ближайшая проверка состоится 24 октября. Против «Балтики» дома краснодарцам придётся самим вскрывать оборону и заранее думать, кому достанется подбор после потери мяча.</p>

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
    'title': '«Балтика», «Динамо» и «Родина» ждут «Краснодар» за восемь дней',
    'desc': 'У команды два матча чемпионата и кубковая встреча между ними. Начнётся отрезок дома против «Балтики», затем приедет московское «Динамо». Завершит неделю выезд к «Родине». Разобрали, как такой календарь влияет на выбор состава.',
    'tag': 'Разбор',
    'date_iso': '2026-10-20T16:00:00+03:00',
    'date_txt': '20 октября 2026',
    'read': '4 минуты',
    'body': '''
<p class="ar-lead">24 октября в Краснодар приедет «Балтика», 27-го там же сыграет московское «Динамо», а 31-го команда Мусаева встретится с «Родиной» в гостях. На три матча отведено восемь дней. Последняя победа за 90 минут осталась в августе.</p>

<p>Шесть побед, четыре ничьи и одно поражение принесли «Краснодару» 22 очка после 11 туров. Мячи 19:13. От московского «Динамо» команду отделяют три очка, от «Зенита» два.</p>

<ul class="ar-score">
  <li><span>24 окт, «Балтика»</span><b class="mono">19:30</b></li>
  <li><span>27 окт, «Динамо», Кубок</span><b class="mono">20:30</b></li>
  <li><span>31 окт, «Родина», гости</span><b class="mono">19:45</b></li>
</ul>

<h2>Ничья, которая не успокоила</h2>
<p>В Москве краснодарцы забили уже на пятой минуте. На 78-й они уступали «Локомотиву» 1:3. Оласа сократил разрыв на 86-й, Кордоба сравнял в добавленное время.</p>

<p>После ничьей Мусаев больше говорил о трёх пропущенных. Тренера беспокоит, как легко соперники добираются до ворот. С созданием моментов, по его оценке, команда справляется лучше.</p>

<p>Летом клуб расстался со Сперцяном, затем из-за травмы выбыл Кривцов. Мусаев ждёт его на тренировках в январе. Андрей Тихонов в разговоре с Metaratings связал спад с тем, насколько трудно заменить сразу двух игроков, отвечавших за созидание.</p>

<h2>Три соперника, три разных вопроса</h2>
<p><b>«Балтика»</b> занимает седьмое место с 13 очками. За 11 туров калининградцы пропустили 12 раз, а перед поездкой на юг удержали 0:0 с «Ростовом».</p>

<p>Дома против «Акрона» краснодарцы били гораздо чаще гостей (21:8) и владели мячом 69% времени, но с 13-й минуты отыгрывались. До ничьей 1:1 дело довёл Боселли лишь на 88-й.</p>

<p><b>Московское «Динамо»</b> приедет как лидер чемпионата. В первом кубковом матче 19 августа победу в Москве гостям принёс Казбек Мукаилов, забив на 44-й минуте. После ответной встречи у «Краснодара» в группе останется выезд к «Ахмату» 25 ноября.</p>

<p><b>«Родина»</b> замыкает таблицу с шестью очками. Команда пропустила уже 27 раз, но дома с «Оренбургом» напомнила, как опасно считать исход решённым: хозяева сравняли на 90-й минуте и взяли очко (2:2).</p>

<h2>Что на кону</h2>
<p>В календаре только две игры из трёх дают очки в чемпионате. Если выиграть обе, у «Краснодара» их станет 28. В кубковой встрече своя задача: улучшить положение в группе перед последним туром в Грозном.</p>

<p>Дальше, 7 ноября, в Краснодар приедет ЦСКА. Сейчас, перед серией октябрьских матчей, у соперников поровну очков.</p>

<section class="ar-src" aria-labelledby="src-h">
  <h2 id="src-h">Источники</h2>
  <ul>
    <li><a href="https://www.euro-football.ru/article/29/1006383228_musaev__o_nichey_s_lokomotivom_ne_ponravilis_legkie_golyi" target="_blank" rel="noopener">«Евро-Футбол»: Мусаев о ничьей с «Локомотивом» ↗</a></li>
    <li><a href="https://sport-express.ru/football/rfpl/news/trener-krasnodara-murad-musaev-kommentariy-o-niche-v-matche-s-lokomotivom-17-oktyabrya-2026-2464229" target="_blank" rel="noopener">«Спорт-Экспресс»: комментарий Мусаева после матча ↗</a></li>
    <li><a href="https://metaratings.ru/news/tikhonov-s-krasnodarom-chto-to-tvoritsya-neladnoe-delo-v-glubine-sostava-663602/" target="_blank" rel="noopener">Metaratings: Тихонов о «Краснодаре» ↗</a></li>
    <li><a href="https://www.sovsport.ru/football/news/trener-krasnodara-musaev-podtverdil-chto-krivczov-bolshe-ne-sygraet-v-etom-godu" target="_blank" rel="noopener">«Советский спорт»: Мусаев о Кривцове ↗</a></li>
    <li><a href="https://news.mail.ru/society/72676561/" target="_blank" rel="noopener">«Новости Mail»: Мусаев о возвращении Кривцова ↗</a></li>
    <li><a href="https://www.sport-express.ru/football/rfpl/news/rodina-orenburg-schet-i-rezultat-machta-11-tura-rpl-19-oktyabrya-2026-2464875/" target="_blank" rel="noopener">«Спорт-Экспресс»: «Родина» / «Оренбург» 2:2 ↗</a></li>
  </ul>
</section>
''',
}, {
    'slug': 'krasnodar-baltika-prevyu-matcha-12-tura.html',
    'title': 'Что важно перед домашней игрой с «Балтикой»',
    'desc': '24 октября «Краснодар» принимает калининградцев после ничьей 3:3 в Москве. Дома команде предстоит самой искать пространство для Кордобы. В отдельном разборе собрали результаты соперников и кадровые новости перед туром.',
    'tag': 'Матч',
    'date_iso': '2026-10-22T10:30:00+03:00',
    'date_txt': '22 октября 2026',
    'read': '3 минуты',
    'body': '''
<p class="ar-lead">24 октября «Балтика» приедет на «Ozon Арену» после двух ничьих 0:0 подряд. «Краснодар» ждёт первой с августа победы в основное время. Начало в 19:30 по Москве.</p>

<p>Перед 12-м туром хозяева занимают пятое место с 22 очками, гости седьмое с 13. В прошлом сезоне в Калининграде команды обменялись ранними голами (1:1), а в Краснодаре хозяева спаслись в добавленное время (2:2).</p>

<h2>Дома труднее, чем в гостях</h2>
<p>На выезде у «Краснодара» три победы и три ничьи, мячи 11:7. Дома команда тоже выиграла трижды, но были и ничья с «Акроном» (1:1), и поражение от «Зенита» (2:3). В пяти домашних играх краснодарцы забили восемь голов и пропустили шесть.</p>
<p>Против «Акрона» хозяева довели владение до 69% и нанесли 21 удар. Гости ответили восемью. При перевесе 1,40 против 0,33 по ожидаемым голам краснодарцы сумели сравнять только в концовке.</p>

<h2>Что за соперник</h2>
<p>У команды Андрея Талалаева три победы за 11 туров, мячи 14:12. В лиге калининградцы подряд сыграли 0:0 с «Ахматом» на выезде и с «Ростовом» дома. Между этими встречами забили два безответных мяча «Крыльям Советов» в Кубке.</p>

<ul class="ar-score">
  <li><span>«Зенит», дома</span><b class="mono">2:3</b></li>
  <li><span>«Ахмат», гости</span><b class="mono">0:0</b></li>
  <li><span>«Крылья Советов», Кубок</span><b class="mono">2:0</b></li>
  <li><span>«Ростов», дома</span><b class="mono">0:0</b></li>
</ul>

<p>У Брайана Хиля четыре гола в чемпионате по данным «Спорт Mail». Год назад ему понадобились всего две минуты, чтобы ответить на гол Сперцяна в Калининграде. В апреле отличился уже защитник хозяев: Жубал сравнял на второй добавленной минуте, когда «Балтика» вела 2:1.</p>
<p>К выезду в Краснодар клуб подходит на фоне сообщений о возможном уходе спортивного директора Армена Маргаряна. На поле у команды Талалаева при этом три сухих матча подряд с учётом Кубка.</p>

<h2>Что у Быков</h2>
<p>Мусаев рассчитывает на возвращение Кривцова к тренировкам в январе. До тех пор он пробует другие варианты в центре. Есть вопросы и к игре у своих ворот: «Зенит» и «Локомотив» в двух последних матчах РПЛ забили по три мяча.</p>
<p>Когда краснодарцы в последний раз сыграли на ноль в лиге, в воротах соперника гола тоже не случилось. Это было 17 сентября в Оренбурге. После московских 3:3 Мусаев отдельно отметил ошибки, которые позволили железнодорожникам слишком легко забить.</p>
<p>Главным судьёй назначен Андрей Прокопов, за видеоповторы отвечает Павел Шадыханов. После «Балтики» хозяева примут «Динамо» в Кубке 27 октября и отправятся на выезд к «Родине» 31-го.</p>

<section class="ar-src" aria-labelledby="src-h">
  <h2 id="src-h">Источники</h2>
  <ul>
    <li><a href="https://www.sport-express.net/football/rfpl/news/sudi-matchey-12-tura-rpl-derbi-cska-spartak-sudit-levnikov-arbitry-igr-chempionata-rossii-23-25-oktyabrya-2026-2465861/" target="_blank" rel="noopener">«Спорт-Экспресс»: судьи матчей 12-го тура РПЛ ↗</a></li>
    <li><a href="https://www.sports.ru/football/match/baltika-vs-krasnodar/" target="_blank" rel="noopener">Sports.ru: «Краснодар» / «Балтика», страница матча ↗</a></li>
    <li><a href="https://sportmail.ru/team/703/statistics" target="_blank" rel="noopener">«Спорт Mail»: «Балтика», статистика и новости ↗</a></li>
    <li><a href="https://sportmail.ru/football-rus-premier/377/match/420400/" target="_blank" rel="noopener">«Спорт Mail»: «Балтика» / «Краснодар» 1:1, 9 ноября 2025 ↗</a></li>
    <li><a href="https://sportmail.ru/football-rus-premier/377/match/420477/" target="_blank" rel="noopener">«Спорт Mail»: «Краснодар» / «Балтика» 2:2, 19 апреля 2026 ↗</a></li>
    <li><a href="https://sportmail.ru/football-rus-premier/398/match/444314/" target="_blank" rel="noopener">«Спорт Mail»: «Балтика» / «Зенит» 2:3 ↗</a></li>
    <li><a href="https://www.sovsport.ru/football/news/trener-krasnodara-musaev-rasskazal-o-sostoyanii-travmirovannyh-futbolistov" target="_blank" rel="noopener">«Советский спорт»: Мусаев о травмированных ↗</a></li>
    <li><a href="https://www.euro-football.ru/article/29/1006383228_musaev__o_nichey_s_lokomotivom_ne_ponravilis_legkie_golyi" target="_blank" rel="noopener">«Евро-Футбол»: Мусаев о ничьей с «Локомотивом» ↗</a></li>
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
_ar_style = SRC[SRC.index('<style>'):style_end].replace('</style>', NP_CSS + ASIDE_CSS + AR_CSS + '</style>')
for _a in ARTICLES:
    _og = make_og(_a['slug'], _a['title'], _a['tag'], _a['date_txt'])
    _ld = _ja.dumps({'@context': 'https://schema.org', '@type': 'NewsArticle', 'headline': _a['title'][:110],
                     'description': _a['desc'], 'datePublished': _a['date_iso'], 'dateModified': _a['date_iso'],
                     'inLanguage': 'ru', 'mainEntityOfPage': 'https://bikinews.ru/' + _a['slug'],
                     'image': ['https://bikinews.ru/' + _og],
                     'author': {'@type': 'Organization', 'name': 'Быки News', 'url': 'https://bikinews.ru/'},
                     'publisher': {'@type': 'Organization', 'name': 'Быки News', 'url': 'https://bikinews.ru/'},
                     'about': 'ФК «Краснодар»'}, ensure_ascii=False)
    _main = f'''<main class="wrap na" id="top">
  <nav class="na-crumbs" aria-label="Навигация"><a href="./">Главная</a><span>›</span><a href="news.html">Новости ФК «Краснодар»</a></nav>
  <div class="na-grid"><div class="na-main">
  <article class="na-art ar-art">
    <div class="na-meta"><span class="tag">{_ae(_a["tag"])}</span><time datetime="{_a["date_iso"]}">{_ae(_a["date_txt"])}</time><span>· {_ae(_a["read"])} чтения</span></div>
    <h1>{_ae(_a["title"])}</h1>
    {_a["body"]}
  </article>
  <p><a class="na-all" href="news.html">Все новости «Краснодара» →</a></p>
  </div>{aside_html()}</div>
</main>
'''
    _page = (head(_ae(_a['title']) + ' | Быки News', _ae(_a['desc']), _a['slug'], _og)
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
