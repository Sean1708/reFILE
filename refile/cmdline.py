import sys
import argparse
from . import engine


def setup_all_share(parser):
    parser.add_argument(
        '-r', '--recurse',
        action='store_true',
        help='search directories recursively'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress all output except errors'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='print extra information'
    )
    # use infinity as default so that limit can't be reached if not specified
    parser.add_argument(
        '-L', '--limit',
        action='store',
        type=int,
        default=float('inf'),
        help='maximum depth limit when searching recursively'
    )
    # if not specified use a regex which will not match anything
    parser.add_argument(
        '-I', '--ignore',
        action='store',
        help='ignore files matching this regex'
    )


def setup_mvrm_share(parser):
    parser.add_argument(
        '-d', '--directories',
        action='store_true',
        help='delete and rename directories'
    )
    parser.add_argument(
        '-i', '--confirm',
        action='store_true',
        help='prompt for confirmation before renaming or deleting any files'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='never prompt for confirmation'
    )


def setup_print(subparsers, parents):
    print_cmd = subparsers.add_parser(
        'ls',
        help='print the names of files which match the regex pattern',
        parents=parents
    )
    print_cmd.add_argument('PATTERN', help='regex to match filenames against')
    print_cmd.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    print_cmd.add_argument(
        '-n', '--no-column',
        action='store_true',
        help='disable columnated ouput'
    )
    print_cmd.add_argument(
        '-l', '--long',
        action='store_true',
        help='print extra information'
    )
    print_cmd.set_defaults(cmd=engine.Printer)


def setup_rename(subparsers, parents):
    rename = subparsers.add_parser(
        'mv',
        help='rename matching files according to replace string',
        parents=parents
    )
    rename.add_argument('PATTERN', help='regex to match filenames against')
    rename.add_argument('REPLACE', help='pattern to rename files')
    rename.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    rename.add_argument(
        '-m', '--moveto',
        action='store',
        help='move files to the directory'
    )
    rename.add_argument(
        '-D', '--date',
        action='store',
        help='strftime format string to be prepended to the name'
    )
    rename.set_defaults(cmd=engine.Renamer)


def setup_delete(subparsers, parents):
    delete = subparsers.add_parser(
        'rm',
        help='delete files which match the regex',
        parents=parents
    )
    delete.add_argument('PATTERN', help='regex to match filenames against')
    delete.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    delete.set_defaults(cmd=engine.Deleter)


def main():
    parser = argparse.ArgumentParser(
        description="""Interact with files whose names match regular
        expressions. See `pydoc refile` for comprehensive documentation."""
    )
    # arguments that all commands share
    all_share = argparse.ArgumentParser(add_help=False)
    setup_all_share(all_share)
    # arguments that mv and rm share
    mvrm_share = argparse.ArgumentParser(add_help=False)
    setup_mvrm_share(mvrm_share)

    subparsers = parser.add_subparsers(title='subcommands')
    setup_print(subparsers, [all_share])
    setup_rename(subparsers, [all_share, mvrm_share])
    setup_delete(subparsers, [all_share, mvrm_share])

    # get dictionary of the command line arguments
    args = vars(parser.parse_args())
    # running `python refile/cmdline.py` works as expected but once installed
    # with entry_points, running `refile` does not bring up the usual argparse
    # error but instead keeps on running and raises KeyError since there is no
    # cmd if no subcommand has been selected
    # this try statement gets around it but feels a bit hacky for my liking
    try:
        # no point telling the class which class it is, it already knows
        Command = args.pop('cmd')
    except KeyError:
        parser.print_help()
    else:
        program = Command(**args)
        program.match_files(program.directory)
        program.run()
