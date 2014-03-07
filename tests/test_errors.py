import os

from mock import patch
from nose.tools import assert_raises
from tvrenamr.errors import (EpisodeAlreadyExistsInDirectoryException,
                             MissingInformationException,
                             NoMoreLibrariesException,
                             IncorrectCustomRegularExpressionSyntaxException,
                             UnexpectedFormatException)
from tvrenamr.main import File

from .base import BaseTest
from .mock_requests import bad_response


class TestExceptionsAreRaised(BaseTest):
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        args = (self.tv.extract_details_from_file, 'chuck.avi')
        assert_raises(UnexpectedFormatException, *args)

    @patch('tvrenamr.libraries.requests.get', new=bad_response)
    def test_nonexistant_episode_doesnt_work_on_any_library(self):
        args = (
           NoMoreLibrariesException,
           self.tv.retrieve_episode_title,
           self._file.episodes[0],
        )
        assert_raises(*args)

    def test_episode_already_exists_raise_exception(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        filename = 'The Big Bang Theory - 301 - The Electric Can Opener Fluctuation'
        existing_path = os.path.join(self.files, filename)
        args = (self.tv.rename, fn, existing_path)
        with open(existing_path, 'w'):
            assert_raises(EpisodeAlreadyExistsInDirectoryException, *args)

    def test_custom_syntax_snippets_missing_raises_exception(self):
        assert_raises(
            IncorrectCustomRegularExpressionSyntaxException,
            self.tv.extract_details_from_file,
            'chuck.s02e05.avi',
            '.'
        )

    def test_missing_show_name_raises_missing_information_exception(self):
        _file = File(season=1, episodes=[1])
        assert_raises(MissingInformationException, _file.safety_check)

    def test_missing_season_raises_missing_information_exception(self):
        _file = File(show_name='foo', episodes=[1])
        assert_raises(MissingInformationException, _file.safety_check)

    def test_missing_episode_raises_missing_information_exception(self):
        _file = File(show_name='foo', season=1,)
        assert_raises(MissingInformationException, _file.safety_check)
