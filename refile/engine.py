import re
import os
import sys
import pathlib
import datetime
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

    def match_files(self, directory):
        if not directory.is_dir():
            prt.print_err('{0} is not a directory.'.format(directory))
            sys.exit(-1)

        if self.options['verbose'] is True:
            prt.print_info('Searching {0}'.format(directory))

        # each time this func is called a new directory has been entered
        self.current_depth += 1

        self.files[directory] = []
        for file in directory.iterdir():
            if self.match_pattern(file.name):
                self.files[directory].append(file)
            # avoid crashing on symlink loops
            try:
                if (self.options['recurse'] is True and file.is_dir()
                        and self.current_depth <= self.max_depth):
                    self.match_files(file)
            except OSError:
                prt.print_warn('Symlink loop from {0}'.format(file))

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
        # access it straight from the dictionary using dict[]

        # moveto is not set for all options so default it to none
        moveto = options.pop('moveto', None)
        self.destination = pathlib.Path(moveto) if moveto else None

        self.max_depth = abs(options.pop('limit'))

        self.ignore = options.pop('ignore')
        if self.ignore:
            self.ignore = re.compile(self.ignore)
            def _match_pattern(filename):
                return (self.regex.search(filename) and not
                        self.ignore.search(filename))
        else:
            def _match_pattern(filename):
                return self.regex.search(filename)
        self.match_pattern = _match_pattern

        if options.pop('quiet', False):
            sys.stdout = open(os.devnull, 'w')

        return options


class Printer(Matcher):

    def run(self):
        for directory, file_list in self.files.items():
            if self.options['long'] is True:
                prt.print_long_format(directory, file_list)
            elif self.options['no_column'] is True:
                prt.print_single_column(directory, file_list)
            else:
                prt.print_files(directory, file_list)


class Renamer(Matcher):

    def run(self):
        for file_list in self.files.values():
            for old_file in file_list:
                if (old_file.is_file() or old_file.is_dir() and
                        self.options['directories'] is True):
                    new_name = self.regex.sub(self.replace, old_file.name)
                    # ensure file stays in same directory
                    new_file = self.rename_file(old_file, new_name)
                    print('Rename: {0} -> {1}'.format(old_file, new_file))

                    # only false if --force is set and --confirm is not set
                    if (self.options['confirm'] is True or
                            self.options['force'] is not True):
                        rename = self.overwrite_guard(new_file)
                    if rename:
                        old_file.rename(new_file)

    def overwrite_guard(self, new_file):
        if new_file.exists():
            prt.print_warn(
                'File {0} already exists!'.format(new_file),
                end=' '
            )
            rename = input('Overwrite (y/n)? ')[0].lower()
        elif self.options['confirm'] is True:
            rename = input('Continue (y/n)? ')[0].lower()
        else:
            # if it doesn't exist continue with the rename
            rename = 'y'

        if rename == 'y':
            return True
        else:
            if rename != 'n':
                prt.print_info('Invalid option. File was not overwritten.')
            return False

    def rename_file(self, old_file, new_name):
        if self.options['date']:
            creation_time = os.path.getctime(str(old_file))
            date_str = datetime.datetime.fromtimestamp(
                float(creation_time)
            ).strftime(self.options['date'])
            new_name = date_str + new_name

        if self.destination:
            return self.destination / new_name
        else:
            return old_file.with_name(new_name)


class Deleter(Matcher):

    def run(self):
        for file_list in self.files.values():
            for file in file_list:
                if self.options['verbose'] is True:
                    print('Deleting {0}'.format(file))
                if self.options['confirm'] is True:
                    delete = self.confirm_delete(file)
                    if not delete:
                        return None
                if file.is_file():
                    file.unlink()
                elif file.is_dir() and self.options['directories'] is True:
                    # if next() returns a file, directory is not empty and
                    # if-statement will evaluate to False
                    if not next(file.iterdir(), False):
                        file.rmdir()
                else:
                    prt.print_warn('{0} is not a file/directory.'.format(file))
                    prt.print_info('{0} was not deleted.'.format(file))

    def confirm_delete(self, file):
        delete = input('Delete {0} (y/n)? '.format(file))[0].lower()

        if delete == 'y':
            return True
        else:
            if delete != 'n':
                prt.print_info('Invalid option. File was not overwritten.')
            return False
