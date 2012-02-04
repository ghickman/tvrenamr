#!/usr/bin/python

import logging
import os
import sys

from __init__ import get_version
from config import Config
from episode import Episode
from errors import *
from logs import start_logging
from main import TvRenamr
from options import OptionParser

log = logging.getLogger('Core')

parser = OptionParser(usage='tvr [options] <file/folder>', version='Tv Renamr %s' % get_version())
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
            os.path.join(sys.path[0], 'config.yml')
        )

        # get the first viable config from the list of possibles
        self.config = None
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
            file_list = self._build_file_list(path, options.recursive,
                                                options.ignore_filelist)
        except OSError:
            parser.error('\'%s\' is not a file or directory. Ruh Roe!' % path)

        if options.dry or options.debug:
            self._start_dry_run()

        # kick off a rename for each file in the list
        for details in file_list:
            self.rename(details)

            # if we're not doing a dry run add a blank line for clarity
            if options.debug is False and options.dry is False:
                log.info('')

        if options.dry or options.debug:
            self._stop_dry_run()

    def _build_file_list(self, path, recursive=False, ignore_filelist=None):
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
            episode = Episode(tv.extract_details_from_file(filename, user_regex=options.regex))
            if options.show:
                episode.show = options.show
            if options.season:
                episode.season = options.season
            if options.episode:
                episode.episode = options.episode

            episode.title = tv.retrieve_episode_name(episode, library=options.library,
                                                        canonical=options.canonical)

            episode.show_name = tv.format_show_name(episode.show_name, the=options.the,
                                                override=options.show_override)

            path = tv.build_path(episode, rename_dir=options.rename_dir,
                                    organise=options.organise, format=options.output_format)

            tv.rename(filename, path)
        except (ConfigNotFoundException,
                NoMoreLibrariesException,
                NoNetworkConnectionException):
            if options.dry or options.debug:
                self._stop_dry_run()
            sys.exit(1)
        except (EmptyEpisodeNameException,
                EpisodeAlreadyExistsInDirectoryException,
                EpisodeNotFoundException,
                IncorrectCustomRegularExpressionSyntaxException,
                OutputFormatMissingSyntaxException,
                ShowNotFoundException,
                UnexpectedFormatException,
                XMLEmptyException):
            pass
        except Exception as err:
            if options.debug:
                # In debug mode, show the full traceback.
                raise
            log.critical('tvr: critical error: %s' % str(err))
            sys.exit(1)

    def _start_dry_run(self):
        log.log(26, 'Dry Run beginning.')
        log.log(26, '-' * 70)
        log.log(26, '')

    def _stop_dry_run(self):
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

