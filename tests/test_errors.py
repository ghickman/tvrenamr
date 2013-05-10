import os

from mock import patch
from nose.tools import assert_raises
from tvrenamr.errors import (EpisodeAlreadyExistsInDirectoryException,
                             NoMoreLibrariesException,
                             IncorrectCustomRegularExpressionSyntaxException,
                             UnexpectedFormatException)

from .base import BaseTest
from .mock_requests import bad_response


class TestExceptionsAreRaised(BaseTest):
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        args = (self.tv.extract_details_from_file, 'chuck.avi')
        assert_raises(UnexpectedFormatException, *args)

    @patch('requests.get', new=bad_response)
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
