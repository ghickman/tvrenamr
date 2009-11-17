import shutil
import os

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr
from core.lib.tvrage import TvRage

class TestTvRage(object):
    working = 'tests/data/working'
    
    def setup(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    def test_searching_tv_rage_with_an_ambiguous_name_returns_the_correct_show(self):
        pass
    
    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        fn = 'chuck.s1e08.blah.HDTV.XViD.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(series=credentials['series'], season=credentials['season'], episode=credentials['episode'])
        credentials['title'] = title['title']
        path = self.tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'])
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.working, 'Chuck - 108 - Chuck Versus the Truth.avi')))
    