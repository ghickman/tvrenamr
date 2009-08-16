import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestAutoMoving(object):
    
    def setUp(self):
        files = 'tests/data/files'
        working = 'tests/data/working'
        self.tv = TvRenamr(working)
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(working, fn))
    
    def tearDown(self):
        working = 'tests/data/working'
        auto_move = 'tests/data/auto_move/'
        for fn in os.listdir(working): os.remove(os.path.join(working,fn))
        for each_tuple in os.walk(auto_move):
            for fname in each_tuple[2]:
                os.remove(os.path.join(each_tuple[0],fname))
        for fn in os.listdir(auto_move): shutil.rmtree(os.path.join(auto_move,fn))
    
    def test_using_auto_move_renames_the_file_correctly(self):
        fn = 'chuck.s1e06.foo.HD.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move='tests/data/auto_move')
        assert_equal(self.tv.rename(fn, path), 'Chuck - 106 - Chuck Versus the Sandworm.avi')
    
    def test_using_auto_move_moves_the_file_to_the_correct_folder(self):
        fn = 'stargate.sg-1.s10e18.xvid.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move='tests/data/auto_move')
        self.tv.rename(fn, path)
        auto_move = 'tests/data/auto_move'
        for fn in os.listdir(auto_move):
            if fn == 'Stargate SG-1':
                full_path = fn
                for other in os.listdir(os.path.join(auto_move,fn)):
                    if other == 'Season 10':
                        full_path = full_path +'/'+ other +'/'
                        for fn in os.listdir(os.path.join(auto_move,full_path)):
                            full_path = full_path + fn
        assert_equal(full_path, 'Stargate SG-1/Season 10/Stargate SG-1 - 1018 - Family Ties.avi')
    