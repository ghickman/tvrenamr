import os
import shutil

import pytest
from tvrenamr.config import Config
from tvrenamr.main import TvRenamr

from .utils import PATH, build_path, join_path

FILES = build_path(join_path('files'))


@pytest.fixture
def files(request):
    """Build the file list"""
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


@pytest.fixture
def files_path():
    if not os.path.exists(FILES):
        os.makedirs(FILES)

    path = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
    open(os.path.join(FILES, path), 'a').close()

    return FILES


@pytest.fixture
def tv():
    config = Config()
    config.config['defaults']['renamed'] = FILES
    return TvRenamr(files, config, cache=False)
