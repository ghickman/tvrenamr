from os.path import dirname, join
from shutil import copytree, rmtree

from nose.tools import assert_equal, assert_raises

from tvrenamr.config import Config
from tvrenamr.episode import Episode
from tvrenamr.errors import EpisodeNotFoundException, ShowNotFoundException
from tvrenamr.main import TvRenamr
import urlopenmock

class TestLibraries(object):
    libs = ('thetvdb', 'tvrage')
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/files'
        self.config = Config(join(dirname(__file__), 'config.yml'))
        self.tv = TvRenamr(self.working, self.config)
        copytree(files, self.working)

    def tearDown(self):
        rmtree(self.working)

    def test_searching_with_an_ambiguous_name_returns_the_correct_show(self):
        episode = Episode(('the o.c.', 3, 4, '.avi'))
        for library in self.libs:
            self.tv.retrieve_episode_name(episode, library=library)
            assert_equal(self.tv.format_show_name(episode.show_name, the=False), 'The O.C.')
            assert_equal(self.tv.format_show_name(episode.show_name), 'O.C., The')

    def test_searching_for_an_incorrect_name_returns_an_exception(self):
        episode = Episode(('west, wing', 4, 1, '.avi'))
        for library in self.libs:
            assert_raises(ShowNotFoundException, self.tv.retrieve_episode_name,
                          episode, library=library)

    def test_searching_for_an_episode_that_does_not_exist_returns_an_exception(self):
        episode = Episode(('chuck', 1, 99, '.avi'))
        for library in self.libs:
            assert_raises(EpisodeNotFoundException, self.tv.retrieve_episode_name,
                          episode, library=library)

    def test_searching_for_a_specific_episode_returns_the_correct_episode(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        for library in self.libs:
            assert_equal(self.tv.retrieve_episode_name(episode, library=library),
                         'The Electric Can Opener Fluctuation')

    def test_the_return_of_a_formatted_show_name(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode(self.tv.extract_details_from_file(fn))
        for library in self.libs:
            self.tv.retrieve_episode_name(episode, library=library)
            assert_equal(self.tv.format_show_name(episode.show_name, the=False), 'The Big Bang Theory')
            assert_equal(self.tv.format_show_name(episode.show_name), 'Big Bang Theory, The')

