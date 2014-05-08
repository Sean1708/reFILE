import re
import os
import sys
import pathlib
from . import printing as prt
from collections import OrderedDict


class Matcher:

    def __init__(self, PATTERN, DIR, REPLACE=None, **kwargs):
        self.regex = re.compile(PATTERN)
        self.replace = REPLACE
        self.directory = pathlib.Path(DIR)
        self.options = self.parse_options(kwargs)

        self.files = OrderedDict()
        self.current_depth = 0
        self.match_files(self.directory)

    def match_files(self, directory):
        if not directory.is_dir():
            prt.print_err('{0} is not a directory.'.format(directory))
            sys.exit()

        # each time this func is called a new directory has been entered
        self.current_depth += 1

        self.files[directory] = []
        for f in directory.iterdir():
            if self.regex.search(f.name) and not self.ignore.search(f.name):
                self.files[directory].append(f)
            if (self.options.get('recurse') is True and f.is_dir()
                    and self.current_depth <= self.max_depth):
                self.match_files(f)

        # once the for-loop has been finished a directory has been left
        self.current_depth -= 1

        # if there are no matching files in the directory,
        # don't bother keeping the directory entry
        if not self.files[directory]:
            del self.files[directory]

    def parse_options(self, options):
        # remove any flags which require a specific action and perform the
        # action
        # if it just holds true or false (i.e. 'recurse') then leave it and
        # access it straight from the dictionary using dict.get()

        ## --limit
        # ensure max depth is not negative
        self.max_depth = abs(options.pop('limit', float('inf')))
        ## --ignore
        # argparse stores None by default
        ignore_pattern = options.pop('ignore', None)
        if ignore_pattern is not None:
            self.ignore = re.compile(ignore_pattern)
        else:
            # if no ignore pattern is given, set ignore to an unmatchable regex
            self.ignore = re.compile(r'(?!.*)')
        ## --quiet
        if options.pop('quiet', False):
            sys.stdout = open(os.devnull, 'w')

        return options


class Printer(Matcher):

    def run(self):
        for d, f_list in self.files.items():
            prt.print_files(d, f_list)

class Renamer(Matcher):

    def run(self):
        for f_list in self.files.values():
            for f in f_list:
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
            prt.print_warn('File {0} already exists!'.format(new_file), end=' ')
            overwrite = input('Overwrite (y/n)? ')[0].lower()

            if overwrite == 'y':
                return True
            else:
                if overwrite != 'n':
                    prt.print_info('Invalid option. File was not overwritten.')
                return False
        else:
            # if it doesn't exist continue with the rename
            return True


class Deleter(Matcher):

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
                    prt.print_warn('{0} is not a file or directory.'.format(f))
                    prt.print_info('{0} was not deleted.'.format(f))
