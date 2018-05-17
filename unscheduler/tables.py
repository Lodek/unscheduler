
class ArchicadTableParser():
    """ Receives a file object for an archicad building text schedule and returns the parsed data """
    def __init__(self, f):
        clean = lambda name : name.replace(' ', '_').lower()
        self.texble = [line[:-2].split('\t') for line in f]
        self.headers = self.texble[0]
        self.attributes = [clean(header) for header in self.headers]
        self.matrix = np.array(self.texble[1:])
        self.header_dim = 'x'
        


class mrStoryTable(MrTable):
    pass

class mrSubplotTable(MrTable):
    pass

class mrLotTable(MrTable):
    pass
