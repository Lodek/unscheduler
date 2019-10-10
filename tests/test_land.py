#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
from land import Land

class TestLand(TestCase):
    """
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        """Test Land's init. Expect certain attributes can be used as kwargs while 
        others raise an exception."""
        land = Land(0, 'test-land', 10, area_perm=3)
        self.assertEqual(land.area_perm, 3)
        with self.assertRaises(AttributeError):
            land = Land(0, 'test-land', 10, random_attr=3)

    def test_calculations(self):
        """ """
        pass

    

if __name__ == '__main__':
    main()
