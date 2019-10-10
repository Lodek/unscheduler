from tables import SubAreasFormatter, SubStatsFormatter, SiteFormatter, LotStatsFormatter, TOSFormatter
from aux import ProjectInfo, parse_arguments, read_texts, Charlie
from factory import BuildingFactory, SubplotFactory, SiteFactory
from pathlib import Path
from land import Lot

def main():
    args = parse_arguments()
    root = Path(args.directory).absolute()
    schedules = root / 'publisher' / 'schedules'
    out = root / 'publisher' / 'unscheduler'
    project_info = ProjectInfo(root/'config.ini')
    texts = read_texts(schedules)

    site = SiteFactory(texts['topografico.txt'], project_info)
    buildings = BuildingFactory.get_buildings(texts, project_info.misc.files) 
    project_info.build_relations(buildings)
    subplots = SubplotFactory.get_subplots(texts['subplots.txt'], texts['area_perm.txt'], project_info.relations)
    lot = Lot.from_lands(0, 'lote', subplots, **project_info.misc._asdict())
    write_tables(site, lot, buildings, out)
    Charlie.do(out, out)

def write_tables(site, lot, buildings, out):
    with (out / 'topografico.tex').open('w') as f:
        f.write(SiteFormatter().format(site))

    for building in buildings:
        building.write_latex(out)
 
    with (out / 'subplot-areas.tex').open('w') as f:
        f.write(SubAreasFormatter().format(lot))

    with (out / 'suplot-stats.tex').open('w') as f:
        f.write(SubStatsFormatter().format(lot))
   
    with (out / 'lot-stats.tex').open('w') as f:
        f.write(LotStatsFormatter().format(site, lot))

    with (out / 'tos.tex').open('w') as f:
        f.write(TOSFormatter().format(lot))

if __name__ == '__main__':
    main()

    
