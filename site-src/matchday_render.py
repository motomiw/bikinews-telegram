import html
import json
import re
from datetime import datetime

import matchday as md
import rpl_sync as rpl


def date_label(d):
    value = datetime.fromisoformat(d)
    return f'{value.day} {rpl.MONTH_SHORT[value.month-1]}'


def js_array(src, name, rows):
    # JSON strings placed inside an HTML script element.
    data = json.dumps(rows, ensure_ascii=False).replace('<', r'\u003c')
    return re.sub(r'var '+name+r' = \[.*?\];', lambda _: f'var {name} = {data};', src, count=1, flags=re.S)


def render(src, state):
    records = state.get('matches', {})
    done = {m['d']: m for m in md.history() + list(md.final_rows(state))}
    future = [f for f in rpl.load_schedule() if f[0] not in done]
    if state.get('table'):
        src = js_array(src, 'table', state['table'])
    league = state.get('players', {}).get('РПЛ', {})
    if league:
        leaders = sorted(league.items(), key=lambda v: (-v[1][2], v[1][0], v[0]))
        src = js_array(src, 'scorers', [[n, v[2], v[0]] for n,v in leaders[:5]])
    src = js_array(src, 'played', [[date_label(m['d']), m['comp']+' · '+m['rnd'], m['opp'], m['home'], m['gf'], m['ga']]
                                    for m in sorted(done.values(), key=lambda v:v['d'], reverse=True)])
    src = js_array(src, 'upcoming', [[date_label(d), rpl.WEEKDAY[datetime.fromisoformat(d).weekday()], comp+' · '+rnd, opp, home, records.get(d, {}).get('t', t)]
                                      for d,t,comp,rnd,opp,home in future[:3]])
    if future:
        d,t,comp,rnd,opp,home = future[0]
        m = records.get(d, {})
        live = m.get('stage') == 'live'
        names = {v:k for k,v in reversed(list(rpl.TEAM_ALIASES.items()))}
        sides = ('krasnodar',opp) if home else (opp,'krasnodar')
        def badge(slug):
            return f'<div><span class="club big" data-logo="{slug}"></span><div class="name">{html.escape(names[slug])}</div></div>'
        center = ':'.join(map(str,m['score'])) if live else m.get('t',t) or 'Уточняется'
        label = 'Матч идёт' if live else 'Ближайший матч'
        countdown = ('<span>Текущий счёт</span>' if live else '<span id="cdwrap">до матча <b id="cd"></b></span>')
        body = (f'<div class="match-top"><span class="eyebrow" id="match-title">{label}</span><span>{comp} · {rnd}</span></div>'
                f'<div class="teams">{badge(sides[0])}<div class="kick mono">{center}<small>{date_label(d)}</small></div>{badge(sides[1])}</div>'
                f'<div class="countdown"><span>{"Дома" if home else "В гостях"} · время московское</span>{countdown}</div>')
        src = re.sub(r'(<aside class="match"[^>]*>).*?(<a class="allnews calink")', lambda x:x[1]+body+x[2], src, count=1, flags=re.S)
    else:
        src = re.sub(r'<aside class="match".*?</aside>', '', src, count=1, flags=re.S)
    if done:
        last = done[max(done)]
        teams = last.get('teams')
        if teams:
            footer = f'<div class="last"><span class="lastl">Прошлый матч · {last["comp"]}</span><a href="matches.html#m-{last["d"]}">{html.escape(" — ".join(teams))} · {":".join(map(str,last["score"]))}</a></div>'
            src = re.sub(r'<div class="last">.*?</div>', lambda _:footer, src, count=1, flags=re.S)
    stories = []
    for m in records.values():
        title = ' — '.join(m['teams'])
        if m.get('preview'):
            stories.append((m['preview'], title+' · превью', m['preview_text'], m))
        if m.get('report'):
            score = ':'.join(map(str,m['score']))
            names = [f'{g[1]} ({g[0]}′)' for g in m.get('goals',[])]
            lines = [f"{m['comp']}, {m['rnd']}. {title} — {score}."]
            if names:
                lines.append('Голы: '+', '.join(names)+'.')
            article = m.get('article', {})
            stories.append((m['report'], article.get('title', title+' · '+score), article.get('paragraphs', lines), m))
    for ts,title,lines,m in sorted(stories, key=lambda s:s[0]):
        dt = datetime.fromtimestamp(ts, md.MSK)
        paragraphs = ''.join('<p>'+html.escape(s)+'</p>' for s in lines)
        source, url = ('Sports.ru', m['url'])
        if ts == m.get('report') and m.get('article'):
            source, url = m['article']['source'], m['article']['url']
        entry = (f'<li><article><time class="mono" datetime="{dt.isoformat()}">{date_label(dt.date().isoformat())} · {dt:%H:%M}</time>'
                 f'<div class="nb"><span class="tag">Матч</span><h3>{html.escape(title)}</h3>{paragraphs}'
                 f'<a class="src" href="{html.escape(url)}" target="_blank" rel="noopener">Источник: {html.escape(source)} ↗</a></div></article></li>')
        start = src.index('<ul class="feed">')+len('<ul class="feed">')
        # Keep later newsroom posts above the automatic story.
        end = src.index('</ul>',start)
        feed = src[start:end]
        offset = len(feed)
        for item in re.finditer(r'<li><article>\s*<time[^>]*>(.*?)</time>',feed,re.S):
            stamp = re.search(r'(\d+)\s+([а-я]{3})(?:\D+?(\d{1,2}):(\d{2}))?',md.plain(item[1]))
            if stamp:
                day,mon,h,minute = stamp.groups()
                month = rpl.MONTH_SHORT.index(mon)+1
                when = datetime(2026 if month>=7 else 2027,month,int(day),int(h or 12),int(minute or 0),tzinfo=md.MSK)
                if when.timestamp() <= ts:
                    offset = item.start()
                    break
        src = src[:start+offset]+entry+'\n'+src[start+offset:]
    if stories:
        _,title,lines,m = max(stories,key=lambda s:s[0])
        summary = lines[0] if m.get('article') else ' '.join(lines)
        lead = f'<article class="lead"><h1>{html.escape(title)}</h1><p>{html.escape(summary)}</p><a class="read" href="matches.html#m-{m["d"]}">Календарь и статистика →</a></article>'
        src = re.sub(r'<article class="lead">.*?</article>',lambda _:lead,src,count=1,flags=re.S)
    return src
