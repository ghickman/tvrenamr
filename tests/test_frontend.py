import os
import random

from nose.tools import assert_true

from .base import BaseTest
from tvrenamr.frontend import FrontEnd


class TestFrontEnd(BaseTest):
    def setup(self):
        super(TestFrontEnd, self).setup()
        self.frontend = FrontEnd()
        self.frontend.get_config(os.path.join(self.path, 'config.yml'))

    def test_config_variable_exists(self):
        assert_true(hasattr(self.frontend, 'config'))

    def test_file_list_contains_files_from_test_dir(self):
        self.frontend.build_file_list([self.files])
        for fn in os.listdir(self.files):
            assert_true((self.files, fn) in self.frontend.file_list)

    def test_passing_current_dir_makes_file_list_a_list(self):
        self.frontend.build_file_list([self.files])
        assert_true(isinstance(self.frontend.file_list, list))

    def test_passing_multiple_files_are_added_to_file_list(self):
        possible_files = os.listdir(self.files)
        files = [os.path.join(self.files, random.choice(possible_files)) for choice in range(3)]
        self.frontend.build_file_list(files)
        assert_true(all(os.path.split(fn) in self.frontend.file_list for fn in files))

    def test_passing_single_file_is_added_to_file_list(self):
        fn = random.choice(os.listdir(self.files))
        self.frontend.build_file_list([os.path.join(self.files, fn)])
        assert_true((self.files, fn) in self.frontend.file_list)

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
        self.frontend.build_file_list([self.files], recursive=True)
        for root, dirs, files in os.walk(self.files):
            for fn in files:
                assert_true((root, fn) in self.frontend.file_list)

    def test_ignoring_files(self):
        ignore = [random.choice(os.listdir(self.files)) for i in range(3)]
        self.frontend.build_file_list([self.files], ignore_filelist=ignore)
        for fn in [fn for fn in os.listdir(self.files) if fn not in ignore]:
            assert_true((self.files, fn) in self.frontend.file_list)

