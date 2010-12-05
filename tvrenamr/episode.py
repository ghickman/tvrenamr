class Episode(object):
    
    def __init__(self, show_name=None, season=None, episode=None, title=None, extension=None, format='%n - %s%e - %t.%x'):
        self.show_name = show_name
        self.title = title
        self.extension = extension
        self.format = format

        if season is None:
            self.season = season
        else:
            self.season = str(season)
        
        if season is None:
            self.episode = episode
        else:
            self.episode = str(episode)

    def __getattr__(self, item):
        if item is 'episode_2':
            return '0%s' % self.episode
        else:
            try:
                self.__getitem__(item)
            except KeyError:
                raise AttributeError

    def __repr__(self):
        filename = self.format
        try:
            filename = filename.replace('%n', self.show_name)
            filename = filename.replace('%s', self.season)
            filename = filename.replace('%e', self.episode_2)
            filename = filename.replace('%t', self.title)
            filename = filename.replace('%x', self.extension)
            return filename
        except TypeError, e:
            return '%s \n%s' % (filename, e)

e = Episode('chuck', 2, 5)
e.title = 'test'
e.extension = 'avi'
print e.episode
print e