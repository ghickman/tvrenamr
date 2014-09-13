#!/usr/bin/env python

import logging
import os
import sys

import click

from tvrenamr.config import Config
from tvrenamr.errors import *
from tvrenamr.logs import start_logging
from tvrenamr.main import File, TvRenamr
from .decorators import logfile_option


log = logging.getLogger('CLI')


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
            canonical = config.get(
                'canonical',
                _file.show_name,
                default=episode._file.show_name,
                override=options.canonical
            )

            episode.title = tv.retrieve_episode_title(episode, canonical=canonical)

        show = config.get_output(_file.show_name, override=options.show_override)
        the = config.get('the', show=_file.show_name, override=options.the)
        _file.show_name = tv.format_show_name(show, the=the)

        _file.set_output_format(config.get(
            'format',
            _file.show_name,
            default=_file.output_format,
            override=options.output_format
        ))

        organise = config.get(
            'organise',
            _file.show_name,
            default=False,
            override=options.organise
        )
        rename_dir = config.get(
            'renamed',
            _file.show_name,
            default=working,
            override=options.rename_dir
        )
        specials_folder = config.get(
            'specials_folder',
            _file.show_name,
            default='Season 0',
            override=options.specials_folder
        )
        path = tv.build_path(
            _file,
            rename_dir=rename_dir,
            organise=organise,
            specials_folder=specials_folder,
        )

        tv.rename(filename, path)
    except KeyboardInterrupt:
        sys.exit()
    except (errors.NoMoreLibrariesException,
            errors.NoNetworkConnectionException):
        if options.dry or options.debug:
            stop_dry_run()
        sys.exit(1)
    except (AttributeError,
            errors.EmptyEpisodeTitleException,
            errors.EpisodeAlreadyExistsInDirectoryException,
            errors.EpisodeNotFoundException,
            errors.IncorrectCustomRegularExpressionSyntaxException,
            errors.InvalidXMLException,
            errors.MissingInformationException,
            errors.OutputFormatMissingSyntaxException,
            errors.ShowNotFoundException,
            errors.UnexpectedFormatException) as e:
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


@click.group()
@click.option('--config', type=click.Path(), help='Select a location for your config file. If the path is invalid the default locations will be used.')
@click.option('-c', '--canonical', help='Set the show\'s canonical name to use when performing the online lookup.')
@click.option('--debug', is_flag=True)
@click.option('-d', '--dry-run', is_flag=True, help='Dry run your renaming.')
@click.option('-e', '--episode', type=int, help='Set the episode number. Currently this will cause errors when working with more than one file.')
@click.option('--ignore-filelist', default=())
@click.option('--ignore-recursive', is_flag=True, help='Only use files from the root of a given directory, not entering any sub-directories.')
@logfile_option
@click.option('-l', '--log-level', help='Set the log level. Options: short, minimal, info and debug.')
@click.option('--library', default='thetvdb', help='Set the library to use for retrieving episode titles. Options: thetvdb & tvrage.')
@click.option('-n', '--name', help="Set the episode's name.")
@click.option('--no-cache', is_flag=True, help='Force all renames to ignore the cache.')
@click.option('-o', '--output', help='Set the output format for the episodes being renamed.')
@click.option('--organise/--no-organise', default=True, help='Organise renamed files into folders based on their show name and season number. Can be explicitly disabled.')
@click.option('-p', '--partial', is_flag=True, help='Allow partial regex matching of the filename.')
@click.option('-q', '--quiet', is_flag=True, help="Don't output logs to the command line")
@click.option('-r', '--recursive', is_flag=True, help='Recursively lookup files in a given directory')
@click.option('--rename-dir', type=click.Path(), help='The directory to move renamed files to, if not specified the working directory is used.')
@click.option('--no-rename-dir', is_flag=True, default=False, help='Explicity tell Tv Renamr not to move renamed files. Used to override the config.')
@click.option('--regex', help='The regular expression to use when extracting information from files.')
@click.option('-s', '--season', help='Set the season number.')
@click.option('--show', help="Set the show's name (will search for this name).")
@click.option('--show-override', help="Override the show's name (only replaces the show's name in the final file)")
@click.option('--specials', help='Set the show\'s specials folder (defaults to "Season 0")')
@click.option('-t', '--the', is_flag=True, help="Set the position of 'The' in a show's name to the end of the show name")
@click.argument('files', nargs=3, required=False, type=click.Path(exists=True))
def cli(config, canonical, debug, dry_run, episode, ignore_filelist,
        ignore_recursive, log_level, library, name, no_cache, output, organise,
        partial, quiet, recursive, rename_dir, regex, season, show, show_override,
        specials, the, files):
    if debug:
        log_level = 10
    start_logging(log_file, log_level, quiet)
    logger = functools.partial(log.log, level=26)

    import pdb;pdb.set_trace()

    try:
        files = build_file_list(files, recursive, ignore_filelist)
    except IOError as e:
        click.error("'{0}' is not a file or directory.".format(e))

    if dry or debug:
        start_dry_run(logger)

    # kick off a rename for each file in the list
    for path in files:
        rename(path, options)

        # if we're not doing a dry run add a blank line for clarity
        if not (debug and dry):
            log.info('')

    if dry or debug:
        stop_dry_run(logger)


if __name__ == "__main__":
    cli()
