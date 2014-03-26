import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""Interact with files whose names match the regular
        expression PATTERN. See `pydoc refile` for comprehensive
        documentation."""
    )

    parser.add_argument("PATTERN", help="regex to match filenames against")

    args = parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
