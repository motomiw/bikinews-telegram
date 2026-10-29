#!/usr/bin/env python3
"""Быки News → Telegram. Запускается GitHub Actions каждые 20 минут.

Берёт новости с сайта bikinews.ru и публикует новые в канал через вашего бота:
  • наши пересказы (data/glavnoe.json) — по мере появления, не больше 3 за запуск;
  • дайджест изданий (data/news.json) — в 12:00 и 20:00 по Москве.
Токен и канал берутся из секретов репозитория TG_TOKEN и TG_CHAT.
"""
import datetime, html, json, os, sys, urllib.parse, urllib.request, urllib.error

SITE = os.environ.get('SITE_URL', 'https://bikinews.ru/')
API = os.environ.get('TG_API', 'https://api.telegram.org')
TOKEN = os.environ.get('TG_TOKEN', '').strip()
CHAT = os.environ.get('TG_CHAT', '').strip()
# RuStore Push: уведомления в приложении «Быки News». Токен — секрет репозитория RUSTORE_PUSH_TOKEN, без него пуши не отправляются.
RS_TOKEN = os.environ.get('RUSTORE_PUSH_TOKEN', '').strip()
RS_PROJECT = os.environ.get('RUSTORE_PROJECT_ID', '').strip()
RS_TOPIC = 'news'
STATE = 'state.json'
MAX_PER_RUN = 3
MSK = datetime.timezone(datetime.timedelta(hours=3))
UA = {'User-Agent': 'Mozilla/5.0 (compatible; BikinewsPoster/1.0; +https://bikinews.ru)'}


def get_json(path):
    req = urllib.request.Request(SITE + path + '?t=' + str(int(datetime.datetime.now().timestamp())), headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))


def send(text):
    data = urllib.parse.urlencode({'chat_id': CHAT, 'parse_mode': 'HTML', 'text': text,
                                   'disable_web_page_preview': 'true'}).encode()
    req = urllib.request.Request(f'{API}/bot{TOKEN}/sendMessage', data=data)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            res = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print('Ошибка Telegram: HTTP', e.code)
        return False
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        # Не выводим исключение: URL запроса содержит токен бота.
        print('Ошибка Telegram: сеть или некорректный ответ')
        return False
    if not res.get('ok'):
        print('Ошибка Telegram:', res.get('description'))
    return bool(res.get('ok'))


def esc(t):
    return html.escape(str(t or ''), quote=True)


def item_text(g):
    """Текст поста: ссылки — словами (гиперссылки), а не голым адресом."""
    lead = g['paras'][0] if g.get('paras') else ''
    if g['url'].startswith(SITE):   # своя статья Быки News — ведём прямо на неё
        return (f"<b>{esc(g['title'])}</b>\n\n" + '\n\n'.join(esc(p) for p in g.get('paras', [])) +
                f"\n\n👉 <a href=\"{esc(g['url'])}\">Читать статью полностью</a>")
    page = SITE + g['page'] if g.get('page') else f"{SITE}news.html#{urllib.parse.quote(g['id'])}"
    return (f"<b>{esc(g['title'])}</b>\n\n{esc(lead)}\n\n"
            f"👉 <a href=\"{esc(page)}\">Подробнее на сайте</a>\n"
            f"Источник: <a href=\"{esc(g['url'])}\">{esc(g['source'])}</a>")


def push(g):
    """Пуш в приложение через RuStore (тема «news»). Любая ошибка только пишется в журнал: Telegram от неё не страдает."""
    if not RS_TOKEN or not RS_PROJECT:
        print('::notice::RuStore Push не отправлен: в секретах репозитория нет RUSTORE_PUSH_TOKEN')
        return
    lead = (g['paras'][0] if g.get('paras') else '').strip()
    if len(lead) > 220:
        lead = lead[:220].rsplit(' ', 1)[0].rstrip(',;:—- ') + '…'
    page = g.get('page') or f"news.html#{urllib.parse.quote(g['id'])}"
    body = {'providers': {'rustore': {'project_id': RS_PROJECT, 'auth_token': RS_TOKEN}},
            'topic': RS_TOPIC,
            'message': {'data': {'id': str(g['id']), 'title': str(g['title']), 'text': lead,
                                 'tag': str(g.get('tag') or ''), 'ts': str(int(g.get('ts') or 0)), 'page': page}}}
    req = urllib.request.Request('https://vkpns-universal.rustore.ru/v1/send/topic',
                                 data=json.dumps(body, ensure_ascii=False).encode('utf-8'),
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f'::notice::RuStore Push отправлен: {r.status}')
    except urllib.error.HTTPError as e:
        print('::warning::RuStore Push: ошибка', e.code, e.read()[:200].decode('utf-8', 'replace').replace('\n', ' '))
    except Exception as e:
        print('::warning::RuStore Push: ошибка', e)


def save_state(st):
    # Замена файла целиком защищает от частично записанного JSON.
    tmp = STATE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE)


def main():
    if not TOKEN or not CHAT:
        sys.exit('Не заданы секреты TG_TOKEN и TG_CHAT')
    try:
        with open(STATE, encoding='utf-8') as f:
            st = json.load(f)
        first = False
    except FileNotFoundError:
        st, first = {'posted': [], 'digest': {}}, True

    failed = False
    if os.environ.get('TG_TEST') == 'true':
        ok = send('✅ Быки News подключены к каналу. Новости будут появляться здесь автоматически.\n\n'
                  f'<a href="{SITE}">bikinews.ru</a>')
        print('Тестовое сообщение:', 'отправлено' if ok else 'ошибка')
        return 0 if ok else 1

    gl = get_json('data/glavnoe.json').get('items', [])
    sent = 0
    if any(str(g.get('id', '')).startswith('g') for g in gl):
        print('На сайте ещё старая версия glavnoe.json — пересказы пропускаю до обновления сайта')
        gl = [] if not first else gl
    NOT_YET = ('n99917600', 'n7ec4b5e3', 'n92feea3e')   # «Факел» сменил тренера, анонс матча, цифры клуба — ещё не выходили
    if not first and st.get('v') != 3:
        ids = [g['id'] for g in gl]
        if not all(x in ids for x in NOT_YET):
            print('На сайте ещё не залит свежий glavnoe.json — жду обновления сайта')
            gl = []
        else:
            # переход на постоянные номера новостей: всё, что уже на сайте, считаем опубликованным, кроме трёх новых
            st['posted'] = [i for i in ids if i not in NOT_YET]; st['v'] = 3
            print('Обновление формата: отмечено как опубликованное —', len(st['posted']))
    elif first:
        st['v'] = 3
    if first:
        st['posted'] = [g['id'] for g in gl]
        print('Первый запуск: отмечено как уже опубликованное —', len(gl))
    else:
        new = sorted([g for g in gl if g['id'] not in st['posted']], key=lambda g: g['ts'])
        for g in new[:MAX_PER_RUN]:
            text = item_text(g)
            if not send(text):
                failed = True
                break
            st['posted'].append(g['id']); sent += 1
            save_state(st)
            push(g)
        print('Опубликовано пересказов:', sent)

    now = datetime.datetime.now(MSK)
    if now.hour in (12, 20):
        slot = now.strftime('%Y-%m-%d-') + str(now.hour)
        if not st['digest'].get(slot):
            since = now.timestamp() - 12 * 3600
            try:
                items = [i for i in get_json('data/news.json').get('items', []) if i['ts'] >= since][:7]
            except Exception as e:
                print('Лента изданий недоступна'); items = []; failed = True
            if items:
                lines = [f"▪️ <a href=\"{esc(i['url'])}\">{esc(i['title'])}</a> <i>— {esc(i['source'])}</i>" for i in items]
                text = (f"<b>📰 Что пишут о «Краснодаре» · {now:%d.%m}, {'день' if now.hour == 12 else 'вечер'}</b>\n\n"
                        + '\n\n'.join(lines) + f"\n\n📲 <a href=\"{SITE}news.html\">Все новости со ссылками</a>")
                ok = send(text)
                print('Дайджест:', 'опубликован' if ok else 'ошибка')
                if ok:
                    st['digest'][slot] = 1
                    save_state(st)
                else:
                    failed = True

    st['posted'] = st['posted'][-500:]
    st['digest'] = dict(list(st['digest'].items())[-20:])
    save_state(st)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
