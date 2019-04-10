from pathlib import Path
import unittest
from factory import Parser, BuildingFactory, SubplotFactory


class TestParser(unittest.TestCase):

    def setUp(self):
        self.p = Path('samples/area-story-header.txt')
        self.parser = Parser(self.p.read_text(), 'story type area'.split(), title=True, header=False)

    def test_parse_txt(self):
        self.parser.parse_txt()
        l1 = ['TERREO PAV', 'C', '51.04']
        l2 = ['SEGUNDO PAVIMENTO', 'C', '55.27']
        l3 = ['TERCEIRO PAVIMENTO', 'NC', '17.28']
        l = [l1, l2, l3]
        self.assertEqual(self.parser.matrix, l)

    def test_tablefy(self):
        self.parser.parse_txt()
        self.parser.tablefy()
        l1 = ['TERREO PAV', 'C', 51.04]
        l2 = ['SEGUNDO PAVIMENTO', 'C', 55.27]
        l3 = ['TERCEIRO PAVIMENTO', 'NC', 17.28]
        l = [l1, l2, l3]
        self.assertEqual(len(self.parser.table), 3)
        for e, record in zip(l, self.parser.table):
            self.assertEqual(e, list(record))

            
class TestBuildingFactory(unittest.TestCase):

    def test_get(self):
        p = Path('samples/test-building.txt')
        b = BuildingFactory.get_building('test', p.read_text())
        self.assertEqual(b.area_comp, 10)
        self.assertEqual(b.area_ncomp, 5)

class TestSubplotFacotry(unittest.TestCase):

    def test_get(self):
        p_subplots = Path('samples/test-subplots.txt')
        p_perm = Path('samples/test-perm.txt')
        subplots = SubplotFactory.get_subplots(p_subplots.read_text(),
                                               p_perm.read_text(), {})
        self.assertEqual(len(subplots), 3)
        print(subplots)


if __name__ == '__main__':
    unittest.main()
