import sys
import argparse


class Engine:
    pass


def main():
    parser = argparse.ArgumentParser(
        description='''Interact with files whose names match the regular
        expression PATTERN. See `pydoc refile` for comprehensive
        documentation.'''
    )

    parser.add_argument('PATTERN', help='regex to match filenames against')
    parser.add_argument(
        'DIR',
        nargs='?',
        default='.',
        help='directory to search for files (defaults to current directory)'
    )

    matcher = parser.parse_args(namespace=Engine())

    print(vars(matcher))


if __name__ == '__main__':
    sys.exit(main())
