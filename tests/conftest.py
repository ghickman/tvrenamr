import os
import shutil

import pytest

from .utils import PATH, build_path, join_path


@pytest.fixture
def files(request):
    """Build the file list"""
    FILES = build_path(join_path('files'))

    with open(os.path.join(PATH, 'file_list'), 'r') as f:
        paths = f.readlines()

    full_paths = list(map(lambda p: os.path.join(FILES, p.strip()), paths))
    for path in full_paths:
        with open(path, 'w') as f:
            f.write('')

    # TODO: write the same files to subfolder

    def fin():
        shutil.rmtree(FILES)
    request.addfinalizer(fin)

    return FILES
