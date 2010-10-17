import os
import shutil

from nose.tools import *

import urlopenmock

import tvrenamr.config

class TestConfig(object):
    working = 'tests/data/working'

    def setUp(self):
        files = 'tests/data/files'
        #self.tv = TvRenamr(self.working, log_level='critical')
        for fn in os.listdir(files):
            shutil.copy(os.path.join(files, fn), os.path.join(self.working, fn))

    def tearDown(self):
        for fn in os.listdir(self.working):
            os.remove(os.path.join(self.working,fn))

    def test_defaults_are_used(self):
        # format: '%n - %s%e - %t%x'
        # library: thetvdb
        # organise: yes
        # renamed: tests/data/working
        # the: true
        pass

    def test_show_options_are_used(self):
        # format: '%n - %s%e - %t%x'
        # library: thetvdb
        # organise: yes
        # renamed: tests/data/working
        # the: true
        # canonical
        # output
        pass

    def test_falling_back_on_default_options_when_not_present_in_show(self):
        # format: '%n - %s%e - %t%x'
        # library: thetvdb
        # organise: yes
        # renamed: tests/data/working
        # the: true
        pass

    def test_getting_canonical_returns_shows_canonical_name_or_given_name_if_not_specified(self):
        # get_canonical(csi)
        # get_canonical(chuck)
        pass

    # def test passing in a
    # test passing in a show not in the config
    # test passing in a show in the config but with no x option
    # test passing in a show in the config with x option
    #
    #
    #
