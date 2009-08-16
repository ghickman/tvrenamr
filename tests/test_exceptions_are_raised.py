import shutil, os, urllib2

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr
from core.errors import *

class TestExceptionsAreRaised(object):
    
    def setUp(self):
        files = 'tests/data/files'
        working = 'tests/data/working'
        self.tv = TvRenamr(working)
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(working, fn))
    
    def tearDown(self):
        working = 'tests/data/working'
        for fn in os.listdir(working): os.remove(os.path.join(working,fn))
    
    def test_already_named_exception_should_be_raised_when_file_already_named_correctly(self):
        #assert_raises(AlreadyNamedException, self.tv.extract_episode_details_from_file, 'Chuck - 205 - w00t.avi')
        pass
    
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.extract_episode_details_from_file, 'chuck.avi')
    
    def test_url_error_should_be_raised_when_episode_not_found(self):
        details = self.tv.extract_episode_details_from_file('chuck.s04e05.avi')
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, details[0], details[1], details[2])
    
    def test_episode_already_exists_in_folder_exception_is_raised_when_new_file_name_already_exists_in_folder(self):
        fn = 'chuck.s02e05.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(details[0],details[1],details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3])
        assert_raises(EpisodeAlreadyExistsInFolderException, self.tv.rename, fn, path)
    