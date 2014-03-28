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
        print(new_file)


def teardown():
    for f in test_dir.iterdir():
        f.unlink()
    test_dir.rmdir()


def test_match_files():
    matcher = Engine(r'[0-9]{4}-?[01][0-9]-?[0-3][0-9]', directory)

    matched_files = []
    for f in matcher.files:
        matched_files.append(f.name)

    assert set(files) == set(matched_files)
