from collections import namedtuple
from argparse import ArgumentParser
from configparser import ConfigParser

class ProjectInfo:
    """
    Class contains processed information extracted from the project's configuration file.
    Load ini file, process the subdicts and assign it to self using named tuples.
    Process buildings and create relations dictionary.
    """
    def __init__(self, ini_file):
        self.path = ini_file
        self._config = ConfigParser()
        self._config.read(self.path)
        self.project = self.parse_project()
        self.misc = self.parse_misc()
        self.topografico = self.parse_topografico()
        self.relations = {}
       
    def attr_factory(self, translation_dict, values_dict):
        factory = namedtuple('Attributes', list(translation_dict.keys()))
        try:
            arguments = {key : values_dict[value] for key, value in translation_dict.items()}
        except KeyError:
            raise KeyError(f'Malformed configuration file. Error while processing {translation_dict}')
        return factory(**arguments)

    def parse_project(self):
        translation = dict(title='titulo', prop='proprietario', start_date='data_inicio')
        d = dict(self._config['projeto'])
        return self.attr_factory(translation, d)

    def parse_topografico(self):
        translation = dict(area_ri='area_ri', quadricula='quadricula', ind_fiscal='ind_fiscal')
        d = dict(self._config['topografico'])
        try:
            d['area_ri'] = float(d['area_ri'])
        except KeyError as e:
            raise KeyError('Missing area_ri field from config file')
        return self.attr_factory(translation, d)

    def parse_misc(self):
        translation = dict(files='arquivos', rec_subplots='sublotes_rec', rec_cob='rec_cob', rec_desc='rec_desc', units='unidades', ca='ca')
        d = dict(self._config['misc'])
        try: 
            d['arquivos'] = d['arquivos'].split()
            d['sublotes_rec'] = [int(element) for element in  d['sublotes_rec'].split()]
            d['rec_cob'] = sum(map(float, d['rec_cob'].split()))
            d['rec_desc'] = sum(map(float, d['rec_desc'].split()))
            d['unidades'] = int(d['unidades'])
            d['ca'] = int(d['ca'])
        except KeyError as e:
            raise KeyError('Missing field from field misc in config file')
        return self.attr_factory(translation, d)
        
    def build_relations(buildings):
        """Produces ictionary with subplot id as key and list of buildings as value.
        Used in subplot factory to assign the correct building to each subplot."""
        relations = {int(id) : models.split() for id, models in self._config['relations'].items()}
        buildings_dict = {building.model : building for building in buildings}
        self.relations = {id : [buildings_dict[model] for model in models] for id, models in self._config['relations'].items()}

   
def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('directory', default='.', help='Root directory of project. Must follow the expected folder structure')
    return parser.parse_args()

def read_texts(self, path):
    """Iterate over path, read all files with .txt in their name, remove
    bytes that equal 0xa0, convert to string and return texts dict
    where key is file name and value is the processed string."""
    texts = {}
    files = [p for p in path.iterdir() if '.txt' in p.name]
    for file in files:
        bs = bytes([b for b in p.read_bytes() if b != 0xa0])
        texts[file.name] = bs.decode(encoding='utf8')
    return texts
