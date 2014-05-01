import re
import os
import sys
import pathlib


class Engine:

    def __init__(self, PATTERN, DIR, REPLACE=None, **kwargs):
        self.regex = re.compile(PATTERN)
        self.replace = REPLACE
        self.directory = pathlib.Path(DIR)
        self.options = self.parse_options(kwargs)

        # dict of the form {<directory>: [<files_in_directory>, ...]}
        self.files = {}
        self.match_files(self.directory)

    def match_files(self, directory):
        if not directory.is_dir():
            sys.exit('Error: {0} is not a directory.'.format(directory))
        self.files[directory] = []
        for f in directory.iterdir():
            if self.regex.search(f.name):
                self.files[directory].append(f)
            if self.options.get('recurse') is True and f.is_dir():
                self.match_files(f)

        # if there are no matching files in the directory,
        # don't bother keeping the directory entry
        if not self.files[directory]:
            del self.files[directory]

    def parse_options(self, options):
        # remove any flags which require a specific action and perform the
        # action
        # if it just holds true or false (i.e. 'recurse') then leave it and
        # access it straight from the dictionary using dict.get()
        if options.pop('quiet', False):
            sys.stdout = open(os.devnull, 'w')
        return options

    def run(self):
        pass


class Printer(Engine):

    def run(self):
        for d, f_list in self.files.items():
            # if not current directory ('.')
            if f_list and d.name != '':
                print(d, end='\n  ')
                print('\n  '.join(f.name for f in f_list))
            elif f_list:
                print('\n'.join(f.name for f in f_list))


class Renamer(Engine):

    def run(self):
        for f_list in self.files.values():
            for f in f_list:
                # maybe implement this in the matching method instead
                if (f.is_file() or f.is_dir() and
                        self.options.get('directories') is True):
                    new_name = self.regex.sub(self.replace, f.name)
                    # ensure file stays in same directory
                    new_file = f.with_name(new_name)
                    print('Rename: {0} -> {1}'.format(f, new_file))

                    rename = self.overwrite_guard(new_file)
                    if rename:
                        f.rename(new_file)

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
        for f_list in self.files.values():
            for f in f_list:
                if self.options.get('verbose') is True:
                    print('Deleting {0}'.format(f))
                if f.is_file():
                    f.unlink()
                elif f.is_dir() and self.options.get('directories') is True:
                    # if next() returns a file, directory is not empty and
                    # if-statement will evaluate to False
                    if not next(f.iterdir(), False):
                        f.rmdir()
                else:
                    print(
                        '  Warning: {0} is not a file or directory.'.format(f)
                    )
                    print('  Info: {0} was not deleted.'.format(f))
