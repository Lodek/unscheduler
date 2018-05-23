""" This file contains all of the classes responsible for generating the formatted .tex file.
Each type of Table is a subclass of BaseBuilder """

import pdb
from pathlib import Path

class BaseBuilder():
    
    """ Base class for Table classes."""

    #temporary assumption of where templates will reside
    template_root = Path(__file__).parent / '..' / 'templates'    

    def __init__(self):
        """ Outlines attributes needed by the methods implemented in BaseBuilder.
        -self.output_path: points to the output .tex file.
        -self.template_path: points to a file containg the Latex template for that class
        -self.tabular: is a list where each element is a line in the latex file
        (equivalent to a latex formatted row).
        -self.latex: contains the formatted latex text that will be written to self.output """
        self.output_path = None
        self.template_path = None
        self.tabular = None
        self.latex = None

    @staticmethod
    def tabularfy(matrix, headers=None):
        """ Generate simple latex formatting for a latex tabular environment. 
        Returns the contents of the Latex tabular environment as a list of strings.
        Optionally it takes a list of strings to be used as 'headers'.
        Headers are placed as the first row in the table and
        separated from its body by an hline element"""
        hline = r'\hline'
        format_row = lambda row : ' & '.join(row) + r' \\'
        tabular = [format_row(row) for row in matrix]
        tabular.insert(0, hline)
        if headers:
            tabular.insert(0, format_row(headers))
            tabular.insert(0, hline)
        tabular.append(hline)
        return tabular

    @staticmethod
    def format_row(row):
        """ Takes a list of strings under the assumption that each
        element in that list is a cell in a tabular row. 
        Returns a string with matching latex code for the row """
        code = ' & '.join(row) + r' \\'
        return code

    def latexfy(self, *args):
        """ Generates self.latex. Essentially opens self.template_path, inserts argumetns in template using .format()
        and returns self.latex. """
        with self.template_path.open() as f:
            template = f.read()
        latex = template.format(*args)
        return latex

    def write_latex(self):
        """ Opens self.output_path as 'w' and writes self.latex. """
        with self.output_path.open('w') as f:
            f.write(self.latex)


class BuildingTable(BaseBuilder):

    """ BuildingTable generates the .tex file for any Building class. """
    
    def __init__(self, building, root_path):
        self.template_path = self.template_root / 'building-table-template.tex'
        self.output_path = root_path / '{}.tex'.format(building.model)
        self.building = building
        self.tabular = self.build_tabular(building)
        self.tabular_str = '\n'.join(self.tabular)
        self.latex = self.latexfy(self.tabular_str)

    def build_tabular(self, building):
        """ Generates tabular list for Building Table """
        formatter = lambda name, area_comp, area_ncomp : [name, '${:.2f}$ m$^2$'.format(area_comp), '${:.2f}$ m$^2$'.format(area_ncomp)]
        matrix = [formatter(story.name, story.area_comp, story.area_ncomp) for story in building.stories]
        matrix.append(formatter('Total', building.area_comp, building.area_ncomp))
        headers = ['PAVIMENTO', 'AREA COMP.', 'AREA NAO COMP.']
        tabular = self.tabularfy(matrix, headers)
        return tabular


class SubplotBuildingTable(BaseBuilder):
    def __init__(self, lot, root_path):
        self.template_path = self.template_root / 'subplot-building-table-template.tex'
        self.output_path = root_path / 'subplot-building-table.tex'
        self.lot = lot
        self.tabular_specs = ''
        self.tabular = self.build_tabular()
        self.tabular_str = '\n'.join(self.tabular)
        self.latex = self.latexfy(self.tabular_specs, self.tabular_str)

    def build_tabular(self):
        story_names = [story.name.upper() for story in self.lot.stories]
        num_stories = len(self.lot.stories)
        multirow = lambda cell : '\multicolumn{{2}}{{c}}{{{}}}'.format(cell)
        stringfy = lambda s : '${:.2f}$ m$^2$'.format(s)
        latex_stories = [multirow(name) for name in story_names]
        latex_stories.append(multirow('TOTAL'))
        latex_stories.insert(0, '')
        latex_stories = self.format_row(latex_stories)
        subplots = self.lot.subplots
        headers = ['SUBLOTE']
        for i in range(num_stories+1):
            headers.extend(['COMP', 'N. COMP'])
        matrix = []
        for subplot in subplots:
            row = [subplot.name]
            for i in range(num_stories):
                row.append(stringfy(subplot.building[i].area_comp))
                row.append(stringfy(subplot.building[i].area_ncomp))
            row.append(stringfy(subplot.area_comp))
            row.append(stringfy(subplot.area_ncomp))
            matrix.append(row)
        row = ['TOTAL']
        for story in self.lot.stories:
            row.append(stringfy(story.area_comp))
            row.append(stringfy(story.area_ncomp))
        row.append(stringfy(self.lot.area_comp))
        row.append(stringfy(self.lot.area_ncomp))
        matrix.append(row)
        tabular = self.tabularfy(matrix, headers)
        tabular.insert(0, latex_stories)
        self.tabular_specs = 'l' + 'c'*2*(num_stories+1)
        return tabular
        

class SubplotTable(BaseBuilder):

    """ SubplotTable generates the .tex file for the Subplot statistics table. """
    
    def __init__(self, subplots, lot, root_path):
        self.template_path = self.template_root / 'subplot-table-template.tex'
        self.output_path = root_path / 'subplot-table.tex'
        self.subplots = subplots
        self.lot = lot
        self.tabular = self.build_tabular()
        self.tabular_str = '\n'.join(self.tabular)
        self.latex = self.latexfy(self.tabular_str)

    def build_tabular(self):
        """ Generates tabular list for Building Table """
        #for context only, headers are now included in template
        headers = ['NOME', 'AREA PROJECAO', 'AREA SUBLOTE', 'TAXA OCUPACAO',
                   'COEF.APROVEITAMENTO', 'AREA PERMEAVEL', 'TAXA PERMEABILIDADE']
        matrix = [self._gen_row(subplot) for subplot in self.subplots]
        matrix.append(self._gen_total())
        tabular = self.tabularfy(matrix)
        return tabular

    def _gen_total(self):
        total = ['TOTAL']
        total.append('${:.2f}$ m$^2$'.format(self.lot.area_proj))
        total.append('${:.2f}$ m$^2$'.format(self.lot.area_net))
        total.append('${:.2f}$\%'.format(self.lot.taxa_ocp))
        total.append('${:.2f}$'.format(self.lot.coef_aprov))
        total.append('${:.2f}$ m$^2$'.format(self.lot.area_perm))
        total.append('${:.2f}$\%'.format(self.lot.taxa_perm))
        return total
    
    def _gen_row(self, subplot):
        row = [subplot.name]
        row.append('${:.2f}$ m$^2$'.format(subplot.area_proj))
        row.append('${:.2f}$ m$^2$'.format(subplot.area_net))
        row.append('${:.2f}$\%'.format(subplot.taxa_ocp))
        row.append('${:.2f}$'.format(subplot.coef_aprov))
        row.append('${:.2f}$ m$^2$'.format(subplot.area_perm))
        row.append('${:.2f}$\%'.format(subplot.taxa_perm))
        return row


class LotTable(BaseBuilder):

    """ LotTable generates the .tex file for the Lot statistics table. """
    
    def __init__(self, lot, root_path):
        self.template_path = self.template_root / 'lot-table-template.tex'
        self.output_path = root_path / 'lot-table.tex'
        self.lot = lot
        self.tabular = self.build_tabular()
        self.tabular_str = '\n'.join(self.tabular)
        self.latex = self.latexfy(self.tabular_str)
        
    def build_tabular(self):
        headers = ['ESTATISTICAS', '']
        matrix = [['AREA DO LOTE ORIGINAL', '${:.2f}$ m$^2$'.format(self.lot.area_lot)]]
        matrix.append(['AREA ANTIGIDA DO LOTE', '${:.2f}$ m$^2$'.format(self.lot.area_useless)])
        matrix.append(['AREA DO LOTE REAL', '${:.2f}$ m$^2$'.format(self.lot.area_net)])
        matrix.append(['AREA TOTAL COMPUTAVEL', '${:.2f}$ m$^2$'.format(self.lot.area_comp)])
        matrix.append(['AREA TOTAL NAO COMPUTAVEL', '${:.2f}$ m$^2$'.format(self.lot.area_ncomp)])
        matrix.append(['AREA PROJECAO', '${:.2f}$ m$^2$'.format(self.lot.area_proj)])
        matrix.append(['TAXA DE OCUPACAO', '${:.2f}$\%'.format(self.lot.taxa_ocp)])
        matrix.append(['COEFICIENTE DE APROVEITAMENTO', '${:.2f}$'.format(self.lot.coef_aprov)])
        matrix.append(['AREA PERMEAVEL', '${:.2f}$ m$^2$'.format(self.lot.area_perm)])
        matrix.append(['COEFICIENTE PERMEABILIDADE', '${:.2f}$\%'.format(self.lot.taxa_perm)])
        matrix.append(['NUMERO DE UNIDADES', '{} UN'.format(self.lot.units)])
        matrix.append(['RECREACAO DESCOBERTA', '${:.2f}$ m$^2$'.format(self.lot.rec_ncov)])
        matrix.append(['RECREACAO COBERTA', '${:.2f}$ m$^2$'.format(self.lot.rec_cov)])
        matrix.append(['RECREACAO TOTAL', '${:.2f}$ m$^2$'.format(self.lot.rec_net)])
        tabular = self.tabularfy(matrix, headers)
        return tabular

class StoryTable(BaseBuilder):

    """ Table for total area for a single story in Lot """

    def __init__(self, story, root_path):
        self.template_path = self.template_root / 'story-table-template.tex'
        self.output_path = root_path / 'story-{}-table.tex'.format(story.name)
        self.story = story
        self.tabular = self.build_tabular()
        self.tabular_str = '\n'.join(self.tabular)
        self.latex = self.latexfy(self.tabular_str)

    def build_tabular(self):
        matrix = [['AREA COMP.', '${:.2f}$ m$^2$'.format(self.story.area_comp)]]
        matrix.append(['AREA NAO COMP.', '${:.2f}$ m$^2$'.format(self.story.area_ncomp)])
        tabular = self.tabularfy(matrix)
        return tabular
