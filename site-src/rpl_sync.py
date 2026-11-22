#!/usr/bin/env python3
"""Безопасное обновление таблицы РПЛ и результатов «Краснодара».

Данные берутся из публичной страницы турнира Sports.ru. Если страница изменилась,
не загрузилась или в ней не нашлись все 16 клубов, файл сайта не меняется.
"""
from __future__ import annotations

import ast
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "bykinews.html"
MATCHES = ROOT / "matches_build.py"
STATE = ROOT / "rpl-sync.json"
SOURCE_URL = "https://www.sports.ru/football/tournament/rfpl/"
SOURCE_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; BikiNewsRPLUpdater/1.1; +https://bikinews.ru/)"}

TEAM_ALIASES = {
    "Зенит": "zenit", "Динамо": "dynamo", "Динамо Москва": "dynamo",
    "Спартак": "spartak", "Краснодар": "krasnodar", "ЦСКА": "cska",
    "Ростов": "rostov", "Рубин": "rubin", "Балтика": "baltika",
    "Крылья Советов": "krylia", "Ахмат": "akhmat", "Оренбург": "orenburg",
    "Динамо Махачкала": "dynamo-mkh", "Динамо Мх": "dynamo-mkh",
    "Родина": "rodina", "Родина Москва": "rodina", "Акрон": "akron",
    "Локомотив": "lokomotiv", "Факел": "fakel",
}
EXPECTED_TEAMS = set(TEAM_ALIASES.values())
SPORTS_MATCH_SLUGS = {
    "dynamo-mkh": "dinamo-mx", "krylia": "krylia-sovetov", "rodina": "rodina-moscow",
}
MONTH_SHORT = ("янв", "фев", "мар", "апр", "мая", "июн", "июл", "авг", "сен", "окт", "ноя", "дек")
WEEKDAY = ("пн", "вт", "ср", "чт", "пт", "сб", "вс")


def clean(value: str) -> str:
    return " ".join(html.unescape(value).replace("\xa0", " ").split())


class StandingsParser(HTMLParser):
    """Достаёт строки именно из турнирной таблицы, не полагаясь на CSS-классы."""
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.depth = 0
        self.in_cell = False
        self.cell = []
        self.row = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and "Турнирная таблица Премьер-лига Россия" in attrs.get("title", ""):
            self.in_table, self.depth = True, 1
            return
        if not self.in_table:
            return
        if tag == "table":
            self.depth += 1
        elif tag == "tr":
            self.row = []
        elif tag == "td":
            self.in_cell, self.cell = True, []

    def handle_data(self, data):
        if self.in_cell:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if not self.in_table:
            return
        if tag == "td" and self.in_cell:
            self.row.append(clean("".join(self.cell)))
            self.in_cell = False
        elif tag == "tr" and self.row:
            self.rows.append(self.row)
            self.row = []
        elif tag == "table":
            self.depth -= 1
            if not self.depth:
                self.in_table = False


def team_slug(value: str) -> str | None:
    value = clean(value)
    if value in TEAM_ALIASES:
        return TEAM_ALIASES[value]
    for name, slug in TEAM_ALIASES.items():
        if name in value:
            return slug
    return None


def parse_standings(page: str) -> list[list]:
    parser = StandingsParser()
    parser.feed(page)
    out = []
    for row in parser.rows:
        slug = next((team_slug(cell) for cell in row if team_slug(cell)), None)
        if not slug:
            continue
        # В полной таблице у некоторых клубов сайт показывает рядом отдельный
        # счёт последнего матча («1 - 0»). Это не столбец таблицы.
        cells = [cell for cell in row if not (len(row) > 9 and re.fullmatch(r"\d+\s*[−–—-]\s*\d+", cell))]
        numbers = [int(n) for cell in cells for n in re.findall(r"(?<!\d)\d+(?!\d)", cell)]
        scores = next((re.findall(r"(\d+)\s*[−–—-]\s*(\d+)", cell) for cell in cells if re.search(r"\d+\s*[−–—-]\s*\d+", cell)), [])
        if len(numbers) < 8:
            continue
        # Обычно: место, команда, И, В, Н, П, разница, О. Берём первые 5 и последнее число.
        games, wins, draws, losses = numbers[1:5]
        # В полной таблице мячи — отдельные колонки; в компактной — одна «33−18».
        gf, ga = map(int, scores[-1]) if scores else (numbers[5], numbers[6])
        points = numbers[-1]
        out.append([slug, games, wins, draws, losses, gf, ga, points])
    unique = {row[0] for row in out}
    if len(out) != 16 or unique != EXPECTED_TEAMS:
        raise ValueError("не удалось подтвердить все 16 клубов РПЛ")
    for _, games, wins, draws, losses, gf, ga, points in out:
        if not (0 <= games <= 30 and wins + draws + losses == games and gf >= 0 and ga >= 0 and points == wins * 3 + draws):
            raise ValueError("в таблице найдены некорректные показатели")
    return out


def parse_completed_matches(page: str) -> dict[tuple[str, str, str], tuple[int, int]]:
    """Возвращает {(дата, хозяева, гости): (голы хозяев, гостей)} только с финальным статусом."""
    time_re = re.compile(
        r'<time[^>]+datetime="(?P<dt>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}[^\"]*)"[^>]+title="Время проведения матча (?P<home>[^\"]+?) - (?P<away>[^\":]+):',
        re.S)
    score_re = re.compile(
        r'<div(?=[^>]*data-testid="actual-matches-widget-score")(?=[^>]*aria-label="Счёт:\s*(?P<h>\d+)\s*—\s*(?P<a>\d+)")[^>]*>',
        re.S)
    results = {}
    for score in score_re.finditer(page):
        before = page[max(0, score.start() - 12000):score.start()]
        times = list(time_re.finditer(before))
        # Статус находится в шапке карточки, до счёта; между ними бывают
        # логотипы и составы, поэтому оставляем достаточное окно одной карточки.
        if not times or "Завершен" not in before[-12000:]:
            continue
        match = times[-1]
        home, away = team_slug(match.group("home")), team_slug(match.group("away"))
        if home and away:
            results[(match.group("dt")[:10], home, away)] = (int(score.group("h")), int(score.group("a")))
    return results


def sports_match_slug(slug: str) -> str:
    """Slug клуба в URL протокола Sports.ru."""
    return SPORTS_MATCH_SLUGS.get(slug, slug)


def match_protocol_url(home: str, away: str) -> str:
    return "https://www.sports.ru/football/match/{}-vs-{}/".format(
        sports_match_slug(home), sports_match_slug(away))


def _text(fragment: str) -> str:
    return clean(re.sub(r"<[^>]+>", " ", fragment))


def parse_match_protocol(page: str, krasnodar_home: bool) -> list[tuple[str, str, str, str]]:
    """Достаёт авторов и ассистентов из протокола матча Sports.ru.

    Возвращает кортежи в формате, который использует страница матчей: минута,
    игрок, команда (k/o), ассистент. Некорректный или неполный протокол не
    считается ошибкой синхронизации — счёт и таблица от него не зависят.
    """
    goal_re = re.compile(
        r"<li(?P<attrs>[^>]*\bgoal-wrapper\b[^>]*)>(?P<body>.*?)</li>", re.S)
    goals = []
    for item in goal_re.finditer(page):
        attrs, body = item.group("attrs"), item.group("body")
        is_home = "goal-wrapper--home" in attrs
        is_away = "goal-wrapper--away" in attrs
        minute = re.search(r"goal-time[^>]*>(?P<value>.*?)</", body, re.S)
        scorer = re.search(r"goal-scorer[^>]*>.*?<a[^>]*>(?P<value>.*?)</a>", body, re.S)
        assist = re.search(r"goal-assists__link[^>]*>(?P<value>.*?)</a>", body, re.S)
        if not (minute and scorer and (is_home or is_away)):
            continue
        value = _text(minute.group("value")).replace("'", "").replace("’", "")
        name = _text(scorer.group("value"))
        if not value or not name:
            continue
        side = "k" if is_home == krasnodar_home else "o"
        goals.append((value, name, side, _text(assist.group("value")) if assist else ""))
    return goals


def load_schedule() -> list[tuple]:
    tree = ast.parse(MATCHES.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "UPCOMING" for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError("в matches_build.py не найден календарь UPCOMING")


def update_master(source: str, table: list[list], completed: list[dict]) -> str:
    table_text = "  var table = [\n" + ",\n".join("    " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in table) + "\n  ];"
    source, count = re.subn(r"  var table = \[\n.*?\n  \];", table_text, source, count=1, flags=re.S)
    if count != 1:
        raise ValueError("в главной не найдена таблица РПЛ")
    source = re.sub(r"  // РПЛ,.*?\n  var table", "  // РПЛ: автоматически проверяется после завершения матчей.\n  var table", source, count=1)

    upcoming_re = re.compile(r"(  var upcoming = \[\n)(.*?)(\n  \];)", re.S)
    played_re = re.compile(r"(  var played = \[\n)(.*?)(\n  \];)", re.S)

    def date_label(value: str) -> tuple[str, str]:
        day = datetime.strptime(value, "%Y-%m-%d").date()
        return f"{day.day} {MONTH_SHORT[day.month - 1]}", WEEKDAY[day.weekday()]

    done_keys = {(m["d"], m["opp"], m["home"]) for m in completed}
    upcoming = upcoming_re.search(source)
    played = played_re.search(source)
    if not upcoming or not played:
        raise ValueError("в главной не найдены списки матчей")

    kept_upcoming = []
    for line in upcoming.group(2).splitlines():
        if any(f"'{date_label(m['d'])[0]}'" in line and f"'{m['opp']}'" in line and str(m["home"]).lower() in line for m in completed):
            continue
        kept_upcoming.append(line)
    source = source[:upcoming.start(2)] + "\n".join(kept_upcoming) + source[upcoming.end(2):]

    # Индекс нужно найти заново: после правки его координаты изменились.
    played = played_re.search(source)
    fresh = []
    current = played.group(2)
    for m in sorted(completed, key=lambda x: x["d"], reverse=True):
        label, _ = date_label(m["d"])
        marker = f"['{label}', 'РПЛ · {m['rnd']}', '{m['opp']}', {str(m['home']).lower()}, {m['gf']}, {m['ga']}]"
        if marker not in current:
            fresh.append("    " + marker + ",")
    if fresh:
        source = source[:played.start(2)] + "\n".join(fresh) + "\n" + source[played.start(2):]
    return source


def fetch_url(url: str) -> str:
    request = urllib.request.Request(url, headers=SOURCE_HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status != 200:
            raise ValueError(f"источник вернул HTTP {response.status}")
        return response.read().decode("utf-8", errors="replace")


def fetch_page() -> str:
    return fetch_url(SOURCE_URL)


def run(page: str | None = None) -> bool:
    page = page if page is not None else fetch_page()
    table = parse_standings(page)
    source_results = parse_completed_matches(page)
    schedule = load_schedule()
    old_state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"matches": []}
    results = {(m["d"], m["opp"], m["home"]): m for m in old_state.get("matches", [])}
    for d, time, comp, rnd, opp, home in schedule:
        if comp != "РПЛ":
            continue
        host, guest = ("krasnodar", opp) if home else (opp, "krasnodar")
        score = source_results.get((d, host, guest))
        if score:
            gf, ga = score if home else score[::-1]
            old = results.get((d, opp, home), {})
            item = {**old, "d": d, "t": time, "rnd": rnd, "opp": opp, "home": home, "gf": gf, "ga": ga}
            # Счёт уже подтверждён таблицей матчей. Протокол добавляем только
            # если он сходится со счётом: иначе сайт не получит выдуманные голы.
            if not item.get("goals"):
                try:
                    protocol_url = match_protocol_url(host, guest)
                    goals = parse_match_protocol(fetch_url(protocol_url), home)
                    if len(goals) == gf + ga:
                        item["goals"] = goals
                        item["protocol_source"] = protocol_url
                except (OSError, ValueError, urllib.error.URLError):
                    pass
            results[(d, opp, home)] = item
    completed = sorted(results.values(), key=lambda x: x["d"])
    original = MASTER.read_text(encoding="utf-8")
    updated = update_master(original, table, completed)
    changed = updated != original
    if changed:
        MASTER.write_text(updated, encoding="utf-8")
    state = {"source": SOURCE_URL, "matches": completed}
    state_text = json.dumps(state, ensure_ascii=False, indent=2) + "\n"
    if not STATE.exists() or STATE.read_text(encoding="utf-8") != state_text:
        STATE.write_text(state_text, encoding="utf-8")
        changed = True
    return changed


if __name__ == "__main__":
    try:
        print("РПЛ обновлена." if run() else "Новых данных РПЛ нет.")
    except Exception as exc:
        print(f"РПЛ не обновлена: {exc}", file=sys.stderr)
        sys.exit(1)
