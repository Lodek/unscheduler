"""
Module disposes of factory classes/functions that return Buildings, Lots and Subplots
from Archicad's exported schedule.
"""
import collections, logging, re
from building import Story, Building
from land import Lot, Subplot

logger = logging.getLogger(__name__)

def caster(s):
    """Identify if s is a float, int or a string and cast s to its matching type"""
    is_float = lambda s : True if re.search(r'^[\d,]+\.\d+$', s) else False
    is_int = lambda s : True if re.search(r'^\d+$', s) else False
    if is_float(s):
        s = re.sub(',', '', s)
        return float(s)
    elif is_int(s):
        return int(s)
    else:
        return s
 
class Parser:
    """
    Parser for Archicad schedule export. The result is a sequence of Record objects.
    Each Record is a line in the table, the attributes of record match the headers
    of the table.
    txt - Raw string corresponding to exported schedule
    fields - Sequence of strings, in order, naming the headers in the schedule
    title - boolean indicating the presence of title line
    header - boolean indicating the presence of header line
    """
    def __init__(self, txt, fields, title, header):
        self.txt = txt
        self.fields = fields
        self.title = title
        self.header = header
        self.matrix = []
        self.records = []
    
    @classmethod
    def parse(cls, txt, fields, title=False, header=True):
        p = cls(txt, fields, title, header)
        p.parse_txt()
        p.tablefy()
        logger.debug('Parsed table. Result: {}'.format(p.table))
        return p.table

    def parse_txt(self):
        """From txt (assumed to be Archicad's tab separated schedule)
        remove title and header (if present) and creates a table in a
        list of lists format"""
        lines = [line.strip('\t') for line in self.txt.split('\n')][:-1] #removes trailing ''
        if self.title:
            lines = lines[1:]
        if self.header:
            lines = lines[1:]
        self.matrix = [line.split('\t') for line in lines]

    def tablefy(self):
        """Generator that iterates over rows in texble and converts each element
        to either a float or keeps it as a string. Choice is made through a regex. 
        Yields a namedtuple whose attributes are the same as the passed as parameter"""
        Record = collections.namedtuple('Record', self.fields)
        matrix = [list(map(caster, line)) for line in self.matrix]
        self.table = [Record(*line) for line in matrix]
            
       
class BuildingFactory:
    """
    From the text representation of the 'area-by-story' schedule in an Archicad
    file, return an instance of Building.
    """
    @staticmethod
    def get_building(model, txt):
        logger.info('Getting building of model {}'.format(model))
        txt = txt
        fields = 'story category area'.split()
        table = Parser.parse(txt, fields)
        stories = {record.story : Story(i, record.story) for i, record in enumerate(table)}
        for r in table:
            stories[r.story].add_area(r.area, r.category)
        building = Building(model, list(stories.values()))
        return building

    @staticmethod
    def get_null_building():
        return Building.get_null_building()

class SubplotFactory:
    """
    
    """
    @staticmethod
    def get_subplots(txt_subplots, txt_perm, relations):
        """Receive raw text for subplot schedules, raw text for permeable
        areas, list of buildings, dictionary with relationships
        between subplot id and buildings"""
        logger.info('Call to get subplots')
        table = SubplotFactory._parse_subplots_table(txt_subplots)
        subplots = {record.id : Subplot(*record) for record in table}
        logger.debug('Subplots from table: {}'.format(subplots))
        for id, buildings in relations.items():
            subplots[id].buildings = buildings
        SubplotFactory.parse_perm(txt_perm, subplots)
        for subplot in subplots.values():
            subplot.calc_all()
        result = sorted(subplots.values(), key=lambda subplot: subplot.id)
        logger.info('Result from subplots: {}'.format(result))
        return result
    
    @staticmethod
    def parse_perm(txt, subplots):
        logger.info('Parsing permeable areas table')
        fields = 'id area'.split()
        areas = Parser.parse(txt, fields, header=True)
        for record in areas:
            logger.debug('Assigning permeable area {} to subplot {}'.format(record.id, record.area))
            subplots[record.id].area_perm = record.area

    @staticmethod
    def _parse_subplots_table(txt):
        """Parse subpot defines table.Turn txt into table, rename duplicate records
        by appending number to its name"""
        logger.info('Parsing subplots table.')
        fields = 'id name area'.split()
        table = Parser.parse(txt, fields, header=True)
        name_dict = collections.defaultdict(list)
        for record in table:
            name_dict[record.name].append(record)

        repeated_names = [seq for seq in name_dict.values() if len(seq) > 1]
        unique_names = [seq[0] for seq in name_dict.values() if len(seq) == 1]

        table_new = list(unique_names)
        for sequence in repeated_names:
            for i, record in enumerate(sequence):
                cls = type(record)
                name = '{} {}'.format(record.name, i+1)
                table_new.append(cls(record.id, name, record.area))
        logger.debug('Result: {}'.format(table_new))
        return table_new
