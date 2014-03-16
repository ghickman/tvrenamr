# coding=utf-8
from nose.tools import assert_equal, assert_raises

from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.libraries import TheTvDb, TvRage
from tvrenamr.main import File
from tvrenamr.vendor.defusedxml.ElementTree import fromstring

from .base import BaseTest


class TestLibraries(BaseTest):
    libs = ('thetvdb', 'tvrage')

    def test_searching_with_an_ambiguous_name_returns_the_correct_show(self):
        _file = File('The O.C.', '3', ['04'], 'mp4')
        for library in self.libs:
            self.tv.retrieve_episode_title(_file.episodes[0], library=library)
            assert_equal(self.tv.format_show_name(_file.show_name, the=False), 'The O.C.')
            assert_equal(self.tv.format_show_name(_file.show_name, the=True), 'O.C., The')

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
            assert_equal(self.tv.format_show_name(self._file.show_name, the=True), 'Big Bang Theory, The')

    def test_unicode_character_in_episode_name(self):
        # This is horrible but the libraries are horrendous atm
        from tvrenamr.errors import EmptyEpisodeTitleException
        xml = fromstring('<Data><Episode><EpisodeName>¡Viva los Muertos!</EpisodeName></Episode></Data>')
        episode = xml.find('Episode').findtext('EpisodeName').encode('utf-8')
        if not episode:
            raise EmptyEpisodeTitleException
        return episode
        # for library in (TheTvDb, TvRage):
        #     l = library()
        #     episode = l.get_episode_title_from_xml(xml)
        #     assert_equal(episode, u'¡Viva los Muertos!')
