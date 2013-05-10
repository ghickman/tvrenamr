from nose.tools import assert_equal, assert_raises

from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.main import File

from .base import BaseTest


class TestLibraries(BaseTest):
    libs = ('thetvdb', 'tvrage')

    def test_searching_with_an_ambiguous_name_returns_the_correct_show(self):
        _file = File('The O.C.', '3', ['04'], 'mp4')
        for library in self.libs:
            self.tv.retrieve_episode_title(_file.episodes[0], library=library)
            assert_equal(self.tv.format_show_name(_file.show_name, the=False), 'The O.C.')
            assert_equal(self.tv.format_show_name(_file.show_name), 'O.C., The')

    def test_searching_for_an_incorrect_name_returns_an_exception(self):
        _file = File('west, wing', '4', ['01'], '.mp4')
        for library in self.libs:
            args = (self.tv.retrieve_episode_title, _file.episodes[0], library)
            assert_raises(NoMoreLibrariesException, *args)

    def test_searching_for_an_episode_that_does_not_exist_returns_an_exception(self):
        _file = File('chuck', '1', ['99'], '.mp4')
        for library in self.libs:
            args = (self.tv.retrieve_episode_title, _file.episodes[0], library)
            assert_raises(NoMoreLibrariesException, *args)

    def test_searching_for_a_specific_episode_returns_the_correct_episode(self):
        for library in self.libs:
            title = self.tv.retrieve_episode_title(self._file.episodes[0], library=library)
            assert_equal(title, 'The Electric Can Opener Fluctuation')

    def test_the_return_of_a_formatted_show_name(self):
        for library in self.libs:
            self.tv.retrieve_episode_title(self._file.episodes[0], library=library)
            assert_equal(self.tv.format_show_name(self._file.show_name, the=False), 'The Big Bang Theory')
            assert_equal(self.tv.format_show_name(self._file.show_name), 'Big Bang Theory, The')
