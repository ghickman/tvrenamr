import shutil
import os

from nose.tools import *

#stub urlopen calls
import urlopenmock

from tvrenamr.main import TvRenamr
from tvrenamr.errors import *

class TestExceptionsAreRaised(object):

    def setUp(self):
        files = 'tests/data/files'
        working = 'tests/data/working'
        self.tv = TvRenamr(working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(working, fn))

    def tearDown(self):
        working = 'tests/data/working'
        for fn in os.listdir(working): os.remove(os.path.join(working,fn))


    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_details_from_file, 'chuck.avi')


    def test_episode_not_found_exception_should_be_raised_when_episode_not_found(self):
        credentials = self.tv.extract_details_from_file('chuck.s04e05.avi')
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, **credentials)


    def test_episode_already_exists_in_folder_exception_is_raised_when_new_file_name_already_exists_in_folder(self):
        fn = 'chuck.s02e05.avi'
        credentials = self.tv.extract_details_from_file(fn)
        credentials['title'] = self.tv.retrieve_episode_name(**credentials)
        path = self.tv.build_path(organise=False, **credentials)
        assert_raises(EpisodeAlreadyExistsInDirectoryException, self.tv.rename, fn, path)


    def test_incorrect_custom_regular_expression_syntax_exception_is_raised_when_any_of_the_custom_regular_expression_string_is_missing_the_defined_three_syntax_snippets(self):
        fn = 'chuck.s02e05.avi'
        assert_raises(IncorrectCustomRegularExpressionSyntaxException, self.tv.extract_details_from_file, fn, '.')

