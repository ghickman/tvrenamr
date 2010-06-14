import os, shutil

from nose.tools import *

import urlopenmock #stub urlopen calls
from main import TvRenamr

class TestLogging(object):
    working = 'tests/data/working'
    
    def setUp(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='debug')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        fn = 'avatar.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_episode_details_from_file(fn, user_regex='%n.s%s{1}e%e{2}.blah')
        credentials['show'] = 'Avatar: The Last Airbender'
        credentials['title'] = 'Winter Solstice (2): Avatar Roku'
        path = self.tv.build_path(**credentials)
        self.tv.rename(fn, path)
        assert_true(os.path.exists(os.path.join(self.working, 'Avatar, The Last Airbender - 108 - Winter Solstice (2), Avatar Roku.avi')))
    