# -*- coding: utf-8 -*-
import os

from tvrenamr.config import Config
from tvrenamr.main import File, TvRenamr
import pytest


def test_instantiate_core():
    assert isinstance(TvRenamr('/', Config()), TvRenamr)


def test_passing_in_a_show_name_renames_a_file_using_that_name(files, tv):
    show_name = 'Doctor Who (2005)'
    _file = File('doctor who', '5', ['10'], 'mp4')
    _file.show_name = show_name
    _file.episodes[0].title = ''
    path = tv.build_path(_file, rename_dir=files, organise=False)
    assert os.path.split(path.split('-')[0].strip())[1] == show_name


def test_passing_in_a_season_number_to_retrieve_episode_name_returns_the_correct_episode_name_from_that_season(tv):  # noqa
    _file = File('chuck', '1', ['08'], 'mp4')
    _file.season = '2'
    _file.episodes[0].title = ''
    title = tv.retrieve_episode_title(_file.episodes[0])
    assert title == 'Chuck Versus the Gravitron'


@pytest.mark.usefixtures('files_path')
class TestWithBigBang:
    def setup(self):
        self._file = File('The Big Bang Theory', '3', ['01'], '.mp4')
        self._file.episodes[0].title = 'The Electric Can Opener Fluctuation'

    def test_passing_in_a_season_number_renames_a_file_using_that_season_number(self, files, tv):
        self._file.season = '2'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        season_number = path.split('-')[1].strip()[0]
        assert season_number == '2'

    def test_passing_in_an_episode_number_returns_the_correct_episode_title(self, tv):
        self._file.episodes[0].number = '3'
        title = tv.retrieve_episode_title(self._file.episodes[0])
        assert title == 'The Gothowitz Deviation'

    def test_passing_in_an_episode_number_renames_a_file_using_that_episode_number(self, files, tv):
        self._file.episodes[0].number = '3'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        assert path.split('-')[1].strip()[-2:] == '03'

    def test_setting_the_position_of_a_shows_leading_the_to_the_end_of_the_file_name(self, files, tv):
        tv.retrieve_episode_title(self._file.episodes[0])
        self._file.show_name = tv.format_show_name(self._file.show_name, the=True)
        assert self._file.show_name == 'Big Bang Theory, The'

    def test_setting_an_episodes_format_as_name_season_episode_title(self, files, tv):
        self._file.output_format = '%n - %s%e - %t%x'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        filename = 'The Big Bang Theory - 301 - The Electric Can Opener Fluctuation.mp4'
        assert os.path.split(path)[1] == filename

    def test_setting_an_episodes_format_as_season_episode_title_name(self, files, tv):
        self._file.set_output_format('%s - %e - %t - %n%x')
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        filename = '3 - 01 - The Electric Can Opener Fluctuation - The Big Bang Theory.mp4'
        assert os.path.split(path)[1] == filename

    def test_setting_an_episodes_format_as_title_episode_season_name(self, files, tv):
        self._file.output_format = '%t - %e - %s - %n%x'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        filename = 'The Electric Can Opener Fluctuation - 01 - 3 - The Big Bang Theory.mp4'
        assert os.path.split(path)[1] == filename

    def test_setting_season_number_digit_length(self, files, tv):
        self._file.output_format = '%n S%s{2}E%e %t%x'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        filename = 'The Big Bang Theory S03E01 The Electric Can Opener Fluctuation.mp4'
        assert os.path.split(path)[1] == filename

    def test_setting_episode_number_digit_length(self, files, tv):
        self._file.output_format = '%n S%sE%e{2} %t%x'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        filename = 'The Big Bang Theory S3E01 The Electric Can Opener Fluctuation.mp4'
        assert os.path.split(path)[1] == filename

    def test_setting_season_and_episode_number_digit_length(self, files, tv):
        self._file.output_format = '%n S%s{3}E%e{4} %t%x'
        path = tv.build_path(self._file, rename_dir=files, organise=False)
        filename = 'The Big Bang Theory S003E0001 The Electric Can Opener Fluctuation.mp4'
        assert os.path.split(path)[1] == filename

    def test_no_organise_in_config(self, files, tv):
        filename = 'The Big Bang Theory - 301 - The Electric Can Opener Fluctuation.mp4'
        path = tv.build_path(self._file, rename_dir=files)
        expected = os.path.join(files, filename)
        assert path == expected


def test_extracting_season_from_file_format_s0e00(tv):
    season = tv.extract_details_from_file('chuck.s2e06.avi')['season']
    assert season == '2'


def test_extracting_season_from_file_format_s00e00(tv):
    season = tv.extract_details_from_file('chuck.s20e05.avi')['season']
    assert season == '20'


def test_extracting_episode_from_file_format_s0e00(tv):
    details = tv.extract_details_from_file('chuck.s2e05.avi')
    assert details['episodes'][0] == '5'


def test_extracting_episode_from_file_format_s00e00(tv):
    details = tv.extract_details_from_file('chuck.s20e05.avi')
    assert details['episodes'][0] == '5'


def test_extracting_season_from_file_format_0x00(tv):
    season = tv.extract_details_from_file('chuck.2x05.avi')['season']
    assert season == '2'


def test_extracting_season_from_file_format_00x00(tv):
    season = tv.extract_details_from_file('chuck.20x05.avi')['season']
    assert season == '20'


def test_extracting_episode_from_file_format_0x00(tv):
    details = tv.extract_details_from_file('chuck.2x05.avi')
    assert details['episodes'][0] == '5'


def test_extracting_episode_from_file_format_00x00(tv):
    details = tv.extract_details_from_file('chuck.20x05.avi')
    assert details['episodes'][0] == '5'


def test_extracting_season_from_file_format_000(tv):
    season = tv.extract_details_from_file('chuck.205.avi')['season']
    assert season == '2'


def test_extracting_season_from_file_format_0000(tv):
    season = tv.extract_details_from_file('chuck.2005.avi')['season']
    assert season == '20'


def test_extracting_episode_from_file_format_000(tv):
    details = tv.extract_details_from_file('chuck.205.avi')
    assert details['episodes'][0] == '5'


def test_extracting_episode_from_file_format_0000(tv):
    details = tv.extract_details_from_file('chuck.2005.avi')
    assert details['episodes'][0] == '5'


def test_extracting_season_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(tv):  # noqa
    regex = '%n.%s{2}%e{1}'
    details = tv.extract_details_from_file('chuck.025', user_regex=regex)
    assert details['season'] == '2'


def test_extracting_episode_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(tv):  # noqa
    regex = '%n.%s{2}%e{1}'
    details = tv.extract_details_from_file('chuck.025', user_regex=regex)
    assert details['episodes'][0] == '5'


def test_extracting_season_with_custom_regular_expression_passing_in_season_digit_lengths_from_file_format_000(tv):  # noqa
    regex = '%n.%s{2}%e'
    details = tv.extract_details_from_file('chuck.0250', user_regex=regex)
    assert details['season'] == '2'


def test_extracting_season_with_custom_regular_expression_passing_in_episode_digit_lengths_from_file_format_000(tv):  # noqa
    regex = '%n.%s%e{1}'
    details = tv.extract_details_from_file('chuck.025', user_regex=regex)
    assert details['season'] == '2'


def test_720_before_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.720.S01E03.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_720_after_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.S01E03.720.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_720p_before_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.720p.S01E03.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_720p_after_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.S01E03.720p.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_1080_before_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.1080.S01E03.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_1080_after_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.S01E03.1080.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_1080p_before_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.1080p.S01E03.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_1080p_after_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.S01E03.1080p.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_H264_before_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.H.264.S01E03.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_H264_after_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.S01E03.H.264.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_h264_before_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.h.264.S01E03.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_h264_after_season_and_episode(tv):
    details = tv.extract_details_from_file('chuck.S01E03.h.264.mp4')
    assert details['show_name'] == 'chuck'
    assert details['season'] == '1'
    assert details['episodes'][0] == '3'


def test_unicode_in_filename(tv):
    fn = 'chuck.s03e04.hdtv.’.mkv'
    details = tv.extract_details_from_file(fn)
    expected = {
        'show_name': 'chuck',
        'season': '3',
        'episodes': ['4'],
        'extension': '.mkv',
    }
    assert details == expected
