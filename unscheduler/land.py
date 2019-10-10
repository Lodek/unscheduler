from building import Story, Building
import logging

logger = logging.getLogger(__name__)

class Land:
    """
    Abstract a section of land
    """
    def __init__(self, id, name, area, **kwargs):
        self.id = name
        self.name = name
        self.area = area
        self.area_ri = 0.0
        self.lands = []
        #mutables
        self.area_perm = 0.0
        self.buildings = []
        self.super_building = None
        self.coef_aprov = 0.0
        self.taxa_perm = 0.0
        self.taxa_ocp = 0.0
        for key, value in kwargs.items():
            try:
                getattr(self, key)
                setattr(self, key, value)
            except AttributeError as e:
                msg = f'Error assigning {key} to {self}. Invalid attribute.'
                raise AttributeError(msg) from e
        self.update()
            
    def __repr__(self):
        s = '{}: id={}, name={}, area={}'
        return s.format(self.__class__, self.id, self.name, self.area)
    
    def update(self):
        """Rebuild super_building, update coefficients and rates"""
        self.super_building = Building.get_super_building(self.name, self.buildings)
        self.coef_aprov = self.super_building.area_comp / self.area
        self.taxa_perm = (self.area_perm / self.area) * 100
        self.taxa_ocp = (self.super_building.area_proj / self.area) * 100

    @classmethod
    def from_lands(cls, id, name, lands, **kwargs):
        """Assume lands compose a partition of the Land under creation.
        Return Land object with area equal to the sum of the areas and 
        buildings equal to the superbuildings of all the lands"""
        area = sum(land.area for land in lands)
        super_buildings = [land.super_building for land in lands]
        perm = sum(land.area_perm for land in lands)
        obj = cls(id, name, area, area_perm=perm, lands=lands, buildings=super_buildings, **kwargs)
        return obj


class Site(Land):
    """Builds upon Land and define Site. Site contains properties
    to access 'atingido' and 'remanescente'."""
    ind_fiscal = ''
    quadricula = ''
    @property
    def remanescente(self):
        return self.lands[0]

    @property
    def atingido(self):
        return self.lands[1]
    

class Lot(Land):
    """Lot refeers to the main object of interest in the project.
    Lot is the section of land where the building will actually take place
    Builds upon land and define extra attibutes such as number of units, 
    rec areas and contain a reference to recreation subplots"""
    rec_subplots = []
    units = 0
    rec_cob = 0
    rec_desc = 0
    rec = 0
    ca = 0
    files = []
    @property
    def recreation_subplots(self):
        return [self.lands[n] for n in self.rec_subplots]

    def calc_cm(self):
        """Return CM for the lot"""
        common = self.recreation_subplots + [self.lands[0]]
        ac = sum(sub.area for sub in common)
        cm = self.area / (self.area - ac)
        return cm
