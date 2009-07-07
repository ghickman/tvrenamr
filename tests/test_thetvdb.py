from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr
from core.thetvdb import TheTvDb
from core.errors import *

class TestTheTvDb(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files/")
    
    def test_searching_the_tv_db_with_an_ambiguous_name_returns_the_correct_show(self):
        details = self.tv.extract_episode_details_from_file('chuck.s02e05.avi')
        name = self.tv.retrieve_episode_name(details[0],details[1],details[2])
        path = self.tv.build_path(details,name)
        assert_raises(EpisodeAlreadyExistsInFolderException, self.tv.rename, 'chuck.s02e05.avi', path)
    