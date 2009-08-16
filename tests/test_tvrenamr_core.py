import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestTvrenamrCore(object):
    
    def setUp(self):
        files = 'tests/data/files'
        working = 'tests/data/working'
        self.tv = TvRenamr(working)
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(working, fn))
    
    def tearDown(self):
        working = 'tests/data/working'
        for fn in os.listdir(working): os.remove(os.path.join(working,fn))
    
    def test_instantiate_core(self):
        assert_true(isinstance(TvRenamr("/"), TvRenamr))
    
    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        fn = 'avatar.s1e08.blah.HDTV.XViD.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series='Avatar: The Last Airbender', season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3])
        assert_equal(self.tv.rename(fn, path), 'Avatar: The Last Airbender - 108 - Winter Solstice (2): Avatar Roku.avi')
    
    def test_passing_in_a_season_number_to_retrieve_episode_name_returns_the_correct_episode_name_from_that_season(self):
        details = self.tv.extract_episode_details_from_file('chuck.s1e08.blah.avi')
        names = self.tv.retrieve_episode_name(series=details[0], season='2', episode=details[2])
        assert_equal(names[1], 'Chuck Versus the Gravitron')
    
    def test_passing_in_a_season_number_renames_a_file_using_that_season_number(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series=details[0], season='2', episode=details[2])
        path = self.tv.build_path(series=names[0], season='2', episode=details[2], episode_name=names[1], extension=details[3])
        assert_equal(self.tv.rename(fn, path), 'Chuck - 208 - Chuck Versus the Gravitron.avi')
    
    def test_passing_in_an_episode_number_renames_a_file_using_that_episode_number(self):
        details = self.tv.extract_episode_details_from_file('chuck.s1e08.blah.HDTV.XViD.avi')
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode='9')
        assert_equal('Chuck Versus the Imported Hard Salami', names[1])
    
    def test_using_auto_move_returns_the_correct_path_based_on_the_episode(self):
        details = self.tv.extract_episode_details_from_file('true.blood.0205.avi')
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move='tests/data/auto_move')
        assert_equal(path, 'tests/data/auto_move/True Blood/Season 2/True Blood - 205 - Never Let Me Go.avi')
    