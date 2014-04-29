import re
from nose.tools import *
from refile.engine import *

directory = 'tests/files'
test_dir = pathlib.Path(directory)
files = [
    '20140703piccy',
    '19941123piccy',
    '1900-01-01-piccy',
    '2006-08-12piccy',
    'piccy2047-02-13'
]


def setup():
    test_dir.mkdir()

    for f in files:
        new_file = test_dir / f
        new_file.touch()


def teardown():
    for f in test_dir.iterdir():
        f.unlink()
    test_dir.rmdir()


'yo'
