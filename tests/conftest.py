import os
import shutil

import pytest

from .utils import PATH, files


@pytest.fixture(scope='session', autouse=True)
def build_files(request):
    """Build the file list"""
    with open(os.path.join(PATH, 'file_list'), 'r') as f:
        paths = f.readlines()

    full_paths = list(map(lambda p: os.path.join(files(), p.strip()), paths))
    for path in full_paths:
        with open(path, 'w') as f:
            f.write('')

    # TODO: write the same files to subfolder

    def fin():
        shutil.rmtree(files())
    request.addfinalizer(fin)
