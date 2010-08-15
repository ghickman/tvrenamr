import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

import config

class TestConfig(object):
    working = 'tests/data/working'
    
    def setUp(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files):
            shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
    
    
    # def test passing in a 
    # test passing in a show not in the config
    # test passing in a show in the config but with no x option
    # test passing in a show in the config with x option
    # 
    # 
    # 