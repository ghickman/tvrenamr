import collections
import os
import sys

from tvrenamr.cli import helpers

from .utils import random_files


def test_passing_current_dir_makes_file_list_a_list(files):
    file_list = helpers.build_file_list([files])

    assert isinstance(file_list, collections.Iterable)

    PY3 = sys.version_info[0] == 3
    string_type = str if PY3 else basestring
    text_type = str if PY3 else unicode
    assert not isinstance(file_list, (string_type, text_type))


def test_setting_recursive_adds_all_files_below_the_folder(files):
    new_folders = ('herp', 'derp', 'test')
    os.makedirs(os.path.join(files, *new_folders))

    def build_folder(folder):
        new_files = ('foo', 'bar', 'blah')
        for fn in new_files:
            with open(os.path.join(files, folder, fn), 'w') as f:
                f.write('')
    build_folder('herp')
    build_folder('herp/derp')
    build_folder('herp/derp/test')
    file_list = helpers.build_file_list([files], recursive=True)
    for root, dirs, files in os.walk(files):
        for fn in files:
            assert (root, fn) in file_list


def test_ignoring_files(files):
    ignore = random_files(files)
    file_list = helpers.build_file_list([files], ignore_filelist=ignore)
    assert all(fn not in file_list for fn in ignore)
