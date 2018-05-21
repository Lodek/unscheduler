import configparser, argparse, re, pdb
from pathlib import Path
from parser import BuildingParser, SubplotParser
from tables import StoryTable, BuildingTable, SubplotBuildingTable, SubplotTable, LotTable
from land import Lot

def main():
    args = parse_arguments()
    root = Path(args.directory)
    paths = [path for path in root.iterdir() if path.is_file()]
    building_paths = [path for path in paths if 'subplot' not in path.name and path.suffix == '.txt']
    subplot_paths = [path for path in paths if 'subplot' in path.name and path.suffix == '.txt']
    project_info = get_info(root)
    buildings = BuildingParser(building_paths).buildings
    building_dict = construct_dict(project_info, buildings)
    subplots = SubplotParser(subplot_paths, building_dict).subplots
    lot = Lot(subplots, project_info['lot'])
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
    #fin

    
def construct_dict(project_info, buildings):
    base_dict = project_info['subplot_mapper']
    building_dict = {key : next(filter(lambda building : value == building.model, buildings)) for key, value in base_dict.items()}
    return building_dict
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', default='.', help='Target directory for unscheduler. Directory must contain the schedules outlined by the documentation')
    return parser.parse_args()

def get_info(root):
    path = root / 'project-info.ini'
    config = configparser.ConfigParser()
    config.read(path)
    return config

if __name__ == '__main__':
    main()

    
