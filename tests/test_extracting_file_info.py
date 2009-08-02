from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestExtractFileInfo(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files")
    
    
    def test_extracted_season_is_equal_to_season_from_file_format_s0e00(self):
        results = self.tv.extract_episode_details_from_file("chuck.s2e06.avi")
        assert_equal(results[1], '2')
    
    def test_extracted_season_is_equal_to_season_from_file_format_s00e00(self):
        results = self.tv.extract_episode_details_from_file("chuck.s20e05.avi")
        assert_equal(results[1], '20')
    
    def test_extracted_episode_is_equal_to_episode_from_file_format_s0e00(self):
        results = self.tv.extract_episode_details_from_file('chuck.s2e05.avi')
        assert_equal(results[2], '05')
    
    def test_extracted_episode_is_equal_to_episode_from_file_format_s00e00(self):
        results = self.tv.extract_episode_details_from_file('chuck.s20e05')
        assert_equal(results[2], '05')
    
    
    def test_extracted_season_is_equal_to_season_from_file_format_0x00(self):
        results = self.tv.extract_episode_details_from_file("chuck.2x05.avi")
        assert_equal(results[1], '2')
    
    def test_extracted_season_is_equal_to_season_from_file_format_00x00(self):
        results = self.tv.extract_episode_details_from_file("chuck.20x05.avi")
        assert_equal(results[1], '20')
    
    def test_extracted_episode_is_equal_to_episode_from_file_format_0x00(self):
        results = self.tv.extract_episode_details_from_file('chuck.2x05.avi')
        assert_equal(results[2], '05')
    
    def test_extracted_episode_is_equal_to_episode_from_file_format_00x00(self):
        results = self.tv.extract_episode_details_from_file('chuck.20x05')
        assert_equal(results[2], '05')
    
    
    def test_extracted_season_is_equal_to_season_from_file_format_000(self):
        results = self.tv.extract_episode_details_from_file("chuck.205.avi")
        assert_equal(results[1], '2')
    
    def test_extracted_season_is_equal_to_season_from_file_format_0000(self):
        results = self.tv.extract_episode_details_from_file("chuck.2005.avi")
        assert_equal(results[1], '20')
    
    def test_extracted_episode_is_equal_to_episode_from_file_format_000(self):
        results = self.tv.extract_episode_details_from_file('chuck.205.avi')
        assert_equal(results[2], '05')
    
    def test_extracted_episode_is_equal_to_episode_from_file_format_0000(self):
        results = self.tv.extract_episode_details_from_file('chuck.2005')
        assert_equal(results[2], '05')
    