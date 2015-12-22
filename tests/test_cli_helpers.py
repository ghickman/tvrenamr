import os

from tvrenamr.cli.helpers import build_file_list, get_config
from .utils import build_path, join_path, random_files


def test_build_file_list_from_a_folder_path(files):
    file_list = build_file_list([files])
    for fn in os.listdir(files):
        if os.path.isdir(fn):
            assert os.path.join(files, fn) in file_list


def test_build_file_list_from_folders_and_files(files):
    """
    Tests `build_file_list` deals with paths + directories

    Given a list of file paths and 1+ directory paths this function should
    return a list of paths.
    """
    subfolder = build_path(join_path('subfolder'))

    def full_path(path):
        paths = []
        for p in os.listdir(path):
            paths.append(os.path.join(files, p))
        return paths

    def build_all_paths():
        paths = []
        for path in full_path(files) + full_path(subfolder):
            if os.path.isfile(path):
                paths.append(path)
        return paths

    all_paths = build_all_paths()

    file_list = build_file_list(list(random_files(files)) + [subfolder])

    for path in file_list:
        assert os.path.join(*path) in all_paths


def test_build_file_list_from_multiple_files(files):
    _files = random_files(files)
    file_list = build_file_list(_files)

    for head, tail in file_list:
        assert tail in os.listdir(files)


def test_build_file_list_from_single_file(files):
    fn = list(random_files(files))[0]
    file_list = list(build_file_list([fn]))
    assert file_list == [os.path.split(fn)]


def test_load_config():
    tmp_conf = join_path('test_config.yml')
    with open(tmp_conf, 'w') as f:
        f.writelines(['defaults:\n', '  foo: bar'])

    config = get_config(tmp_conf).config
    assert config
    assert 'defaults' in config
    assert 'foo' in config['defaults']

    os.remove(tmp_conf)
