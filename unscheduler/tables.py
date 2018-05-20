import pdb

class BaseBuilder():
    def __init__(self):
        self.template = None
        self.tabular = None
        self.latex = None
    
    def latexfy(self):
        latex = [r'\documentclass[11pt]{article}']
        latex.append(r'\begin{document}')
        latex.append(r'\begin{tabular}'+'{'+self.rows*'c'+'}')
        latex.extend(self.tabular)
        latex.append(r'\end{tabular}')
        latex.append(r'\end{document}')
        return latex

    def tabularfy(self, matrix, headers=None):
        """ Generate simple latex formatting for a latex tabular environment. 
        Returns the body and the header in a latex format. """
        format_row = lambda row : ' & '.join(row) + r' \\'
        tabular = [format_row(row) for row in matrix]
        tabular.insert(0, r'\hline')
        if headers:
            temp = [r'\hline', ' & '.join(headers) +r'\\']
            temp.extend(tabular)
            tabular = temp
        tabular.append(r'\hline')
        return tabular

    def write_latex(self, path):
        with path.open('w') as f:
            text = '\n'.join(self.latex)
            f.write(text)


class BuildingTable(BaseBuilder):
    def __init__(self, building, root_path):
        self.building = building
        self.root_path = root_path
        self.rows = 0
        self.tabular = self.build_tabular(building)
        self.latex = self.latexfy()

    def build_tabular(self, building):
        formatter = lambda name, area_comp, area_ncomp : [name, '{:.2f}m2'.format(area_comp), '{:.2f}m2'.format(area_ncomp)]
        matrix = [formatter(story.name, story.area_comp, story.area_ncomp) for story in building.stories]
        matrix.append(formatter('Total', building.area_comp, building.area_ncomp))
        self.rows = len(matrix[0])
        headers = ['PAVIMENTO', 'AREA COMP.', 'AREA NAO COMP.']
        tabular = self.tabularfy(matrix, headers)
        return tabular

    def write_latex(self):
        path = self.root_path / '{}.tex'.format(self.building.model)
        super().write_latex(path)

        
class SubplotBuildingTable(BaseBuilder):
     def __init__(self, subplots, root_path):
        self.subplots = subplots
        self.root_path = root_path
        

class SubplotTable(BaseBuilder):
    def __init__(self, subplots, root_path):
        self.subplots = subplots
        self.root_path = root_path
        self.rows = 0
        self.tabular = self.build_tabular()
        self.latex = self.latexfy()


    def write_latex(self):
        super().write_latex(self.root_path / 'subplot-table.tex')
        
    def build_tabular(self):
        headers = ['NONE', 'AREA PROJECAO', 'AREA DO SUBLOTE', 'TAXA OCUPACAO',
                   'COEF. APROVEITAMENTO', 'AREA PERMEAVEL', 'TAXA PERMEABILIDADE']
        matrix = [self._gen_row(subplot) for subplot in self.subplots]
        self.rows = len(headers)
        tabular = self.tabularfy(matrix, headers)

        return tabular

    def _gen_row(self, subplot):
        row = [subplot.name]
        row.append('{:.2f}'.format(subplot.area_proj))
        row.append('{:.2f}'.format(subplot.area_net))
        row.append('{:.2f}'.format(subplot.taxa_ocp))
        row.append('{:.2f}'.format(subplot.coef_aprov))
        row.append('{:.2f}'.format(subplot.area_perm))
        row.append('{:.2f}'.format(subplot.taxa_perm))
        return row


class LotTable(BaseBuilder):
    def __init__(self, lot, root_path):
        self.lot = lot
        self.root_path = root_path
        self.rows = 0
        self.tabular = self.build_tabular()
        self.latex = self.latexfy()
        self.write_latex = lambda self : super().write_latex(self.root_path / 'lot-table.tex')
        
    def build_tabular(self):
        headers = ['ESTATISTICA', '']
        matrix = [['AREA DO LOTE ORIGINAL', '{:.2f}m2'.format(self.lot.area_lot)]]
        matrix.append(['AREA ANTIGIDA DO LOTE', '{:.2f}m2'.format(self.lot.area_useless)])
        matrix.append(['AREA DO LOTE REAL', '{:.2f}m2'.format(self.lot.area_net)])
        matrix.append(['AREA TOTAL COMPUTAVEL', '{:.2f}m2'.format(self.lot.area_comp)])
        matrix.append(['AREA TOTAL NAO COMPUTAVEL', '{:.2f}m2'.format(self.lot.are_ncomp)])
        matrix.append(['AREA PROJECAO', '{:.2f}m2'.format(self.lot.area_proj)])
        matrix.append(['TAXA DE OCUPACAO', '{:.2f}%'.format(self.lot.taxa_ocp)])
        matrix.append(['COEFICIENTE DE APROVEITAMENTO', '{:.2f}'.format(self.coef_aprov)])
        matrix.append(['AREA PERMEAVEL', '{:.2f}m2'.format(self.lot.area_perm)])
        matrix.append(['COEFICIENTE PERMEABILIDADE', '{:.2f}%'.format(self.lot.coef_perm)])
        matrix.append(['NUMERO DE UNIDADES', '{}UN'.format(self.lot.units)])
        matrix.append(['RECREACAO DESCOBERTA', '{:.2f}m2'.format(self.lot.rec_ncov)])
        matrix.append(['RECREACAO COBERTA', '{:.2f}m2'.format(self.lot.rec_cov)])
        matrix.append(['RECREACAO TOTAL', '{:.2f}m2'.format(self.lot.rec_net)])
        self.rows = len(matrix[0])
        tabular = self.tabularfy(matrix, headers)
        return tabular

    

    
