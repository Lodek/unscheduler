
class Lot(Land):
    """ Abstraction for an Archicad land plot.
    Land is built from subplots and data intrinsic to it """

    def __init__(self):
        super().__init__()
        self.area_lot = 0.0
        self.area_useless = 0.0
        self.subplots = []
        self.units = 0
        self.rec_ncov = 0.0
        self.rec_cov = 0.0
        self.rec_net = 0.0

        
    def __len__(self):
        """ Returns the ammount of subplots """
        return len(self.subplots)
