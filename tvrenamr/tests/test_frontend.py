from os import mkdir, system
from os.path import exists, join
from shutil import rmtree

from nose.tools import assert_equals, assert_true

from tvrenamr.tests.base import BaseTest


class TestFrontEnd(BaseTest):
    base = 'python frontend.py --config=tests/config.yml --no-organise -q'

    def setup(self):
        super(TestFrontEnd, self).setup()
        if exists(self.renamed):
            rmtree(self.renamed)
        mkdir(self.renamed)

    def teardown(self):
        super(TestFrontEnd, self).setup()
        rmtree(self.renamed)

    def command(self, filename, extra_option=False):
        extra_option_str = extra_option if extra_option else ''
        tvr = '{0} {1} {2}/{3}'.format(self.base, extra_option_str,
                                               self.files, filename)
        return system(tvr)

    """
    - use no options
    - use -r
    - use -a and -r
    - use -n
    - use -s
    - use -e
    - use -t
    - use -o
    - use --regex
    - use --deluge
    - use --deluge-share-ratio
    - use unexpected format
    """
    def test_single_rename_with_no_options(self):
        cmd = self.command('chuck.s1e08.blah.HDTV.XViD.avi')
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, 'Chuck - 108 - Chuck Versus the Truth.avi')))

    def test_single_rename_with_rename_folder_location_specified(self):
        cmd = self.command('chuck.s1e10.blah.HDTV.XViD.avi',
                           '--rename-dir={0}'.format(self.renamed))
        assert_equals(cmd, 0)
        assert_true(exists(join(self.renamed, 'Chuck - 110 - Chuck Versus the Nemesis.avi')))

    def test_single_rename_with_rename_folder_and_organise_options(self):
        cmd = self.command('chuck.s1e11.blah.HDTV.XViD.avi',
                           '--organise --rename-dir={0}'.format(self.renamed))
        assert_equals(cmd, 0)
        assert_true(exists(join(self.renamed, 'Chuck', 'Season 1',
                                'Chuck - 111 - Chuck Versus the Crown Vic.avi')))

    def test_single_rename_with_show_name_option(self):
        cmd = self.command('chuck.s1e08.blah.HDTV.XViD.avi', '--show "Stargate SG-1"')
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, 'Stargate SG-1 - 108 - The Nox.avi')))

    def test_single_rename_with_season_option(self):
        cmd = self.command('chuck.s1e08.blah.HDTV.XViD.avi', '-s 2')
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, 'Chuck - 208 - Chuck Versus the Gravitron.avi')))

    def test_single_rename_with_episode_option(self):
        cmd = self.command('chuck.s1e08.blah.HDTV.XViD.avi', '-e 9')
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, 'Chuck - 109 - Chuck Versus the Imported Hard Salami.avi')))

    def test_single_rename_with_leading_the_moved_to_end_of_show_name_option(self):
        cmd = self.command('The.Big.Bang.Theory.S03E01.HDTV.XViD-NoTV.avi', '-t')
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, 'Big Bang Theory, The - 301 - The Electric Can Opener Fluctuation.avi')))

    # def test_single_rename_with_output_format_specified(self):
        cmd = self.command('chuck.s1e08.blah.HDTV.XViD.avi',
                           '-o {0}'.format('\'%s%e - %n - %t%x\''))
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, '108 - Chuck - Chuck Versus the Truth.avi')))

    # def test_single_rename_with_custom_regular_expression_specified(self):
        cmd = self.command('e08s1.chuck.blah.HDTV.XViD.avi',
                           '--regex={0}'.format('e%es%s.%n.blah'))
        assert_equals(cmd, 0)
        assert_true(exists(join(self.files, 'Chuck - 108 - Chuck Versus the Truth.avi')))

    """
    - use recursive and no options
    - use recursive and -r
    - use recursive and -a and -r
    - use recursive and -n
    - use recursive and -s
    - use recursive and -e
    - use recursive and -t
    - use recursive and -o
    - use recursive and --regex
    - use recursive and --deluge
    - use recursive and --deluge-share-ratio
    - use recursive and unexpected format
    """

