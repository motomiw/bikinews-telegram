"""Проверки загрузчика: отдельные временные папки, без Telegram и рабочего сайта."""
import datetime as dt
import email.utils
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest

SOURCE=Path(__file__).with_name('news.php')

class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        shutil.copyfile(SOURCE,self.root/'news.php')
        (self.root/'data').mkdir()
    def tearDown(self):self.tmp.cleanup()
    def rss(self,name,rows):
        import xml.sax.saxutils as x
        path=self.root/name
        body=''.join('<item><title>'+x.escape(title)+'</title><link>'+x.escape(url)+'</link><description>Короткий анонс</description><pubDate>'+email.utils.format_datetime(dt.datetime.fromtimestamp(stamp,dt.timezone.utc))+'</pubDate></item>' for title,url,stamp in rows)
        path.write_text('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'+body+'</channel></rss>',encoding='utf-8')
        return str(path)
    def run_collector(self,feeds):
        env=dict(os.environ,BIKINEWS_FEEDS=json.dumps(feeds),BIKINEWS_COLLECT_ONLY='1')
        return subprocess.run(['php','news.php'],cwd=self.root,env=env,capture_output=True,text=True,timeout=30)
    def test_new_sources_and_dedup_preserve_old_news(self):
        now=int(time.time())
        old={'title':'Краснодар готовится к домашнему матчу','text':'','url':'https://example.test/old','source':'Архив','ts':now-600}
        (self.root/'data/news.json').write_text(json.dumps({'updated':now-600,'items':[old]}))
        path=self.rss('valid.xml',[('Краснодар объявил состав на матч','https://example.test/new',now),('Краснодар объявил состав на матч','https://example.test/new',now),('Хоккей: Краснодар выиграл матч','https://example.test/hockey',now),('Краснодар старый материал','https://example.test/stale',now-9*86400)])
        bad=self.root/'broken.xml';bad.write_text('<html>Не RSS</html>')
        result=self.run_collector([['Новый источник',path,'rss'],['Сбой',str(bad),'rss']])
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        news=json.loads((self.root/'data/news.json').read_text())
        self.assertEqual([x['url'] for x in news['items']],['https://example.test/new','https://example.test/old'])
        self.assertEqual(len(news['sources']),2)
        self.assertFalse(news['sources'][1]['ok'])
        self.assertFalse((self.root/'data/tg-state.json').exists())
    def test_total_failure_keeps_feed_and_archive_exactly(self):
        original='{"updated":123,"items":[]}'
        for filename in ('news.json','archive.json'):(self.root/'data'/filename).write_text(original)
        bad=self.root/'bad.xml';bad.write_text('not xml')
        result=self.run_collector([['Сбой',str(bad),'rss']])
        self.assertNotEqual(result.returncode,0)
        for filename in ('news.json','archive.json'):self.assertEqual((self.root/'data'/filename).read_text(),original)
    def test_future_dates_and_unrelated_stories_are_rejected(self):
        now=int(time.time())
        path=self.rss('dates.xml',[('Краснодар будущая новость','https://example.test/future',now+7200),('Зенит начал тренировку','https://example.test/other',now)])
        result=self.run_collector([['Проверка дат',path,'rss']])
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads((self.root/'data/news.json').read_text())['items'],[])
    def test_concurrent_run_does_not_touch_files(self):
        if os.name!='posix':self.skipTest('flock requires Linux')
        import fcntl
        lock=open(self.root/'data/news.lock','w')
        self.addCleanup(lock.close)
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        path=self.rss('a.xml',[('Краснодар объявил состав на матч','https://example.test/new',int(time.time()))])
        result=self.run_collector([['Тест',path,'rss']])
        self.assertIn('Сбор уже выполняется',result.stdout)
        self.assertFalse((self.root/'data/news.json').exists())
    def test_source_has_no_embedded_key_and_contains_ten_rss(self):
        text=SOURCE.read_text(encoding='utf-8')
        self.assertNotIn("define('SECRET', '",text)
        self.assertEqual(text.count("'rss'),"),10)

if __name__=='__main__':unittest.main(verbosity=2)
