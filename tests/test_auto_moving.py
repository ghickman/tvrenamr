import os, shutil

from nose.tools import *

#stub urlopen calls
import urlopenmock

from core.tvrenamr_core import TvRenamr

class TestAutoMoving(object):
    working = 'tests/data/working'
    auto_move = 'tests/data/auto_move'
    
    def setUp(self):
        files = 'tests/data/files'
        self.tv = TvRenamr(self.working)
        for fn in os.listdir(files): shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))
    
    def tearDown(self):
        for fn in os.listdir(self.working): os.remove(os.path.join(self.working,fn))
        for each_tuple in os.walk(self.auto_move):
            for fname in each_tuple[2]:
                os.remove(os.path.join(each_tuple[0],fname))
        for fn in os.listdir(self.auto_move): shutil.rmtree(os.path.join(self.auto_move,fn))
    
    def test_using_auto_move_renames_the_file_correctly(self):
        fn = 'chuck.s1e06.foo.HD.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move=self.auto_move)
        self.tv.rename(fn, path)
        assert_true(os.path.isfile(os.path.join(self.auto_move+'/Chuck/Season 1', 'Chuck - 106 - Chuck Versus the Sandworm.avi')))
    
    def test_using_auto_move_moves_the_file_to_the_correct_folder(self):
        fn = 'stargate.sg-1.s10e18.xvid.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move=self.auto_move)
        self.tv.rename(fn, path)
        for fn in os.listdir(self.auto_move):
            if fn == 'Stargate SG-1':
                full_path = fn
                for other in os.listdir(os.path.join(self.auto_move,fn)):
                    if other == 'Season 10':
                        full_path = full_path +'/'+ other +'/'
                        for fn in os.listdir(os.path.join(self.auto_move,full_path)):
                            full_path = full_path + fn
        assert_equal(full_path, 'Stargate SG-1/Season 10/Stargate SG-1 - 1018 - Family Ties.avi')
    
    def test_using_auto_move_returns_the_correct_path_based_on_the_episode(self):
        details = self.tv.extract_episode_details_from_file('true.blood.0205.avi')
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        path = self.tv.build_path(series=names[0], season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move=self.auto_move)
        assert_equal(path, 'tests/data/auto_move/True Blood/Season 2/True Blood - 205 - Never Let Me Go.avi')
    
    def test_setting_the_position_of_the_variable_to_true_places_a_shows_the_at_the_end_of_the_folder_name_with_automove(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        details = self.tv.extract_episode_details_from_file(fn)
        names = self.tv.retrieve_episode_name(series=details[0], season=details[1], episode=details[2])
        name = self.tv.set_position_of_the_to_the_end_of_a_shows_name(names[0])
        path = self.tv.build_path(series=name, season=details[1], episode=details[2], episode_name=names[1], extension=details[3], auto_move=self.auto_move)
        self.tv.rename(fn, path)
        assert_true(os.path.isdir(os.path.join(self.auto_move, 'Big Bang Theory, The/Season 3')))
    