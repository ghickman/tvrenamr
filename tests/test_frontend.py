import os
import random

from .base import BaseTest
from cli.core import cli


class TestFrontEnd(BaseTest):
    def setup(self):
        super(TestFrontEnd, self).setup()
        self.config = frontend.get_config()

    def test_passing_current_dir_makes_file_list_a_list(self):
        assert isinstance(frontend.build_file_list([self.files]), list)

    def test_setting_recursive_adds_all_files_below_the_folder(self):
        new_folders = ('herp', 'derp', 'test')
        os.makedirs(os.path.join(self.files, *new_folders))

        def build_folder(folder):
            new_files = ('foo', 'bar', 'blah')
            for fn in new_files:
                with open(os.path.join(self.files, folder, fn), 'w') as f:
                    f.write('')
        build_folder('herp')
        build_folder('herp/derp')
        build_folder('herp/derp/test')
        file_list = frontend.build_file_list([self.files], recursive=True)
        for root, dirs, files in os.walk(self.files):
            for fn in files:
                assert os.path.join(root, fn) in file_list

    def test_ignoring_files(self):
        ignore = self.random_files(self.files)
        file_list = frontend.build_file_list([self.files], ignore_filelist=ignore)
        assert all(fn not in file_list for fn in ignore)
