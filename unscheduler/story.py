
class Story():
    """ Abstraction of a story.
    A story is composed of a name, an id, net computable area and net non-computable area
    Each building has multiple stories"""

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.area_comp = 0.0
        self.area_ncomp = 0.0


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
        str.format(self.id, self.name, self.computable_area, self.non_computable_area)
        return str
