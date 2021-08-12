import os
import tempfile
from pathlib import Path

import pytest

import test
from test.harness_utils import dbtvault_harness_utils


def dict_to_directories(dir_dict: dict, root_path: Path):
    """ Generate directory structure from the provided dict representing a directory structure """
    paths = dict()

    for k, v in dir_dict.items():
        full_path = Path(root_path) / k
        Path(full_path).mkdir(parents=True)
        if isinstance(v, dict):
            paths[k] = list()
            for ik, iv in v.items():
                if '.' in ik:
                    file_name, ext = ik.split('.')
                    file = tempfile.NamedTemporaryFile(prefix=file_name, suffix=f'.{ext}', dir=full_path, delete=False)
                    full_file_path = Path(full_path) / file.name
                    paths[k].append(full_file_path)
                    with open(full_file_path, 'w+') as f:
                        f.write(iv)

    return paths


@pytest.fixture()
def sample_directory_tree(tmp_path):
    def _convert(directory_dict):
        paths = dict_to_directories(directory_dict, tmp_path)

        return paths, tmp_path

    return _convert


@pytest.fixture(scope='session', autouse=True)
def setup():
    os.environ['TARGET'] = dbtvault_harness_utils.target()
    os.chdir(test.TESTS_DBT_ROOT)


@pytest.fixture(scope='session', autouse=True)
def clean_database(request):
    os.environ['TARGET'] = dbtvault_harness_utils.target()
    dbtvault_harness_utils.drop_test_schemas()
