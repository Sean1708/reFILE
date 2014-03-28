import sys
import engine
import argparse


def setup_print(subparsers):
    print_cmd = subparsers.add_parser(
        'print',
        help='print the names of files which match the regex pattern'
    )
    print_cmd.add_argument('PATTERN', help='regex to match filenames against')
    print_cmd.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search (defaults to current directory)'
    )
    print_cmd.set_defaults(cls=engine.Printer)


def main():
    parser = argparse.ArgumentParser(
        description='''Interact with files whose names match the regular
        expression PATTERN. See `pydoc refile` for comprehensive
        documentation.'''
    )
    subparsers = parser.add_subparsers(title='subcommands')

    setup_print(subparsers)

    # get dictionary of the args
    args = vars(parser.parse_args())
    # no point telling the class which class it is, it already knows
    cmd = args.pop('cls')
    cmd(**args).run()


if __name__ == '__main__':
    sys.exit(main())
