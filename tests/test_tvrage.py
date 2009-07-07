from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr
from core.tvrage import TvRage

class TestTheTvDb(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files/")
    
    def test_searching_tv_rage_with_an_ambiguous_name_returns_the_correct_show(self):
        pass
    