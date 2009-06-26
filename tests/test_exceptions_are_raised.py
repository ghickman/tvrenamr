import urllib2

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr
from core.errors import *

class TestExceptionsAreRaised(object):
    
    def setup(self):
        self.tv = TvRenamr("/")
    
    def test_exception_raised_when_file_already_named_correctly(self):
        assert_raises(AlreadyNamedException, self.tv.rename, 'Chuck - 205 - w00t.avi')
    
    def test_exception_raised_when_unrecognised_file_format(self):
        assert_raises(UnexpectedFormatException, self.tv.rename, 'chuck .avi')
    
    def test_exception_raised_when_episode_not_found(self):
        assert_raises(urllib2.URLError, self.tv.rename, 'chuck.s04e05.avi')