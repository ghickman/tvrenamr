import logging


log = logging.getLogger('Episode')


class Episode(object):

    def __init__(self, format='%n - %s%e - %t.%x', **kwargs):
        if kwargs.get('show_name'):
            self.show_name = kwargs.get('show_name')
        if kwargs.get('season'):
            self.season = kwargs.get('season')
        if kwargs.get('episode'):
            self.episode = kwargs.get('episode')
        self.extension = kwargs.get('extension')
        self.format = format

    def __getattr__(self, item):
        msg = 'Missing {0}: Set it with {1} or use {2} in your --regex string'

        if item is 'show_name':
            log.error(msg.format('show name', '--show', '%n'))

        if item is 'season':
            log.error(msg.format('season', '--season', '%s'))

        if item is 'episode':
            log.error(msg.format('episode', '--episode', '%e'))

        raise AttributeError

    def __getattribute__(self, item):
        """
        Allow the retrieval of single digit episode numbers but return
        it with a leading zero.
        """
        if item is 'episode_2':
            return '0%s' % self.episode
        return object.__getattribute__(self, item)

    def __repr__(self):
        filename = self.format
        try:
            filename = filename.replace('%n', self.show_name)
        except TypeError:
            pass
        try:
            filename = filename.replace('%s', self.season)
        except TypeError:
            pass
        try:
            filename = filename.replace('%e', self.episode_2)
        except TypeError:
            pass
        try:
            filename = filename.replace('%t', self.title)
        except TypeError:
            pass
        try:
            filename = filename.replace('%x', self.extension)
        except TypeError:
            pass
        return filename

