"""
Unittest hook to add doctests to unittest run
Usage:
    python -m unittest tests.test_doctests

We could add `addopts = --doctest-modules` to `pytest.ini` to run doctests with pytest
but for that you should expose full src to pytest collector and that does not play well with my complicated setup
"""

import app.config
import app.db.session
from tests.config import get_test_config, get_test_session

app.config.get_config = get_test_config
app.db.session.get_session = get_test_session


import doctest
from glob import glob
from importlib import import_module
from os.path import isfile

PY_EXT = ".py"
SRC_DIR = "backend/app/**"


def load_tests(loader, tests, ignore):
    for module_file in glob(f"{SRC_DIR}/*{PY_EXT}", recursive=True):
        if (
            isfile(module_file)
            and not module_file.endswith("__init__.py")
            and not module_file.endswith("test_celery_boilerplate.py")
        ):
            module_path = module_file.replace("/", ".").replace("\\", ".")[: -len(PY_EXT)]
            try:
                module = import_module(module_path)
                tests.addTest(doctest.DocTestSuite(module))
            except Exception as e:
                print(f"Failed to import {module_path}: {e}")
    return tests
