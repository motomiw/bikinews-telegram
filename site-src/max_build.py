# Служебная страница max.html: свежие пересказы в виде готовых постов для канала в MAX
# (абзацы и ссылки-слова сохраняются при копировании). Не индексируется. Выполняется из build.py.
import html as _hm
_e = lambda s: _hm.escape(str(s), quote=True)
_MSK_MON = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
import datetime as _dtm
def _when(it):
    d = _dtm.datetime.fromtimestamp(it['ts'], _dtm.timezone(_dtm.timedelta(hours=3)))
    return f'{d.day} {_MSK_MON[d.month - 1]}' + ('' if it.get('notime') else f', {d:%H:%M}')

_cards = []
for it in items[:25]:
    body = (f'<p><b>⚽ {_e(it["title"])}</b></p>' + ''.join(f'<p>{_e(p)}</p>' for p in it['paras'])
            + f'<p>👉 <a href="https://bikinews.ru/{it["page"]}">' + ('Читать статью полностью' if it.get('article') else 'Подробнее на сайте') + '</a><br>'
            + ('' if it.get('article') else f'📰 Источник: <a href="{_e(it["url"])}">{_e(it["source"])}</a><br>')
            + '📲 <a href="https://bikinews.ru/news.html">Все новости Быки News</a></p>')
    _cards.append(f'<article class="mp"><div class="mp-top"><span>{_when(it)} · {_e(it["tag"])}</span>'
                  f'<button type="button" class="cp">Скопировать пост</button></div><div class="post">{body}</div></article>')

max_page = ('<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Посты для MAX — Быки News</title>\n<style>\n'
 ':root { --bg: #F2F5F1; --card: #FFFFFF; --ink: #111915; --muted: #56645B; --line: #D5DCD4; --accent: #1D6A42; --btn: #0F3B25; --on-btn: #FFFFFF; }\n'
 '@media (prefers-color-scheme: dark) { :root { --bg: #0C120F; --card: #131B17; --ink: #E6ECE7; --muted: #93A399; --line: #24312A; --accent: #55B983; --btn: #E3AE1C; --on-btn: #1A1405; color-scheme: dark; } }\n'
 'body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }\n'
 '.wrap { max-width: 680px; margin: 0 auto; padding: 24px 16px 48px; display: grid; gap: 16px; }\n'
 'h1 { font-size: 22px; margin: 0; } .hint { color: var(--muted); font-size: 14px; margin: 0; }\n'
 '.mp { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; display: grid; gap: 10px; }\n'
 '.mp-top { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; color: var(--muted); font-size: 13px; }\n'
 '.post p { margin: 0 0 10px; } .post p:last-child { margin: 0; } .post a { color: var(--accent); }\n'
 '.cp { font: 700 14px system-ui, sans-serif; background: var(--btn); color: var(--on-btn); border: 0; border-radius: 999px; padding: 8px 14px; cursor: pointer; }\n'
 '.cp.done { opacity: .75; }\n</style>\n</head>\n<body>\n<main class="wrap">\n'
 '<h1>Посты для MAX</h1>\n<p class="hint">Свежие пересказы с сайта, новые сверху. Нажмите «Скопировать пост» и вставьте в MAX — абзацы и ссылки сохранятся. '
 'Если кнопка не сработает, выделите текст поста мышкой и нажмите Ctrl+C.</p>\n'
 + '\n'.join(_cards) +
 '\n</main>\n<script>\n'
 'document.querySelectorAll(".cp").forEach(function (b) { b.addEventListener("click", function () {\n'
 '  var el = b.closest(".mp").querySelector(".post");\n'
 '  function sel() { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }\n'
 '  function fallback() { sel(); var ok = false; try { ok = document.execCommand("copy"); } catch (e) {} b.textContent = ok ? "Скопировано" : "Выделено — Ctrl+C"; b.classList.add("done"); }\n'
 '  try { if (window.ClipboardItem && navigator.clipboard && navigator.clipboard.write) {\n'
 '    navigator.clipboard.write([new ClipboardItem({ "text/html": new Blob([el.innerHTML], { type: "text/html" }), "text/plain": new Blob([el.innerText], { type: "text/plain" }) })])\n'
 '      .then(function () { b.textContent = "Скопировано"; b.classList.add("done"); }, fallback); return; } } catch (e) {}\n'
 '  fallback();\n}); });\n</script>\n</body>\n</html>\n')
(OUT / 'max.html').write_text(max_page, encoding='utf-8')
print('max', len(_cards))
