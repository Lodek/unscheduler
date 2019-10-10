#!/usr/bin/env python
"""

"""
from unittest import TestCase, main
from aux import ProjectInfo

class TestProjectInfo(TestCase):
    """
    Test for the ProjectInfo class
    """
    def setUp(self):
        self.pi = ProjectInfo('samples/config.ini')

    def tearDown(self):
        pass

    def test_project_attrs(self):
        """Test the 'project' dictionary of the config file"""
        self.assertEqual(self.pi.project.title, 'TEST TITLE')
        self.assertEqual(self.pi.project.prop, 'TEST PROP')
        self.assertEqual(self.pi.project.start_date, '05/19')
        
    def test_misc_attrs(self):
        """Test the 'misc' dictionary of the config file"""
        files = 'r1 rec1 rec2'.split()
        rec_subplots = [21, 22]
        rec_cob = 84
        rec_desc = 94
        units = 20
        ca = 50
        self.assertEqual(self.pi.misc.files, files)
        self.assertEqual(self.pi.misc.rec_subplots, rec_subplots)
        self.assertEqual(self.pi.misc.rec_cob, rec_cob)
        self.assertEqual(self.pi.misc.rec_desc, rec_desc)
        self.assertEqual(self.pi.misc.units, units)
        self.assertEqual(self.pi.misc.ca, ca)
        
    def test_topografico_attrs(self):
        area_ri = 10
        quadricula = '120'
        ind_fiscal = '021'
        self.assertEqual(self.pi.topografico.area_ri, area_ri)
        self.assertEqual(self.pi.topografico.quadricula, quadricula)
        self.assertEqual(self.pi.topografico.ind_fiscal, ind_fiscal)


if __name__ == '__main__':
    main()       
