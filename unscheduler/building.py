""" 
The module contains memes.
"""
import logging

logger = logging.getLogger(__name__)

class Building():
    """
    Abstraction for a building file from Archicad.
    A building is a sequence of stories and attributes.
    """
    def __init__(self, model, stories):
        self.model = model
        self.stories = stories
        self.area_comp = 0.0
        self.area_ncomp = 0.0
        self.area_proj = 0.0
        self._calc_net_area()
        self._calc_area_proj()
        logger.info(repr(self))
        logger.debug('Building from stories={}'.format(stories))

    def _calc_area_proj(self):
        """ Iterates over stories to find the Projection Area and assigns it to self.area_proj """
        areas = [story.area_comp for story in self.stories]
        self.area_proj = max(areas)
    
    def _calc_net_area(self):
        """ Calculate the net areas for Building object and assigns those to self"""
        self.area_comp = sum([story.area_comp for story in self.stories])
        self.area_ncomp = sum([story.area_ncomp for story in self.stories])
    
    def __getitem__(self, n):
        """Returns the nth Story if not present, returns an empty story"""
        try:
            value = self.stories[n]
        except IndexError:
            value = Story(key, 'out-of-range')
        return value

    def __len__(self):
        """ Number of stories in building """
        return len(self.stories)

    def __repr__(self):
        s = '{}: model={}; stories={}; area_comp={:.2f}; area_ncomp={:.2f};'
        return s.format(self.__class__, self.model, len(self.stories), self.area_comp, self.area_ncomp)
        

class Story():
    """
    Abstraction of a Story.
    A story is composed of a name, an id, net computable area and net non-computable area
    Each building has multiple stories
    """
    def __init__(self, id, name, area_comp=0.0, area_ncomp=0.0):
        self.id = id
        self.name = name
        self.area_comp = area_comp
        self.area_ncomp = area_ncomp
        logger.info(repr(self))
        
    def add_area(self, area, category):
        """Adds given area to the matching category,
        area: float
        category: str ('NC' or 'C') """
        logger.debug('Add area call: area={}, category={}, self={}'.format(area, category, repr(self)))
        if category == 'NC':
            self.area_ncomp += area
        elif category == 'C':
            self.area_comp += area
        else:
            raise ValueError('Invalid category')

    def __repr__(self):
        s = '{}: id={}; name={}; area_comp={:.2f}; area_ncomp={:.2f};'
        return s.format(self.__class__, self.id, self.name, self.area_comp, self.area_ncomp)
