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
        t = tables.LaTexFactory.get_latex(matrix, template, headers=headers, title=title)
        self.assertTrue(type(t) == str)

    def test_story_table_factory(self):
        s1 = Story(0, 'terreo', 1, 1)
        t = tables.StoryTableFactory.get_latex(s1)
        self.assertTrue(type(t) == str)

    def test_building_table_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        t = tables.BuildingTableFactory.get_latex(building)
        self.assertTrue(type(t) == str)
        
    def test_suplot_areas_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        subplots = [Subplot(i, str(i), 5, [building]) for i in range(2)]
        lot_info = collections.defaultdict(lambda : int(10))
        lot = Lot(subplots, lot_info)
        t = tables.SubplotAreasFactory.get_latex(lot)

    def test_subplot_stats_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        subplots = [Subplot(i, str(i), 5, [building]) for i in range(2)]
        lot_info = collections.defaultdict(lambda : int(10))
        lot = Lot(subplots, lot_info)
        t = tables.SubplotStatsFactory.get_latex(lot)

    def test_lot_stats_factory(self):
        s1 = Story(0, 'terreo', 1)
        s2 = Story(1, 'sup', 1, 1)
        building = Building('test', [s1, s2])
        subplots = [Subplot(i, str(i), 5, [building]) for i in range(2)]
        lot_info = collections.defaultdict(lambda : int(10))
        lot = Lot(subplots, lot_info)
        t = tables.LotStatsFactory.get_latex(lot)

  
if __name__ == '__main__':
    unittest.main()
