import tables
from factory import BuildingFactory, SubplotFactory, caster
import configparser, argparse, re
from pathlib import Path
from land import Lot
import worker


def main():
    root = Path(parse_arguments().directory).absolute()
    schedules = root / 'publisher' / 'schedules'
    out = root / 'publisher' / 'unscheduler'
    defs = get_defs(root)

    buildings = []
    for model in defs['project_info']['buildings'].split():
        p = schedules / '{}.txt'.format(model)
        buildings.append(BuildingFactory.get_building(model, p.read_text()))
    buildings.append(BuildingFactory.get_null_building())

    subplot_buildings_dict = subplot_building_relations(defs, buildings)
    subplots_path = schedules / 'subplots.txt'
    perm_path = schedules / 'area_perm.txt'
    subplots = SubplotFactory.get_subplots(subplots_path.read_text(),
                                           perm_path.read_text(),
                                           subplot_buildings_dict)
    lot_info = proc_lot_info(defs)                                       
    lot = Lot(subplots, lot_info)

    for building in buildings:
        building.write_latex(out)
    
    lot.write_latex(out)
    write_sheet_chart(out, defs['project_info'])
    worker.Charlie.do(out, out)

def write_sheet_chart(out_path, project_info):
    fmt = tables.SheetChartFormatter()
    target = out_path / 'sheet_chart.tex'
    with target.open('w') as f:
        f.write(fmt.format(project_info))

def subplot_building_relations(defs, buildings):    
    """Return dictionary with subplot id as key and list of buildings as value.
    Used in subplot factory to assign the correct building to each subplot."""
    models_relations = {caster(id) : models.split() for id, models in defs['relations'].items()}
    buildings_dict = {building.model : building for building in buildings}
    relations = {id : [buildings_dict[model] for model in models] for id, models in models_relations.items()}
    return relations
    
def proc_lot_info(defs):
    lot_info = {attr : caster(value) for attr, value in defs['lot_info'].items()}
    lot_info['rec_cov'] = sum(map(float, str(lot_info['rec_cov']).split()))
    lot_info['rec_ncov'] = sum(map(float, str(lot_info['rec_ncov']).split()))
    lot_info['rec_subplots'] = [int(n) for n in str(lot_info['rec_subplots']).split()]
    return lot_info
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', default='.', help='Root directory of project. Must follow the expected folder structure')
    return parser.parse_args()

def get_defs(root):
    path = root / 'config.ini'
    config = configparser.ConfigParser()
    config.read(path)
    return config

if __name__ == '__main__':
    main()

    
