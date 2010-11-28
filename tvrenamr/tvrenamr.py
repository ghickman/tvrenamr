#!/usr/bin/python

__author__ = 'George Hickman'
__version__ = '2.2.6'

import os
import sys
from optparse import OptionParser, SUPPRESS_HELP

from config import Config
from errors import *
from logs import start_logging
from main import TvRenamr

log = logging.getLogger('Core')

parser = OptionParser(usage="tvr [options] <file/folder>",
                        version="Tv Renamr %s" % __version__)
parser.add_option('--config', dest='config', \
                    help='Select a location for your config file. If the path \
                            is invalid the default locations will be used.')
parser.add_option('-c', '--canonical', dest='canonical',
                    help='Set the show\'s canonical name to use when \
                            performing the online lookup.')
parser.add_option('--debug', action='store_true', dest='debug',
                    help=SUPPRESS_HELP)
parser.add_option('--deluge', action='store_true', dest='deluge',
                    help='Checks Deluge to make sure the file has been \
                            completed before renaming.')
parser.add_option('--deluge-ratio', dest='deluge_ratio',
                    help='Checks Deluge for completed and that the file has \
                            at least reached X share ratio.')
parser.add_option('-d', '--dry-run', dest='dry', action='store_true',
                    help='Dry run your renaming.')
parser.add_option('-e', '--episode', dest='episode',
                    help='Set the episode number. Currently this will cause \
                            errors when working with more than one file.')
parser.add_option('--ignore-filelist', dest='ignore_filelist',
                    help=SUPPRESS_HELP)
parser.add_option('--ignore-recursive', action='store_true',
                    dest='ignore_recursive',
                    help='Only use files from the root of a given directory, \
                            not entering any sub-directories.')
parser.add_option('--log-file', dest='log_file',
                    help='Set the log file location.')
parser.add_option('-l', '--log-level', dest='log_level',
                    help='Set the log level. Options: short, minimal, info and \
                            debug.')
parser.add_option('--library', dest='library', default='thetvdb',
                    help='Set the library to use for retrieving episode \
                            titles. Options: thetvdb & tvrage.')
parser.add_option('-n', '--name', dest='name',
                    help='Set the show\'s name. This will be used as the \
                            show\'s when the renaming is completed.')
parser.add_option('-o', '--output', dest='output_format',
                    help='Set the output format for the episodes being \
                            renamed.')
parser.add_option('--organise', action='store_true', dest='organise',
                    help='Organise renamed files into folders based on their \
                            show name and season number.')
parser.add_option('--no-organise', action='store_false', dest='organise',
                    help='Explicitly tell Tv Renamr not to organise renamed \
                            files. Used to override the config.')
parser.add_option('-q', '--quiet', action='store_true', dest='quiet',
                    help='Don\'t output logs to the command line')
parser.add_option('-r', '--recursive', action='store_true', dest='recursive',
                    help='Recursively lookup files in a given directory')
parser.add_option('--rename-dir', dest='rename_dir',
                    help='The directory to move renamed files to, \
                            if not specified the working directory is used.')
parser.add_option('--no-rename-dir', action='store_false', dest='rename_dir',
                    help='Explicity tell Tv Renamr not to move renamed files. \
                            Used to override the config.')
parser.add_option('--regex', dest='regex',
                    help='The regular expression to use when extracting \
                            information from files.')
parser.add_option('-s', '--season', dest='season',
                    help='Set the season number.')
parser.add_option('-t', '--the', action='store_true', dest='the',
                    help='Set the position of \'The\' in a show\'s name to \
                            the end of the file')
options, args = parser.parse_args()


class FrontEnd():

    def __init__(self, path):
        # start logging
        if options.debug:
            options.log_level = 10
        start_logging(options.log_file, options.log_level, options.quiet)

        possible_config = (
            options.config,
            os.path.expanduser('~/.tvrenamr/config.yml'),
            os.path.join(sys.path[0], 'config.yml'))

        # get the first viable config from the list of possibles
        for config in possible_config:
            if config is not None and os.path.exists(config):
                self.config = Config(config)
                break
        if self.config is None:
            raise ConfigNotFoundException

        # no path was passed in so assuming current directory.
        if not path:
            if options.debug:
                log.debug('No file or directory specified, using '
                            'current directory')
            path = [os.getcwd()]

        # determine type
        try:
            file_list = self.__determine_type(path, options.recursive,
                                                options.ignore_filelist)
        except OSError:
            parser.error('\'%s\' is not a file or directory. Ruh Roe!' % path)

        if options.dry or options.debug:
            self.__start_dry_run()

        # kick off a rename for each file in the list
        for details in file_list:
            self.rename(details)

            # if we're not doing a dry run add a blank line for clarity
            if options.debug is False and options.dry is False:
                log.info('')

        if options.dry or options.debug:
            self.__stop_dry_run()

    def __determine_type(self, path, recursive=False, ignore_filelist=None):
        """
        Determines which files need to be processed for renaming.

        :param path: The input file or directory.
        :param recursive: Do a recursive search for files if 'path' is a
        directory. Default is False.
        :param ignore_filelist: Optional set of files to ignore from renaming.
        Often used by filtering
        methods such as Deluge.

        :returns: A list of files to be renamed.
        :rtype: A list of dictionaries, with the keys directory and filename.
        """
        filelist = []
        if len(path) > 1:
            # must have used wildcards
            for fn in path:
                filelist.append(os.path.split(fn))
            return filelist
        else:
            if os.path.isdir(path[0]):
                for root, dirs, files in os.walk(path[0]):
                    for fname in files:
                        # If we have a file we should be ignoring and skipping.
                        if ignore_filelist is not None and \
                            (os.path.join(root, fname) in ignore_filelist):
                            continue
                        filelist.append((root, fname))
                    # Don't want a recursive walk?
                    if not recursive:
                        break
                return filelist
            elif os.path.isfile(path[0]):
                return [os.path.split(path[0])]
            else:
                raise OSError

    def rename(self, details):
        working, filename = details

        try:
            tv = TvRenamr(working, self.config, options.debug, options.dry)
            credentials = tv.extract_details_from_file(filename, \
                                                    user_regex=options.regex)
            if options.season:
                credentials['season'] = options.season
            if options.episode:
                credentials['episode'] = options.episode

            credentials['title'] = tv.retrieve_episode_name( \
                                                library=options.library, \
                                                canonical=options.canonical, \
                                                **credentials)
            credentials['show'] = tv.format_show_name( \
                                    show=credentials['show'], the=options.the,\
                                    override=options.name)
            path = tv.build_path(rename_dir=options.rename_dir, \
                                organise=options.organise, \
                                format=options.output_format, **credentials)
            tv.rename(filename, path)
        except (ConfigNotFoundException, NoNetworkConnectionException):
            if options.dry or options.debug:
                self.__stop_dry_run()
            exit()
        except (EmptyEpisodeNameException, \
                EpisodeAlreadyExistsInDirectoryException, \
                EpisodeNotFoundException, \
                IncorrectCustomRegularExpressionSyntaxException, \
                OutputFormatMissingSyntaxException, ShowNotFoundException, \
                UnexpectedFormatException, XMLEmptyException):
            pass
        except Exception as err:
            if options.debug:
                log.critical(err)
            pass

    def __start_dry_run(self):
        log.log(26, 'Dry Run beginning.')
        log.log(26, '-' * 70)
        log.log(26, '')

    def __stop_dry_run(self):
        log.log(26, '')
        log.log(26, '-' * 70)
        log.log(26, 'Dry Run complete. No files were harmed in the process.')
        log.log(26, '')


def run():
    # Need to capture the Deluge arguments here, before we enter rename so
    # we can instead pass it as a callback to be called once we've fetched
    # the required information from deluge.
    if options.deluge or options.deluge_ratio:
        if options.deluge and not options.deluge_ratio:
            options.deluge_ratio = 0
        from lib.filter_deluge import get_deluge_ignore_file_list
        get_deluge_ignore_file_list(rename, options.deluge_ratio, args[0])
    else:
        FrontEnd(args)


if __name__ == "__main__":
    run()
