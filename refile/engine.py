import re
import sys
import pathlib


class Engine:

    def __init__(self, PATTERN, DIR, REPLACE=None, **kwargs):
        self.regex = re.compile(PATTERN)
        self.replace = REPLACE
        self.directory = pathlib.Path(DIR)
        self.files = self.match_files()

    def match_files(self):
        files = []
        for f in self.directory.iterdir():
            if self.regex.search(f.name):
                files.append(f)

        return files

    def run(self):
        pass


class Printer(Engine):

    def run(self):
        for f in self.files:
            print(f)


class Renamer(Engine):

    def run(self):
        for f in self.files:
            new_name = self.regex.sub(self.replace, f.name)
            # ensure file stays in same directory
            new_file = f.with_name(new_name)
            print('Rename: {0} -> {1}'.format(f, new_file))

            rename = self.overwrite_guard(new_file)
            if rename: f.rename(new_file)

    def overwrite_guard(self, new_file):
        if new_file.exists():
            print(
                '  Warning: File {0} already exists!'.format(new_file),
                end=' '
            )
            overwrite = input('Overwrite (y/n)? ')[0].lower()

            if overwrite == 'y':
                return True
            else:
                if overwrite != 'n':
                    print('  Invalid option. File will not be overwritten.')
                return False
        else:
            # if it doesn't exist continue with the rename
            return True


class Deleter(Engine):

    def run(self):
        for f in self.files:
            if f.is_file():
                f.unlink()
