
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

    def __init__(self, subplots, project_info):
        super().__init__()
        self.area_lot = 0.0
        self.area_useless = 0.0
        self.units = 0
        self.rec_ncov = 0.0
        self.rec_cov = 0.0
        self.rec_net = 0.0
        self.subplots = subplots
        for key, value in project_info.items():
            setattr(self, key, value)

    def calc_all(self):
        self.area_net = sum([subplot.area_net for subplot in self.subplots])
        self.area_perm = sum([subplot.area_perm for subplot in self.subplots])
        self.area_comp = sum([subplot.area_comp for subplot in self.subplots])
        self.area_ncomp = sum([subplot.area_ncomp for subplot in self.subplots])
        self.area_proj = sum([subplot.area_proj for subplot in self.subplots])
        super().calc_all()

    def __len__(self):
        """ Returns the ammount of subplots """
        return len(self.subplots)

class Subplot(Land):

    def __init__(self, id, name, area_net, building=None):
        super().__init__()
        self.id = id
        self.area_net = area_net
        self.name = name
        self.building = building
        
    def calc_all(self):
        self.area_comp = self.building.area_comp
        self.area_ncomp = self.building.area_ncomp
        self.area_proj = self.building.area_proj
        super().calc_all()
        
    def __repr__(self):
        str = 'id: {}, name: {}, building model: {} \nNet Area: {}'
        str = str.format(self.id, self.name, self.building.model, self.area_net)
        return str
