from pathlib import Path
from subprocess import run

class Charlie():
    def __init__(self, root_path, out_path):
        self.root_path = root_path
        self.out_path = out_path
        self.tex_files = self.find_tex(root_path)
        
    def find_tex(self, root_path):
        return [file for file in root_path.iterdir() if file.suffix == '.tex']

    def work(self):
        for file in self.tex_files:
            command = ['pdflatex', '-output-directory', str(self.out_path.absolute()), str(file.absolute())]
            run(command)
