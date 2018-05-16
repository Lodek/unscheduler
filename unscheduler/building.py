
class Building():
    """ Abstraction for a building plan from Archicad.
    A building plan can be thought of as a group of areas and stories. """
    
    def __init__(self):
        self.model = ''
        self._stories = []
        self.area_comp = 0.0
        self.area_ncomp = 0.0
        self.area_proj = 0.0
        self._calc_net_area()
        self._calc_area_proj()

    @classmethod
    def get_from_text(cls, f):
        """ Construct a Building object from a text file
        It parses the text file, retrieves the Story objects associated to it
        and does the nescessary computations to initialize the Building object """
        self = cls()
        table = ArchicadTableParser(f)
        self._stories = [Story(id=i, name=story_name) for i, story_name in enumerate(table.stories)]


    def _calc_area_proj(self):
        """ Iterates over stories to find the Projection Area """
        areas = [story.area_comp for story in self._stories]
        return max(areas)
    
    @property
    def stories(self):
        """ Returns an iterator that iterates over Story objects in Building """
        return iter(self._stories)

    def _calc_net_area(self):
        """ Calculate the net areas for Building object"""
        for story in self._stories:
            self.area_comp += story.area_comp
            self.area_ncomp += story.area_ncomp
    
    def __getitem__(self, key):
        """ Returns the Story object by index """
        return self._stories[key]

    def __len__(self):
        """ Number of stories in building """
        return len(self._stories)
    
    def __repr__(self):
        str = 'Model: {}, Stories: {}\nArea_C: {}m2\tArea_NC {}m2'
        str.format(self.model, len(self), self.area_comp, self.area_ncomp)
        return str
        
