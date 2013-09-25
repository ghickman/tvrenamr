import os

from nose.tools import assert_equal, assert_true
from tvrenamr.main import File, TvRenamr

from .base import BaseTest


class TestMain(BaseTest):
    def test_instantiate_core(self):
        assert_true(isinstance(TvRenamr('/', self.config), TvRenamr))

    def test_passing_in_a_show_name_renames_a_file_using_that_name(self):
        show_name = 'Doctor Who (2005)'
        _file = File('doctor who', '5', ['10'], 'mp4')
        _file.show_name = show_name
        _file.episodes[0].title = ''
        path = self.tv.build_path(_file, organise=False)
        assert_equal(os.path.split(path.split('-')[0].strip())[1], show_name)

    def test_passing_in_a_season_number_to_retrieve_episode_name_returns_the_correct_episode_name_from_that_season(self):
        _file = File('chuck', '1', ['08'], 'mp4')
        _file.season = '2'
        _file.episodes[0].title = ''
        title = self.tv.retrieve_episode_title(_file.episodes[0])
        assert_equal(title, 'Chuck Versus the Gravitron')

    def test_passing_in_a_season_number_renames_a_file_using_that_season_number(self):
        self._file.season = '2'
        path = self.tv.build_path(self._file, organise=False)
        season_number = path.split('-')[1].strip()[0]
        assert_equal(season_number, '2')

    def test_passing_in_an_episode_number_returns_the_correct_episode_title(self):
        self._file.episodes[0].number = '3'
        title = self.tv.retrieve_episode_title(self._file.episodes[0])
        assert_equal(title, 'The Gothowitz Deviation')

    def test_passing_in_an_episode_number_renames_a_file_using_that_episode_number(self):
        self._file.episodes[0].number = '3'
        path = self.tv.build_path(self._file, organise=False)
        assert_equal(path.split('-')[1].strip()[-2:], '03')

    def test_setting_the_position_of_a_shows_leading_the_to_the_end_of_the_file_name(self):
        self.tv.retrieve_episode_title(self._file.episodes[0])
        self._file.show_name = self.tv.format_show_name(self._file.show_name, the=True)
        assert_equal(self._file.show_name, 'Big Bang Theory, The')

    def test_setting_an_episodes_format_as_name_season_episode_title(self):
        self._file.output_format = '%n - %s%e - %t%x'
        path = self.tv.build_path(self._file, organise=False)
        filename = 'The Big Bang Theory - 301 - The Electric Can Opener Fluctuation.mp4'
        assert_equal(os.path.split(path)[1], filename)

    def test_setting_an_episodes_format_as_season_episode_title_name(self):
        self._file.output_format = '%s - %e - %t - %n%x'
        path = self.tv.build_path(self._file, organise=False)
        filename = '3 - 01 - The Electric Can Opener Fluctuation - The Big Bang Theory.mp4'
        assert_equal(os.path.split(path)[1], filename)

    def test_setting_an_episodes_format_as_title_episode_season_name(self):
        self._file.output_format = '%t - %e - %s - %n%x'
        path = self.tv.build_path(self._file, organise=False)
        filename = 'The Electric Can Opener Fluctuation - 01 - 3 - The Big Bang Theory.mp4'
        assert_equal(os.path.split(path)[1], filename)

    def test_setting_season_number_digit_length(self):
        self._file.output_format = '%n S%s{2}E%e %t%x'
        path = self.tv.build_path(self._file, organise=False)
        filename = 'The Big Bang Theory S03E01 The Electric Can Opener Fluctuation.mp4'
        assert_equal(os.path.split(path)[1], filename)

    def test_setting_episode_number_digit_length(self):
        self._file.output_format = '%n S%sE%e{2} %t%x'
        path = self.tv.build_path(self._file, organise=False)
        filename = 'The Big Bang Theory S3E01 The Electric Can Opener Fluctuation.mp4'
        assert_equal(os.path.split(path)[1], filename)

    def test_setting_season_and_episode_number_digit_length(self):
        self._file.output_format = '%n S%s{3}E%e{4} %t%x'
        path = self.tv.build_path(self._file, organise=False)
        filename = 'The Big Bang Theory S003E0001 The Electric Can Opener Fluctuation.mp4'
        assert_equal(os.path.split(path)[1], filename)

    def test_extracting_season_from_file_format_s0e00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.s2e06.avi')['season'], '2')

    def test_extracting_season_from_file_format_s00e00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.s20e05.avi')['season'], '20')

    def test_extracting_episode_from_file_format_s0e00(self):
        details = self.tv.extract_details_from_file('chuck.s2e05.avi')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_episode_from_file_format_s00e00(self):
        details = self.tv.extract_details_from_file('chuck.s20e05.avi')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_season_from_file_format_0x00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.2x05.avi')['season'], '2')

    def test_extracting_season_from_file_format_00x00(self):
        assert_equal(self.tv.extract_details_from_file('chuck.20x05.avi')['season'], '20')

    def test_extracting_episode_from_file_format_0x00(self):
        details = self.tv.extract_details_from_file('chuck.2x05.avi')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_episode_from_file_format_00x00(self):
        details = self.tv.extract_details_from_file('chuck.20x05.avi')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_season_from_file_format_000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.205.avi')['season'], '2')

    def test_extracting_season_from_file_format_0000(self):
        assert_equal(self.tv.extract_details_from_file('chuck.2005.avi')['season'], '20')

    def test_extracting_episode_from_file_format_000(self):
        details = self.tv.extract_details_from_file('chuck.205.avi')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_episode_from_file_format_0000(self):
        details = self.tv.extract_details_from_file('chuck.2005.avi')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_season_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        details = self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')
        assert_equal(details['season'], '2')

    def test_extracting_episode_with_custom_regular_expression_passing_in_season_and_episode_digit_lengths_from_file_format_000(self):
        details = self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s{2}%e{1}')
        assert_equal(details['episodes'][0], '5')

    def test_extracting_season_with_custom_regular_expression_passing_in_season_digit_lengths_from_file_format_000(self):
        details = self.tv.extract_details_from_file('chuck.0250', user_regex='%n.%s{2}%e')
        assert_equal(details['season'], '2')

    def test_extracting_season_with_custom_regular_expression_passing_in_episode_digit_lengths_from_file_format_000(self):
        details = self.tv.extract_details_from_file('chuck.025', user_regex='%n.%s%e{1}')
        assert_equal(details['season'], '2')

    def test_720_before_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.720.S01E03.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_720_after_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.S01E03.720.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_720p_before_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.720p.S01E03.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_720p_after_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.S01E03.720p.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_1080_before_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.1080.S01E03.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_1080_after_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.S01E03.1080.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_1080p_before_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.1080p.S01E03.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_1080p_after_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.S01E03.1080p.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_H264_before_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.H.264.S01E03.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_H264_after_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.S01E03.H.264.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_h264_before_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.h.264.S01E03.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')

    def test_h264_after_season_and_episode(self):
        details = self.tv.extract_details_from_file('chuck.S01E03.h.264.mp4')
        assert_equal(details['show_name'], 'chuck')
        assert_equal(details['season'], '1')
        assert_equal(details['episodes'][0], '3')
