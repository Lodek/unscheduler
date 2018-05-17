
class Land():
    """ Base class for a piece of Land. 
    Land has attributes for its areas, coeficients and rates """
    def __init__(self):
        self.area_net = 0.0
        self.area_perm = 0.0
        self.area_comp = 0.0
        self.area_ncomp = 0.0
        self.area_proj = 0.0
        self.coef_aprov = 0.0
        self.taxa_perm = 0.0
        self.taxa_ocp = 0.0

    def calc_coef_aprov(self):
        """ Calculates the coef aprov for the instance """
        coef = self.area_comp/self.area_net
        return coef

    def calc_taxa_perm(self):
        """ Calculates the Land's permeability rate """
        rate = self.area_perm / self.area_net
        return rate

    def calc_taxa_ocp(self):
        """ Calculates the Land's ocp rate """
        rate = self.area_proj / self.area_net
        return rate

    def calc_all(self):
        """ Updates all of the instance's rates and coeffs. """
        self.coef_aprov = self.calc_coef_aprov()
        self.taxa_perm = self.calc_taxa_perm()
        self.taxa_ocp = self.calc_taxa_ocp()

        
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


class Subplot(Land):

    def __init__(self):
        super().__init__()
        self.id = -1
        self.name = ''
        self.building = None

    def __repr__(self):
        str = 'id: {}, name: {}, building model: {} \nNet Area: {}'
        str.format(self.id, self.name, self.building.model, self.area_net)
        return str

