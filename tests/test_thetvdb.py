import shutil
import os

from nose.tools import *

#stub urlopen calls
import urlopenmock

from main import TvRenamr
from lib.thetvdb import TheTvDb
from errors import *

class TestTheTvDb(object):
    working = 'tests/data/working'
    
    def setup(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    def test_searching_the_tv_db_with_an_ambiguous_name_returns_the_correct_show(self):
        assert_equal(self.tv.retrieve_episode_name(library='thetvdb', **{'show':'the o.c.', 'season':'03', 'episode':'04'})[0], 'The O.C.')
    
    def test_searching_the_tv_db_for_an_incorrect_name_returns_a_show_not_found_exception(self):
        assert_raises(ShowNotFoundException, self.tv.retrieve_episode_name, library='thetvdb', **{'show':'west wing', 'season':'04', 'episode':'01'})
    
    def test_searching_the_tv_db_for_an_episode_that_does_not_exist_returns_an_episode_not_found_exception(self):
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, 'chuck', '03', '32', 'thetvdb')
    
    def test_searching_the_tv_db_for_a_specific_episode_returns_the_correct_episode(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(library='thetvdb', **credentials)[1]
        assert_equals(title, 'The Electric Can Opener Fluctuation')
    
    def test_the_tv_db_returns_a_formatted_show_name(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        credentials = self.tv.extract_episode_details_from_file(fn)
        title = self.tv.retrieve_episode_name(library='thetvdb', **credentials)[0]
        assert_equals(title, 'The Big Bang Theory')
    