import logging
import os
import re

from . import errors
from .lib.thetvdb import TheTvDb
from .lib.tvrage import TvRage

log = logging.getLogger('Core')


def clean_name(filename, before=':', after=','):
    """
    Cleans the string passed in.

    A wrapper of Python's str.replace() with the idea of making the string
    safe for all file systems, but not using the horrible \ character.
    Also allows the user to specify the new characters to be used.

    """
    return filename.replace(before, after)


class Episode(object):

    def __init__(self, _file, number):
        self._file = _file  # cache reverse reference to parent object
        self.number = number

    def __getattr__(self, name):
        if name == 'episode':
            msg = 'Missing episode: Set it with --episode or use %e in your --regex string'
            raise AttributeError(msg)

        msg = "'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name)
        raise AttributeError(msg)

    def __getattribute__(self, item):
        """
        Allow the retrieval of single digit episode numbers but return
        it with a leading zero.
        """
        if item is 'episode_2':
            return '0{0}'.format(self.number)
        return object.__getattribute__(self, item)

    def __str__(self):
        return '{0} - {1}'.format(self.number, self.title)


class File(object):
    default_format = '%n - %s%e - %t.%x'

    def __init__(self, show_name, season, episodes, extension):
        self.show_name = show_name
        self.season = season
        self.episodes = [Episode(_file=self, number=str(int(i))) for i in episodes]
        self.extension = extension

    def __str__(self):
        filename = getattr(self, 'output_format', self.default_format)

        filename = filename.replace('%n', self.show_name)
        filename = filename.replace('%s', self.season)
        filename = filename.replace('%t', self.title)
        filename = filename.replace('%x', self.extension)

        filename = filename.replace('%e', self.episode)

        return filename

    @property
    def episode(self):
        return '-'.join([e.number.zfill(2) for e in self.episodes])

    @property
    def title(self):
        titles = [e.title for e in self.episodes]

        # Check the titles aren't all the same with different (x) parts
        suffixes = tuple('({0})'.format(i+1) for i in range(len(titles)))
        if any([t.endswith(suffixes) for t in titles]):
            stripped_titles = set([t[:-4] for t in titles])
            if len(stripped_titles) is 1:
                titles = stripped_titles

        return ' & '.join(titles)

    def set_output_format(self, user_format, config):
        if user_format is None:
            self.output_format = config.get(self.show_name, 'format')
        else:
            self.output_format = user_format

    def user_overrides(self, show_name, season, episode):
        if show_name:
            self.show_name = show_name

        for e in self.episodes:
            if season:
                e.season = season
            if episode:
                e.number = episode


class TvRenamr(object):
    def __init__(self, working_dir, config, debug=False, dry=False):
        self.working_dir = working_dir
        self.dry = dry
        self.debug = debug
        self.config = config

    def remove_part_from_multiple_episodes(self, show_name):
        """Remove the string "Part " from a filename.

        In episode titles of multi-part episodes that use the format
        (Part n) remove the 'Part ' section so the format is (n).

        """
        log.debug('Removing Part from episode name')
        return show_name.replace('(Part ', '(')

    def extract_details_from_file(self, fn, user_regex=None):
        """Using a regular expression extract information from the filename passed in.

        Looks at the file given and extracts from it the show title, it's
        season number and episode number using regular expression magic.
        The default formats accepted are: series.0x00.xxx or series.s0e00.xxx
        A user can specify their own regular expression for a format not
        already covered.

        """
        fn = fn.replace("_", ".").replace(" ", ".")  # santise filename
        log.log(22, 'Renaming: {0}'.format(fn))

        regex = self._build_regex(user_regex)
        matches = re.match(regex, fn)
        if not matches:
            raise errors.UnexpectedFormatException(fn)

        log.debug('Renaming using: {0}'.format(regex))

        return self._build_credentials(fn, matches)

    def retrieve_episode_title(self, episode, library='thetvdb', canonical=None):
        """Retrieves the title of a given episode.

        The series name, season and episode numbers must be specified to get
        the episode's title. The library specified by the user will be used
        first but will fall back to the other library if an error occurs.

        The first library defaults to The Tv DB.

        """
        libraries = [
            TheTvDb,
            TvRage
        ]
        [libraries.insert(0, libraries.pop(libraries.index(lib)))
        for lib in libraries if lib.__name__.lower() == library]

        # TODO: Make this bit not suck.
        if canonical:
            episode._file.show_name = canonical
        else:
            episode._file.show_name = self.config.get_canonical(episode._file.show_name)
        log.debug('Show Name: {0}'.format(episode._file.show_name))

        # loop the libraries until one works
        for lib in libraries:
            try:
                log.debug('Using {0}'.format(lib.__name__))
                args = [episode._file.show_name, episode._file.season, episode.number]
                self.lookup = lib(*args)  # assign to self for use in format_show_name
                break  # first library worked - nothing to see here
            except (errors.EmptyEpisodeTitleException, errors.EpisodeNotFoundException,
                    errors.InvalidXMLException, errors.NoNetworkConnectionException,
                    errors.ShowNotFoundException) as e:
                if lib == libraries[-1]:
                    raise errors.NoMoreLibrariesException(lib, e)
                continue

        log.info('Episode: {0}'.format(self.lookup.title))
        return self.lookup.title

    def format_show_name(self, show_name, the=None, override=None):
        if the is None:
            the = self.config.get(show_name, 'the')

        try:
            show_name = self.config.get_output(show_name)
            log.debug('Using config output name: {0}'.format(show_name))
        except errors.ShowNotInConfigException:
            show_name = self.lookup.show
            msg = 'Using the formatted show name retrieved by the library: {0}'
            log.debug(msg.format(show_name))

        if override is not None:
            show_name = override
            log.debug('Overrode show name with: {0}'.format(show_name))

        if the is True:
            show_name = self._move_leading_the_to_trailing_the(show_name)

        log.debug('Final show name: {0}'.format(show_name))

        return show_name

    def build_path(self, _file, rename_dir=None, organise=None):
        """Build the full destination path and filename of the renamed file.

        By default the format is:

        Show Name - Season NumberEpisode Number - Episode Title.format.

        Builds the new path for the file to be renamed to, by default this is
        the working directory. Users can specify a directory to move files to
        once renamed using the renamed_dir option. The auto_move option can be
        used to specify a top level directory where files will be placed in
        season and show folders, i.e. Show/Season 1/episodes

        """
        if rename_dir is None:
            rename_dir = self.config.get(_file.show_name, 'renamed')
        if rename_dir is False:
            rename_dir = self.working_dir

        if organise is None:
            organise = self.config.get(_file.show_name, 'organise')
        if organise is True:
            args = [rename_dir, _file.show_name, _file.season]
            rename_dir = self._build_organise_path(*args)

        log.log(22, 'Directory: {0}'.format(rename_dir))

        path = os.path.join(rename_dir, str(_file))
        log.debug('Full path: {0}'.format(path))

        return path

    def rename(self, current_filepath, destination_filepath):
        """Renames a file.

        This is more akin to the UNIX `mv` operation as the destination filepath
        can be anywhere on the filesystem.
        Returns the new filename for use elsewhere.

        """
        if os.path.exists(destination_filepath):
            raise errors.EpisodeAlreadyExistsInDirectoryException(destination_filepath)

        log.debug(os.path.join(self.working_dir, current_filepath))
        log.debug(destination_filepath)
        if not self.dry and not self.debug:
            source_filepath = os.path.join(self.working_dir, current_filepath)
            os.rename(source_filepath, destination_filepath)
        destination_file = os.path.split(destination_filepath)[1]
        log.log(26, 'Renamed: "{0}"'.format(destination_file))
        return destination_filepath

    def _build_credentials(self, fn, matches):
        """Build a dictionary of a file's extracted credentials."""
        details = {}

        try:
            details.update({'show_name': matches.group('show_name').replace('.', ' ').strip()})
        except IndexError:
            pass
        try:
            details.update({'season': str(int(matches.group('season')))})
        except IndexError:
            pass

        details.update({
            'episodes': list(filter(lambda x: x is not None, matches.groups()[2:])),
            'extension': os.path.splitext(fn)[1]
        })

        msg = ', '.join('{0}: {1}'.format(key, value) for key, value in details.items())
        log.debug('Filename yielded: {0}'.format(msg))
        return details

    def _build_organise_path(self, start_path, show_name, season_number):
        """Constructs a directory path using the show's details.

        Show name and season number of an episode dictate the folder structure.

        """
        if start_path[-1:] != '/':
            start_path = start_path + '/'
        path = start_path + show_name + '/Season ' + str(int(season_number)) + '/'
        if not os.path.exists(path) and not self.dry and not self.debug:
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
        series = r"(?P<show_name>[\w\s.',_-]+)"
        season = r"(?P<season>\d{1,2})"
        episode = r"(\d{2})"
        second_episode = r".E?(\d{2})*"

        if regex is None:
            # Build default regex
            return series + r"\.[Ss]?" + season + r"[XxEe]?" + episode + second_episode

        if not partial and not ('%n' in regex or '%s' in regex or '%e' in regex):
            raise errors.IncorrectCustomRegularExpressionSyntaxException(regex)

        # series name
        regex = regex.replace('%n', series)

        # season number
        # %s{n}
        if '%s{' in regex:
            log.debug('Season digit number found')
            r = regex.split('%s{')[1][:1]
            log.debug('Specified {0} season digits'.format(r))
            s = season.replace('1,2', r)
            regex = regex.replace('%s{' + r + '}', s)
            log.debug('Season regex set: {0}'.format(s))

        # %s
        if '%s' in regex:
            regex = regex.replace('%s', season)
            log.debug('Default season regex set: {0}'.format(regex))

        # episode number
        # %e{n}
        if '%e{' in regex:
            log.debug('User set episode digit number found')
            r = regex.split('%e{')[1][:1]
            log.debug('User specified {0} episode digits'.format(r))
            e = episode.replace('2', r)
            regex = regex.replace('%e{' + r + '}', e)
            log.debug('Episode regex set: {0}'.format(e))

        # %e
        if '%e' in regex:
            regex = regex.replace('%e', episode)
            log.debug('Default episode regex set: {0}'.format(regex))

        return regex

    def _move_leading_the_to_trailing_the(self, show_name):
        """Moves the leading 'The' of a show name to a trailing 'The'.

        A comma and space are added before the new 'The'.

        """
        if not(show_name.startswith('The ')):
            return show_name
        log.debug("Moving leading 'The' to end of: {0}".format(show_name))
        return show_name[4:] + ', The'
