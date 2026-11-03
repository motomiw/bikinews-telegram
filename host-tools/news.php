<?php
/**
 * Быки News — автоматическая лента новостей о ФК «Краснодар».
 * Работает на PHP 5.6 и новее.
 *
 * Скрипт забирает RSS спортивных изданий и новости с официального сайта клуба,
 * оставляет только материалы о «Краснодаре», убирает дубли и пишет результат в data/news.json.
 *
 * Запуск:
 *   из cron:     php /путь/к/сайту/news.php
 *   по ссылке:   http://bikinews.ru/news.php?key=СЕКРЕТНЫЙ_КЛЮЧ
 */

date_default_timezone_set('Europe/Moscow');

// ===== НАСТРОЙКИ =====
// Секрет остаётся только на хостинге, вне публичного репозитория.
$secretConfig = dirname(__FILE__) . '/data/news-secret.php';
$secretValue = is_file($secretConfig) ? include $secretConfig : getenv('BIKINEWS_NEWS_SECRET');
define('SECRET', is_string($secretValue) ? $secretValue : '');      // ключ для запуска по ссылке
define('MAX_ITEMS', 30);            // сколько новостей хранить
define('MAX_AGE_DAYS', 7);          // новости старше — удаляются
define('SNIPPET_LEN', 240);         // длина анонса, символов
define('OUT_FILE', dirname(__FILE__) . '/data/news.json');
define('ARCHIVE_FILE', dirname(__FILE__) . '/data/archive.json'); // все новости для страницы «Новости», не очищается
define('ARCHIVE_MAX', 3000);       // предел записей в архиве (≈ год-полтора)

// Источники: [название, адрес, тип]. Тип 'rss' — лента RSS,
// 'html' — страница сайта клуба (RSS у него нет, берём ссылки на новости со страницы)
$FEEDS = array(
    array('Чемпионат',      'https://www.championat.com/rss/news/football/', 'rss'),
    array('Спорт-Экспресс', 'https://www.sport-express.ru/services/materials/news/football/se/', 'rss'),
    array('Евро-Футбол',    'https://www.euro-football.ru/rss/', 'rss'),
    array('Сила спорта',   'https://silasporta.ru/feed/', 'rss'),
    array('Sport.ru',       'https://www.sport.ru/rssfeeds/football.rss', 'rss'),
    array('РБК Спорт',      'https://rssexport.rbc.ru/sport/news/30/base.rss', 'rss'),
    array('Sports.ru',      'https://www.sports.ru/rss/topnews/football.xml', 'rss'),
    array('Soccer365',      'https://s.scr365.net/s1/news.xml', 'rss'),
    array('Soccer.ru',      'https://www.soccer.ru/rss.xml', 'rss'),
    array('Rusfootball',    'https://www.rusfootball.info/rss.xml', 'rss'),
    array('ФК «Краснодар»', 'https://fckrasnodar.ru/', 'html'),
);
// С официального сайта не берём рекламные записи
$OFFICIAL_SKIP = array('подарочный сертификат', 'магазин', 'скидк', 'промокод');
define('SEEN_FILE', dirname(__FILE__) . '/data/seen-official.json');

// Новость попадает в ленту, если в заголовке или анонсе есть одно из слов...
$KEYWORDS = array('краснодар', 'мусаев', 'кордоба', 'агкацев', 'батчи', 'кривцов', 'сперцян',
                  'оздоев', 'боселли', 'жубал', 'тормена', 'пальцев', 'вахания', 'быки');
// ...и нет ни одного из этих
$EXCLUDE = array('краснодарский край', 'аэропорт краснодар', 'баскетбол', 'хоккей', 'гандбол', 'волейбол');

// Для проверки можно подменить источники локальными файлами
if (PHP_SAPI === 'cli' && getenv('BIKINEWS_FEEDS')) {
    $testFeeds = json_decode((string)getenv('BIKINEWS_FEEDS'), true);
    if (!is_array($testFeeds) || !$testFeeds) { fwrite(STDERR, "Invalid test feeds\n"); exit(1); }
    $FEEDS = $testFeeds;
}

// ===== ДОСТУП =====
$isCli = (PHP_SAPI === 'cli');
$key = isset($_POST['key']) ? (string)$_POST['key'] : (isset($_GET['key']) ? (string)$_GET['key'] : '');
if (!$isCli && (SECRET === '' || !hash_equals(SECRET, $key))) {
    header('HTTP/1.1 403 Forbidden');
    exit('Forbidden');
}
if (!$isCli) {
    header('Content-Type: text/plain; charset=utf-8');
    header('X-Accel-Buffering: no');   // nginx: не копить ответ, отдавать сразу
    ini_set('display_errors', '1');     // при запуске по ссылке покажем ошибки, если будут
    error_reporting(E_ALL & ~E_DEPRECATED);
}
@set_time_limit(120);

// Проверка нужных расширений PHP
$missing = array();
foreach (array('dom', 'mbstring', 'json') as $ext) { if (!extension_loaded($ext)) { $missing[] = $ext; } }
if ($missing) { exit('Нет расширений PHP: ' . implode(', ', $missing) . '. Включите их в панели хостинга.'); }

// ===== ФУНКЦИИ =====
define('LOG_FILE', dirname(__FILE__) . '/data/last-run.txt');
define('T_START', microtime(true));
define('TIME_BUDGET', 40);          // секунд на все загрузки, чтобы хостинг не оборвал скрипт
if (!is_dir(dirname(LOG_FILE))) { @mkdir(dirname(LOG_FILE), 0755, true); }
$runLock = @fopen(dirname(LOG_FILE) . '/news.lock', 'c');
if (!$runLock || !flock($runLock, LOCK_EX | LOCK_NB)) { exit("Сбор уже выполняется, повторный запуск пропущен.\n"); }
@file_put_contents(LOG_FILE, ''); @chmod(LOG_FILE, 0644);   // журнал пишется по ходу работы — видно, на чём остановилось
function bn_say($line) {            // печатаем сразу, чтобы в браузере было видно ход работы
    $row = date('d.m H:i:s') . sprintf(' [%4.1fс] ', microtime(true) - T_START) . $line;
    @file_put_contents(LOG_FILE, $row . "\n", FILE_APPEND);
    echo $row, "\n";
    if (function_exists('ob_get_level')) { while (ob_get_level() > 0) { @ob_end_flush(); } }
    @flush();
}
function bn_fetch($url) {
    if (is_file($url)) { return (string)file_get_contents($url); }
    $ua = 'Mozilla/5.0 (compatible; BikinewsBot/1.0; +http://bikinews.ru)';
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_MAXREDIRS, 3);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
        curl_setopt($ch, CURLOPT_TIMEOUT, 12);
        curl_setopt($ch, CURLOPT_NOSIGNAL, 1);
        curl_setopt($ch, CURLOPT_ENCODING, '');
        curl_setopt($ch, CURLOPT_USERAGENT, $ua);
        $body = curl_exec($ch);
        $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $err = curl_error($ch);
        if (PHP_VERSION_ID < 80000) { curl_close($ch); }
        if ($body !== false && $code >= 200 && $code < 300) { return (string)$body; }
        return array('error' => $err ? $err : ('HTTP ' . $code));
    }
    $ctx = stream_context_create(array('http' => array('timeout' => 12, 'user_agent' => $ua)));
    $body = @file_get_contents($url, false, $ctx);
    return $body === false ? array('error' => 'file_get_contents не смог открыть адрес') : (string)$body;
}


// Все источники загружаются независимо. Ни один медленный сайт не блокирует остальные.
function bn_fetch_many($feeds) {
    $results = array();
    if (!function_exists('curl_multi_init')) {
        // Без curl порядок меняется между запусками, чтобы последние источники не голодали.
        $order = array_keys($feeds); $offset = ((int)floor(time() / 600)) % count($order);
        $order = array_merge(array_slice($order, $offset), array_slice($order, 0, $offset));
        foreach ($order as $i) {
            $results[$i] = microtime(true) - T_START < TIME_BUDGET - 12 ? bn_fetch($feeds[$i][1]) : array('error'=>'Общий лимит времени');
        }
        return $results;
    }
    $multi = curl_multi_init(); $handles = array();
    foreach ($feeds as $i => $feed) {
        $url = $feed[1];
        if (is_file($url)) { $results[$i] = bn_fetch($url); continue; }
        $ch = curl_init($url);
        curl_setopt_array($ch, array(CURLOPT_RETURNTRANSFER=>true, CURLOPT_FOLLOWLOCATION=>true,
            CURLOPT_MAXREDIRS=>3, CURLOPT_CONNECTTIMEOUT=>5, CURLOPT_TIMEOUT=>12,
            CURLOPT_NOSIGNAL=>1, CURLOPT_ENCODING=>'',
            CURLOPT_USERAGENT=>'Mozilla/5.0 (compatible; BikinewsBot/1.0; +https://bikinews.ru)'));
        if (defined('CURLOPT_PROTOCOLS')) { curl_setopt($ch, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS); }
        if (defined('CURLOPT_REDIR_PROTOCOLS')) { curl_setopt($ch, CURLOPT_REDIR_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS); }
        $handles[$i] = $ch; curl_multi_add_handle($multi, $ch);
    }
    $running = 0;
    do {
        do { $status = curl_multi_exec($multi, $running); } while ($status === CURLM_CALL_MULTI_PERFORM);
        if ($status !== CURLM_OK || microtime(true) - T_START >= TIME_BUDGET) { break; }
        if ($running && curl_multi_select($multi, 0.2) === -1) { usleep(10000); }
    } while ($running);
    foreach ($handles as $i => $ch) {
        $code = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $body = curl_multi_getcontent($ch); $error = curl_error($ch);
        $results[$i] = !$error && $code >= 200 && $code < 300 && is_string($body) ? $body : array('error'=>$error ? $error : 'HTTP ' . $code);
        curl_multi_remove_handle($multi, $ch);
        if (PHP_VERSION_ID < 80000) { curl_close($ch); }
    }
    curl_multi_close($multi);
    return $results;
}

function bn_write_json($path, $value) {
    $flags = JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT;
    $json = json_encode($value, $flags);
    if ($json === false) { return false; }
    $temp = $path . '.tmp';
    if (@file_put_contents($temp, $json, LOCK_EX) === false) { return false; }
    @chmod($temp, 0644);
    if (!@rename($temp, $path)) { @unlink($temp); return false; }
    return true;
}

function bn_parse($xml, &$valid = null) {
    $valid = false;
    libxml_use_internal_errors(true);
    $dom = new DOMDocument();
    $dom->recover = true;   // переживёт обрезанный или «кривой» XML
    if (!@$dom->loadXML($xml, LIBXML_NOCDATA | LIBXML_NONET)) { return array(); }
    if (!$dom->documentElement || !in_array(strtolower($dom->documentElement->localName), array('rss','rdf'))) { return array(); }
    $valid = true;
    $items = array();
    foreach ($dom->getElementsByTagName('item') as $it) {
        $row = array();
        foreach (array('title', 'link', 'description', 'pubDate') as $tag) {
            $n = $it->getElementsByTagName($tag)->item(0);
            $row[$tag] = $n ? trim($n->textContent) : '';
        }
        $items[] = $row;
    }
    return $items;
}

function bn_clean($html) {
    $t = html_entity_decode(strip_tags($html), ENT_QUOTES, 'UTF-8');
    $t = preg_replace('/\s*(Читать дальше|Читать далее|Подробнее)\s*\.*\s*$/u', '', $t);
    return trim(preg_replace('/\s+/u', ' ', (string)$t));
}

function bn_snippet($t, $len) {
    if (mb_strlen($t, 'UTF-8') <= $len) { return $t; }
    $cut = mb_substr($t, 0, $len, 'UTF-8');
    $sp = mb_strrpos($cut, ' ', 0, 'UTF-8');
    if ($sp) { $cut = mb_substr($cut, 0, $sp, 'UTF-8'); }
    return rtrim($cut, ' ,.;:—-') . '…';
}

function bn_key($title) {
    $t = mb_strtolower($title, 'UTF-8');
    $t = preg_replace('/[^\p{L}\p{N}]+/u', '', $t);
    return mb_substr((string)$t, 0, 60, 'UTF-8');
}

function bn_match($text, $yes, $no) {
    $t = mb_strtolower($text, 'UTF-8');
    foreach ($no as $w)  { if (mb_strpos($t, $w, 0, 'UTF-8') !== false) { return false; } }
    foreach ($yes as $w) { if (mb_strpos($t, $w, 0, 'UTF-8') !== false) { return true; } }
    return false;
}

// Есть ли внутри блока ссылки на другие новости (значит, это уже не карточка одной новости)
function bn_other_news($node, $id) {
    if (!($node instanceof DOMElement)) { return true; }
    foreach ($node->getElementsByTagName('a') as $x) {
        if (preg_match('~object_id=(\d+)~', $x->getAttribute('href'), $m) && $m[1] !== $id) { return true; }
    }
    return false;
}

// Страница официального сайта: ссылки вида ...?object_id=123 и дата ДД.ММ.ГГГГ рядом с ними
function bn_parse_html($html, $base) {
    libxml_use_internal_errors(true);
    $dom = new DOMDocument();
    if (!@$dom->loadHTML('<?xml encoding="UTF-8">' . $html)) { return array(); }
    $out = array();
    foreach ($dom->getElementsByTagName('a') as $a) {
        $href = trim($a->getAttribute('href'));
        if (!preg_match('~object_id=(\d+)~', $href, $m)) { continue; }
        $id = $m[1];
        $title = bn_clean($a->textContent);
        if (mb_strlen($title, 'UTF-8') < 15 && $a->getAttribute('title') !== '') { $title = bn_clean($a->getAttribute('title')); }
        // дата ищется в ближайших родительских блоках карточки новости
        $date = ''; $node = $a;
        for ($i = 0; $i < 4 && $node && $date === ''; $i++) {
            if ($i > 0 && bn_other_news($node, $id)) { break; }   // дошли до общего блока с другими новостями
            if (preg_match('~\b(\d{2})\.(\d{2})\.(20\d{2})\b~', $node->textContent, $d)) { $date = $d[3] . '-' . $d[2] . '-' . $d[1]; }
            $node = $node->parentNode;
            if ($node && $node->nodeType !== XML_ELEMENT_NODE) { break; }
        }
        if (strpos($href, '//') === 0) { $href = 'https:' . $href; }
        elseif (!preg_match('~^https?://~', $href)) { $href = rtrim($base, '/') . '/' . ltrim($href, '/'); }
        // у одной новости бывает несколько ссылок (картинка + заголовок) — оставляем самый длинный текст
        if (!isset($out[$id]) || mb_strlen($title, 'UTF-8') > mb_strlen($out[$id]['title'], 'UTF-8')) {
            $out[$id] = array('id' => $id, 'title' => $title, 'link' => $href, 'date' => $date !== '' ? $date : (isset($out[$id]) ? $out[$id]['date'] : ''));
        } elseif ($out[$id]['date'] === '' && $date !== '') { $out[$id]['date'] = $date; }
    }
    return array_values($out);
}

// сохранённая ранее новость остаётся, если она с сайта клуба или о «Краснодаре» в заголовке
function bn_keep($it) {
    global $KEYWORDS, $EXCLUDE;
    if (strpos($it['source'], 'ФК') === 0) { return true; }
    return bn_match($it['title'], $KEYWORDS, $EXCLUDE);
}

function bn_sort($a, $b) { return $b['ts'] - $a['ts']; }

// ===== СБОР =====
$old = array();
if (is_file(OUT_FILE)) {
    $prev = json_decode((string)file_get_contents(OUT_FILE), true);
    if (is_array($prev) && isset($prev['items']) && is_array($prev['items'])) { $old = $prev['items']; }
}

$found = array(); $report = array(); $successful = 0;
bn_say('Старт сбора, PHP ' . PHP_VERSION . ', запуск ' . ($isCli ? 'по расписанию' : 'по ссылке') . ', curl: ' . (function_exists('curl_init') ? 'да' : 'нет'));
$bodies = bn_fetch_many($FEEDS);
foreach ($FEEDS as $feedIndex => $feed) {
    $name = $feed[0]; $url = $feed[1];
    bn_say('Загружаю: ' . $name . ' …');
    $body = isset($bodies[$feedIndex]) ? $bodies[$feedIndex] : array('error'=>'Нет ответа');
    if (is_array($body)) { $report[] = array('source'=>$name,'ok'=>false,'error'=>$body['error']); bn_say($name . ': не удалось загрузить (' . $body['error'] . ')'); continue; }
    $n = 0;
    if (isset($feed[2]) && $feed[2] === 'html') {
        // первый запуск: всё, что уже есть на странице без даты, считаем старым
        $seenOff = is_file(SEEN_FILE) ? json_decode((string)file_get_contents(SEEN_FILE), true) : null;
        $firstRun = !is_array($seenOff);
        if ($firstRun) { $seenOff = array(); }
        $today = date('Y-m-d');
        $officialItems = bn_parse_html($body, $url);
        if (!$officialItems) { $report[] = array('source'=>$name,'ok'=>false,'error'=>'Нет карточек клуба'); bn_say($name . ': нет карточек новостей — прежние записи сохранены'); continue; }
        $successful++;
        foreach ($officialItems as $it) {
            $title = $it['title'];
            if (mb_strlen($title, 'UTF-8') < 15) { continue; }
            if (bn_match($title, $OFFICIAL_SKIP, array())) { continue; }
            if (isset($seenOff[$it['id']])) {
                $ts = (int)$seenOff[$it['id']];
            } elseif ($it['date'] !== '' && $it['date'] < $today) {
                $ts = strtotime($it['date'] . ' 12:00');
            } elseif ($firstRun && $it['date'] === '') {
                $ts = 0;                          // старая новость без даты — не показываем
            } else {
                $ts = time();                     // появилась сегодня — время первого обнаружения
            }
            $seenOff[$it['id']] = $ts;
            if (!$ts) { continue; }
            $found[] = array('title' => $title, 'text' => '', 'url' => $it['link'], 'source' => $name, 'ts' => $ts);
            $n++;
        }
        if (count($seenOff) > 500) { $seenOff = array_slice($seenOff, -300, null, true); }
        if (!bn_write_json(SEEN_FILE, $seenOff)) { bn_say('Не удалось сохранить историю клуба'); }
        $report[] = array('source'=>$name,'ok'=>true,'matched'=>$n);
        bn_say($name . ': новостей клуба на странице — ' . $n);
        continue;
    }
    $valid = false; $rssItems = bn_parse($body, $valid);
    if (!$valid) { $report[] = array('source'=>$name,'ok'=>false,'error'=>'Некорректный RSS'); bn_say($name . ': вместо RSS получена непригодная страница'); continue; }
    $successful++;
    foreach ($rssItems as $it) {
        $title = bn_clean($it['title']);
        $desc  = bn_clean($it['description']);
        $link  = trim($it['link']);
        if ($title === '' || !preg_match('~^https?://~', $link)) { continue; }
        // о «Краснодаре» должен быть сам заголовок; анонс проверяем только на слова-исключения
        if (!bn_match($title, $KEYWORDS, $EXCLUDE) || bn_match($desc, $EXCLUDE, array())) { continue; }
        $ts = strtotime($it['pubDate']);
        if (!$ts || $ts > time() + 3600) { continue; }
        $found[] = array('title' => $title, 'text' => bn_snippet($desc, SNIPPET_LEN),
                         'url' => $link, 'source' => $name, 'ts' => $ts);
        $n++;
    }
    $report[] = array('source'=>$name,'ok'=>true,'matched'=>$n);
    bn_say($name . ': найдено о «Краснодаре» — ' . $n);
}

if (!$successful) {
    bn_say('ОШИБКА: все источники недоступны. Лента и архив не изменены.');
    if (!$isCli) { http_response_code(503); }
    exit(1);
}

// новые + сохранённые ранее, без дублей, свежие сверху
$old = array_values(array_filter($old, 'bn_keep'));
$all = array_merge($found, $old);
usort($all, 'bn_sort');
$seen = array(); $items = array(); $minTs = time() - MAX_AGE_DAYS * 86400;
foreach ($all as $it) {
    $k = bn_key($it['title']);
    if (isset($seen[$k]) || isset($seen[$it['url']]) || $it['ts'] < $minTs) { continue; }
    foreach ($items as $kept) {      // почти одинаковые заголовки за 6 часов — дубль
        if (abs($kept['ts'] - $it['ts']) < 6 * 3600) {
            similar_text(bn_key($kept['title']), $k, $pct);
            if ($pct > 80) { continue 2; }
        }
    }
    $seen[$k] = true; $seen[$it['url']] = true;
    $items[] = $it;
    if (count($items) >= MAX_ITEMS) { break; }
}

// ===== АРХИВ для страницы «Новости»: копим всё, ничего не удаляем по возрасту =====
$arch = array();
if (is_file(ARCHIVE_FILE)) {
    $prevA = json_decode((string)file_get_contents(ARCHIVE_FILE), true);
    if (is_array($prevA) && isset($prevA['items']) && is_array($prevA['items'])) { $arch = $prevA['items']; }
}
$allA = array_merge($found, $old, array_values(array_filter($arch, 'bn_keep')));
usort($allA, 'bn_sort');
$seenA = array(); $archItems = array();
foreach ($allA as $it) {
    $k = bn_key($it['title']);
    if (isset($seenA[$k]) || isset($seenA[$it['url']])) { continue; }
    foreach (array_slice($archItems, -40) as $kept) {     // дубль от другого издания в пределах 6 часов
        if (abs($kept['ts'] - $it['ts']) < 6 * 3600) {
            similar_text(bn_key($kept['title']), $k, $pct);
            if ($pct > 80) { continue 2; }
        }
    }
    $seenA[$k] = true; $seenA[$it['url']] = true;
    $archItems[] = $it;
    if (count($archItems) >= ARCHIVE_MAX) { break; }
}

$dir = dirname(OUT_FILE);
if (!is_dir($dir)) { @mkdir($dir, 0755, true); }
if (!bn_write_json(ARCHIVE_FILE, array('updated'=>time(), 'items'=>$archItems))) {
    bn_say('ОШИБКА: не удалось записать архив — лента не изменена');
    if (!$isCli) { http_response_code(500); }
    exit(1);
}
if (!bn_write_json(OUT_FILE, array('updated'=>time(), 'items'=>$items, 'sources'=>$report))) {
    bn_say('ОШИБКА: не удалось записать ленту');
    if (!$isCli) { http_response_code(500); }
    exit(1);
}
bn_say('Готово. В ленте: ' . count($items) . ' новостей');
bn_say('Архив для страницы «Новости»: ' . count($archItems) . ' новостей');
// журнал последнего запуска: http://bikinews.ru/data/last-run.txt

// Проверочный сбор после выкладки не отправляет сообщения.
if (($isCli && getenv('BIKINEWS_COLLECT_ONLY')) || (!$isCli && !empty($_POST['collect_only']))) { exit(0); }

// ===== TELEGRAM: автопостинг в канал =====
// Настройки — в data/tg-config.php (токен бота и адрес канала). Нет файла или токена — шаг пропускается.
define('TG_CONFIG', dirname(__FILE__) . '/data/tg-config.php');
define('TG_STATE',  dirname(__FILE__) . '/data/tg-state.json');
define('TG_MAX_PER_RUN', 3);        // не больше 3 постов за запуск, остальные — через 20 минут

function tg_call($cfg, $method, $params) {
    $api = getenv('BIKINEWS_TG_API') ? getenv('BIKINEWS_TG_API') : (!empty($cfg['api']) ? rtrim($cfg['api'], '/') : 'https://api.telegram.org');
    $url = $api . '/bot' . $cfg['token'] . '/' . $method;
    if (!function_exists('curl_init')) { return array('ok' => false, 'description' => 'нет curl'); }
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_TIMEOUT, 12);
    $body = curl_exec($ch);
    $err = curl_error($ch);
    if (PHP_VERSION_ID < 80000) { curl_close($ch); }
    if ($body === false) { return array('ok' => false, 'description' => $err); }
    $r = json_decode((string)$body, true);
    return is_array($r) ? $r : array('ok' => false, 'description' => 'непонятный ответ');
}
function tg_esc($t) { return htmlspecialchars((string)$t, ENT_QUOTES, 'UTF-8'); }

$tgCfg = is_file(TG_CONFIG) ? @include TG_CONFIG : null;
if (!is_array($tgCfg) || empty($tgCfg['token']) || empty($tgCfg['chat']) || (isset($tgCfg['enabled']) && !$tgCfg['enabled'])) {
    bn_say('Telegram: не настроен (нет токена в data/tg-config.php) — пропускаю');
} else {
    $st = is_file(TG_STATE) ? json_decode((string)file_get_contents(TG_STATE), true) : null;
    $first = !is_array($st);
    if ($first) { $st = array('posted' => array(), 'digest' => array()); }
    $sent = 0; $site = 'https://bikinews.ru/';

    // проверка связи: news.php?key=...&tgtest=1
    if (!$isCli && isset($_GET['tgtest'])) {
        $r = tg_call($tgCfg, 'sendMessage', array('chat_id' => $tgCfg['chat'], 'parse_mode' => 'HTML',
            'text' => "✅ Быки News подключены к каналу. Новости будут появляться здесь автоматически.\n\n<a href=\"{$site}\">bikinews.ru</a>"));
        bn_say('Telegram: тестовое сообщение — ' . (!empty($r['ok']) ? 'отправлено' : 'ОШИБКА: ' . (isset($r['description']) ? $r['description'] : '?')));
    }

    // 1) наши пересказы из data/glavnoe.json
    $gl = is_file(dirname(__FILE__) . '/data/glavnoe.json') ? json_decode((string)file_get_contents(dirname(__FILE__) . '/data/glavnoe.json'), true) : null;
    $glItems = (is_array($gl) && isset($gl['items'])) ? $gl['items'] : array();
    if ($first) {
        // первый запуск: всё, что уже есть на сайте, считаем опубликованным, чтобы не завалить канал
        foreach ($glItems as $g) { $st['posted'][] = $g['id']; }
        bn_say('Telegram: первый запуск, отмечено как уже опубликованное: ' . count($glItems));
    } else {
        $new = array();
        foreach ($glItems as $g) { if (!in_array($g['id'], $st['posted'])) { $new[] = $g; } }
        usort($new, function ($a, $b) { return $a['ts'] - $b['ts']; });   // старые раньше
        foreach ($new as $g) {
            if ($sent >= TG_MAX_PER_RUN) { break; }
            $lead = isset($g['paras'][0]) ? $g['paras'][0] : '';
            $text = '<b>' . tg_esc($g['title']) . "</b>\n\n" . tg_esc($lead) . "\n\n"
                  . '👉 <a href="' . $site . 'news.html#' . rawurlencode($g['id']) . '">Читать на Быки News</a>'
                  . "\nИсточник: " . '<a href="' . tg_esc($g['url']) . '">' . tg_esc($g['source']) . '</a>';
            $r = tg_call($tgCfg, 'sendMessage', array('chat_id' => $tgCfg['chat'], 'parse_mode' => 'HTML', 'text' => $text,
                'disable_web_page_preview' => 'true'));
            if (!empty($r['ok'])) { $st['posted'][] = $g['id']; $sent++; }
            else { bn_say('Telegram: ошибка публикации — ' . (isset($r['description']) ? $r['description'] : '?')); break; }
        }
        if ($sent) { bn_say('Telegram: опубликовано пересказов — ' . $sent); }
    }

    // 2) дайджест изданий в 12:00 и 20:00
    $slotH = (int)date('G');
    if (($slotH === 12 || $slotH === 20) && (int)date('i') < 40) {
        $slot = date('Y-m-d') . '-' . $slotH;
        if (empty($st['digest'][$slot]) && $sent < TG_MAX_PER_RUN) {
            $pick = array(); $since = time() - 12 * 3600;
            foreach ($items as $it) {
                if ($it['ts'] >= $since && count($pick) < 7) { $pick[] = $it; }
            }
            if ($pick) {
                $lines = array();
                foreach ($pick as $it) {
                    $lines[] = '▪️ <a href="' . tg_esc($it['url']) . '">' . tg_esc($it['title']) . '</a> <i>— ' . tg_esc($it['source']) . '</i>';
                }
                $text = '<b>📰 Что пишут о «Краснодаре» · ' . date('d.m') . ($slotH === 12 ? ', день' : ', вечер') . "</b>\n\n"
                      . implode("\n\n", $lines) . "\n\n" . '<a href="' . $site . 'news.html">Все новости на Быки News</a>';
                $r = tg_call($tgCfg, 'sendMessage', array('chat_id' => $tgCfg['chat'], 'parse_mode' => 'HTML', 'text' => $text,
                    'disable_web_page_preview' => 'true'));
                if (!empty($r['ok'])) { bn_say('Telegram: дайджест опубликован (' . count($pick) . ')'); }
                else { bn_say('Telegram: ошибка дайджеста — ' . (isset($r['description']) ? $r['description'] : '?')); }
            }
            $st['digest'][$slot] = 1;   // слот закрыт, даже если новостей не было
        }
    }

    $st['posted'] = array_slice(array_values(array_unique($st['posted'])), -500);
    $st['digest'] = array_slice($st['digest'], -20, null, true);
    @file_put_contents(TG_STATE, json_encode($st));
}
