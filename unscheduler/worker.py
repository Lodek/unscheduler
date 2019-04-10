"""Module with runner class to generate run pdflatex and generate PDFs"""
from subprocess import run
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Charlie():
    """
    Charlie works
    """
    @classmethod
    def do(cls, work_dir, out_path):
        """Wrapper method for Charlie, work_dir is a Path object with tex files,
        out_path is a Path with the destination of the pdf files"""
        charlie = cls(work_dir, out_path)
        charlie.pdfy()
        charlie.clean()
        
    def __init__(self, work_dir, out_path):
        self.work_dir = work_dir
        self.out_path = out_path
        logger.info(repr(self))

    def __repr__(self):
        s = '{}: work_dir={}; out_path={};'
        return s.format(self.__class__, self.work_dir, self.out_path)
        
    def clean(self):
        """Remove all .aux, .log and .tex files from work_dir and out_path"""
        logger.info('Charlie, CLEAN!')
        rm_suffixes = '.aux .log .tex'.split()
        kill_list = [p for p in self.out_path.iterdir() if p.suffix in rm_suffixes]
        kill_list_2 = [p for p in self.work_dir.iterdir() if p.suffix in rm_suffixes]
        for path in kill_list + kill_list_2:
            command = ['rm', str(path.absolute())]
            logger.debug('Removing {}'.format(path.name))
            run(command)
            
    def pdfy(self):
        """Run pdflatex on every .tex file in work_dir, send outputs to out_path"""
        logger.info('Charlie, PDFY!')
        targets = [path for path in self.work_dir.iterdir() if path.suffix == '.tex']
        for path in targets:
            command = ['pdflatex', '-output-directory', str(self.out_path.absolute()), str(path.absolute())]
            logger.debug('Converting {}'.format(path.name))
            run(command)
