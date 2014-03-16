from nose.tools import assert_equal

from .base import BaseTest


class TestSpecialFolder(BaseTest):
    def test_manually_setting_specials_folder_name(self):
        self.tv.debug = True
        args = ('foo', 'Chuck', 0, 'Specials')
        path = self.tv._build_organise_path(*args)
        assert_equal(path, 'foo/Chuck/Specials')

    def test_non_zero_season(self):
        self.tv.debug = True
        args = ('foo', 'Chuck', 2)
        path = self.tv._build_organise_path(*args)
        assert_equal(path, 'foo/Chuck/Season 2')

    def test_setting_specials_folder_in_config_defaults(self):
        self.tv.debug = True
        self.tv.config.config['defaults']['specials_folder'] = 'Specials'
        args = ('foo', 'Chuck', 0)
        path = self.tv._build_organise_path(*args)
        assert_equal(path, 'foo/Chuck/Specials')

    def test_setting_specials_folder_in_config_show_name(self):
        self.tv.debug = True
        self.tv.config.config['chuck']['specials_folder'] = 'Specials'
        args = ('foo', 'Chuck', 0)
        path = self.tv._build_organise_path(*args)
        assert_equal(path, 'foo/Chuck/Specials')
