from os import listdir, mkdir
from os.path import dirname, join
from shutil import copy, rmtree

from nose.tools import assert_equal, assert_raises

#stub urlopen calls
import urlopenmock

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.errors import EpisodeNotFoundException, ShowNotFoundException
from tvrenamr.main import TvRenamr

class TestTheTvDb(object):
    library = 'thetvdb'
    working = 'tests/data/working'

    def setup(self):
        files = 'tests/data/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        for fn in listdir(files):
            copy(join(files, fn), join(self.working, fn))

    def tearDown(self):
        rmtree(self.working)
        mkdir(self.working)

    def test_searching_the_tv_db_with_an_ambiguous_name_returns_the_correct_show(self):
        episode = Episode()
        episode.show = 'the o.c.'
        episode.season = 3
        episode.episode = 4
        self.tv.retrieve_episode_name(episode, library=self.library)
        assert_equal(self.tv.format_show_name(episode.show, the=False), 'The O.C.')
        assert_equal(self.tv.format_show_name(episode.show), 'O.C., The')

    def test_searching_the_tv_db_for_an_incorrect_name_returns_a_show_not_found_exception(self):
        episode = Episode()
        episode.show = 'west wing'
        episode.season = 4
        episode.episode = 1
        assert_raises(ShowNotFoundException, self.tv.retrieve_episode_name, episode, library=self.library)

    def test_searching_the_tv_db_for_an_episode_that_does_not_exist_returns_an_episode_not_found_exception(self):
        episode = Episode()
        episode.show = 'chuck'
        episode.season = 1
        episode.episode = 99
        assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name, episode, library=self.library)

    def test_searching_the_tv_db_for_a_specific_episode_returns_the_correct_episode(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode()
        episode.show, episode.season, episode.episode, episode.extension = self.tv.extract_details_from_file(fn)
        assert_equal(self.tv.retrieve_episode_name(episode, library=self.library), 'The Electric Can Opener Fluctuation')

    def test_the_tv_db_returns_a_formatted_show_name(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode()
        episode.show, episode.season, episode.episode, episode.extension = self.tv.extract_details_from_file(fn)
        self.tv.retrieve_episode_name(episode, library=self.library)
        assert_equal(self.tv.format_show_name(episode.show, the=False), 'The Big Bang Theory')
        assert_equal(self.tv.format_show_name(episode.show), 'Big Bang Theory, The')

