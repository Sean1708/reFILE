import sys
import refile.engine
import argparse


def setup_print(subparsers):
    print_cmd = subparsers.add_parser(
        'ls',
        help='print the names of files which match the regex pattern'
    )
    print_cmd.add_argument('PATTERN', help='regex to match filenames against')
    print_cmd.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    print_cmd.set_defaults(cls=refile.engine.Printer)


def setup_rename(subparsers):
    rename = subparsers.add_parser(
        'mv',
        help='rename matching files according to replace string'
    )
    rename.add_argument('PATTERN', help='regex to match filenames against')
    rename.add_argument('REPLACE', help='pattern to rename files')
    rename.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    rename.set_defaults(cls=refile.engine.Renamer)


def setup_delete(subparsers):
    delete = subparsers.add_parser(
        'rm',
        help='delete files which match the regex'
    )
    delete.add_argument('PATTERN', help='regex to match filenames against')
    delete.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    delete.set_defaults(cls=refile.engine.Deleter)


def main():
    parser = argparse.ArgumentParser(
        description='''Interact with files whose names match regular
        expressions. See `pydoc refile` for comprehensive documentation.'''
    )
    subparsers = parser.add_subparsers(title='subcommands')

    setup_print(subparsers)
    setup_rename(subparsers)
    setup_delete(subparsers)

    # get dictionary of the command line arguments
    args = vars(parser.parse_args())
    # running `python refile/cmdline.py` works as expected but once installed
    # with entry_points running `refile` does not bring up the usual argparse
    # error but instead keeps on running and raises KeyError since there is no
    # cls if no subcommand has been selected
    # this try statement gets around it but feels a bit hacky for my liking
    try:
        # no point telling the class which class it is, it already knows
        cmd = args.pop('cls')
        cmd(**args).run()
    except KeyError:
        parser.print_help()


if __name__ == '__main__':
    sys.exit(main())
