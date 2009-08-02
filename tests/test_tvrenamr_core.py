from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestTvrenamrCore(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files")
    
    def test_instantiate_core(self):
        assert_true(isinstance(TvRenamr("/"), TvRenamr))
        
    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        new_name = 'Avatar: The Last Airbender'
        details = self.tv.extract_episode_details_from_file('avatar.s1e08.blah.HDTV.XViD.avi')
        details[0] = new_name
        names = self.tv.retrieve_episode_name(details[0],details[1],details[2])
        assert_equal(new_name, names[0])
    
    def test_passing_in_a_season_number_renames_a_file_using_that_season_number(self):
        details = self.tv.extract_episode_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi')
        two = '2'
        names = self.tv.retrieve_episode_name(details[0],'2',details[2])
        assert_equal('Chuck Versus the Gravitron', names[1])
    
    def test_passing_in_an_episode_number_renames_a_file_using_that_episode_number(self):
        details = self.tv.extract_episode_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi')
        names = self.tv.retrieve_episode_name(details[0],details[1],'9')
        assert_equal('Chuck Versus the Imported Hard Salami', names[1])
    
    def test_renaming_an_episode_with_a_two_digit_season_number_and_no_characters_before_the_episode_number(self):
        details = self.tv.extract_episode_details_from_file('stargate.sg-1.1010.avi', user_regex='%n\.%s%e')
        names = self.tv.retrieve_episode_name(details[0],details[1],details[2])
        path = self.tv.build_path(details, series_name=names[0], episode_name=names[1])
        assert_equal('tests/data/files/Stargate SG-1 - 1010 - Quest (1).avi', path)
    
    def test_renaming_an_episode_with_a_two_digit_season_number_and_a_character_before_the_episode_number(self):
        details = self.tv.extract_episode_details_from_file('stargate.sg-1.s10e10.avi')
        names = self.tv.retrieve_episode_name(details[0],details[1],details[2])
        path = self.tv.build_path(details, series_name=names[0], episode_name=names[1])
        assert_equal('tests/data/files/Stargate SG-1 - 1010 - Quest (1).avi', path)