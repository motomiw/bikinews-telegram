#!/usr/bin/env python3
"""Прогон приложения на эмуляторе: открывает вкладки и делает скриншоты (для проверки и карточки RuStore)."""
import os, re, subprocess, sys, time

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
PKG = 'ru.bikinews.app'
log = open(os.path.join(OUT, 'log.txt'), 'w')


def sh(*a, check=False):
    r = subprocess.run(['adb', 'shell', *a], capture_output=True, text=True)
    log.write('$ ' + ' '.join(a) + '\n' + r.stdout[-2000:] + r.stderr[-2000:] + '\n')
    return r.stdout


def shot(name, wait=4):
    time.sleep(wait)
    with open(os.path.join(OUT, name + '.png'), 'wb') as f:
        f.write(subprocess.run(['adb', 'exec-out', 'screencap', '-p'], capture_output=True).stdout)
    print('shot', name, flush=True)


def nodes():
    sh('uiautomator', 'dump', '/sdcard/u.xml')
    x = subprocess.run(['adb', 'exec-out', 'cat', '/sdcard/u.xml'], capture_output=True, text=True).stdout
    return x


def tap_node(attr, value, xml=None):
    xml = xml or nodes()
    ms = re.findall(r'<node[^>]*' + attr + r'="' + re.escape(value) + r'"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
    m = ms[-1] if ms else None   # последний — верхний слой (меню, диалог)
    if not m:
        print('not found', attr, value, flush=True)
        log.write('NOT FOUND ' + value + '\n')
        return False
    x1, y1, x2, y2 = map(int, m)
    sh('input', 'tap', str((x1 + x2) // 2), str((y1 + y2) // 2))
    return True


def tab(label, xml=None):
    """Кнопка нижней панели приложения (не одноимённая ссылка на странице)."""
    xml = xml or nodes()
    m = re.search(r'<node[^>]*class="android.widget.LinearLayout"[^>]*content-desc="' + re.escape(label) + r'"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', xml)
    if not m:
        print('tab not found', label, flush=True); log.write('TAB NOT FOUND ' + label + '\n'); return False
    x1, y1, x2, y2 = map(int, m.groups())
    sh('input', 'tap', str((x1 + x2) // 2), str((y1 + y2) // 2))
    return True


sh('settings', 'put', 'global', 'window_animation_scale', '0')
sh('settings', 'put', 'global', 'transition_animation_scale', '0')
sh('pm', 'set-app-links-user-selection', '--user', '0', '--package', PKG, 'true', 'all')
sh('cmd', 'uimode', 'night', 'no')
sh('pm', 'grant', PKG, 'android.permission.POST_NOTIFICATIONS')   # без системного окна с вопросом на первом кадре
sh('am', 'start', '-W', '-n', PKG + '/.MainActivity')
time.sleep(10)
# уведомление о cookie: ищем кнопку «Понятно», иначе жмём по её обычному месту
for _ in range(6):
    xml = nodes()
    if tap_node('text', 'Отказаться', xml) or tap_node('text', 'Понятно', xml):
        break
    time.sleep(3)
time.sleep(6)
shot('01-home', 3)
sh('input', 'swipe', '540', '1600', '540', '500', '400')
shot('02-home-feed', 2)
tab('Новости'); shot('03-news', 6)
tab('Матчи'); shot('04-matches', 6)
tab('Таблица'); shot('05-table', 7)
tab('Ещё'); shot('06-more-menu', 2)
tap_node('text', 'Состав'); shot('07-squad', 7)
tab('Ещё'); time.sleep(1); tap_node('text', 'О приложении'); shot('08-about', 2)
sh('input', 'keyevent', 'KEYCODE_BACK')
tab('Главная'); time.sleep(5)
sh('cmd', 'uimode', 'night', 'yes'); shot('09-home-dark', 8)
tab('Матчи'); shot('10-matches-dark', 6)
sh('cmd', 'uimode', 'night', 'no'); time.sleep(3)
# без сети
sh('svc', 'wifi', 'disable'); sh('svc', 'data', 'disable'); time.sleep(3)
tab('Новости'); shot('11-offline-cached', 6)
sh('am', 'start', '-a', 'android.intent.action.VIEW', '-d', 'https://bikinews.ru/club.html')
shot('12-offline-new', 6)
sh('svc', 'wifi', 'enable'); sh('svc', 'data', 'enable'); time.sleep(5)
tap_node('text', 'Повторить'); shot('13-back-online', 7)
# ссылка из Telegram открывается в приложении
sh('am', 'start', '-a', 'android.intent.action.VIEW', '-d', 'https://bikinews.ru/squad.html')
shot('14-deeplink', 6)
sh('dumpsys', 'package', 'domain-preferred-apps')
open(os.path.join(OUT, 'domains.txt'), 'w').write(sh('pm', 'get-app-links', PKG))
subprocess.run(['adb', 'logcat', '-d', '-t', '3000'], stdout=open(os.path.join(OUT, 'logcat.txt'), 'w'))
print('done')
