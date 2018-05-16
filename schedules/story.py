
class Story():
    """ Abstraction of a story.
    A story is abstracted through it's name, id, computable area and non computable area
    Each building has multiple stories"""

    def __init__(self):
        self.id = -1
        self.name = ''
        self.area_comp = 0.0
        self.area_ncomp = 0.0

    def __repr__(self):
        str = 'ID: {}, Name: {}, Area_C: {:.2f}m2, Area_NC: {:.2f}m2'
        str.format(self.id, self.name, self.computable_area, self.non_computable_area)
        return str
