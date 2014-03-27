import re
import pathlib


class Engine:

    def run(self):
        self.regex = re.compile(self.PATTERN)
        self.directory = pathlib.Path(self.DIR)

        self.print_files()

    def print_files(self):
        for f in self.directory.iterdir():
            if self.regex.search(f.name):
                print(f)
