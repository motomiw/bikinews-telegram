# Страница «Политика конфиденциальности», уведомление о cookie и подключение аналитики.
# Выполняется из build.py после сборки остальных страниц: доступны head, nav_header, footer, SRC, style_end, OUT.

# ===== НАСТРОЙКИ (заполнить, когда появятся коды) =====
YM_ID = '113747465'              # номер счётчика Яндекс.Метрики. Пусто — аналитики и баннера cookie на сайте нет.
                        # Google Analytics отключён 23.10.2026 (передача данных в США); счётчик включается только после согласия
GOOGLE_VERIFY = ''    # Google Search Console: значение content из <meta name="google-site-verification" ...>
YANDEX_VERIFY = '0f3fa5f2f3f50b3c'    # Яндекс.Вебмастер: значение content из <meta name="yandex-verification" ...>
POLICY_DATE = '23 октября 2026 г.'

PRIVACY_CSS = r'''
/* политика конфиденциальности */
.nav a[aria-current="page"] { background: var(--turf-2); }
.doc { display: block; padding-block: 28px 48px; max-width: 760px; }
.doc h1 { font-family: var(--font-display); font-weight: 800; font-size: clamp(26px, 4.5vw, 40px); letter-spacing: -.01em; line-height: 1.12; margin: 0 0 8px; }
.doc .upd { color: var(--muted); font-size: 14px; margin: 0 0 24px; }
.doc h2 { font-family: var(--font-display); font-weight: 700; font-size: 19px; margin: 32px 0 10px; }
.doc p, .doc li { line-height: 1.6; }
.doc p { margin: 0 0 12px; }
.doc ul { margin: 0 0 12px; padding-left: 22px; }
.doc li { margin-bottom: 6px; }
.doc a { color: var(--accent); }
'''

if YM_ID:
    S45 = '''  <h2>4. Cookie и сервисы веб-аналитики</h2>
  <p>Cookie — небольшие файлы, которые сайт сохраняет в браузере, чтобы узнавать повторные визиты. Мы используем:</p>
  <ul>
    <li><b>Яндекс.Метрика</b> (ООО «Яндекс») — статистика посещаемости. Счётчик включается только после того, как вы нажали «Согласен» в уведомлении о cookie; если нажали «Отказаться» или не ответили, он не загружается и ничего не передаёт. Правила Яндекса — на странице <a href="https://yandex.ru/legal/confidential/" target="_blank" rel="noopener">yandex.ru/legal/confidential</a>.</li>
    <li><b>Хранилище браузера</b> — сайт запоминает ваш выбор в уведомлении о cookie и настройки отображения (например, режим для слабовидящих). Эти отметки остаются на вашем устройстве и нам не передаются.</li>
  </ul>
  <p>Кроме того, хостинг-провайдер сайта ведёт стандартные журналы сервера (IP-адрес, время запроса, адрес страницы, браузер) — без них сайт не может работать.</p>

  <h2>5. Ваше согласие и как отказаться</h2>
  <p>При первом визите сайт показывает уведомление о cookie с двумя кнопками. Аналитика включается только после вашего согласия. Передумать можно в любой момент:</p>
  <ul>
    <li><a href="#" data-ck-reset>изменить выбор</a> — уведомление появится снова;</li>
    <li>запретить или удалить cookie в настройках браузера — сайт продолжит работать;</li>
    <li>пользоваться режимом инкогнито или блокировщиком счётчиков;</li>
    <li>отозвать согласие, написав на <a href="mailto:i@bikinews.ru">i@bikinews.ru</a>, либо просто покинуть сайт.</li>
  </ul>
'''
else:
    S45 = '''  <h2>4. Cookie и сервисы веб-аналитики</h2>
  <p>Сейчас на сайте не подключены сервисы веб-аналитики и рекламные счётчики, а сторонние скрипты не загружаются. Сайт сохраняет в браузере только ваши настройки отображения (например, режим для слабовидящих) — они остаются на устройстве и нам не передаются.</p>
  <p>Хостинг-провайдер сайта ведёт стандартные журналы сервера (IP-адрес, время запроса, адрес страницы, браузер) — без них сайт не может работать.</p>
  <p>Если мы подключим сервис аналитики, он будет включаться только после вашего согласия, а этот раздел будет обновлён.</p>

  <h2>5. Ваше согласие и как отказаться</h2>
  <p>Согласие на cookie и аналитику не требуется, пока они не используются. Если вы не согласны с обработкой технических сведений, описанных выше, вы можете запретить или удалить cookie в настройках браузера, пользоваться режимом инкогнито либо отозвать согласие, написав на <a href="mailto:i@bikinews.ru">i@bikinews.ru</a>.</p>
'''

privacy_main = f'''<main class="wrap doc" id="top">
  <h1>Политика конфиденциальности</h1>
  <p class="upd">Редакция от {POLICY_DATE}</p>

  <h2>1. О чём этот документ</h2>
  <p>Здесь описано, какие сведения о посетителях получает сайт bikinews.ru («Быки News», далее — сайт), зачем они нужны и как ими распоряжаются. Сайт — неофициальный фан-проект болельщиков ФК «Краснодар». Оператор — физическое лицо, администратор сайта Морозов Геннадий Евгеньевич; связаться с ним можно по адресу <a href="mailto:i@bikinews.ru">i@bikinews.ru</a>.</p>
  <p>Документ применяется ко всем страницам на домене bikinews.ru и к приложению «Быки News» для Android (далее — приложение). На сайты, куда ведут наши ссылки (спортивные издания, сайт клуба, Telegram, MAX), он не распространяется — у них свои правила.</p>

  <h2>2. Какие сведения мы получаем</h2>
  <p>На сайте нет регистрации, комментариев и форм, поэтому имя, телефон или другие анкетные данные мы не запрашиваем. Автоматически, как и любой сайт, мы получаем технические сведения:</p>
  <ul>
    <li>файлы cookie и обезличенный идентификатор браузера;</li>
    <li>IP-адрес и примерное местоположение (страна, город), которое по нему определяется;</li>
    <li>тип устройства, операционную систему, браузер, язык и размер экрана;</li>
    <li>какие страницы открывались, сколько времени на них провели, откуда был переход (поисковик, Telegram, другой сайт), дату и время визита.</li>
  </ul>
  <p>Если вы пишете нам на почту, мы получаем ваш адрес электронной почты и всё, что вы сами указали в письме.</p>

  <p><b>Приложение для Android</b> показывает страницы этого же сайта, поэтому в нём действует всё, что описано в этом документе. Само приложение не требует регистрации и просит только доступ в интернет: оно не обращается к контактам, местоположению, камере, микрофону и файлам на телефоне. Открытые страницы и настройки (например, версия для слабовидящих) сохраняются в памяти приложения, чтобы их можно было читать без сети; они удаляются вместе с приложением или при очистке его данных в настройках телефона. Ссылки на другие сайты, Telegram и MAX приложение открывает в браузере или в соответствующих приложениях.</p>

  <h2>3. Зачем это нужно</h2>
  <ul>
    <li>понимать, сколько людей читает сайт, какие новости и разделы им интересны и с каких устройств заходят;</li>
    <li>находить ошибки и делать сайт удобнее и быстрее;</li>
    <li>обеспечивать работу сайта и защищать его от злоупотреблений;</li>
    <li>отвечать на письма.</li>
  </ul>
  <p>Мы не показываем персонализированную рекламу, не продаём и не передаём сведения о посетителях для рекламы и не пытаемся установить личность читателей.</p>

{S45}
  <h2>6. Кому передаются сведения</h2>
  <p>Только сервисам, без которых сайт не работает или не может считать статистику: хостинг-провайдеру и сервисам аналитики из раздела 4. Другим лицам сведения передаются лишь в случаях, прямо предусмотренных законом Российской Федерации.</p>

  <h2>7. Сколько хранятся сведения и как защищены</h2>
  <p>Статистика хранится в сервисах аналитики не дольше 14 месяцев, после чего удаляется автоматически. Журналы сервера хранятся столько, сколько предусмотрено у хостинг-провайдера. Переписка хранится, пока это нужно для ответа на обращение, и удаляется по вашей просьбе. Доступ к статистике и почте есть только у оператора, вход в эти сервисы защищён паролем.</p>

  <h2>8. Ваши права</h2>
  <p>Вы вправе узнать, какие сведения о вас обрабатываются, потребовать уточнить или удалить их и отозвать согласие. Запрос отправляйте на <a href="mailto:i@bikinews.ru">i@bikinews.ru</a> — ответим в течение 10 рабочих дней. Если вы считаете, что ваши права нарушены, вы можете обратиться в Роскомнадзор или в суд.</p>

  <h2>9. Изменения</h2>
  <p>Политика может обновляться, например при подключении новых сервисов. Актуальная редакция всегда доступна на этой странице, дата последних изменений указана в начале.</p>
</main>
'''

privacy = (head('Политика конфиденциальности — Быки News',
                'Какие данные получает сайт Быки News, как используются cookie и сервисы аналитики и как от них отказаться.',
                'privacy.html')
           + '<title>Политика конфиденциальности — Быки News</title>\n'
           + SRC[SRC.index('<style>'):style_end].replace('</style>', PRIVACY_CSS + '</style>')
           + '\n</head>\n<body>\n' + nav_header('privacy') + '\n\n' + privacy_main + '\n' + footer + '\n</body>\n</html>\n')
(OUT / 'privacy.html').write_text(privacy, encoding='utf-8')

# ---------- уведомление о cookie + счётчик Метрики (только после согласия) ----------
COOKIE_HTML = r"""
<div class="ckb" id="ckb" role="region" aria-label="Уведомление о cookie" hidden>
  <p>Мы считаем посещаемость сервисом Яндекс.Метрика (он использует cookie) — только с вашего согласия. <a href="privacy.html">Подробнее</a></p>
  <span class="ckb-btns"><button type="button" id="ckbOk">Согласен</button><button type="button" id="ckbNo" class="ghost">Отказаться</button></span>
</div>
<style>
.ckb { position: fixed; left: 16px; right: 16px; bottom: 16px; z-index: 50; max-width: 680px; margin-inline: auto;
  display: flex; align-items: center; gap: 12px 16px; padding: 14px 16px; border-radius: 14px;
  background: var(--surface); color: var(--ink); border: 1px solid var(--line); box-shadow: 0 8px 28px rgba(0,0,0,.18); font-size: 14px; line-height: 1.45; }
.ckb p { margin: 0; flex: 1; }
.ckb a { color: var(--accent); }
.ckb-btns { display: flex; gap: 8px; flex: none; }
.ckb button { flex: none; font: inherit; font-weight: 700; padding: 9px 16px; border-radius: 10px; border: 2px solid var(--accent); cursor: pointer;
  background: var(--accent); color: #fff; }
.ckb button.ghost { background: transparent; color: var(--accent); }
@media (max-width: 520px) { .ckb { left: 8px; right: 8px; bottom: 8px; padding: 10px 12px; font-size: 13px; gap: 10px; border-radius: 12px; flex-wrap: wrap; } .ckb-btns { width: 100%; } .ckb button { flex: 1; padding: 9px 14px; } }
</style>
<script>
(function () {
  var K = 'bn_consent', ID = __YM__, box = document.getElementById('ckb');
  function get() { try { return localStorage.getItem(K); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(K, v); } catch (e) {} }
  function start() {   // Метрика грузится только здесь — после явного согласия
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date();
      k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })
      (window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    window.ym(ID, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true });
  }
  var v = get();
  if (v === 'yes') start(); else if (v !== 'no') box.hidden = false;
  document.getElementById('ckbOk').addEventListener('click', function () { box.hidden = true; set('yes'); start(); });
  document.getElementById('ckbNo').addEventListener('click', function () { box.hidden = true; set('no'); });
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('[data-ck-reset]');
    if (a) { ev.preventDefault(); try { localStorage.removeItem(K); } catch (e) {} box.hidden = false; }
  });
})();
</script>
"""

head_extra = ''
if GOOGLE_VERIFY:
    head_extra += f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">\n'
if YANDEX_VERIFY:
    head_extra += f'<meta name="yandex-verification" content="{YANDEX_VERIFY}">\n'

for _page in ['index.html', 'news.html', 'matches.html', 'squad.html', 'club.html', 'privacy.html'] + [it['page'] for it in items]:
    _p = OUT / _page
    _h = _p.read_text(encoding='utf-8')
    if head_extra:
        _h = _h.replace('</head>', head_extra + '</head>', 1)
    if YM_ID:
        _i = _h.rindex('</body>')
        _h = _h[:_i] + COOKIE_HTML.replace('__YM__', str(int(YM_ID))) + _h[_i:]
    _p.write_text(_h, encoding='utf-8')
print('privacy', len(privacy), 'Метрика', YM_ID or '— (аналитики нет)', 'verify', 'G' if GOOGLE_VERIFY else '-', 'Y' if YANDEX_VERIFY else '-')
