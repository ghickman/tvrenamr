from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr
from core.lib.tvrage import TvRage

class TestTvRage(object):
    
    def setup(self):
        self.tv = TvRenamr("tests/data/files/", log_level='critical')
    
    def test_searching_tv_rage_with_an_ambiguous_name_returns_the_correct_show(self):
        pass
    