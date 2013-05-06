import logging


log = logging.getLogger('Episode')


def clean_name(filename, before=':', after=','):
    """
    Cleans the string passed in.

    A wrapper of Python's str.replace() with the idea of making the string
    safe for all file systems, but not using the horrible \ character.
    Also allows the user to specify the new characters to be used.

    """
    return filename.replace(before, after)


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
