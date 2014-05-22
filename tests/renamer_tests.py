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
        'date': None,
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


def test_rename():
    renamer = Renamer(
        r'^([0-9]{4}-?[01][0-9]-?[0-3][0-9]-?)piccy',
        directory,
        r'\1picture',
        **args
    )
    renamer.match_files(renamer.directory)
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
    assert_set_equal(set(new_files + dirs), renamed_files)

    args['directories'] = True
    renamer = Renamer(
        r'piccy',
        directory,
        r'picture',
        **args
    )
    renamer.match_files(renamer.directory)
    renamer.run()
    p = pathlib.Path(directory)
    renamed_files = set(f.name for f in p.iterdir())
    new_files = [
        '20140703picture',
        '19941123picture',
        '1900-01-01-picture',
        '2006-08-12picture',
        'picture2047-02-13',
        'epic_pictures',
        'ok_piccies'
    ]
    assert_set_equal(set(new_files), renamed_files)


def test_recursive():
    pass
