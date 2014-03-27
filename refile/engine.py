import re
import pathlib


class Engine:

    def __init__(self, PATTERN, DIR, **kwargs):
        self.regex = self.parse_regex(PATTERN)
        self.directory = pathlib.Path(DIR)
        self.files = self.match_files()

    def parse_regex(self, pattern):
        return re.compile(pattern)

    def match_files(self):
        files = []
        for f in self.directory.iterdir():
            if self.regex.search(f.name): files.append(f)

        return files

    def run(self):
        pass


class Printer(Engine):

    def run(self):
        for f in self.files:
            print(f)
