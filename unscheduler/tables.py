""" This file contains all of the classes responsible for generating the formatted .tex file.
Each type of Table is a subclass of BaseBuilder """

from pathlib import Path

templates_path = Path(__file__).parent / '..' / 'templates'
fmt_area = lambda s : '${:.2f}$ m$^2$'.format(s)
fmt_perc = lambda s : '${:.2f}$\%'.format(s)
fmt_float = lambda s : '${:.2f}$'.format(s)

class LatexFormatter:
    """
    Base class with methods to format a table from a list of lists
    into text which can be written into a .tex file and processed.
    """
    template = None
    headers = True
    title = False
    def _tabularfy(self, matrix):
        """Generate simple latex formatting for a latex tabular environment. 
        Returns the contents of the Latex tabular environment as a list of strings.
        title flag indicates whether or not matrix the first row of the matrix
        contais a "title".
        headers flag indicates whether or not the second row (first if there's
        no title) is a row of headers.
        """
        hline = r'\hline'
        tabular = []
        if self.title:
            tabular.append(self._format_row(matrix.pop(0)))
        if self.headers:
            tabular.append(hline)
            tabular.append(self._format_row(matrix.pop(0)))
        tabular.append(hline)
        tabular.extend([self._format_row(row) for row in matrix])
        tabular.append(hline)
        return tabular

    @staticmethod
    def _format_row(row):
        """ Takes a list of strings under the assumption that each
        element in that list is a cell in a tabular row. 
        Returns a string with matching latex code for the row """
        code = ' & '.join(row) + r' \\'
        return code

    def _get_latex(self, matrix, args=[]):
        """From matrix (which contains the body of the table as a list of lists,
        return string which is the corresponding matrix in a LaTeX format
        inserted into template. Optionally passes *args to format call on template"""
        tabular = '\n'.join(self._tabularfy(matrix))
        return self.template.format(*args + [tabular])

    
class StoryFormatter(LatexFormatter):
    """
    An initialized instance of StoryFormatter returns text
    matching a latex file for a Story Table
    """
    template_path = templates_path / 'story-template.tex'
    template = template_path.read_text()
    headers = True
    title = True
    def format(self, story):
        """Format a story object into a latex compatible string representing
        a file ready for compilation"""
        table = self._build_table(story)
        return self._get_latex(table)

    def _build_table(self, story):
        title = ['', story.name.upper(), '']
        headers = ['AREA COMP.', 'AREA NAO COMP.', 'TOTAL']
        body = [[fmt_area(story.area_comp), fmt_area(story.area_ncomp), fmt_area(story.total)]]
        return [title, headers] + body


class BuildingFormatter(LatexFormatter):
    """
    Transform a Building object into a table in the Latex format. Return a string
    which when written to a file can be processed by pdflatex.
    """
    template_path = templates_path / 'building-template.tex'
    template = template_path.read_text()
    headers = True
    title = False
    def format(self, building):
        """Format a building object into a latex compatible string representing
        a file ready for compilation"""
        table = self._build_table(building)
        return self._get_latex(table)
        
    def _build_table(self, building):
        headers = ['PAVIMENTO', 'AREA COMP.', 'AREA NAO COMP.']
        formatter = lambda s : [s.name.upper(), fmt_area(s.area_comp), fmt_area(s.area_ncomp)]
        body = [formatter(story) for story in building.stories + [building.super_story]]
        return [headers] + body


class SubAreasFormatter(LatexFormatter):
    """
    Class that operate on an instance of Lot to generate a string representing
    the Subplot Areas table needed for the building plans.
    """
    title = True
    headers = True
    template_path = templates_path / 'subplot-areas-template.tex'
    template = template_path.read_text()
    def format(self, lot):
        table = self._build_table(lot)
        table_fmt = 'l' * len(table[0])
        args = [table_fmt]
        tex = self._get_latex(table, args)
        return tex
 
    @staticmethod
    def _build_table(lot):
        title = ['']
        for story in lot.super_building.all_stories():
            title.extend([story.name.upper(), ''])
        header = ['SUBLOTE']
        for _ in lot.super_building.all_stories():
            header.extend(['COMP', 'N COMP'])
        body = []
        for s in lot.subplots + [lot]:
            row = []
            row.append(s.name.upper())
            for story in s.super_building.all_stories():
                row.append(fmt_area(story.area_comp))
                row.append(fmt_area(story.area_ncomp))
            body.append(row)
        return [title, header] + body


class SubStatsFormatter(LatexFormatter):
    """Operate on lot to produce the Suplot stats text
    for the Subplot stats table
    """
    template_path = templates_path / 'subplot-stats-template.tex'
    template = template_path.read_text()
    headers = False
    title = False
    def format(self, lot):
        table = self._build_table(lot)
        return self._get_latex(table)

    def _build_table(self, lot):
        headers = ['NOME', 'AREA PROJECAO', 'AREA SUBLOTE', 'TAXA OCUPACAO',
                   'COEF.APROVEITAMENTO', 'AREA PERMEAVEL', 'TAXA PERMEABILIDADE']
        body = [self._gen_row(sub) for sub in lot.subplots + [lot]]
        return body

    @staticmethod
    def _gen_row(s):
        row = [s.name.upper()]
        row.append(fmt_area(s.area_proj))
        row.append(fmt_area(s.area_net))
        row.append(fmt_perc(s.taxa_ocp))
        row.append(fmt_float(s.coef_aprov))
        row.append(fmt_area(s.area_perm))
        row.append(fmt_perc(s.taxa_perm))
        return row


class LotStatsFormatter(LatexFormatter):
    """
    Operate on lot to return the text for the Lot statistics table.
    """
    template_path = templates_path / 'lot-stats-template.tex'
    template = template_path.read_text()
    headers = True
    title = False
    def format(self, lot):
        """Operate on lot and return the lot-stats.tex file text"""
        table = self._build_table(lot)
        return self._get_latex(table)

    def _build_table(self, lot):
        title = ['ESTATISTICAS', '']
        body = []
        body.append(['AREA DO LOTE - RI', fmt_area(lot.area_ri)])
        body.append(['AREA DO LOTE REAL', fmt_area(lot.net_area)])
        body.append(['AREA DO LOTE ATINGIDA', fmt_area(lot.useless_area)])
        body.append(['AREA DO LOTE REMANESCENTE', fmt_area(lot.area)])
        body.append(['AREA TOTAL COMPUTAVEL', fmt_area(lot.area_comp)])
        body.append(['AREA TOTAL NAO COMPUTAVEL', fmt_area(lot.area_ncomp)])
        body.append(['AREA PROJECAO', fmt_area(lot.area_proj)])
        body.append(['TAXA DE OCUPACAO', fmt_perc(lot.taxa_ocp)])
        body.append(['COEFICIENTE DE APROVEITAMENTO', fmt_float(lot.coef_aprov)])
        body.append(['AREA PERMEAVEL', fmt_area(lot.area_perm)])
        body.append(['COEFICIENTE PERMEABILIDADE', fmt_perc(lot.taxa_perm)])
        body.append(['NUMERO DE UNIDADES', '{} UN'.format(lot.units)])
        body.append(['RECREACAO DESCOBERTA', fmt_area(lot.rec_ncov)])
        body.append(['RECREACAO COBERTA', fmt_area(lot.rec_cov)])
        body.append(['RECREACAO TOTAL', fmt_area(lot.rec_net)])
        return [title] + body

class TOSFormatter(LatexFormatter):
    """TOS calculation latex file"""
    template_path = templates_path / 'tos-template.tex'
    template = template_path.read_text()
    title = False
    headers = False
    def format(self, lot):
        """Operate on lot and return the tos-stats.tex file text"""
        args = [fmt_float(lot.cm), fmt_perc(lot.tos)]
        return self._get_latex([], args=args)

    
class SheetChartFormatter(LatexFormatter):
    """Formatter that generate the tex for the information chart present
    in every building plan sheet."""
    template_path = templates_path / 'sheet-chart-template.tex'
    template = template_path.read_text()
    title = False
    headers = False
    def format(self, project_info):
        "Return the tex text for the information chart"
        init_month, init_year = project_info['inicio'].split('/')
        args = [init_month, init_year, project_info['titulo'], project_info['prop']]
        return self._get_latex([], args=args)

   
