import tables
from pathlib import Path
import unittest, collections
from building import Building, Story
from land import Lot, Subplot

class TestTable(unittest.TestCase):

    def test_latex_factory(self):
        template = '{}'
        matrix = ['a b'.split(), '1 2'.split()]
        headers = True
        title = False
        formatter = tables.LatexFormatter()
        formatter.template = '{}'
        t = formatter._get_latex(matrix)
        self.assertTrue(type(t) == str)

    def test_story_table_factory(self):
        s1 = Story(0, 'terreo', 1, 1)
        fmt = tables.StoryFormatter()
        t = fmt.format(s1)
        self.assertTrue(type(t) == str)

    def test_building_table_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        fmt = tables.BuildingFormatter()
        t = fmt.format(building)
        self.assertTrue(type(t) == str)
        
    def test_suplot_areas_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        subplots = [Subplot(i, str(i), 5, [building]) for i in range(2)]
        lot_info = collections.defaultdict(lambda : int(10))
        lot = Lot(subplots, lot_info)
        fmt = tables.SubAreasFormatter()
        t = fmt.format(lot)
        self.assertTrue(type(t) == str)

    def test_subplot_stats_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        subplots = [Subplot(i, str(i), 5, [building]) for i in range(2)]
        lot_info = collections.defaultdict(lambda : int(10))
        lot = Lot(subplots, lot_info)
        fmt = tables.SubStatsFormatter()
        t = fmt.format(lot)
        self.assertTrue(type(t) == str)

    def test_lot_stats_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        subplots = [Subplot(i, str(i), 5, [building]) for i in range(2)]
        lot_info = collections.defaultdict(lambda : int(10))
        lot = Lot(subplots, lot_info)
        fmt = tables.LotStatsFormatter()
        t = fmt.format(lot)
        self.assertTrue(type(t) == str)

  
if __name__ == '__main__':
    unittest.main()
