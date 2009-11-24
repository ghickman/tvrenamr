from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr

class TestExtractFileInfo(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files", log_level='critical')
    
    def test_extracting_season_from_file_format_s0e00(self):
        credentials = self.tv.extract_episode_details_from_file("chuck.s2e06.avi")
        assert_equal(credentials['season'], '2')
    
    def test_extracting_season_from_file_format_s00e00(self):
        credentials = self.tv.extract_episode_details_from_file("chuck.s20e05.avi")
        assert_equal(credentials['season'], '20')
    
    def test_extracting_episode_from_file_format_s0e00(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.s2e05.avi')
        assert_equal(credentials['episode'], '05')
    
    def test_extracting_episode_from_file_format_s00e00(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.s20e05')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_season_from_file_format_0x00(self):
        credentials = self.tv.extract_episode_details_from_file("chuck.2x05.avi")
        assert_equal(credentials['season'], '2')
    
    def test_extracting_season_from_file_format_00x00(self):
        credentials = self.tv.extract_episode_details_from_file("chuck.20x05.avi")
        assert_equal(credentials['season'], '20')
    
    def test_extracting_episode_from_file_format_0x00(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.2x05.avi')
        assert_equal(credentials['episode'], '05')
    
    def test_extracting_episode_from_file_format_00x00(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.20x05')
        assert_equal(credentials['episode'], '05')
    
    
    def test_extracting_season_from_file_format_000(self):
        credentials = self.tv.extract_episode_details_from_file("chuck.205.avi")
        assert_equal(credentials['season'], '2')
    
    def test_extracting_season_from_file_format_0000(self):
        credentials = self.tv.extract_episode_details_from_file("chuck.2005.avi")
        assert_equal(credentials['season'], '20')
    
    def test_extracting_episode_from_file_format_000(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.205.avi')
        assert_equal(credentials['episode'], '05')
    
    def test_extracting_episode_from_file_format_0000(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.2005')
        assert_equal(credentials['episode'], '05')
    
    def test_extracting_season_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')
        assert_equal(credentials['season'], '02')
    
    def test_extracting_episode_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')
        assert_equal(credentials['episode'], '5')
    
    def test_extracting_season_with_custom_regular_expression_passing_in_season_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.0250', user_regex='%n.%s{2}%e')
        assert_equal(credentials['season'], '02')
    
    def test_extracting_season_with_custom_regular_expression_passing_in_episode_digit_lengths_from_file_format_000(self):
        credentials = self.tv.extract_episode_details_from_file('chuck.025', user_regex='%n.%s%e{1}')
        assert_equal(credentials['episode'], '5')
    