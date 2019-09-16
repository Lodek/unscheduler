from building import Story, Building
import logging
import tables

logger = logging.getLogger(__name__)

class Land():
    """
    Base class for a piece of Land. 
    Land has attributes for its areas, coeficients and rates
    """
    area_net = 0.0
    area_perm = 0.0
    area_comp = 0.0
    area_ncomp = 0.0
    area_proj = 0.0
    coef_aprov = 0.0
    taxa_perm = 0.0
    taxa_ocp = 0.0

    def calc_coef(self):
        """Updates all of the instance's rates and coeffs."""
        logger.info('Calc all call from {}'.format(self))
        self.coef_aprov = self.area_comp/self.area_net
        self.taxa_perm = (self.area_perm / self.area_net) * 100
        self.taxa_ocp = (self.area_proj / self.area_net)*100


class Subplot(Land):
    """
    Lot is divided into Subplots. Subplot may have one or more buildings,
    the usual area attributes and a net area. 
    """
    def __init__(self, id, name, area_net, buildings=[]):
        self.id = id
        self.area_net = area_net
        self.name = name
        self.buildings = buildings
        self.super_building = Building.get_super_building(name, buildings)
        self.calc_all()

    def calc_all(self):
        self.super_building = Building.get_super_building(self.name, self.buildings)
        self.area_comp = self.super_building.area_comp
        self.area_ncomp = self.super_building.area_ncomp
        self.area_proj = self.super_building.area_proj
        super().calc_coef()
        
    def __repr__(self):
        str = 'Subplot: id={}; name={}; buildings={}; Net Area={}'
        str = str.format(self.id, self.name, self.buildings, self.area_net)
        return str


class Lot(Land):
    """
    Abstraction for an architectural plot. A plot is the whole of the land
    on which the buildings are planned.
    Land is divided into subplots and data intrinsic to it.
    """
    sub_stats_formatter = tables.SubStatsFormatter()
    sub_areas_formatter = tables.SubAreasFormatter()
    lot_stats_formatter = tables.LotStatsFormatter()
    tos_formatter = tables.TOSFormatter()
    def __init__(self, subplots, lot_info):
        self.name = 'total'
        self.useless_subplots = [subplots[n] for n in lot_info['sublotes_atingidos']]
        self.rec_subplots = [subplots[n] for n in lot_info['sublotes_rec']]
        self.common_subplots = self.rec_subplots + [subplots[0]]
        self.unit_subplots = [sub for sub in subplots if sub not in self.common_subplots + self.useless_subplots]
        self.subplots = self.unit_subplots + self.common_subplots
        
        self.area_ri = lot_info['area_ri']
        self.area= sum(s.area_net for s in self.common_subplots + self.unit_subplots)
        self.useless_area = sum(s.area_net for s in self.useless_subplots)
        self.net_area = self.area + self.useless_area

        self.units = lot_info['unidades']

        self.rec_ncov = lot_info['rec_desc']
        self.rec_cov = lot_info['rec_cob']
        self.rec_net = self.rec_ncov + self.rec_cov

        self.super_building = Building.get_super_building('lot-super-building', [subplot.super_building for subplot in self.subplots])
        sum_attr = lambda attr : sum(getattr(element, attr) for element in self.subplots)
        self.ca = lot_info['ca']
        self.area_perm = sum_attr('area_perm')
        self.area_comp = sum_attr('area_comp')
        self.area_ncomp = sum_attr('area_ncomp')
        self.area_proj = sum_attr('area_proj')
        self.cm = self._calc_cm()
        self.tos = self.ca * self.cm

        self.coef_aprov = self.area_comp/self.area
        self.taxa_perm = (self.area_perm / self.area) * 100
        self.taxa_ocp = (self.area_proj / self.area) * 100


    def _calc_cm(self):
        """Return CM for the lot"""
        area_comum = sum(sub.area_net for sub in self.common_subplots)
        cm = self.area / (self.area - area_comum)
        return cm

    def write_latex(self, target_dir):
        """Write latex tables for Subplot Stats table, Subplot Areas,
        Lot Stats and Lot super building table."""
        self.super_building.write_latex(target_dir)
        for story in self.super_building.all_stories():
            story.write_latex(target_dir)

        p_sub_area = target_dir / 'subplot-areas.tex'
        p_sub_stats = target_dir / 'subplot-stats.tex'
        p_lot_stats = target_dir / 'lot-stats.tex'
        p_tos = target_dir / 'tos.tex'

        funcs = [self.sub_areas_formatter.format,
                 self.sub_stats_formatter.format,
                 self.lot_stats_formatter.format,
                 self.tos_formatter.format]
        ps = [p_sub_area, p_sub_stats, p_lot_stats, p_tos]

        for p, func in zip (ps, funcs):
            latex = func(self)
            with p.open('w') as f:
                f.write(latex)

    def __len__(self):
        """ Returns the ammount of subplots """
        return len(self.subplots)

