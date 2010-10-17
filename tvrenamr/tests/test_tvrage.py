import shutil
import os

from nose.tools import *

#stub urlopen calls
import urlopenmock

from tvrenamr.main import TvRenamr
from tvrenamr.lib.tvrage import TvRage
from tvrenamr.errors import *

class TestTvRage(object):
    working = 'tests/data/working'
    
    def setup(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    
    def test_searching_tv_rage_with_an_ambiguous_name_returns_the_correct_show(self):
        self.tv.retrieve_episode_name(library='tvrage', **{'show':'the o.c.', 'season':'03', 'episode':'04'})
        assert_equal(self.tv.format_show_name('the o.c.', the=False), 'The O.C.')
    
    
    def test_searching_tv_rage_for_an_incorrect_name_returns_a_show_not_found_exception(self):
        assert_raises(ShowNotFoundException, self.tv.retrieve_episode_name, library='tvrage', **{'show':'west wing', 'season':'04', 'episode':'01'})
    
    
    def test_searching_tv_rage_for_an_episode_that_does_not_exist_returns_an_episode_not_found_exception(self):
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, library='tvrage', **{'show':'chuck', 'season':'03', 'episode':'32'})
    
    
    def test_searching_tv_rage_for_a_specific_episode_returns_the_correct_episode(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        credentials = self.tv.extract_details_from_file(fn)
        title = self.tv.retrieve_episode_name(library='tvrage', **credentials)
        assert_equals(title, 'The Electric Can Opener Fluctuation')
    
    
    def test_tv_rage_returns_a_formatted_show_name(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        credentials = self.tv.extract_details_from_file(fn)
        self.tv.retrieve_episode_name(library='tvrage', **credentials)
        assert_equals(self.tv.format_show_name(credentials['show'], the=False), 'The Big Bang Theory')
