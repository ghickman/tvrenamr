#!/usr/bin/env python

import logging
import os
import sys

from .config import Config
from .errors import *
from .history import parse_history
from .logs import start_logging
from .main import File, TvRenamr
from .options import OptionParser


log = logging.getLogger('FrontEnd')


def build_file_list(paths, recursive=False, ignore_filelist=()):
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
    file_list = []

    for glob in paths:
        if not os.path.exists(glob):
            raise IOError(glob)

        if os.path.isfile(glob):
            file_list.append(glob)

        if os.path.isdir(glob):
            for root, dirs, files in os.walk(glob):
                for fname in files:
                    file_path = os.path.join(root, fname)
                    if file_path not in ignore_filelist:
                        file_list.append(file_path)

                if not recursive:
                    break

    return file_list


def get_config(path=None):
    """Get the first viable config from the list of possiblities"""
    def exists(x):
        return x is not None and os.path.exists(x)

    possible_configs = iter(filter(exists, (
        path,
        os.path.join(sys.path[0], 'config.yml'),
        os.path.expanduser('~/.tvrenamr/config.yml'),
    )))

    location = next(possible_configs, None)

    return Config(location)


def rename(path, options):
    working, filename = os.path.split(path)
    try:
        tv = TvRenamr(working, options.debug, options.dry, options.cache)

        _file = File(**tv.extract_details_from_file(filename, user_regex=options.regex))
        # TODO: Warn setting season & episode will override *all* episodes
        _file.user_overrides(options.show_name, options.season, options.episode)
        _file.safety_check()

        config = get_config(options.config)

        for episode in _file.episodes:
            canonical = config.get('canonical', show=_file.show_name,
                default=episode._file.show_name, override=options.canonical)

            ep_kwargs = {'library': options.library, 'canonical': canonical}
            episode.title = tv.retrieve_episode_title(episode, **ep_kwargs)

        show = config.get_output(_file.show_name, override=options.show_override)
        the = config.get('the', show=_file.show_name, override=options.the)
        _file.show_name = tv.format_show_name(show, the=the)

        _file.set_output_format(config.get('format', show=_file.show_name,
            default=_file.output_format, override=options.output_format))

        organise = config.get('organise', show=_file.show_name,
            default=False, override=options.organise)
        rename_dir = config.get('renamed', show=_file.show_name,
            default=working, override=options.rename_dir)
        specials_folder = config.get('specials_folder', show=_file.show_name,
            default='Season 0', override=options.specials_folder)
        path = tv.build_path(
            _file,
            rename_dir=rename_dir,
            organise=organise,
            specials_folder=specials_folder,
        )

        tv.rename(filename, path)
    except KeyboardInterrupt:
        sys.exit()
    except (NoMoreLibrariesException,
            NoNetworkConnectionException):
        if options.dry or options.debug:
            stop_dry_run()
        sys.exit(1)
    except (AttributeError,
            EmptyEpisodeTitleException,
            EpisodeAlreadyExistsInDirectoryException,
            EpisodeNotFoundException,
            IncorrectCustomRegularExpressionSyntaxException,
            InvalidXMLException,
            MissingInformationException,
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


def run():
    parser = OptionParser()
    options, args = parser.parse_args()

    if options.debug:
        options.log_level = 10
    start_logging(options.log_file, options.log_level, options.quiet)

    if options.history:
        return parse_history(options.log_file)

    # use current directory if no args specified
    if not args:
        log.debug('No file or directory specified, using current directory')
        args = [os.getcwd()]
    try:
        files = build_file_list(args, options.recursive, options.ignore_filelist)
    except IOError as e:
        parser.error("'{0}' is not a file or directory.".format(e))

    if options.dry or options.debug:
        start_dry_run()

    # kick off a rename for each file in the list
    for path in files:
        rename(path, options)

        # if we're not doing a dry run add a blank line for clarity
        if not (options.debug and options.dry):
            log.info('')

    if options.dry or options.debug:
        stop_dry_run()


def start_dry_run():
    log.log(26, 'Dry Run beginning.')
    log.log(26, '-' * 70)
    log.log(26, '')


def stop_dry_run():
    log.log(26, '')
    log.log(26, '-' * 70)
    log.log(26, 'Dry Run complete. No files were harmed in the process.')
    log.log(26, '')


if __name__ == "__main__":
    run()
