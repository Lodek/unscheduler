"""
Module contains classes responsible for parsing the table files. 
A Parser object returns object(s) which are abstraction of architectural
entities existing in the project, such as buildings, subplots or a lot.
"""

import collections, re
from land import Lot, Subplot
from building import Story, Building
import pdb

class BaseParser():
    """ Receives a file object for an archicad building text schedule 
    returns the objects matching the data"""
    def parse_txt(self, txt, attributes):
        self._texble = [line[:-1].split('\t') for line in txt.split('\n')][1:-1]
        table = list(self.caster(attributes))
        return table

    def caster(self, attributes):
        """Generator that iterates over rows in texble and converts each element
        to either a float or keeps it as a string. Choice is made through a regex. 
        Yields a namedtuple whose attributes are the same as the passed as parameter"""
        Record = collections.namedtuple('Record', attributes)
        is_float = lambda element : True if re.search(r'^[\d,]+\.\d+$', element) else False
        is_int = lambda element : True if re.search(r'^\d+$', element) else False
        for row in self._texble:
            new_row = []
            for element in row:
                if is_float(element):
                    s = re.sub(',', '', element)
                    new_element = float(s)
                elif is_int(element):
                    new_element = int(element)
                else:
                    new_element = element
                new_row.append(new_element)
            record = Record(*new_row)
            yield record
            
            
class BuildingParser(BaseParser):
    """ Parser for an archicad building table """
    def __init__(self, paths):
        self.paths = paths
        self.tables = self._parse_tables()
        self.buildings = self._creator()

    def _parse_tables(self):
        attributes = ('story', 'category', 'area')
        tables = [self.parse_txt(path.read_text(), attributes) for path in self.paths]
        return tables

    def _creator(self):
        null_story = Story(0, 'null')
        buildings = [Building('null', [null_story])]
        for table, path in zip(self.tables, self.paths):
            storie_names = self._unique_list([record.story for record in table])
            stories = {story : Story(id=i, name=story) for i, story in enumerate(storie_names)}
            for record in table:
                stories[record.story].add_area(record.area, record.category)
            stories = list(stories.values())
            stories = sorted(stories, key=lambda story: story.id)
            model = path.name.replace(path.suffix, '')
            buildings.append(Building(model, stories))
        return buildings

    def _unique_list(self, l):
        temp = []
        for i in l:
            if i not in temp:
                temp.append(i)
        return temp
        
class SubplotParser(BaseParser):
    """ Parser for subplots """
    def __init__(self, paths, building_dict):
        self.paths = paths
        self.building_dict = building_dict
        self.defines_table = self._parse_defines_table()
        self.perm_table = self._parse_perm_table()
        self.subplots = self._creator()

    def _parse_defines_table(self):
        path = next(filter(lambda path : path.name == '_sublotes.txt', self.paths))
        attributes = ('id', 'name', 'area')
        table = self.parse_txt(path.read_text(), attributes)
        return table

    def _parse_perm_table(self):
        path = next(filter(lambda path : path.name == '_area-perm.txt', self.paths))
        attributes = ('id', 'area')
        table = self.parse_txt(path.read_text(), attributes)
        return table

    def _creator(self):
        """ Constructs instances of subplots according to the subplot_definitions """
        subplots = {id : Subplot(id, name, area) for id, name, area in self.defines_table}
        for id, subplot in subplots.items():
            subplot.building = self.building_dict[id]
            subplot.calc_all()
        for id, area in self.perm_table:
            subplots[id].area_perm = area
            subplots[id].calc_all()
        subplots = list(subplots.values())
        subplots = sorted(subplots, key=lambda subplot: subplot.id)
        return subplots
