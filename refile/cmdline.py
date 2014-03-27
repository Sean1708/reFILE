import sys
import engine
import argparse


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
        help='directory to search (defaults to current directory)'
    )

    matcher = parser.parse_args(namespace=engine.Engine())
    matcher.run()


if __name__ == '__main__':
    sys.exit(main())
