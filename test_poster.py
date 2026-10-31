import datetime
import importlib.util
import json
import os
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('poster', os.path.join(os.path.dirname(__file__), 'poster.py'))
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class PosterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = os.path.join(self.tmp.name, 'state.json')
        self.base = {'v': 3, 'posted': [], 'digest': {}}
        self.write(self.base)
        for name, value in [('STATE', self.state), ('TOKEN', 'fake'), ('CHAT', 'fake')]:
            ctx = patch.object(p, name, value)
            ctx.start()
            self.addCleanup(ctx.stop)
        ctx = patch.dict(os.environ, {'TG_TEST': 'false'})
        ctx.start()
        self.addCleanup(ctx.stop)

    def write(self, state):
        with open(self.state, 'w', encoding='utf-8') as f:
            json.dump(state, f)

    def read(self):
        with open(self.state, encoding='utf-8') as f:
            return json.load(f)

    def run_main(self, items, responses, hour=13, feed_error=False, digest_items=None):
        class Clock(datetime.datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2026, 10, 30, hour, 10, tzinfo=p.MSK)
        def feed(path):
            if path.endswith('glavnoe.json'):
                return {'items': items}
            if feed_error:
                raise OSError('offline')
            return {'items': digest_items if digest_items is not None else [{'ts': Clock.now().replace(minute=0).timestamp()-60, 'url': 'https://example.com', 'title': 'Test', 'source': 'Source'}]}
        with patch.object(p.datetime, 'datetime', Clock), patch.object(p, 'get_json', side_effect=feed), patch.object(p, 'send', side_effect=responses) as send, patch.object(p, 'push'):
            result = p.main()
            self.sent_texts = [call.args[0] for call in send.call_args_list]
        return result, send.call_count

    def test_digest_retry_then_success(self):
        self.assertEqual(self.run_main([], [False])[0], 1)
        self.assertEqual(self.read()['digest'], {})
        self.assertEqual(self.run_main([], [True])[0], 0)
        self.assertTrue(self.read()['digest'])
        self.assertEqual(self.run_main([], [])[1], 0)

    def test_all_requested_digest_hours(self):
        for hour in (0, 3, 6, 9, 11, 13, 15, 17, 19, 21, 23):
            with self.subTest(hour=hour):
                self.write(self.base)
                self.assertEqual(self.run_main([], [True], hour=hour), (0, 1))
        for hour in (1, 2, 4, 5, 7, 8, 10, 12, 14, 16, 18, 20, 22):
            with self.subTest(hour=hour):
                self.write(self.base)
                self.assertEqual(self.run_main([], [], hour=hour), (0, 0))

    def test_feed_error_does_not_consume_slot(self):
        self.assertEqual(self.run_main([], [], feed_error=True)[0], 1)
        self.assertEqual(self.read()['digest'], {})

    def test_digest_windows_do_not_overlap_at_midnight(self):
        midnight=datetime.datetime(2026,10,30,tzinfo=p.MSK).timestamp()
        feed=[dict(ts=midnight-60,url='https://example.com/a',title='Before midnight',source='Source'),
              dict(ts=midnight+60,url='https://example.com/b',title='After midnight',source='Source')]
        self.run_main([], [True],hour=0,digest_items=feed)
        self.assertIn('Before midnight',self.sent_texts[0])
        self.assertNotIn('After midnight',self.sent_texts[0])
        self.run_main([], [True],hour=3,digest_items=feed)
        self.assertIn('After midnight',self.sent_texts[0])
        self.assertNotIn('Before midnight',self.sent_texts[0])

    def test_partial_success_is_saved(self):
        items = [dict(id=str(i), ts=i, title='Test', paras=['Text'], url='https://example.com', source='Source') for i in range(5)]
        self.assertEqual(self.run_main(items, [True, False], hour=10)[0], 1)
        self.assertEqual(self.read()['posted'], ['0'])
        self.assertEqual(self.run_main(items, [True]*3, hour=10)[1], 3)
        self.assertEqual(self.read()['posted'], ['0', '1', '2', '3'])

    def test_test_mode_sends_once_without_fetching(self):
        with patch.dict(os.environ, {'TG_TEST': 'true'}), patch.object(p, 'send', return_value=True) as send, patch.object(p, 'get_json') as fetch:
            self.assertEqual(p.main(), 0)
            send.assert_called_once()
            fetch.assert_not_called()

    def test_invalid_state_fails_without_sending(self):
        with open(self.state, 'w') as f:
            f.write('{broken')
        with patch.object(p, 'send') as send, self.assertRaises(ValueError):
            p.main()
        send.assert_not_called()

    def test_network_failure_returns_false(self):
        with patch.object(p.urllib.request, 'urlopen', side_effect=p.urllib.error.URLError('offline')):
            self.assertFalse(p.send('Test'))

if __name__ == '__main__':
    unittest.main()

