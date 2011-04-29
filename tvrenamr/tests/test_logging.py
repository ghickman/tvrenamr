from os import listdir, mkdir
from os.path import dirname, isfile, join
from shutil import copy, rmtree

from nose.tools import assert_true

import urlopenmock #stub urlopen calls

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.main import TvRenamr

class TestLogging(object):
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/data/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        for fn in listdir(files):
            copy(join(files, fn), join(self.working, fn))

    def tearDown(self):
        rmtree(self.working)
        mkdir(self.working)

    def test_passing_in_a_series_name_renames_a_file_using_that_name(self):
        fn = 'avatar.s1e08.blah.HDTV.XViD.avi'
        episode = Episode()
        episode.show, episode.season, episode.episode, episode.extension = self.tv.extract_details_from_file(fn, user_regex='%n.s%s{1}e%e{2}.blah')
        episode.show = 'Avatar: The Last Airbender'
        episode.title = 'Winter Solstice (2): Avatar Roku'
        path = self.tv.build_path(episode, organise=False)
        self.tv.rename(fn, path)
        assert_true(isfile(join(self.working, 'Avatar, The Last Airbender - 108 - Winter Solstice (2), Avatar Roku.avi')))

