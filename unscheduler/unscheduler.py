import configparser, argparse, re, pdb
from pathlib import Path
from parser import BuildingParser, SubplotParser
from tables import StoryTable, BuildingTable, SubplotBuildingTable, SubplotTable, LotTable
from land import Lot
from worker import Charlie

def main():
    args = parse_arguments()
    root = Path(args.directory)
    out = Path(args.output)
    paths = [path for path in root.iterdir() if path.is_file()]
    building_paths = [path for path in paths if 'subplot' not in path.name and path.suffix == '.txt']
    subplot_paths = [path for path in paths if 'subplot' in path.name and path.suffix == '.txt']
    project_info = get_info(root)
    lot_dict = {key : caster(value) for key, value in project_info['lot'].items()}
    buildings = BuildingParser(building_paths).buildings
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

    
def construct_dict(project_info, buildings):
    base_dict = project_info['subplot_mapper']
    building_dict = {int(key) : next(filter(lambda building : value == building.model, buildings)) for key, value in base_dict.items()}
    return building_dict
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', default='.', help='Directory for unscheduler. Directory must contain the schedules outlined by the documentation')
    parser.add_argument('-o', '--output', default='.', help='Output directory for unscheduler. Pdf files will be written to it')
    return parser.parse_args()

def caster(element):
    is_float = lambda element : True if re.search(r'^\d+\.\d+$', element) else False
    is_int = lambda element : True if re.search(r'^\d+$', element) else False
    if is_float(element):
        new_element = float(element)
    elif is_int(element):
        new_element = int(element)
    else:
        new_element = element
    return new_element
    

def get_info(root):
    path = root / 'project-info.ini'
    config = configparser.ConfigParser()
    config.read(path)
    return config

if __name__ == '__main__':
    main()

    
