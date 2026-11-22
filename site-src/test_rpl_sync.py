import unittest

import rpl_sync


PAGE = '''
<table title="Турнирная таблица Премьер-лига Россия (РПЛ) 2026/2027"><tr><th>Клуб</th></tr>
<tr><td>1</td><td>Зенит</td><td>15</td><td>10</td><td>1</td><td>4</td><td>33−18</td><td>31</td></tr>
<tr><td>2</td><td>Динамо</td><td>15</td><td>9</td><td>2</td><td>4</td><td>25−16</td><td>29</td></tr>
<tr><td>3</td><td>Спартак</td><td>15</td><td>8</td><td>3</td><td>4</td><td>24−16</td><td>27</td></tr>
<tr><td>4</td><td>Краснодар</td><td>15</td><td>7</td><td>5</td><td>3</td><td>26−19</td><td>26</td></tr>
<tr><td>5</td><td>ЦСКА</td><td>15</td><td>7</td><td>4</td><td>4</td><td>22−18</td><td>25</td></tr>
<tr><td>6</td><td>Ростов</td><td>15</td><td>6</td><td>3</td><td>6</td><td>20−19</td><td>21</td></tr>
<tr><td>7</td><td>Рубин</td><td>15</td><td>5</td><td>5</td><td>5</td><td>18−20</td><td>20</td></tr>
<tr><td>8</td><td>Балтика</td><td>15</td><td>5</td><td>4</td><td>6</td><td>18−16</td><td>19</td></tr>
<tr><td>9</td><td>Крылья Советов</td><td>15</td><td>4</td><td>5</td><td>6</td><td>18−23</td><td>17</td></tr>
<tr><td>10</td><td>Ахмат</td><td>15</td><td>4</td><td>4</td><td>7</td><td>20−22</td><td>16</td></tr>
<tr><td>11</td><td>Оренбург</td><td>15</td><td>3</td><td>7</td><td>5</td><td>14−17</td><td>16</td></tr>
<tr><td>12</td><td>Динамо Махачкала</td><td>15</td><td>4</td><td>3</td><td>8</td><td>17−25</td><td>15</td></tr>
<tr><td>13</td><td>Родина</td><td>15</td><td>3</td><td>4</td><td>8</td><td>15−28</td><td>13</td></tr>
<tr><td>14</td><td>Акрон</td><td>15</td><td>2</td><td>6</td><td>7</td><td>17−26</td><td>12</td></tr>
<tr><td>15</td><td>Локомотив</td><td>15</td><td>2</td><td>5</td><td>8</td><td>15−22</td><td>11</td></tr>
<tr><td>16</td><td>Факел</td><td>15</td><td>2</td><td>3</td><td>10</td><td>11−25</td><td>9</td></tr></table>
<time datetime="2026-11-22T14:00:00+03:00" title="Время проведения матча Динамо - Краснодар: 2026-11-22 в 14:00:00 МСК"></time><span>Завершен</span><div data-testid="actual-matches-widget-score" aria-label="Счёт: 1 — 2"></div>
'''

PROTOCOL = '''
<li class="timeline__event goal-wrapper goal-wrapper--away"><span class="goal-time">11&#39;</span><span class="goal-scorer"><a>Джон Кордоба</a></span><a class="goal-assists__link">Диего Родригес</a></li>
<li class="timeline__event goal-wrapper goal-wrapper--home"><span class="goal-time">27&#39;</span><span class="goal-scorer"><a>Ярослав Гладышев</a></span><a class="goal-assists__link">Максим Осипенко</a></li>
'''


class RPLSyncTests(unittest.TestCase):
    def test_standings_are_parsed_and_checked(self):
        table = rpl_sync.parse_standings(PAGE)
        self.assertEqual(len(table), 16)
        self.assertEqual(table[0], ["zenit", 15, 10, 1, 4, 33, 18, 31])

    def test_finished_match_is_parsed(self):
        self.assertEqual(rpl_sync.parse_completed_matches(PAGE), {("2026-11-22", "dynamo", "krasnodar"): (1, 2)})

    def test_goal_authors_are_parsed_from_protocol(self):
        self.assertEqual(rpl_sync.parse_match_protocol(PROTOCOL, False), [
            ("11", "Джон Кордоба", "k", "Диего Родригес"),
            ("27", "Ярослав Гладышев", "o", "Максим Осипенко"),
        ])

    def test_separate_goal_columns_are_parsed(self):
        page = PAGE.replace("33−18", "33</td><td>18", 1)
        self.assertEqual(rpl_sync.parse_standings(page)[0][5:7], [33, 18])

    def test_last_match_score_cell_is_ignored(self):
        page = PAGE.replace("33−18", "33</td><td>18", 1)
        page = page.replace("<td>Зенит</td>", "<td>Зенит</td><td>1 - 0</td>", 1)
        self.assertEqual(rpl_sync.parse_standings(page)[0], ["zenit", 15, 10, 1, 4, 33, 18, 31])

    def test_same_opponent_on_another_date_is_not_removed(self):
        master = '''  var table = [\n    ["zenit",1,0,1,0,1,1,1]\n  ];\n  var upcoming = [\n    ['22 ноя', 'вс', 'РПЛ · 15 тур', 'dynamo', false, '14:00'],\n    ['20 мар', 'сб', 'РПЛ · 21 тур', 'dynamo', true, '14:00']\n  ];\n  var played = [\n    ['7 ноя', 'РПЛ · 14 тур', 'cska', true, 4, 2]\n  ];'''
        table = [[slug, 1, 0, 1, 0, 1, 1, 1] for slug in sorted(rpl_sync.EXPECTED_TEAMS)]
        result = rpl_sync.update_master(master, table, [{'d': '2026-11-22', 'rnd': '15 тур', 'opp': 'dynamo', 'home': False, 'gf': 2, 'ga': 1}])
        self.assertIn("'20 мар', 'сб', 'РПЛ · 21 тур', 'dynamo', true", result)

    def test_incomplete_table_is_rejected(self):
        with self.assertRaises(ValueError):
            rpl_sync.parse_standings("<table title='Турнирная таблица Премьер-лига Россия'></table>")
