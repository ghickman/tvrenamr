from optparse import OptionParser as OptParser, SUPPRESS_HELP

from . import __version__


class OptionParser(OptParser):

    def __init__(self):
        usage = 'tvr [options] <file/folder>'
        version = 'Tv Renamr {0}'.format(__version__)

        OptParser.__init__(self, usage=usage, version=version)

        self.add_option('--config', dest='config', help='Select a location for your config file. If the path is invalid the default locations will be used.')
        self.add_option('-c', '--canonical', dest='canonical', help='Set the show\'s canonical name to use when performing the online lookup.')
        self.add_option('--debug', action='store_true', dest='debug', help=SUPPRESS_HELP)
        self.add_option('-d', '--dry-run', dest='dry', action='store_true', help='Dry run your renaming.')
        self.add_option('-e', '--episode', dest='episode', help='Set the episode number. Currently this will cause errors when working with more than one file.')
        self.add_option('--ignore-filelist', dest='ignore_filelist', default=(), help=SUPPRESS_HELP)
        self.add_option('--ignore-recursive', action='store_true', dest='ignore_recursive', help='Only use files from the root of a given directory, not entering any sub-directories.')
        self.add_option('--log-file', dest='log_file', help='Set the log file location.')
        self.add_option('-l', '--log-level', dest='log_level', help='Set the log level. Options: short, minimal, info and debug.')
        self.add_option('--library', dest='library', default='thetvdb', help='Set the library to use for retrieving episode titles. Options: thetvdb & tvrage.')
        self.add_option('-n', '--name', dest='name', help='Set the episode\'s name.')
        self.add_option('--no-cache', action='store_true', dest='cache', help='Force all renames to ignore the cache.')
        self.add_option('-o', '--output', dest='output_format', help='Set the output format for the episodes being renamed.')
        self.add_option('--organise', action='store_true', dest='organise', help='Organise renamed files into folders based on their show name and season number.')
        self.add_option('--no-organise', action='store_false', dest='organise', help='Explicitly tell Tv Renamr not to organise renamed files. Used to override the config.')
        self.add_option('-p', '--partial', action='store_true', dest='partial', help='Allow partial regex matching of the filename.')
        self.add_option('-q', '--quiet', action='store_true', dest='quiet', help='Don\'t output logs to the command line')
        self.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='Recursively lookup files in a given directory')
        self.add_option('--rename-dir', dest='rename_dir', help='The directory to move renamed files to, if not specified the working directory is used.')
        self.add_option('--no-rename-dir', action='store_false', dest='rename_dir', help='Explicity tell Tv Renamr not to move renamed files. Used to override the config.')
        self.add_option('--regex', dest='regex', help='The regular expression to use when extracting information from files.')
        self.add_option('-s', '--season', dest='season', help='Set the season number.')
        self.add_option('--show', dest='show_name', help='Set the show\'s name (will search for this name).')
        self.add_option('--show-override', dest='show_override', help='Override the show\'s name (only replaces the show\'s name in the final file)')
        self.add_option('--specials', dest='specials_folder', help='Set the show\'s specials folder (defaults to "Season 0")')
        self.add_option('-t', '--the', action='store_true', dest='the', help='Set the position of \'The\' in a show\'s name to the end of the show name')
