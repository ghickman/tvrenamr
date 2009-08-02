import urllib2
import os.path

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr
from core.errors import *

class TestExceptionsAreRaised(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files/")
    
    def test_already_named_exception_should_be_raised_when_file_already_named_correctly(self):
        #assert_raises(AlreadyNamedException, self.tv.extract_episode_details_from_file, 'Chuck - 205 - w00t.avi')
        pass
    
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_episode_details_from_file, 'chuck.avi')
    
    def test_url_error_should_be_raised_when_episode_not_found(self):
        details = self.tv.extract_episode_details_from_file('chuck.s04e05.avi')
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, details[0], details[1], details[2])
    
    def test_episode_already_exists_in_folder_exception_is_raised_when_new_file_name_already_exists_in_folder(self):
        details = self.tv.extract_episode_details_from_file('chuck.s02e05.avi')
        names = self.tv.retrieve_episode_name(details[0],details[1],details[2])
        path = self.tv.build_path(details, series_name=names[0], episode_name=names[1])
        assert_raises(EpisodeAlreadyExistsInFolderException, self.tv.rename, 'chuck.s02e05.avi', path)