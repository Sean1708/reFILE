import sys
import engine
import argparse


def main():
    # top-level parser
    parser = argparse.ArgumentParser(
        description='''Interact with files whose names match the regular
        expression PATTERN. See `pydoc refile` for comprehensive
        documentation.'''
    )
    subparsers = parser.add_subparsers( title='subcommands')

    # parser for print command
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
    print_cmd.set_defaults(cls=engine.Engine)

    # parse the args and run selected command
    args = vars(parser.parse_args())
    cmd = args.pop('cls')
    cmd(**args)


if __name__ == '__main__':
    sys.exit(main())
