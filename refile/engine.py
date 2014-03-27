import re
import pathlib


class Engine:

    def run(self):
        self.regex = re.compile(self.PATTERN)
        self.directory = pathlib.Path(self.DIR)
        self.files = []

        self.match_files()
        self.print_files()

    def match_files(self):
        for f in self.directory.iterdir():
            if self.regex.search(f.name):
                self.files.append(f)

    def print_files(self):
        for f in self.files:
            print(f)
