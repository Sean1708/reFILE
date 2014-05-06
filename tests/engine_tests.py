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


def test_init():
    pattern = r'[0-9]{4}-?[01][0-9]-?[0-3][0-9]'
    replace = r'hellothere\1'
    engine = Engine(
        pattern, directory, replace,
        **{
            'recurse': True,
            'quiet': True,
        }
    )

    assert_equal(engine.regex, re.compile(pattern))
    assert_equal(engine.replace, replace)
    assert_equal(engine.directory, test_dir)
    assert_dict_contains_subset({'recurse': True}, engine.options)
    assert_not_in('quiet', engine.options)


def test_match_files():
    matcher = Engine(r'[0-9]{4}-?[01][0-9]-?[0-3][0-9]', directory)
    matched_files = []
    for f_list in matcher.files.values():
        for f in f_list:
            matched_files.append(f.name)
    assert_set_equal(set(files), set(matched_files))

    matcher = Engine(r'^[0-9]{4}-?[01][0-9]-?[0-3][0-9]', directory)
    matched_files = []
    for f_list in matcher.files.values():
        for f in f_list:
            matched_files.append(f.name)
    assert_set_equal(set(files[:4]), set(matched_files))

    matcher = Engine(r'[0-9]{4}-[01][0-9]-[0-3][0-9]', directory)
    matched_files = []
    for f_list in matcher.files.values():
        for f in f_list:
            matched_files.append(f.name)
    assert_set_equal(set(files[2:]), set(matched_files))


def test_recursive():
    pass
