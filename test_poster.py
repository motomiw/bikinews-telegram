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
        self.write({'v': 3, 'posted': [], 'digest': {'legacy': 1}})
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

    def run_main(self, items, responses):
        def feed(path):
            self.assertTrue(path.endswith('glavnoe.json'))
            return {'items': items}
        with patch.object(p, 'get_json', side_effect=feed) as fetch,              patch.object(p, 'send', side_effect=responses) as send,              patch.object(p, 'push'):
            result = p.main()
        return result, send.call_count, fetch.call_count

    def test_posts_only_new_editorial_items(self):
        items = [dict(id=str(i), ts=i, title='Test', paras=['Text'], url='https://example.com', source='Source') for i in range(5)]
        self.assertEqual(self.run_main(items, [True, False]), (1, 2, 1))
        self.assertEqual(self.read()['posted'], ['0'])
        self.assertNotIn('digest', self.read())
        self.assertEqual(self.run_main(items, [True, True, True]), (0, 3, 1))
        self.assertEqual(self.read()['posted'], ['0', '1', '2', '3'])

    def test_no_digest_is_sent_when_there_are_no_new_articles(self):
        self.assertEqual(self.run_main([], []), (0, 0, 1))
        self.assertNotIn('digest', self.read())

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
