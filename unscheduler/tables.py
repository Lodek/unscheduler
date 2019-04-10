""" This file contains all of the classes responsible for generating the formatted .tex file.
Each type of Table is a subclass of BaseBuilder """

from pathlib import Path

templates_path = Path(__file__).parent / '..' / 'templates'

class LaTexFactory():
    """
    From list of lists formats a latex file
    """
    @classmethod
    def _tabularfy(cls, matrix, headers=True, title=False):
        """Generate simple latex formatting for a latex tabular environment. 
        Returns the contents of the Latex tabular environment as a list of strings.
        title flag indicates whether or not matrix the first row of the matrix
        contais a "title".
        headers flag indicates whether or not the second row (first if there's
        no title) is a row of headers.
        """
        hline = r'\hline'
        tabular = []
        if title:
            tabular.append(cls._format_row(matrix.pop(0)))
        if headers:
            tabular.append(hline)
            tabular.append(cls._format_row(matrix.pop(0)))
        tabular.append(hline)
        tabular.extend([cls._format_row(row) for row in matrix])
        tabular.append(hline)
        return tabular

    @staticmethod
    def _format_row(row):
        """ Takes a list of strings under the assumption that each
        element in that list is a cell in a tabular row. 
        Returns a string with matching latex code for the row """
        code = ' & '.join(row) + r' \\'
        return code

    @classmethod
    def get_latex(cls, matrix, template, args=[], headers=True, title=False):
        """From matrix (which contains the body of the table as a list of lists,
        return string which is the corresponding matrix in a LaTeX format
        inserted into template. Optionally passes *args to format call on template"""
        tabular = '\n'.join(cls._tabularfy(matrix, headers, title))
        return template.format(*args + [tabular])

    
fmt_area = lambda s : '${:.2f}$ m$^2$'.format(s)
fmt_perc = lambda s : '${:.2f}$\%'.format(s)
fmt_float = lambda s : '${:.2f}$'.format(s)

class StoryTableFactory:
    """
    Factory that returns the representation of a Story as a LaTeX table
    """
    @classmethod
    def get_latex(cls, story):
        template_path = templates_path / 'story-template.tex'
        template = template_path.read_text()
        table = cls._build_table(story)
        tex = LaTexFactory.get_latex(table, template, title=True)
        return tex

    @staticmethod
    def _build_table(story):
        title = ['', story.name.upper(), '']
        headers = ['AREA COMP.', 'AREA NAO COMP.', 'TOTAL']
        body = [[fmt_area(story.area_comp), fmt_area(story.area_ncomp), fmt_area(story.total)]]
        return [title, headers] + body


class BuildingTableFactory:
    """
    Factory class that returns the representation of a building as a table in Tex
    """
    @classmethod
    def get_latex(cls, building):
        template_path = templates_path / 'building-template.tex'
        template = template_path.read_text()
        table = cls._build_table(building)
        tex = LaTexFactory.get_latex(table, template)
        return tex
        
    @staticmethod
    def _build_table(building):
        """ Generates tabular list for Building Table """
        headers = ['PAVIMENTO', 'AREA COMP.', 'AREA NAO COMP.']
        formatter = lambda s : [s.name.upper(), fmt_area(s.area_comp), fmt_area(s.area_ncomp)]
        body = [formatter(story) for story in building.stories + [building.super_story]]
        return [headers] + body


class SubplotAreasFactory:
    """

    """
    @classmethod
    def get_latex(cls, lot):
        template_path = templates_path / 'subplot-areas-template.tex'
        template = template_path.read_text()
        table = cls._build_table(lot)
        table_fmt = 'l' * len(table[0])
        args = [table_fmt]
        tex = LaTexFactory.get_latex(table, template, args=args, title=True)
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


class SubplotStatsFactory:
    """ SubplotTable generates the .tex file for the Subplot statistics table. """
    @classmethod
    def get_latex(cls, lot):
        template_path = templates_path / 'subplot-stats-template.tex'
        template = template_path.read_text()
        table = cls._build_table(lot)
        tex = LaTexFactory.get_latex(table, template, headers=False)
        return tex

    @classmethod
    def _build_table(cls, lot):
        headers = ['NOME', 'AREA PROJECAO', 'AREA SUBLOTE', 'TAXA OCUPACAO',
                   'COEF.APROVEITAMENTO', 'AREA PERMEAVEL', 'TAXA PERMEABILIDADE']
        body = [cls._gen_row(sub) for sub in lot.subplots + [lot]]
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

class LotStatsFactory:
    """ LotTable generates the .tex file for the Lot statistics table. """
    @classmethod
    def get_latex(cls, lot):
        template_path = templates_path / 'lot-stats-template.tex'
        template = template_path.read_text()
        table = cls._build_table(lot)
        tex = LaTexFactory.get_latex(table, template, title=True, headers=False)
        return tex

    def _build_table(lot):
        title = ['ESTATISTICAS', '']
        body = [['AREA DO LOTE', fmt_area(lot.area_lot)]]
        body.append(['AREA DO LOTE ATINGIDA', fmt_area(lot.area_useless)])
        body.append(['AREA DO LOTE REMANESCENTE', fmt_area(lot.area_net)])
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

