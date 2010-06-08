import shutil
import os

from nose.tools import *

#stub urlopen calls
import urlopenmock

from main import TvRenamr
from errors import *

class TestExceptionsAreRaised(object):
    
    def setUp(self):
        files = 'tests/data/files'
        working = 'tests/data/working'
        self.tv = TvRenamr(working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(working, fn))
    
    def tearDown(self):
        working = 'tests/data/working'
        for fn in os.listdir(working): os.remove(os.path.join(working,fn))
    
    def test_already_named_exception_should_be_raised_when_file_already_named_correctly(self):
        #assert_raises(AlreadyNamedException, self.tv.extract_episode_details_from_file, 'Chuck - 205 - w00t.avi')
        pass
    
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_episode_details_from_file, 'chuck.avi')
    
    def test_episode_not_found_exception_should_be_raised_when_episode_not_found(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.s04e05.avi')
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, credentials['show'], credentials['season'], credentials['episode'])
    
    def test_episode_already_exists_in_folder_exception_is_raised_when_new_file_name_already_exists_in_folder(self):
        fn = 'chuck.s02e05.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(credentials['show'],credentials['season'],credentials['episode'])
        credentials['show'] = title['show']
        credentials['title'] = title['title']
        path = self.tv.build_path(show=credentials['show'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'])
        assert_raises(EpisodeAlreadyExistsInDirectoryException, self.tv.rename, fn, path)
    
    def test_no_leading_the_exception_is_raised_when_set_leading_the_to_end_of_show_name_method_is_called_on_a_show_with_no_leading_the(self):
        fn = 'chuck.s02e05.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(credentials['show'], credentials['season'], credentials['episode'])
        credentials['show'] = title['show']
        assert_raises(NoLeadingTheException, self.tv.move_leading_the_to_trailing_the, credentials['show'])
    
    def test_incorrect_custom_regular_expression_syntax_exception_is_raised_when_any_of_the_custom_regular_expression_string_is_missing_the_defined_three_syntax_snippets(self):
        fn = 'chuck.s02e05.avi'
        assert_raises(IncorrectCustomRegularExpressionSyntaxException, self.tv.extract_episode_details_from_file, fn, '.')
    
    def test_output_format_missing_syntax_exception_is_raised_when_one_of_the_output_format_syntax_snippets_is_missing(self):
        fn = 'chuck.s02e05.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(credentials['show'], credentials['season'], credentials['episode'])
        credentials['show'] = title['show']
        credentials['title'] = title['title']
        assert_raises(OutputFormatMissingSyntaxException, self.tv.build_path, show=credentials['show'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], format='test')
    