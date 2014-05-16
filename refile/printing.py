# the future statement in __init__.py isn't picked up for some reason
from __future__ import print_function
import shutil
import sys


def print_err(msg='unknown error', **kwargs):
    ERROR = '\033[31mError:\033[0m'
    print(ERROR, msg, **kwargs)


def print_warn(msg='unknown warning', **kwargs):
    WARNING = '\033[33mWarning:\033[0m'
    print(WARNING, msg, **kwargs)


def print_info(msg='well this isn\'t particularly helpful', **kwargs):
    INFO = '\033[34mInfo:\033[0m'
    print(INFO, msg, **kwargs)


def print_files(directory, file_list):
    # get_terminal_size is new in 3.3
    if sys.version_info[:2] < (3, 3):
        return print_single_column(directory, file_list)

    # if width is -1 then size couldn't be found so just use single column
    width, _ = shutil.get_terminal_size((-1, -1))
    if width < 0:
        return print_single_column(directory, file_list)

    print_list = pack_files(file_list, width, directory)
    if directory.name != '':
        print(directory)
    print('\n'.join(print_list))

def print_single_column(directory, file_list):
    # if not current directory
    if directory.name != '' and file_list:
        print(directory, end='\n  ')
        print('\n  '.join(f.name for f in file_list))
    elif file_list:
        print('\n'.join(f.name for f in file_list))

def pack_files(files, width, directory):
    """Sort files into columns.

    Simple algorithm which puts files into columns which have a size based on
    the largest filename length.

    """

    START = '  ' if directory.name != '' else ''
    col_width = max(len(f.name) for f in files) + 5

    lines = [START]
    for file in files:
        for i, line in enumerate(lines):
            if len(line) + col_width <= width:
                lines[i] += file.name + ' '*(col_width - len(file.name))
                break
        else:
            lines.append(START + file.name + ' '*(col_width - len(file.name)))

    return lines
