import logging
import urllib2
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError

log = logging.getLogger('The Tv DB')

apikey = 'C4C424B4E9137AFD'
url_base = 'http://www.thetvdb.com/api/'
url_series = 'GetSeries.php?seriesname='


class TheTvDb():

    def __init__(self, show, season, episode):
        """
        :param show_name: The show name of the episode title to be retrieved.
        """
        self.show = show
        log.info('Searching: %s' % self.show)
        self.season = season
        self.episode = episode

        self.show_id, self.show = self.__get_show_id()
        log.debug('Retrieved show id: %s' % self.show_id)
        log.debug('Retrieved canonical show name: %s' % self.show)
        self.title = self.__get_episode_name()
        log.debug('Retrieved episode name: %s' % self.title)

    def get_show(self):
        return self.show

    def get_title(self):
        return self.title

    def __get_show_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is
        instantiated.

        :raises URLError: Raised when a network error occurs. Usually when
        there is no internet connection.
        :raises XMLEmptyException: Raised when the XML document returned from
        The Tv Db is empty.
        :raises ShowNotFoundException: Raised when the given Show cannot be
        found on The Tv Db.

        :returns: A show ID.
        :rtype: A string.
        """
        log.debug('Retrieving series id for %s' % self.show)
        url = '%s%s%s' % (url_base, url_series, urllib2.quote(self.show))
        log.debug('Series url: %s' % url)

        try:
            data = urllib2.urlopen(url).read()
        except urllib2.URLError:
            raise NoNetworkConnectionException('thetvdb.org')

        log.debug('XML: Attempting to parse')
        try:
            dom = ElementTree.fromstring(data)
        except ExpatError, e:
            log.error('Invalid XML was received from The TvDB. Maybe try \
                        querying Tv Rage?')
            exit()

        if dom is None:
            raise XMLEmptyException(log.name, self.show)
        log.debug('XML retrieved, searching for series')

        for name in dom.findall("Series"):
            show = name.findtext("SeriesName")
            if show.lower() == self.show.lower():
                log.debug('Series chosen: %s' % show)
                return name.findtext('seriesid'), show
            else:
                raise ShowNotFoundException(log.name, self.show)

    def __get_episode_name(self):
        """
        Retrieves the episode title for the given episode from tvrage.com.

        :param season: The season number of the episode
        :param episode: The episode number of the episode

        :raises EpisodeNotFoundException: Raised when the url for an episode
        doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from
        The Tv Db is empty.

        :returns: The series name and title. Series name is returned so that it
        is formatted correctly.
        :rtype: A dictionary whose keys are 'series' and 'title'.
        """
        episode_url = '%s%s/series/%s/default/%s/%s/en.xml' % \
                        (url_base, apikey, self.show_id, \
                        str(int(self.season)), str(int(self.episode)))
        log.debug('Episode URL: %s' % episode_url)

        log.debug('Attempting to retrieve episode name')
        try:
            tempfile = urllib2.urlopen(episode_url)
            log.debug('XML: Retreived')
        except urllib2.URLError:
            raise EpisodeNotFoundException(log.name, self.show, self.season, \
                                            self.episode)

        log.debug('XML: Attempting to parse')
        try:
            dom = ElementTree.fromstring(tempfile.read())
            log.debug('XML: parsed')
        except ExpatError, e:
            log.error('Invalid XML was received from The TvDB. Maybe try \
                        querying Tv Rage?')
            exit()

        if dom is None:
            raise XMLEmptyException(log.name, self.show)
        log.debug('Episode XML retrived for %s - %s%s' % \
                    (self.show, self.season, self.episode))

        return dom.find("Episode").findtext("EpisodeName")
