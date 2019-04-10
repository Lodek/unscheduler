""" 
The module contains memes.
"""
import logging
import tables

logger = logging.getLogger(__name__)

class Building():
    """
    A building is a named collection of stories.
    """
    formatter = tables.BuildingFormatter()
    def __init__(self, model, stories):
        self.model = model
        self.stories = stories
        self.super_story = None
        acs = [story.area_comp for story in self.stories]
        ncs = [story.area_ncomp for story in self.stories]
        self.super_story = Story(-1, 'TOTAL', sum(acs), sum(ncs))
        self.area_proj = max(acs)
        logger.info(repr(self))
        logger.debug('Building from stories={}'.format(stories))

    @classmethod
    def get_null_building(cls):
        return cls('null', [Story.null_story()])

    @classmethod
    def get_super_building(cls, model, buildings):
        """Super building return a building from a sequence of buildings as opposed
        to a sequence of stories. Super building does a per story sum of areas.
        Super building's idiosyncrasy is that area_proj instead of being the max
        becomes the sum of the projection areas for each building"""
        if not buildings:
            return cls.get_null_building()
        tallest_building = sorted(buildings, key=len)[-1]
        story_names = [story.name for story in tallest_building.stories]
        total_area_proj = sum(building.area_proj for building in buildings)
        stories = []
        for i, name in enumerate(story_names):
            ac = sum(building[i].area_comp for building in buildings)
            nc = sum(building[i].area_ncomp for building in buildings)
            stories.append(Story(i, name, ac, nc))
        new_building = cls(model, stories)
        new_building.area_proj = total_area_proj
        return new_building
            
    @property
    def area_comp(self):
        return self.super_story.area_comp

    @property
    def area_ncomp(self):
        return self.super_story.area_ncomp

    @property
    def total(self):
        return self.super_story.total

    def write_latex(self, target_dir):
        target = target_dir / '{}.tex'.format(self.model)
        latex = self.formatter.format(self)
        with target.open('w') as f:
            f.write(latex)

    def all_stories(self):
        return self.stories + [self.super_story]
    
    def __getitem__(self, n):
        """Returns the nth Story if not present, returns an empty story"""
        try:
            value = self.stories[n]
        except IndexError:
            value = Story(n, 'out-of-range')
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
    formatter = tables.StoryFormatter()
    def __init__(self, id, name, area_comp=0.0, area_ncomp=0.0):
        self.id = id
        self.name = name
        self.area_comp = area_comp
        self.area_ncomp = area_ncomp
        logger.debug(repr(self))
        

    @classmethod
    def null_story(cls):
        return Story(0, 'null')
    
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

    @property
    def total(self):
        return self.area_comp + self.area_ncomp

    def write_latex(self, target_dir):
        target_path = target_dir / 'story-{}.tex'.format(self.id)
        latex = self.formatter.format(self)
    
    def __repr__(self):
        s = '{}: id={}; name={}; area_comp={:.2f}; area_ncomp={:.2f};'
        return s.format(self.__class__, self.id, self.name, self.area_comp, self.area_ncomp)
