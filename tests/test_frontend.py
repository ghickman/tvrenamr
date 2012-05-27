import os
import random

from nose.tools import assert_true

from .base import BaseTest
from tvrenamr.frontend import FrontEnd


class TestFrontEnd(BaseTest):
    def setup(self):
        super(TestFrontEnd, self).setup()
        self.frontend = FrontEnd()

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


    """
    recursively walking a directory
    ignoring files
    tidy up the file resolution code after this!
    """

