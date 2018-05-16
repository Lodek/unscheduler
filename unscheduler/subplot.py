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
        self.calc_coef_aprov()
        self.calc_taxa_perm()
        self.calc_taxa_ocp()

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

