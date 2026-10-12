#!/usr/bin/env python3
"""Быки News → Telegram. Запускается GitHub Actions каждые 20 минут.

Берёт новости с сайта bikinews.ru и публикует новые в канал через вашего бота:
  • наши пересказы (data/glavnoe.json) — по мере появления, не больше 3 за запуск;
  • дайджест изданий (data/news.json) — в 12:00 и 20:00 по Москве.
Токен и канал берутся из секретов репозитория TG_TOKEN и TG_CHAT.
"""
import datetime, html, json, os, sys, urllib.parse, urllib.request

SITE = os.environ.get('SITE_URL', 'https://bikinews.ru/')
API = os.environ.get('TG_API', 'https://api.telegram.org')
TOKEN = os.environ.get('TG_TOKEN', '').strip()
CHAT = os.environ.get('TG_CHAT', '').strip()
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
        res = json.loads(e.read().decode('utf-8') or '{}')
    if not res.get('ok'):
        print('Ошибка Telegram:', res.get('description'))
    return bool(res.get('ok'))


def esc(t):
    return html.escape(str(t or ''), quote=True)


def main():
    if not TOKEN or not CHAT:
        sys.exit('Не заданы секреты TG_TOKEN и TG_CHAT')
    try:
        st = json.load(open(STATE, encoding='utf-8'))
        first = False
    except (FileNotFoundError, ValueError):
        st, first = {'posted': [], 'digest': {}}, True

    if os.environ.get('TG_TEST') == 'true':
        ok = send('✅ Быки News подключены к каналу. Новости будут появляться здесь автоматически.\n\n'
                  f'<a href="{SITE}">bikinews.ru</a>')
        print('Тестовое сообщение:', 'отправлено' if ok else 'ошибка')

    gl = get_json('data/glavnoe.json').get('items', [])
    sent = 0
    if any(str(g.get('id', '')).startswith('g') for g in gl):
        print('На сайте ещё старая версия glavnoe.json — пересказы пропускаю до обновления сайта')
        gl = [] if not first else gl
    if not first and st.get('v') != 2:
        # переход на постоянные номера новостей: всё, что уже на сайте, считаем опубликованным
        st['posted'] = [g['id'] for g in gl if g['id'] not in ('n96ac17bf',)]; st['v'] = 2   # новость про «Факел» ещё не выходила
        print('Обновление формата: отмечено как опубликованное —', len(gl))
    elif first:
        st['v'] = 2
    if first:
        st['posted'] = [g['id'] for g in gl]
        print('Первый запуск: отмечено как уже опубликованное —', len(gl))
    else:
        new = sorted([g for g in gl if g['id'] not in st['posted']], key=lambda g: g['ts'])
        for g in new[:MAX_PER_RUN]:
            lead = g['paras'][0] if g.get('paras') else ''
            text = (f"<b>{esc(g['title'])}</b>\n\n{esc(lead)}\n\n"
                    f"👉 Подробнее: {SITE}news.html#{urllib.parse.quote(g['id'])}\n"
                    f"Источник: <a href=\"{esc(g['url'])}\">{esc(g['source'])}</a>")
            if not send(text):
                break
            st['posted'].append(g['id']); sent += 1
        print('Опубликовано пересказов:', sent)

    now = datetime.datetime.now(MSK)
    if now.hour in (12, 20):
        slot = now.strftime('%Y-%m-%d-') + str(now.hour)
        if not st['digest'].get(slot):
            since = now.timestamp() - 12 * 3600
            try:
                items = [i for i in get_json('data/news.json').get('items', []) if i['ts'] >= since][:7]
            except Exception as e:
                print('Лента изданий недоступна:', e); items = []
            if items:
                lines = [f"▪️ <a href=\"{esc(i['url'])}\">{esc(i['title'])}</a> <i>— {esc(i['source'])}</i>" for i in items]
                text = (f"<b>📰 Что пишут о «Краснодаре» · {now:%d.%m}, {'день' if now.hour == 12 else 'вечер'}</b>\n\n"
                        + '\n\n'.join(lines) + f"\n\n📲 Все новости со ссылками: {SITE}news.html")
                print('Дайджест:', 'опубликован' if send(text) else 'ошибка')
            st['digest'][slot] = 1

    st['posted'] = st['posted'][-500:]
    st['digest'] = dict(list(st['digest'].items())[-20:])
    json.dump(st, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
