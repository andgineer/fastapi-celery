"""
Unittest hook to add doctests to unittest run
"""
import app.config
import app.db.session
from tests.config import get_test_config
from tests.config import get_test_session

app.config.get_config = get_test_config
app.db.session.get_session = get_test_session


import doctest
from glob import glob
from importlib import import_module
from os.path import isfile

PY_EXT = ".py"
SRC_DIR = "app/**"


def load_tests(loader, tests, ignore):
    for module_file in glob(f"{SRC_DIR}/*{PY_EXT}", recursive=True):
        if isfile(module_file) and not module_file.endswith("__init__.py"):
            tests.addTest(
                doctest.DocTestSuite(
                    import_module(f'{module_file.replace("/", ".")[:-len(PY_EXT)]}')
                )
            )
    return tests
