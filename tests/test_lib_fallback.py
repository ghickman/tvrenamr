from mock import patch
from pytest import raises

from tvrenamr.errors import NoMoreLibrariesException
from tvrenamr.libraries import TheTvDb, TvRage
from tvrenamr.main import Episode

from .base import BaseTest
from .mock_requests import initially_bad_xml, invalid_xml


class TestLibrariesFallback(BaseTest):
    @patch('tvrenamr.libraries.requests.get', new=invalid_xml)
    def test_rename_with_all_libraries_returning_invalid_xml(self):
        with raises(NoMoreLibrariesException):
            self.tv.retrieve_episode_title(self._file.episodes[0])

    @patch('tvrenamr.libraries.requests.get', new=initially_bad_xml)
    def test_rename_with_tvdb_falling_over(self):
        episode = Episode(self._file, '8')
        title = self.tv.retrieve_episode_title(episode)
        assert title == 'The Adhesive Duck Deficiency'

    def test_setting_library_stops_fallback(self):
        libraries = self.tv._get_libraries('thetvdb')
        assert type(libraries) == list
        assert len(libraries) == 1
        assert libraries[0] == TheTvDb

        libraries = self.tv._get_libraries('tvrage')
        assert type(libraries) == list
        assert len(libraries) == 1
        assert libraries[0] == TvRage
