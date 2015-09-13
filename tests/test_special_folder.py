import os

from .base import BaseTest


class TestSpecialFolder(BaseTest):
    def test_manually_setting_specials_folder_name(self):
        self.tv.debug = True
        args = ('foo', 'Chuck', 0, 'Specials')
        path = self.tv._build_organise_path(*args)
        assert path == 'foo/Chuck/Specials'

    def test_non_zero_season(self):
        self.tv.debug = True
        args = ('foo', 'Chuck', 2)
        path = self.tv._build_organise_path(*args)
        assert path == 'foo/Chuck/Season 2'

    def test_setting_specials_folder_when_build_path(self):
        self.tv.debug = True

        class File(object):
            name = 'Chuck'
            show_name = 'Chuck'
            season = 0
        path = self.tv.build_path(File(), self.files, True, 'Specials')
        assert path == os.path.join(self.files, 'Chuck/Specials/Chuck')
