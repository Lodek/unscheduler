import pdb
from building import Story
import parsers

class Land():
    """
    Base class for a piece of Land. 
   Land has attributes for its areas, coeficients and rates
    """
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
        """Calculates the coef aprov for the instance"""
        return self.area_comp/self.area_net

    def calc_taxa_perm(self):
        """Calculates the Land's permeability rate"""
        return (self.area_perm / self.area_net) * 100.0

    def calc_taxa_ocp(self):
        """Calculates the Land's ocp rate"""
        return (self.area_proj / self.area_net)*100.0

    def calc_all(self):
        """Updates all of the instance's rates and coeffs."""
        self.coef_aprov = self.calc_coef_aprov()
        self.taxa_perm = self.calc_taxa_perm()
        self.taxa_ocp = self.calc_taxa_ocp()

    def gen_super_building(self, buildings):
        """Create super building whose areas are the sum of all the buildings
        in the buildings."""
        if not buildings:
            self.super_building = parsers.BuildingFactory.null_building()
            return
        stories_len = max(map(len, buildings))
        stories = [Story(i, i) for i in range(stories_len)]
        for i, story in enumerate(stories):
            for building in buildings:
                try:
                    story.add_area(building[i].area_comp, 'C')
                    story.add_area(building[i].area_ncomp, 'NC')
                except IndexError:
                    pass
        self.super_building = Building('Super building', stories)

        
class Lot(Land):
    """
    Abstraction for an architectural plot. A plot is the whole of the land
    on which the buildings are planned.
    Land is divided into subplots and data intrinsic to it.
    """
    def __init__(self, subplots, project_info):
        super().__init__()
        self.area_lot = 0.0
        self.area_useless = 0.0
        self.units = 0
        self.rec_ncov = 0.0
        self.rec_cov = 0.0
        self.rec_net = 0.0
        self.super_building = None
        self.subplots = subplots
        for key, value in project_info.items():
            setattr(self, key, value)

    def calc_all(self):
        sum_attr = lambda attr : sum(getattr(element, attr) for element in self.subplots)
        self.gen_super_building(subplot.super_building for subplot in self.subplots)
        self.area_net = sum_attr('area_net')
        self.area_perm = sum_attr('area_perm')
        self.area_comp = sum_attr('area_comp')
        self.area_ncomp = sum_attr('area_ncomp')
        self.area_proj = sum_attr('area_proj')
        self.rec_net = self.rec_ncov + self.rec_cov
        super().calc_all()

       
    def __len__(self):
        """ Returns the ammount of subplots """
        return len(self.subplots)

class Subplot(Land):
    """
    Lot is divided into Subplots. Subplot may have one or more buildings,
    the usual area attributes and a net area. 
    """
    def __init__(self, id, name, area_net, buildings=[]):
        super().__init__()
        self.id = id
        self.area_net = area_net
        self.name = name
        self.buildings = buildings
        self.super_building = None

    def calc_all(self):
        self.gen_super_building(self.buildings)
        self.area_comp = self.super_building.area_comp
        self.area_ncomp = self.super_building.area_ncomp
        self.area_proj = self.super_building.area_proj
        super().calc_all()
        
    def __repr__(self):
        str = 'id: {}, name: {}, buildings: {} \nNet Area: {}'
        str = str.format(self.id, self.name, self.buildings, self.area_net)
        return str
