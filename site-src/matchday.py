"""Match-day feed. All times are Moscow time, scores are home first."""
import ast
import json
import re
from datetime import datetime, timedelta, timezone

import rpl_sync as rpl

MSK = timezone(timedelta(hours=3))
FILE = rpl.ROOT / 'matchday.json'
PLAYER_URL = 'https://www.sports.ru/football/club/krasnodar/stat/2026-2027/{}/?tid={}'
TOURNAMENTS = {'РПЛ': (1363803, 31), 'Кубок': (1363804, 42)}


def read_state():
    return json.loads(FILE.read_text(encoding='utf8')) if FILE.exists() else {}


def history():
    tree = ast.parse(rpl.MATCHES.read_text(encoding='utf8'))
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id == 'PLAYED')
    return [{arg.arg: ast.literal_eval(arg.value) for arg in row.keywords} for row in node.value.elts]


def plain(s):
    return rpl.clean(re.sub('<[^>]+>', '', s))


def players(page):
    result = {}
    for table in re.findall(r'<table\b[^>]*>(.*?)</table>', page, re.S):
        rows = [[plain(c) for c in re.findall(r'<td\b[^>]*>(.*?)</td>', row, re.S)]
                for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>', table, re.S)]
        if not rows or 'Игрок' not in rows[0]:
            continue
        for row in rows[1:]:
            if len(row) != len(rows[0]):
                continue
            values = dict(zip(rows[0], row))
            if values['М'].isdigit() and values['Игрок']:
                result[values['Игрок']] = [int(values.get(k, '0')) for k in ('М', 'Мин', 'Г', 'П', 'ЖК', 'КК')]
    if len(result) < 11:
        raise ValueError('неполная таблица игроков')
    return result


def protocol(page, fixture):
    d, _, comp, _, opp, home = fixture
    events = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)]
    event = next((x for x in events if isinstance(x, dict) and x.get('@type') == 'SportsEvent'), {})
    teams = [rpl.team_slug(event.get(k, {}).get('name', '')) for k in ('homeTeam', 'awayTeam')]
    if (event.get('startDate', '')[:10] != d or teams != (['krasnodar', opp] if home else [opp, 'krasnodar'])
            or ('Кубок' if comp == 'Кубок' else 'Премьер-лига') not in event.get('description', '')):
        raise ValueError('источник показывает другую встречу')
    status = re.search(r'data-testid="match-status"[^>]*>(.*?)</div>', page, re.S)
    label = plain(status[1]).lower() if status else ''
    scores = [plain(v) for v in re.findall(r'\bmatchboard-score"[^>]*>(.*?)</div>', page, re.S)[:2]]
    final = label.startswith(('заверш', 'окончен'))
    live = re.search(r'тайм|перерыв|пенальти|\d+\s*[\'′’]|^\d+(?:\+\d+)?$', label)
    scored = len(scores) == 2 and all(v.isdigit() for v in scores)
    return event, ('final' if final else 'live') if scored and (final or live) else 'scheduled', list(map(int, scores)) if scored else []


def advance(record, stage, score, now):
    if record.get('stage') == 'final' and stage != 'final':
        return
    if stage == 'scheduled' and record.get('stage') == 'live':
        return
    record['stage'] = stage
    if stage in ('live', 'final'):
        record['score'] = score
    if stage == 'final':
        record.setdefault('final_seen', int(now.timestamp()))
        if now.timestamp() >= record['final_seen'] + 900:
            record.setdefault('report', int(now.timestamp()))


def final_rows(state):
    for m in state.get('matches', {}).values():
        if m.get('stage') == 'final':
            gf, ga = m['score'] if m['home'] else m['score'][::-1]
            yield dict(m, gf=gf, ga=ga, stats={}, goals=m.get('goals', []))


def preview_text(record, state):
    previous = sorted((m for m in history() + list(final_rows(state)) if m['d'] < record['d']), key=lambda m: m['d'])
    recent = previous[-5:]
    start = datetime.fromisoformat(record['start'])
    lines = [f"{start.day} {rpl.MONTH_SHORT[start.month-1]} в {record['t']} МСК сыграют {' и '.join(record['teams'])}. {record['comp']}, {record['rnd']}."]
    if recent:
        lines.append(f"За последние {len(recent)} официальных матчей «Краснодар» забил {sum(m['gf'] for m in recent)} и пропустил {sum(m['ga'] for m in recent)}.")
    last = next((m for m in reversed(previous) if m['opp'] == record['opp']), None)
    if last:
        lines.append(f"Предыдущая встреча этих команд в сезоне закончилась со счётом {last['gf']}:{last['ga']} с точки зрения «Краснодара»." +
                     (f" Быки выиграли серию пенальти {last['pens']}." if last.get('pens') else ''))
    return lines


def sync():
    now = datetime.now(MSK)
    state = read_state()
    errors = []
    try:
        state['table'] = rpl.parse_standings(rpl.fetch_page())
    except Exception as exc:
        errors.append(str(exc))
    records = state.setdefault('matches', {})
    known = {m['d'] for m in history()}
    for fixture in rpl.load_schedule():
        d, t, comp, rnd, opp, home = fixture
        delta = (datetime.fromisoformat(d).date() - now.date()).days
        if d in known or delta > 2 or (delta < -3 and (d not in records or records[d].get('report'))):
            continue
        host, away = ('krasnodar', opp) if home else (opp, 'krasnodar')
        url = records.get(d, {}).get('url') or rpl.match_protocol_url(host, away)
        try:
            page = rpl.fetch_url(url)
            event, stage, score = protocol(page, fixture)
            permanent = re.search(r'tagId:(\d+),isLive:', page)
            if permanent:
                url = f'https://www.sports.ru/football/match/{permanent[1]}/'
            start = datetime.fromisoformat(event['startDate']).astimezone(MSK)
            record = records.setdefault(d, {})
            record.update(d=d, t=start.strftime('%H:%M'), opp=opp, home=home, rnd=rnd, comp=comp, url=url,
                          teams=[event[k]['name'] for k in ('homeTeam','awayTeam')], start=start.isoformat())
            if timedelta(0) < start-now <= timedelta(days=1) and stage == 'scheduled':
                record.setdefault('preview', int(now.timestamp()))
                record.setdefault('preview_text', preview_text(record, state))
            advance(record, stage, score, now)
            if stage == 'final':
                goals = rpl.parse_match_protocol(page, home)
                gf, ga = score if home else score[::-1]
                if sum(g[2]=='k' for g in goals)==gf and sum(g[2]=='o' for g in goals)==ga:
                    record['goals'] = goals
        except Exception as exc:
            errors.append(f'{d} {opp}: {exc}')
    for comp, ids in TOURNAMENTS.items():
        try:
            state.setdefault('players', {})[comp] = players(rpl.fetch_url(PLAYER_URL.format(*ids)))
        except Exception as exc:
            errors.append(f'{comp}: {exc}')
    print('\n'.join('::warning::' + e for e in errors))
    output = json.dumps(state, ensure_ascii=False, indent=1) + '\n'
    if not FILE.exists() or FILE.read_text(encoding='utf8') != output:
        FILE.write_text(output, encoding='utf8')
    if errors and len(errors) >= 3 and not records:
        raise RuntimeError('Источники матчей недоступны')


if __name__ == '__main__':
    sync()
