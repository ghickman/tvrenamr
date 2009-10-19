from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr
from core.lib.thetvdb import TheTvDb
from core.errors import *

class TestTheTvDb(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files/", log_level='critical')
    
    def test_searching_the_tv_db_with_an_ambiguous_name_returns_the_correct_show(self):
        assert_equal(self.tv.retrieve_episode_name('the o.c.', '03', '04')['series'], 'The O.C.')
    
    def test_searching_the_tv_db_for_an_incorrect_name_returns_a_show_not_found_exception(self):
        assert_raises(ShowNotFoundException, self.tv.retrieve_episode_name, 'west wing', '04', '01')
    
    def test_searching_the_tv_db_for_an_episode_that_does_not_exist_returns_an_episode_not_found_exception(self):
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, 'chuck', '03', '32')