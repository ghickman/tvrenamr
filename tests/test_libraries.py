from nose.tools import assert_equal, assert_raises

from tvrenamr.episode import Episode
from tvrenamr.errors import NoMoreLibrariesException

from .base import BaseTest


class TestLibraries(BaseTest):
    libs = ('thetvdb', 'tvrage')

    def test_searching_with_an_ambiguous_name_returns_the_correct_show(self):
        episode = Episode(show_name='the o.c.', season=3, episode=4, extension='.avi')
        for library in self.libs:
            self.tv.retrieve_episode_name(episode, library=library)
            assert_equal(self.tv.format_show_name(episode.show_name, the=False), 'The O.C.')
            assert_equal(self.tv.format_show_name(episode.show_name), 'O.C., The')

    def test_searching_for_an_incorrect_name_returns_an_exception(self):
        episode = Episode(show_name='west, wing', season=4, episode=1, extension='.avi')
        for library in self.libs:
            assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name,
                          episode, library=library)

    def test_searching_for_an_episode_that_does_not_exist_returns_an_exception(self):
        episode = Episode(show_name='chuck', season=1, episode=99, extension='.avi')
        for library in self.libs:
            assert_raises(NoMoreLibrariesException, self.tv.retrieve_episode_name,
                          episode, library=library)

    def test_searching_for_a_specific_episode_returns_the_correct_episode(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        for library in self.libs:
            assert_equal(self.tv.retrieve_episode_name(episode, library=library),
                         'The Electric Can Opener Fluctuation')

    def test_the_return_of_a_formatted_show_name(self):
        fn = 'the.big.bang.theory.S03E01.HDTV.XviD-NoTV.avi'
        episode = Episode(**self.tv.extract_details_from_file(fn))
        for library in self.libs:
            self.tv.retrieve_episode_name(episode, library=library)
            assert_equal(self.tv.format_show_name(episode.show_name,
                         the=False), 'The Big Bang Theory')
            assert_equal(self.tv.format_show_name(episode.show_name),
                         'Big Bang Theory, The')

