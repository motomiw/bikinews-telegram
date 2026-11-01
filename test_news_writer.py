import unittest
import news_writer as w
from unittest.mock import patch
from contextlib import nullcontext
from types import SimpleNamespace
import json
import os

MASTER = '<ul class="feed"><li><article><h3>Кордоба извинился перед болельщиками за последние результаты команды</h3></article></li></ul>'

class EditorialTests(unittest.TestCase):
    def test_missing_key_stops_without_using_a_local_or_paid_model(self):
        with patch.dict(os.environ,{'DEEPSEEK_API_KEY':''}),patch.object(w.urllib.request,'urlopen') as call:
            with self.assertRaisesRegex(ValueError,'DEEPSEEK_API_KEY'):
                w.writer()
        call.assert_not_called()
    def test_remote_writer_uses_direct_deepseek(self):
        result={'choices':[{'message':{'content':'{"supported":true}'}}]}
        with patch.object(w.urllib.request,'urlopen',return_value=nullcontext(SimpleNamespace(read=lambda limit:json.dumps(result).encode()))) as call:
            self.assertEqual(w.deepseek_writer('test-key')('Return JSON',{},w.flag_schema('supported')),{'supported':True})
        request=call.call_args.args[0]
        body=json.loads(request.data)
        self.assertEqual(body['model'],'deepseek-flash')
        self.assertNotIn('models',body)
        self.assertEqual(body['thinking'],{'type':'disabled'})
        self.assertEqual(request.full_url,'https://api.deepseek.com/chat/completions')

    def test_remote_limit_error_does_not_reveal_key_or_fall_back(self):
        with patch.object(w.urllib.request,'urlopen',side_effect=w.urllib.error.HTTPError('https://openrouter.ai',429,'Limit',{},None)) as call:
            with self.assertRaisesRegex(ValueError,'HTTP 429') as err:
                w.deepseek_writer('private-test-key')('Return JSON',{})
        self.assertNotIn('private-test-key',str(err.exception))
        self.assertEqual(call.call_count,1)

    def test_backdated_news_does_not_displace_a_newer_item(self):
        import datetime as dt
        master='<ul class="feed"><li><article><time>1 ноя<br>10:00</time><h3>NEWER</h3></article></li><li><article><time>31 окт<br>21:00</time><h3>OLDER</h3></article></li></ul>'
        now=dt.datetime(2026,11,1,12,tzinfo=w.MSK)
        item={'ts':dt.datetime(2026,11,1,9,tzinfo=w.MSK).timestamp()}
        result=w.insert_story(master,item,'<li><article>MIDDLE</article></li>',now)
        self.assertLess(result.index('NEWER'),result.index('MIDDLE'))
        self.assertLess(result.index('MIDDLE'),result.index('OLDER'))

    def test_sources_are_restricted(self):
        for url in ('http://fckrasnodar.ru/a', 'https://fckrasnodar.ru.attacker.test/a',
                    'https://user:secret@fckrasnodar.ru/a', 'https://127.0.0.1/a'):
            self.assertFalse(w.permitted(url))
        self.assertTrue(w.permitted('https://www.fckrasnodar.ru/team/news/a'))

    def test_old_future_and_duplicate_items_are_excluded(self):
        title = 'Кордоба извинился перед болельщиками Краснодара за последние результаты'
        base = dict(title=title, url='https://championat.com/a', ts=100000)
        self.assertEqual(w.candidates([base], MASTER,100100), [])
        other = dict(base,title='Краснодар объявил о новом тренировочном сборе')
        self.assertEqual(len(w.candidates([other],MASTER,100100)),1)
        self.assertEqual(w.candidates([dict(other,ts=1)],MASTER,100100),[])
        self.assertEqual(w.candidates([dict(other,ts=100101)],MASTER,100100),[])
        official=dict(title='Цифры и факты выездной игры',url='https://fckrasnodar.ru/team/news/object/?object_id=154406',ts=100000)
        self.assertEqual(len(w.candidates([official],MASTER,100100)),1)

    def test_rejects_unsupported_numbers_and_copying(self):
        draft = dict(publish=True,title='Краснодар начал подготовку к следующей игре',
            paras=['Краснодар приступил к занятиям после завершения предыдущего матча. Тренерский штаб сообщил о начале подготовки к новой встрече.',
                   'Участники команды работают по утверждённой программе подготовки. В сообщении клуба не названы дополнительные изменения в составе.'])
        sources=['Клуб сообщил о начале тренировочной работы, занимаются футболисты основной команды.']
        self.assertEqual(w.validate(draft,sources,[])[0],draft['title'])
        with self.assertRaises(ValueError):
            w.validate(dict(draft,title=draft['title']+' 2:1'),sources,[])
        with self.assertRaises(ValueError):
            w.validate(draft,[' '.join(draft['paras'])],[])

    def test_render_escapes_source_and_uses_original_time(self):
        item=dict(ts=1793472480,url='https://championat.com/a',source='Издание <script>')
        output=w.render(item,'Новость & клуб',['Первый абзац','Второй абзац'],'Клуб')
        self.assertNotIn('<script>',output)
        self.assertIn('&amp;',output)
        self.assertIn('target="_blank"',output)

if __name__=='__main__':
    unittest.main()
