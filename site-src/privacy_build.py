# Страница «Политика конфиденциальности», уведомление о cookie и подключение аналитики.
# Выполняется из build.py после сборки остальных страниц: доступны head, nav_header, footer, SRC, style_end, OUT.

# ===== НАСТРОЙКИ (заполнить, когда появятся коды) =====
GA_ID = ''            # Google Analytics 4, вид 'G-XXXXXXXXXX'; пусто — аналитика не подключается
GOOGLE_VERIFY = ''    # Google Search Console: значение content из <meta name="google-site-verification" ...>
YANDEX_VERIFY = ''    # Яндекс.Вебмастер: значение content из <meta name="yandex-verification" ...>
POLICY_DATE = '12 октября 2026 г.'

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

privacy_main = f'''<main class="wrap doc" id="top">
  <h1>Политика конфиденциальности</h1>
  <p class="upd">Редакция от {POLICY_DATE}</p>

  <h2>1. О чём этот документ</h2>
  <p>Здесь описано, какие сведения о посетителях получает сайт bikinews.ru («Быки News», далее — сайт), зачем они нужны и как ими распоряжаются. Сайт — неофициальный фан-проект болельщиков ФК «Краснодар». Обработку организует администратор сайта, связаться с ним можно по адресу <a href="mailto:i@bikinews.ru">i@bikinews.ru</a>.</p>
  <p>Документ применяется ко всем страницам на домене bikinews.ru. На сайты, куда ведут наши ссылки (спортивные издания, сайт клуба, Telegram, MAX), он не распространяется — у них свои правила.</p>

  <h2>2. Какие сведения мы получаем</h2>
  <p>На сайте нет регистрации, комментариев и форм, поэтому имя, телефон или другие анкетные данные мы не запрашиваем. Автоматически, как и любой сайт, мы получаем технические сведения:</p>
  <ul>
    <li>файлы cookie и обезличенный идентификатор браузера;</li>
    <li>IP-адрес и примерное местоположение (страна, город), которое по нему определяется;</li>
    <li>тип устройства, операционную систему, браузер, язык и размер экрана;</li>
    <li>какие страницы открывались, сколько времени на них провели, откуда был переход (поисковик, Telegram, другой сайт), дату и время визита.</li>
  </ul>
  <p>Если вы пишете нам на почту, мы получаем ваш адрес электронной почты и всё, что вы сами указали в письме.</p>

  <h2>3. Зачем это нужно</h2>
  <ul>
    <li>понимать, сколько людей читает сайт, какие новости и разделы им интересны и с каких устройств заходят;</li>
    <li>находить ошибки и делать сайт удобнее и быстрее;</li>
    <li>обеспечивать работу сайта и защищать его от злоупотреблений;</li>
    <li>отвечать на письма.</li>
  </ul>
  <p>Мы не показываем персонализированную рекламу, не продаём и не передаём сведения о посетителях для рекламы и не пытаемся установить личность читателей.</p>

  <h2>4. Cookie и сервисы веб-аналитики</h2>
  <p>Cookie — небольшие файлы, которые сайт сохраняет в браузере, чтобы узнавать повторные визиты. Мы используем:</p>
  <ul>
    <li><b>Google Analytics</b> (Google LLC) — статистика посещаемости. Сведения обрабатываются на серверах Google, которые могут находиться за пределами России. Как Google обращается с данными, описано на странице <a href="https://policies.google.com/privacy?hl=ru" target="_blank" rel="noopener">policies.google.com/privacy</a>.</li>
    <li><b>Яндекс.Метрика</b> (ООО «Яндекс») — статистика посещаемости, если сервис подключён. Правила Яндекса — на странице <a href="https://yandex.ru/legal/confidential/" target="_blank" rel="noopener">yandex.ru/legal/confidential</a>.</li>
    <li><b>Хранилище браузера</b> — сайт запоминает, что вы закрыли уведомление о cookie, чтобы не показывать его снова. Эта отметка остаётся на вашем устройстве и нам не передаётся.</li>
  </ul>
  <p>Кроме того, хостинг-провайдер сайта ведёт стандартные журналы сервера (IP-адрес, время запроса, адрес страницы, браузер) — без них сайт не может работать.</p>

  <h2>5. Ваше согласие и как отказаться</h2>
  <p>При первом визите сайт показывает уведомление о cookie. Продолжая пользоваться сайтом, вы соглашаетесь на обработку описанных выше сведений в указанных целях. Если вы не согласны, вы можете:</p>
  <ul>
    <li>запретить или удалить cookie в настройках браузера — сайт продолжит работать;</li>
    <li>установить официальное дополнение Google для отключения аналитики: <a href="https://tools.google.com/dlpage/gaoptout?hl=ru" target="_blank" rel="noopener">tools.google.com/dlpage/gaoptout</a>;</li>
    <li>пользоваться режимом инкогнито или блокировщиком счётчиков;</li>
    <li>отозвать согласие, написав на <a href="mailto:i@bikinews.ru">i@bikinews.ru</a>, либо просто покинуть сайт.</li>
  </ul>

  <h2>6. Кому передаются сведения</h2>
  <p>Только сервисам, без которых сайт не работает или не может считать статистику: хостинг-провайдеру и сервисам аналитики из раздела 4. Другим лицам сведения передаются лишь в случаях, прямо предусмотренных законом Российской Федерации.</p>

  <h2>7. Сколько хранятся сведения и как защищены</h2>
  <p>Статистика хранится в сервисах аналитики не дольше 14 месяцев, после чего удаляется автоматически. Журналы сервера хранятся столько, сколько предусмотрено у хостинг-провайдера. Переписка хранится, пока это нужно для ответа на обращение, и удаляется по вашей просьбе. Доступ к статистике и почте есть только у администратора сайта, вход в эти сервисы защищён паролем.</p>

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

# ---------- уведомление о cookie + счётчики: на все страницы ----------
COOKIE_HTML = r'''
<div class="ckb" id="ckb" role="region" aria-label="Уведомление о cookie" hidden>
  <p>Мы используем cookie и сервисы веб-аналитики, чтобы понимать, что читают на сайте. Продолжая пользоваться сайтом, вы соглашаетесь с этим. <a href="privacy.html">Подробнее</a></p>
  <button type="button" id="ckbOk">Понятно</button>
</div>
<style>
.ckb { position: fixed; left: 16px; right: 16px; bottom: 16px; z-index: 50; max-width: 640px; margin-inline: auto;
  display: flex; align-items: center; gap: 12px 16px; padding: 14px 16px; border-radius: 14px;
  background: var(--surface); color: var(--ink); border: 1px solid var(--line); box-shadow: 0 8px 28px rgba(0,0,0,.18); font-size: 14px; line-height: 1.45; }
.ckb p { margin: 0; flex: 1; }
.ckb a { color: var(--accent); }
.ckb button { flex: none; font: inherit; font-weight: 700; padding: 9px 16px; border-radius: 10px; border: 0; cursor: pointer;
  background: var(--accent); color: #fff; }
@media (max-width: 520px) { .ckb { flex-direction: column; align-items: stretch; left: 12px; right: 12px; bottom: 12px; } }
</style>
<script>
(function () {
  var K = 'bn_cookie_ok', box = document.getElementById('ckb');
  var ok = false;
  try { ok = localStorage.getItem(K) === '1'; } catch (e) {}
  if (!ok) box.hidden = false;
  document.getElementById('ckbOk').addEventListener('click', function () {
    box.hidden = true;
    try { localStorage.setItem(K, '1'); } catch (e) {}
  });
})();
</script>
'''

head_extra = ''
if GOOGLE_VERIFY:
    head_extra += f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">\n'
if YANDEX_VERIFY:
    head_extra += f'<meta name="yandex-verification" content="{YANDEX_VERIFY}">\n'
if GA_ID:
    head_extra += (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
                   '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
                   f"gtag('js',new Date());gtag('config','{GA_ID}');</script>\n")

for _page in ['index.html', 'news.html', 'matches.html', 'privacy.html']:
    _p = OUT / _page
    _h = _p.read_text(encoding='utf-8')
    if head_extra:
        _h = _h.replace('</head>', head_extra + '</head>', 1)
    _i = _h.rindex('</body>')
    _h = _h[:_i] + COOKIE_HTML + _h[_i:]
    _p.write_text(_h, encoding='utf-8')
print('privacy', len(privacy), 'GA', GA_ID or '—', 'verify', 'G' if GOOGLE_VERIFY else '-', 'Y' if YANDEX_VERIFY else '-')
