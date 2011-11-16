class Episode(object):

    # def __init__(self, show_name=None, season=None, episode=None, title=None,
    #         extension=None, format='%n - %s%e - %t.%x'):
    def __init__(self, fn_parts, format='%n - %s%e - %t.%x'):
        self.show_name = fn_parts[0]
        self.season = fn_parts[1] if not None else str(fn_parts[1])
        self.episode = fn_parts[2] if not None else str(fn_parts[2])
        self.extension = fn_parts[3]
        self.format = format

    def __getattribute__(self, item):
        """
        Allow the retrieval of single digit episode numbers but return
        it with a leading zero.
        """
        if item is 'episode_2':
            return '0%s' % self.episode
        else:
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

