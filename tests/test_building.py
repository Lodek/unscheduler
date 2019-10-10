import unittest
from building import Building, Story

class TestStory(unittest.TestCase):

    def test_story(self):
        story = Story(1, 'pavimento terreo')
        story.add_area(10, 'C')
        self.assertEqual(story.area_comp, 10)
        story.add_area(10, 'NC')
        self.assertEqual(story.area_ncomp, 10)
        with self.assertRaises(ValueError):
            story.add_area(10, 'whatever')
        

class TestBuilding(unittest.TestCase):

    def setUp(self):
        self.s1 = Story(1, 'terreo', 1, 2)
        self.s2 = Story(2, 'terreo', 3, 4)
        self.building = Building('test', [self.s1, self.s2])
        

    def test_building(self):
        self.assertEqual(self.building.area_comp, 4)
        self.assertEqual(self.building.area_ncomp, 6)
        self.assertEqual(len(self.building), 2)
        self.assertEqual(self.building[0], self.s1)
        self.assertEqual(self.building[1], self.s2)

    def test_super_building(self):
        b1 = Building('b1', [self.s1])
        b2 = Building('b2', [self.s2])
        sup = Building.get_super_building('super', [b1, b2])
        self.assertEqual(len(sup), 1)
        self.assertEqual(sup.area_comp, 4)
        self.assertEqual(sup.area_ncomp, 6)
        self.assertEqual(sup.area_proj, 4)
        
        
if __name__ == '__main__':
    unittest.main()
