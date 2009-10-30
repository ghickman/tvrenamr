import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.core import TvRenamr

class TestTvrenamr(object):
    working = 'test/data/working'
    
    def setUp(self):
        files = 'test/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
