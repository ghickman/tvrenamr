from __future__ import unicode_literals

import logging
import os
import re
import shutil

from . import errors
from .tvdb import TVDB

log = logging.getLogger('Core')


class Episode(object):

    def __init__(self, file_, number):
        self.file_ = file_  # cache reverse reference to parent object
        self.number = number

    def __getattr__(self, name):
        if name == 'episode':
            msg = 'Missing episode: Set it with --episode or use %e in your --regex string'
            raise AttributeError(msg)

        msg = "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)
        raise AttributeError(msg)

    def __getattribute__(self, item):
        """
        Allow the retrieval of single digit episode numbers but return
        it with a leading zero.
        """
        if item is 'episode_2':
            return '0{}'.format(self.number)
        return object.__getattribute__(self, item)

    def __int__(self):
        return int(self.number)

    def __repr__(self):
        return 'Episode: {} (season {})'.format(self.number, self.file_.season)

    def __str__(self):
        return '{} - {}'.format(self.number, self.title)


class File(object):
    output_format = '%n - %s%e - %t%x'

    def __init__(self, show_name=None, season=None, episodes=(), extension=''):
        self.show_name = show_name
        self.season = season
        self.episodes = [Episode(file_=self, number=i) for i in episodes]
        self.extension = extension

    def __repr__(self):
        return self.name

    def get_episode_output(self, filename, marker='%e', fill=2):
        if '%e{' in filename:
            fill = filename.split('%e{')[1][:1]
            marker = '%e{' + fill + '}'
        episode = '-'.join([str(e.number).zfill(int(fill)) for e in self.episodes])
        return filename.replace(marker, episode)

    def get_season_output(self, filename, marker='%s', fill=1):
        if '%s{' in filename:
            fill = filename.split('%s{')[1][:1]
            marker = '%s{' + fill + '}'
        season = str(self.season).zfill(int(fill))
        return filename.replace(marker, season)

    @property
    def name(self):
        filename = self.output_format

        filename = filename.replace('%n', self.show_name)
        filename = filename.replace('%t', self.title)
        filename = filename.replace('%x', self.extension)

        filename = self.get_season_output(filename)
        filename = self.get_episode_output(filename)

        return filename

    @property
    def title(self):
        titles = [e.title for e in self.episodes]

        # Check the titles aren't all the same with different (x) parts
        suffixes = tuple('({})'.format(i + 1) for i in range(len(titles)))
        if any([t.endswith(suffixes) for t in titles]):
            stripped_titles = set([t[:-4] for t in titles])
            if len(stripped_titles) is 1:
                titles = stripped_titles

        return ' & '.join(titles)

    def safety_check(self):
        """
        Check we have all the necessary information to rename a file.
        """
        if self.show_name is None:
            raise errors.MissingInformationException('A show name')

        if self.season is None:
            raise errors.MissingInformationException('A season number')

        if not self.episodes:
            raise errors.MissingInformationException('An episode number')

        for e in self.episodes:
            if e.number is None:
                raise errors.MissingInformationException('An episode number')

    def set_output_format(self, user_format):
        self.output_format = user_format

    def user_overrides(self, show_name, season, episode):
        if show_name:
            self.show_name = show_name

        if season:
            self.season = int(season)

        if episode:
            if self.episodes:
                for e in self.episodes:
                    e.number = int(episode)
            else:
                self.episodes = [Episode(file_=self, number=episode)]


class TvRenamr(object):
    def __init__(self, working_dir, debug=False, dry=False, cache=True):
        self.cache = cache
        self.working_dir = working_dir
        self.dry = dry
        self.debug = debug

    def remove_part_from_multiple_episodes(self, show_name):
        """Remove the string "Part " from a filename.

        In episode titles of multi-part episodes that use the format
        (Part n) remove the 'Part ' section so the format is (n).

        """
        log.debug('Removing Part from episode name')
        return show_name.replace('(Part ', '(')

    def extract_details_from_file(self, fn, user_regex=None, partial=False):
        """Using a regular expression extract information from the filename passed in.

        Looks at the file given and extracts from it the show title, it's
        season number and episode number using regular expression magic.
        The default formats accepted are: series.0x00.xxx or series.s0e00.xxx
        A user can specify their own regular expression for a format not
        already covered.

        """
        try:
            fn = fn.decode('utf-8')
        except AttributeError:  # python 3
            pass

        fn = self._sanitise_filename(fn)
        log.log(22, 'Renaming: %s', fn)

        # If we sanitise the filename we shall sanitise the regex too
        if user_regex is not None:
            user_regex = self._sanitise_filename(user_regex)

        regex = self._build_regex(user_regex, partial=partial)
        log.debug('Attempting rename with: {}'.format(regex))

        matches = re.match(regex, fn)
        if not matches:
            raise errors.UnexpectedFormatException(fn)

        return self._build_credentials(fn, matches)

    def retrieve_episode_title(self, episode, canonical=None, override=None):
        """Retrieves the title of a given episode.

        The series name, season and episode numbers must be specified to get
        the episode's title.
        """
        if canonical is not None:
            episode.file_.show_name = canonical

        log.debug('Show Name: %s', episode.file_.show_name)

        args = (episode.file_.show_name, episode.file_.season, episode.number, self.cache)
        self.lookup = TVDB(*args)  # assign to self for use in format_show_name

        log.info('Episode: %s', self.lookup.title)
        return override or self.lookup.title

    def format_show_name(self, show_name, the=False):
        if show_name is None:
            show_name = self.lookup.show
            log.debug('Using the formatted show name retrieved from The TvDb')
        else:
            log.debug('Using config output name: %s', show_name)

        if the is True:
            show_name = self._move_leading_the_to_trailing_the(show_name)

        log.debug('Final show name: %s', show_name)

        return show_name

    def build_path(self, _file, rename_dir, organise=False, specials_folder=None):
        """Build the full destination path and filename of the renamed file.

        By default the format is:

        Show Name - Season NumberEpisode Number - Episode Title.format.

        Builds the new path for the file to be renamed to, by default this is
        the working directory. Users can specify a directory to move files to
        once renamed using the renamed_dir option. The auto_move option can be
        used to specify a top level directory where files will be placed in
        season and show folders, i.e. Show/Season 1/episodes

        """
        if organise is True:
            args = [rename_dir, _file.show_name, _file.season, specials_folder]
            rename_dir = self._build_organise_path(*args)

        log.log(22, 'Directory: %s', rename_dir)

        path = os.path.join(rename_dir, _file.name)
        log.debug('Full path: %s', path)

        return path

    def rename(self, current_filepath, destination_filepath):
        """Renames a file.

        This is more akin to the UNIX `mv` operation as the destination filepath
        can be anywhere on the filesystem.
        Returns the new filename for use elsewhere.

        """
        if os.path.exists(destination_filepath):
            raise errors.PathExistsException(destination_filepath)

        log.debug(os.path.join(self.working_dir, current_filepath))
        log.debug(destination_filepath)
        if not self.dry and not self.debug:
            source_filepath = os.path.join(self.working_dir, current_filepath)
            shutil.move(source_filepath, destination_filepath)
        destination_file = os.path.split(destination_filepath)[1]
        log.log(26, 'Renamed: "%s"', destination_file)
        return destination_filepath

    def _build_credentials(self, fn, matches):
        """Build a dictionary of a file's extracted credentials."""
        details = {}

        try:
            details['show_name'] = matches.group('show_name').replace('.', ' ').strip()
        except IndexError:
            pass
        try:
            details['season'] = str(int(matches.group('season')))
        except IndexError:
            pass

        episodes = []
        for group in ('episode', 'episode2'):
            try:
                episodes.append(str(int(matches.group(group))))
            except (IndexError, KeyError, TypeError):
                pass

        details.update({
            'episodes': episodes,
            'extension': os.path.splitext(fn)[1]
        })

        msg = ', '.join('{}: {}'.format(key, value) for key, value in details.items())
        log.debug('Filename yielded: %s', msg)
        return details

    def _build_organise_path(self, start_path, show_name, season_number, specials=None):
        """
        Constructs a directory path using the show's details.

        Show name and season number of an episode dictate the folder structure.
        """
        season = 'Season {}'.format(season_number)
        if season_number is 0 and specials is not None:  # specials folder
            season = specials

        path = os.path.join(start_path, show_name, season)

        if not (os.path.exists(path) or self.dry or self.debug):
            os.makedirs(path)
            log.debug('Directories created for path: ' + path)

        return path

    def _build_regex(self, regex=None, partial=False):
        """Builds the regular expression to extract a files details.

        Custom syntax can be used in the regular expression to help specify
        parts of the episode's file name. These custom syntax snippets are
        replaced by the regular expression blocks show.

        %n - [\w\s.,_-]+ - The show name.
        %s - \d{1,2} - The season number.
        %e - \d{2} - The episode number.

        """
        series = r"(?P<show_name>[\w\s\(\).',_-]+)"
        season = r"(?P<season>\d{1,2})"
        episode = r"(?P<episode>\d{2})"
        second_episode = r".E?(?P<episode2>\d{2})*"

        if regex is None:
            # Build default regex
            return series + r"\.[Ss]?" + season + r"[XxEe]?" + episode + second_episode

        if not partial and not ('%n' in regex or '%s' in regex or '%e' in regex):
            raise errors.IncorrectRegExpException(regex)

        # series name
        regex = regex.replace('%n', series)

        # season number
        # %s{n}
        if '%s{' in regex:
            log.debug('Season digit number found')
            r = regex.split('%s{')[1][:1]
            log.debug('Specified % season digits', r)
            s = season.replace('1,2', r)
            regex = regex.replace('%s{' + r + '}', s)
            log.debug('Season regex set: %s', s)

        # %s
        if '%s' in regex:
            regex = regex.replace('%s', season)
            log.debug('Default season regex set: %s', regex)

        # episode number
        # %e{n}
        if '%e{' in regex:
            log.debug('User set episode digit number found')
            r = regex.split('%e{')[1][:1]
            log.debug('User specified %s episode digits', r)
            e = episode.replace('2', r)
            regex = regex.replace('%e{' + r + '}', e)
            log.debug('Episode regex set: %s', e)

        # %e
        if '%e' in regex:
            regex = regex.replace('%e', episode)
            log.debug('Default episode regex set: %s', regex)

        return regex

    def _move_leading_the_to_trailing_the(self, show_name):
        """Moves the leading 'The' of a show name to a trailing 'The'.

        A comma and space are added before the new 'The'.

        """
        if not(show_name.startswith('The ')):
            return show_name
        log.debug("Moving leading 'The' to end of: %s", show_name)
        return show_name[4:] + ', The'

    def _sanitise_filename(self, filename):
        """
        Remove bits of the filename that cause a problem.

        Initially added to deal specifically with the issues 720[p] causes
        in filenames by appearing before or after the season/episode block.
        """
        items = (
            ('[', '.'),
            ('_', '.'),
            (' ', '.'),
            ('.720p', ''),
            ('.720', ''),
            ('.1080p', ''),
            ('.1080', ''),
            ('.H.264', ''),
            ('.h.264', ''),
        )
        for target, replacement in items:
            filename = filename.replace(target, replacement)
        return filename
