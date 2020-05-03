from pathlib import Path
from my.common import get_files

import pytest # type: ignore


def test_single_file():
    '''
    Regular file path is just returned as is.
    '''

    "Exception if it doesn't exist"
    with pytest.raises(Exception):
        get_files('/tmp/hpi_test/file.ext')


    create('/tmp/hpi_test/file.ext')

    '''
    Couple of things:
    1. Return type is a tuple, it's friendlier for hashing/caching
    2. It always return pathlib.Path instead of plain strings
    '''
    assert get_files('/tmp/hpi_test/file.ext') == (
        Path('/tmp/hpi_test/file.ext'),
    )


def test_multiple_files():
    '''
    If you pass a directory/multiple directories, it flattens the contents
    '''
    create('/tmp/hpi_test/dir1/')
    create('/tmp/hpi_test/dir1/zzz')
    create('/tmp/hpi_test/dir1/yyy')
    # create('/tmp/hpi_test/dir1/whatever/') # TODO not sure about this... should really allow extra dirs
    create('/tmp/hpi_test/dir2/')
    create('/tmp/hpi_test/dir2/mmm')
    create('/tmp/hpi_test/dir2/nnn')
    create('/tmp/hpi_test/dir3/')
    create('/tmp/hpi_test/dir3/ttt')

    assert get_files([
        Path('/tmp/hpi_test/dir3'), # it takes in Path as well as str
        '/tmp/hpi_test/dir1',
    ]) == (
        # the paths are always returned in sorted order (unless you pass sort=False)
        Path('/tmp/hpi_test/dir1/yyy'),
        Path('/tmp/hpi_test/dir1/zzz'),
        Path('/tmp/hpi_test/dir3/ttt'),
    )


def test_glob():
    '''
    You can pass a blog to restrict the extensions
    '''

    create('/tmp/hpi_test/file_3.zip')
    create('/tmp/hpi_test/file_2.zip')
    create('/tmp/hpi_test/ignoreme')
    create('/tmp/hpi_test/file.zip')

    assert get_files('/tmp/hpi_test', 'file_*.zip') == (
        Path('/tmp/hpi_test/file_2.zip'),
        Path('/tmp/hpi_test/file_3.zip'),
    )

    # named argument should work too
    assert len(get_files('/tmp/hpi_test', glob='file_*.zip')) > 0


test_path = Path('/tmp/hpi_test')
def setup():
    teardown()
    test_path.mkdir()


def teardown():
    import shutil
    if test_path.is_dir():
        shutil.rmtree(test_path)


def create(f: str) -> None:
    if f.endswith('/'):
        Path(f).mkdir()
    else:
        Path(f).touch()
