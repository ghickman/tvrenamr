#!/usr/bin/env python

import logging
import os
import sys

from .config import Config
from .errors import *
from .logs import start_logging
from .main import File, TvRenamr
from .options import OptionParser


log = logging.getLogger('FrontEnd')


parser = OptionParser()
options, args = parser.parse_args()


class FrontEnd(object):
    def __init__(self):
        # start logging
        if options.debug:
            options.log_level = 10
        start_logging(options.log_file, options.log_level, options.quiet)

    def build_file_list(self, glob, recursive=False, ignore_filelist=None):
        """
        Determines which files need to be processed for renaming.

        :param glob: A list of file(s) or directory(s).
        :param recursive: Do a recursive search for files if 'glob' is a
        directory. Default is False.
        :param ignore_filelist: Optional set of files to ignore from renaming.
        Often used by filtering methods such as Deluge.

        :returns: A list of files to be renamed.
        :rtype: A list of tuples
        """
        if len(glob) > 1:
            # must have used wildcards
            self.file_list = [os.path.split(fn) for fn in glob]
            return

        glob = glob[0] # only one item, add some convenience
        if os.path.isdir(glob):
            self.file_list = []
            for root, dirs, files in os.walk(glob):
                for fname in files:
                    # If we have a file we should be ignoring and skipping.
                    full_path = os.path.join(root, fname)
                    if ignore_filelist is not None and (full_path in ignore_filelist):
                        continue
                    self.file_list.append((root, fname))
                # Don't want a recursive walk?
                if not recursive:
                    break
        elif os.path.isfile(glob):
            self.file_list = [os.path.split(glob)]
        else:
            parser.error("'{0}' is not a file or directory. Ruh Roe!".format(args))

    def get_config(self, path=None):
        possible_config = (
            options.config,
            path,
            os.path.expanduser('~/.tvrenamr/config.yml'),
            os.path.join(sys.path[0], 'config.yml')
        )

        # get the first viable config from the list of possibles
        _config = None
        for config in possible_config:
            if config is not None and os.path.exists(config):
                _config = Config(config)
                break
        if _config is None:
            raise ConfigNotFoundException
        self.config = _config

    def rename(self, working, filename):
        try:
            tv = TvRenamr(working, self.config, options.debug, options.dry)

            _file = File(**tv.extract_details_from_file(filename, user_regex=options.regex))
            # TODO: Warn setting season & episode will override *all* episodes
            _file.user_overrides(options.show_name, options.season, options.episode)

            for episode in _file.episodes:
                episode.title = tv.retrieve_episode_title(episode, library=options.library,
                                                          canonical=options.canonical)

            _file.show_name = tv.format_show_name(_file.show_name, the=options.the,
                                                  override=options.show_override)

            _file.set_output_format(options.output_format, self.config)

            path = tv.build_path(_file, rename_dir=options.rename_dir,
                                 organise=options.organise)

            tv.rename(filename, path)
        except KeyboardInterrupt:
            sys.exit()
        except (ConfigNotFoundException,
                NoMoreLibrariesException,
                NoNetworkConnectionException):
            if options.dry or options.debug:
                self._stop_dry_run()
            sys.exit(1)
        except (AttributeError,
                EmptyEpisodeTitleException,
                EpisodeAlreadyExistsInDirectoryException,
                EpisodeNotFoundException,
                IncorrectCustomRegularExpressionSyntaxException,
                InvalidXMLException,
                OutputFormatMissingSyntaxException,
                ShowNotFoundException,
                UnexpectedFormatException) as e:
            for msg in e.args:
                log.critical(e)
            pass
        except Exception as e:
            if options.debug:
                # In debug mode, show the full traceback.
                raise
            for msg in e.args:
                log.critical('Error: {0}'.format(msg))
            sys.exit(1)

    def run(self):
        if options.dry or options.debug:
            self._start_dry_run()

        # kick off a rename for each file in the list
        for details in self.file_list:
            self.rename(*details)

            # if we're not doing a dry run add a blank line for clarity
            if not (options.debug and options.dry):
                log.info('')

        if options.dry or options.debug:
            self._stop_dry_run()

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
    # use current directory if no args specified
    files = args
    if not args:
        log.debug('No file or directory specified, using current directory')
        files = [os.getcwd()]

    frontend = FrontEnd()
    frontend.get_config()
    frontend.build_file_list(files, options.recursive, options.ignore_filelist)
    frontend.run()

if __name__ == "__main__":
    run()
