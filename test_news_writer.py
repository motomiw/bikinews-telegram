import unittest
import news_writer as w

MASTER = '<ul class="feed"><li><article><h3>Кордоба извинился перед болельщиками за последние результаты команды</h3></article></li></ul>'

class EditorialTests(unittest.TestCase):
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
