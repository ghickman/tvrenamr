import os

from pytest import raises
from tvrenamr.errors import (EpisodeAlreadyExistsInDirectoryException,
                             MissingInformationException,
                             IncorrectCustomRegularExpressionSyntaxException,
                             UnexpectedFormatException)
from tvrenamr.main import File

from .base import BaseTest


class TestExceptionsAreRaised(BaseTest):
    def test_unexpected_format_exception_should_be_raised_when_unrecognised_file_format(self):
        with raises(UnexpectedFormatException):
            self.tv.extract_details_from_file('chuck.avi')

    def test_episode_already_exists_raise_exception(self):
        fn = 'The.Big.Bang.Theory.S03E01.HDTV.XviD-NoTV.avi'
        filename = 'The Big Bang Theory - 301 - The Electric Can Opener Fluctuation'
        existing_path = os.path.join(self.files, filename)
        with open(existing_path, 'w'):
            with raises(EpisodeAlreadyExistsInDirectoryException):
                self.tv.rename(fn, existing_path)

    def test_custom_syntax_snippets_missing_raises_exception(self):
        with raises(IncorrectCustomRegularExpressionSyntaxException):
            self.tv.extract_details_from_file('chuck.s02e05.avi', '.')

    def test_missing_show_name_raises_missing_information_exception(self):
        with raises(MissingInformationException):
            File(season=1, episodes=[1]).safety_check()

    def test_missing_season_raises_missing_information_exception(self):
        with raises(MissingInformationException):
            File(show_name='foo', episodes=[1]).safety_check()

    def test_missing_episode_raises_missing_information_exception(self):
        with raises(MissingInformationException):
            File(show_name='foo', season=1,).safety_check()
