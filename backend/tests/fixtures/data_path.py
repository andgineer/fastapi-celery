import os.path
from distutils import dir_util
from pathlib import Path

import pytest


@pytest.fixture
def data_path(tmpdir, request) -> Path:
    """
    If in the same folder as the test module exists a sub folder with the name
    `<test module name without "test_">_data` this fixture moves all contents of the sub
    folder to a temporary directory.
    For example if test module named `test_foo.py` then it will look for folder `foo_data` in the
    same folder as test module.

    You can change the folder name for the test using the decorator (there can be a number of folders
    and the test will run for all of them):
        @pytest.mark.parametrize('data_path', [(<data folders list>)], indirect=['data_path'])

    :return: Path object with the temporary directory

    :param tmpdir: internal pytest fixture which provides a temporary directory unique to the
        test invocation (https://docs.pytest.org/en/latest/tmpdir.html)
    :param request: A request object gives access to the requesting test context
        https://docs.pytest.org/en/latest/reference.html?highlight=request#std:fixture-request
    """
    if hasattr(request, 'param'):
        test_data_dir = os.path.join(
            os.path.split(os.path.splitext(request.module.__file__)[0])[0],
            request.param
        )
    else:
        head, tail = os.path.split(os.path.splitext(request.module.__file__)[0])
        if tail.startswith('test_'):
            tail = tail[len('test_'):]
        test_data_dir = os.path.join(head, tail) + '_data'

    assert os.path.isdir(test_data_dir), \
        f'data_path fixture: Cannot find test data folder {test_data_dir}'
    dir_util.copy_tree(test_data_dir, str(tmpdir))

    return Path(tmpdir)