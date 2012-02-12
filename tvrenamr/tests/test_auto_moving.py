from os import listdir, mkdir
from os.path import isdir, isfile, join
from shutil import rmtree

from nose.tools import assert_equal, assert_true

from tvrenamr.episode import Episode
from tvrenamr.tests.base import BaseTest


class TestAutoMoving(BaseTest):
    organise = True
    organised = 'tests/data/organised'

    def teardown(self):
        super(TestAutoMoving, self).teardown()
        rmtree(self.organised)
        mkdir(self.organised)

    def test_using_organise_renames_the_file_correctly(self):
        fn = 'chuck.s1e06.foo.HD.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        path = self.tv.build_path(episode, organise=self.organise, rename_dir=self.organised)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.organised + '/Chuck/Season 1', 'Chuck - 106 - Chuck Versus the Sandworm.avi')))

    def test_using_organise_moves_the_file_to_the_correct_folder(self):
        fn = 'stargate.sg-1.s10e18.xvid.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name)
        path = self.tv.build_path(episode, organise=self.organise, rename_dir=self.organised)
        self.tv.rename(fn, path)
        for fn in listdir(self.organised):
            if fn == 'Stargate SG-1':
                full_path = fn
                for other in listdir(join(self.organised,fn)):
                    if other == 'Season 10':
                        full_path = full_path +'/'+ other +'/'
                        for fn in listdir(join(self.organised,full_path)):
                            full_path = full_path + fn
        assert_equal(full_path, 'Stargate SG-1/Season 10/Stargate SG-1 - 1018 - Family Ties.avi')

    def test_using_organise_returns_the_correct_path_based_on_the_episode(self):
        episode = Episode(self.tv.extract_details_from_file('true.blood.0205.avi'))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name, the=False)
        path = self.tv.build_path(episode, organise=self.organise, rename_dir=self.organised)
        assert_equal(path, 'tests/data/organised/True Blood/Season 2/True Blood - 205 - Never Let Me Go.avi')

    def test_moving_the_leading_the_to_the_end_of_a_show_name_causes_the_show_folder_name_to_follow_suit_when_using_organise(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        episode.title = self.tv.retrieve_episode_name(episode)
        episode.show_name = self.tv.format_show_name(episode.show_name, the=True)
        path = self.tv.build_path(episode, organise=self.organise, rename_dir=self.organised)
        self.tv.rename(fn, path)
        assert_true(isdir(join(self.organised, 'Big Bang Theory, The/Season 3')))

