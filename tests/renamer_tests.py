import re
import pathlib
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


def test_rename():
    renamer = Renamer(
        r'^([0-9]{4}-?[01][0-9]-?[0-3][0-9]-?)piccy',
        directory,
        r'\1picture',
        **{'quiet': True}
    )
    renamer.run()
    p = pathlib.Path(directory)
    renamed_files = set(f.name for f in p.iterdir())
    new_files = [
        '20140703picture',
        '19941123picture',
        '1900-01-01-picture',
        '2006-08-12picture',
        'piccy2047-02-13'
    ]
    assert_set_equal(set(new_files), renamed_files)

    renamer = Renamer(
        r'piccy',
        directory,
        r'picture',
        **{'quiet': True}
    )
    renamer.run()
    p = pathlib.Path(directory)
    renamed_files = set(f.name for f in p.iterdir())
    new_files = [
        '20140703picture',
        '19941123picture',
        '1900-01-01-picture',
        '2006-08-12picture',
        'picture2047-02-13'
    ]
    assert_set_equal(set(new_files), renamed_files)
