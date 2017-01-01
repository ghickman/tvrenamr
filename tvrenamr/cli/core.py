#!/usr/bin/env python

from __future__ import absolute_import

import functools
import logging
import os
import sys

import click

from tvrenamr import __version__, errors
from tvrenamr.cli.helpers import (build_file_list, get_config, start_dry_run,
                                  stop_dry_run)
from tvrenamr.logs import start_logging
from tvrenamr.main import File, TvRenamr

log = logging.getLogger('CLI')


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.command()
@click.option('--config', type=click.Path(), help='Select a location for your config file. If the path is invalid the default locations will be used.')  # noqa
@click.option('-c', '--canonical', help='Set the show\'s canonical name to use when performing the online lookup.')   # noqa
@click.option('--debug', is_flag=True)
@click.option('-d', '--dry-run', is_flag=True, help='Dry run your renaming.')
@click.option('-e', '--episode', type=int, help='Set the episode number. Currently this will cause errors when working with more than one file.')  # noqa
@click.option('--ignore-filelist', type=tuple, default=())
@click.option('--log-file', type=click.Path(exists=True), help='Set the log file location.')
@click.option('-l', '--log-level', help='Set the log level. Options: short, minimal, info and debug.')   # noqa
@click.option('--log-file', type=click.Path(exists=True), help='Set the log file location.')
@click.option('-n', '--name', help="Set the episode's name.")
@click.option('--no-cache', is_flag=True, help='Force all renames to ignore the cache.')
@click.option('-o', '--output-format', help='Set the output format for the episodes being renamed.')
@click.option('--organise/--no-organise', default=True, help='Organise renamed files into folders based on their show name and season number. Can be explicitly disabled.')   # noqa
@click.option('-p', '--partial', is_flag=True, help='Allow partial regex matching of the filename.')
@click.option('-q', '--quiet', is_flag=True, help="Don't output logs to the command line")
@click.option('-r', '--recursive', is_flag=True, help='Recursively lookup files in a given directory')   # noqa
@click.option('--rename-dir', type=click.Path(), help='The directory to move renamed files to, if not specified the working directory is used.')   # noqa
@click.option('--regex', help='The regular expression to use when extracting information from files.')   # noqa
@click.option('-s', '--season', help='Set the season number.')
@click.option('--show', help="Set the show's name (will search for this name).")
@click.option('--show-override', help="Override the show's name (only replaces the show's name in the final file)")   # noqa
@click.option('--specials', help='Set the show\'s specials folder (defaults to "Season 0")')
@click.option('-t', '--the', is_flag=True, help="Set the position of 'The' in a show's name to the end of the show name")   # noqa
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.argument('paths', nargs=-1, required=False, type=click.Path(exists=True))
def rename(config, canonical, debug, dry_run, episode,  # pylint: disable-msg=too-many-arguments
           ignore_filelist, log_file, log_level, name,  # pylint: disable-msg=too-many-arguments
           no_cache, output_format, organise, partial,  # pylint: disable-msg=too-many-arguments
           quiet, recursive, rename_dir, regex, season,  # pylint: disable-msg=too-many-arguments
           show, show_override, specials, the, paths):  # pylint: disable-msg=too-many-arguments

    if debug:
        log_level = 10
    start_logging(log_file, log_level, quiet)
    logger = functools.partial(log.log, 26)

    if dry_run or debug:
        start_dry_run(logger)

    if not paths:
        paths = [os.curdir]

    for current_dir, filename in build_file_list(paths, recursive, ignore_filelist):
        try:
            tv = TvRenamr(current_dir, debug, dry_run, no_cache)

            _file = File(**tv.extract_details_from_file(
                filename,
                user_regex=regex,
                partial=partial,
            ))
            # TODO: Warn setting season & episode will override *all* episodes
            _file.user_overrides(show, season, episode)
            _file.safety_check()

            conf = get_config(config)

            for ep in _file.episodes:
                canonical = conf.get(
                    'canonical',
                    _file.show_name,
                    default=ep.file_.show_name,
                    override=canonical
                )

                # TODO: Warn setting name will override *all* episodes
                ep.title = tv.retrieve_episode_title(
                    ep,
                    canonical=canonical,
                    override=name,
                )

                # TODO: make this a sanitisation method on ep?
                ep.title = ep.title.replace('/', '-')

            show = conf.get_output(_file.show_name, override=show_override)
            the = conf.get('the', show=_file.show_name, override=the)
            _file.show_name = tv.format_show_name(show, the=the)

            _file.set_output_format(conf.get(
                'format',
                _file.show_name,
                default=_file.output_format,
                override=output_format
            ))

            organise = conf.get(
                'organise',
                _file.show_name,
                default=False,
                override=organise
            )
            rename_dir = conf.get(
                'renamed',
                _file.show_name,
                default=current_dir,
                override=rename_dir
            )
            specials_folder = conf.get(
                'specials_folder',
                _file.show_name,
                default='Season 0',
                override=specials,
            )
            path = tv.build_path(
                _file,
                rename_dir=rename_dir,
                organise=organise,
                specials_folder=specials_folder,
            )

            tv.rename(filename, path)
        except errors.NetworkException:
            if dry_run or debug:
                stop_dry_run(logger)
            sys.exit(1)
        except (AttributeError,
                errors.EmptyEpisodeTitleException,
                errors.EpisodeNotFoundException,
                errors.IncorrectRegExpException,
                errors.InvalidXMLException,
                errors.MissingInformationException,
                errors.OutputFormatMissingSyntaxException,
                errors.PathExistsException,
                errors.ShowNotFoundException,
                errors.UnexpectedFormatException) as e:
            continue
        except Exception as e:
            if debug:
                # In debug mode, show the full traceback.
                raise
            for msg in e.args:
                log.critical('Error: %s', msg)
            sys.exit(1)

        # if we're not doing a dry run add a blank line for clarity
        if not (debug and dry_run):
            log.info('')

    if dry_run or debug:
        stop_dry_run(logger)
