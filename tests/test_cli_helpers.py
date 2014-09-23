import os
import random

import pytest

from cli.helpers import build_file_list, get_config


def build_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

    return path


def join_path(path):
    _path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(_path, path)


@pytest.fixture
def files():
    return build_path(join_path('files'))


def random_files(files):
    for choice in range(3):
        yield os.path.join(files, random.choice(os.listdir(files)))


def test_build_file_list_from_a_folder_path():
    file_list = build_file_list([files])
    for fn in os.listdir(files):
        if os.path.isdir(fn):
            assert os.path.join(files, fn) in file_list


def test_build_file_list_from_folders_and_files():
    files = random_files(files) + [subfolder]
    file_list = build_file_list(files)

    def final_list():
        files = []
        for path in os.listdir(files) + os.listdir(subfolder):
            if not os.path.isfile(path):
                continue
            files.append(path)
        return files
    assert all(fn in file_list for fn in final_list())


def test_build_file_list_from_multiple_files():
    files = random_files(files)
    file_list = build_file_list(files)
    assert all(fn in file_list for fn in files)


def test_build_file_list_from_single_file():
    fn = os.path.join(files, random.choice(os.listdir(files)))
    file_list = build_file_list([fn])
    assert fn in file_list


def test_load_config():
    tmp_conf = os.path.join(path, 'test_config.yml')
    with open(tmp_conf, 'w') as f:
        f.writelines(['defaults:\n', '  foo: bar'])

    config = get_config(tmp_conf).config
    assert config
    assert 'defaults' in config
    assert 'foo' in config['defaults']

    os.remove(tmp_conf)
