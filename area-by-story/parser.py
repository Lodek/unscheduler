import collections
from mpylib.tables import Table
import numpy as np

DumbTable = collections.namedtuple('DumbTable', 'attributes, headers, matrix, header_dim, defines')

class Dumb():
    """ Base class for parsers specific to a table format. Explicitly defines methods and attributes the 
    subclasses must implement """
    def __init__(self):
        self.defines = {}
        self.headers = []
        self.attributes = []
        self.header_dim = ''
        self.matrix = None

class ArchicadTableParser(Dumb):
    """ Class that parses the archicad table with areas by story for each unit """
    def __init__(self, table_fp):
        super().__init__()
        clean = lambda name : name.replace(' ', '_').lower()
        with open(table_fp, 'r') as f:
            self.texble = [line[:-2].split('\t') for line in f]
        self.headers = self.texble[0]
        self.attributes = [clean(header) for header in self.headers]
        self.matrix = np.array(self.texble[1:])
        self.header_dim = 'x'

    
class Story():
    def __init__(self, story_name):
        self.story_name = story_name
        self.nc = 0.0
        self.c = 0.0
        self.total = 0.0
    def add_area(self, area, type):
        if type == 'NC':
            self.nc += area
        elif type == 'C':
            self.c += area
    def comp_total(self):
        self.total = self.c + self.nc

class StoryParser(Dumb):
    def __init__(self, stories):
        super().__init__()
        self.headers = ['PAVIMENTO', 'AREA COMPUTAVEL (m2)', 'AREA NAO COMPUTAVEL (m2)', 'AREA TOTAL (m2)']
        self.attributes = ['pavimento', 'c', 'nc', 'total']
        self.header_dim = 'x'
        self.matrix = np.array([[story.story_name, story.c, story.nc, story.total] for story in stories.values()])
        

        
a = ArchicadTableParser('res1.txt')
b = Table(a)
stories = {story : Story(story) for story in b.home_story}

for story, type, area in zip(b.home_story, b.zone_category_code, b.calculated_area):
    stories[story].add_area(area, type)
    
for story in stories.values():
    story.comp_total
    
c = Table(StoryParser(stories))

