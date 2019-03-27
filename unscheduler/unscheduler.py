import configparser, argparse, re, pdb
from pathlib import Path
from parser import BuildingParser, SubplotParser
from tables import StoryTable, BuildingTable, SubplotBuildingTable, SubplotTable, LotTable
from land import Lot
from worker import Charlie
from parsers import caster


def main():
    root = Path(parse_arguments().directory).absolute()
    schedules = root / 'publisher' / 'schedules'
    out = root / 'publisher' / 'unscheduler'
    defs = get_dict()

    buildings = []
    for model in defs['buildings'].split():
        p = schedules / '{}.txt'.format(model)
        buildings.append(BuildingFactory.get_building(model, p.read_text()))
    buildings.append(BuildingFactory.null_building())

    relations_dict = {caster(id) : buildings.split() for id, buildings in defs['relations'].items()}

    suplots_path = schedules / 'subplots.txt'
    perm_path = schedules / 'area_perm.txt'
    subplots = SubplotFactory.get_subplots(subplots_path.read_text(),
                                           perm_path.read_text(),
                                           buildings, relations_dict)

    project_info = {attr : caster(value) for attr, value in defs['project_info'].items()}
    lot = Lot(subplots, project_info)

    
    

        
    
    


def main():
    root = Path(parse_arguments().directory)
    configs = get_info(root)
    schedules = root / 'publisher' / 'schedules'
    out = root / 'publisher' / 'unscheduler'

    building_paths = [p for p in schedules.iterdir() if p.name in configs['buildings']]
    buildings = BuildingParser(building_paths).buildings #for the love of, change parser to receive a TEXT instead of a list of paths

    subplot_paths = [path for path in paths if path not in building_paths] #wtf is this?
    lot_dict = {key : caster(value) for key, value in project_info['lot'].items()}
    building_dict = construct_dict(project_info, buildings)
    subplots = SubplotParser(subplot_paths, building_dict).subplots
    lot = Lot(subplots, lot_dict)
    lot.calc_all()
    story_tables = [StoryTable(story, root) for story in lot.stories]
    building_tables = [BuildingTable(building, root) for building in buildings if building.model is not 'null']
    subplot_building_table = SubplotBuildingTable(lot, root)
    subplot_table = SubplotTable(subplots, lot, root)
    lot_table = LotTable(lot, root)
    for table in story_tables:
        table.write_latex()
    for table in building_tables:
        table.write_latex()
    subplot_building_table.write_latex()
    subplot_table.write_latex()
    lot_table.write_latex()
    charlie = Charlie(root, out)
    charlie.work()
    #fin

    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', default='.', help='Root directory of project. Must follow the expected folder structure')
    return parser.parse_args()

   
def get_info(root):
    path = root / 'config.ini'
    config = configparser.ConfigParser()
    config.read(path)
    return config

if __name__ == '__main__':
    main()

    
