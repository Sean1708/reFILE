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
dirs = [
    'epic_piccys',
    'ok_piccies'
]


def setup():
    global args
    args = {
        'recurse': False,
        'quiet': True,
        'verbose': False,
        'directories': False,
        'limit': float('inf'),
        'ignore': r'(?!.*)',
        'confirm': False,
        'force': False,
        'moveto': None
    }

    test_dir.mkdir()

    for d in dirs:
        new_dir = test_dir / pathlib.Path(d)
        new_dir.mkdir()

        for f in files:
            new_file = test_dir / f
            new_file.touch()
            new_file = test_dir / d / f
            new_file.touch()


def teardown():
    for f in test_dir.iterdir():
        if f.is_dir():
            for fil in f.iterdir():
                fil.unlink()
            f.rmdir()
        else:
            f.unlink()
    test_dir.rmdir()


def test_delete():
    deleter = Deleter(
        r'^([0-9]{4}-?[01][0-9]-?[0-3][0-9]-?)piccy',
        directory,
        **args
    )
    deleter.match_files(deleter.directory)
    deleter.run()
    p = pathlib.Path(directory)
    remaining_files = set(f.name for f in p.iterdir())
    new_files = [
        'piccy2047-02-13'
    ]
    assert_set_equal(set(new_files + dirs), remaining_files)

    args['directories'] = True
    deleter = Deleter(
        r'piccy',
        directory,
        **args
    )
    deleter.match_files(deleter.directory)
    deleter.run()
    p = pathlib.Path(directory)
    remaining_files = set(f.name for f in p.iterdir())
    # directories are not empty so should not be deleted
    assert_set_equal(set(dirs), remaining_files)


def test_recursive():
    pass
