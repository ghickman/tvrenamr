from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestExtractFileInfo(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files")
    
    def test_season_extracted_is_equal_to_season_in_file_name(self):
        results = self.tv.extract_episode_details_from_file("chuck.s02e05.avi")
        assert_equal(results[1],"02")
    
    def test_episode_extracted_is_equal_to_season_in_file_name(self):
        results = self.tv.extract_episode_details_from_file("chuck.s02e05.avi")
        assert_equal(results[2],"05")
    
    #def test_