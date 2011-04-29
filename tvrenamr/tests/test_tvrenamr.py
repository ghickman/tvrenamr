from os import listdir, mkdir, system
from os.path import isfile, join
from shutil import copy, rmtree

from nose.tools import assert_raises, assert_true

#stub urlopen calls
import urlopenmock

#from tvrenamr.errors import UnexpectedFormatException

base = 'python tvrenamr.py --config=tests/config.yml --no-organise -q'
working = 'tests/data/working'
renamed = 'tests/data/renamed'
organised = 'tests/data/organised'

class TestScript(object):

    def setUp(self):
        files = 'tests/data/files'
        for fn in listdir(files):
            copy(join(files, fn), join(working, fn))

    def tearDown(self):
        rmtree(working)
        mkdir(working)
        rmtree(renamed)
        mkdir(renamed)

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
        system('%s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, working))
        assert_true(isfile(join(working, 'Chuck - 108 - Chuck Versus the Truth.avi')))

    def test_single_rename_with_rename_folder_location_specified(self):
        system('%s --rename-dir=%s %s/chuck.s1e10.blah.HDTV.XViD.avi' % (base, renamed, working))
        assert_true(isfile(join(renamed, 'Chuck - 110 - Chuck Versus the Nemesis.avi')))

    def test_single_rename_with_rename_folder_location_specified_and_organise_option(self):
        system('%s --organise --rename-dir=%s %s/chuck.s1e11.blah.HDTV.XViD.avi' % (base, renamed, working))
        assert_true(isfile(join(renamed, 'Chuck', 'Season 1', 'Chuck - 111 - Chuck Versus the Crown Vic.avi')))

    def test_single_rename_with_show_name_option(self):
        system('%s --show %s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, '\'Stargate SG-1\'', working))
        assert_true(isfile(join(working, 'Stargate SG-1 - 108 - The Nox.avi')))

    def test_single_rename_with_season_option(self):
        system('%s -s 2 %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, working))
        assert_true(isfile(join(working, 'Chuck - 208 - Chuck Versus the Gravitron.avi')))

    def test_single_rename_with_episode_option(self):
        system('%s -e 9 %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, working))
        assert_true(isfile(join(working, 'Chuck - 109 - Chuck Versus the Imported Hard Salami.avi')))

    def test_single_rename_with_leading_the_moved_to_end_of_show_name_option(self):
        system('%s -t %s/The.Big.Bang.Theory.S03E01.HDTV.XViD-NoTV.avi' % (base, working))
        assert_true(isfile(join(working, 'Big Bang Theory, The - 301 - The Electric Can Opener Fluctuation.avi')))

    def test_single_rename_with_output_format_specified(self):
        system('%s -o %s %s/chuck.s1e08.blah.HDTV.XViD.avi' % (base, '\'%s%e - %n - %t%x\'', working))
        assert_true(isfile(join(working, '108 - Chuck - Chuck Versus the Truth.avi')))

    def test_single_rename_with_custom_regular_expression_specified(self):
        system('%s --regex=%s %s/e08s1.chuck.blah.HDTV.XViD.avi' % (base, 'e%es%s.%n.blah', working))
        assert_true(isfile(join(working, 'Chuck - 108 - Chuck Versus the Truth.avi')))

    #def test_single_rename_with_an_unexpected_format_raises_an_unexpected_format_exception(self):
        #assert_raises(UnexpectedFormatException, system('%s %s/\'West Wing.avi\'' % (base, working)))
        #pass

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

