
class Building():
    """ Abstraction for a building plan from Archicad.
    A building plan can be thought of as a group of areas and stories. """
    
    def __init__(self):
        self.model = ''
        self._stories = []
        self.area_comp = 0.0
        self.area_ncomp = 0.0
        self._calc_net_area()

    @classmethod
    def get_from_text(cls, text):
        """ Construct a Building object from a text file
        It parses the text file, retrieves the Story objects associated to it
        and does the nescessary computations to initialize the Building object """
        pass

    @property
    def stories(self):
        """ Returns an iterator that iterates over Story objects in Building """
        pass

    def _calc_net_area(self):
        """ Calculate the net areas for Building object"""
        for story in self._stories:
            self.area_comp += story.area_comp
            self.area_ncomp += story.area_ncomp
    
    def __getitem__(self):
        """ Returns the Story object by index """
        pass

    def __len__(self):
        """ Number of stories in building """
        return len(self._stories)
    
    def __repr__(self):
        str = 'Model: {}, Stories: {}\nArea_C: {}m2\tArea_NC {}m2'
        str.format(self.model, len(self), self.area_comp, self.area_ncomp)
        return str
        
