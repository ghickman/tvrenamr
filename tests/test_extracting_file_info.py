from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestExtractFileInfo(object):
    
    def test_instantiate_core(self):
        assert_true(isinstance(TvRenamr("/"), TvRenamr))
    