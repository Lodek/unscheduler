""" 
The module contains memes.
"""
class Building():
    """ Abstraction for a building plan from Archicad.
    A building plan can be thought of as a group of areas and stories. """
    
    def __init__(self, model, stories):
        self.model = model
        self.stories = stories
        self.area_comp = 0.0
        self.area_ncomp = 0.0
        self.area_proj = 0.0
        self._calc_net_area()
        self._calc_area_proj()

    def _calc_area_proj(self):
        """ Iterates over stories to find the Projection Area and assigns it to self.area_proj """
        areas = [story.area_comp for story in self.stories]
        self.area_proj = max(areas)
    
    def _calc_net_area(self):
        """ Calculate the net areas for Building object and assigns those to self"""
        self.area_comp = sum([story.area_comp for story in self.stories])
        self.area_ncomp = sum([story.area_ncomp for story in self.stories])
    
    def __getitem__(self, key):
        """ Returns the Story object by index """
        try:
            value = self.stories[key]
        except IndexError:
            value = Story(key, 'out-of-range')
        return value

    def __len__(self):
        """ Number of stories in building """
        return len(self.stories)
    
    def __repr__(self):
        str = 'Model: {}, Stories: {}\nArea_C: {}m2\tArea_NC {}m2'
        str = str.format(self.model, len(self), self.area_comp, self.area_ncomp)
        return str
        

class Story():
    """ Abstraction of a story.
    A story is composed of a name, an id, net computable area and net non-computable area
    Each building has multiple stories"""

    def __init__(self, id, name, area_comp=0.0, area_ncomp=0.0):
        self.id = id
        self.name = name
        self.area_comp = area_comp
        self.area_ncomp = area_ncomp

    def add_area(self, area, category):
        """ Adds given area to the matching category,
        area: float
        category: str ('NC' or 'C') """
        if category == 'NC':
            self.area_ncomp += area
        elif category == 'C':
            self.area_comp += area

    def __repr__(self):
        str = 'ID: {}, Name: {}, Area_C: {:.2f}m2, Area_NC: {:.2f}m2'
        str = str.format(self.id, self.name, self.computable_area, self.non_computable_area)
        return str
