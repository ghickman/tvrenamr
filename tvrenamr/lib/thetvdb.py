import logging
import urllib
from xml.etree.ElementTree import fromstring

import requests

from tvrenamr.errors import (EmptyEpisodeNameException,
                             EpisodeNotFoundException,
                             NoNetworkConnectionException,
                             ShowNotFoundException,
                             XMLEmptyException)

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
        self.season = season
        self.episode = episode

        log.info('Searching: %s' % self.show)
        self.show_id, self.show = self._get_show_id()
        log.debug('Retrieved show id: %s' % self.show_id)
        log.debug('Retrieved canonical show name: %s' % self.show)
        self.title = self._get_episode_name()
        log.debug('Retrieved episode name: %s' % self.title)

    def _get_show_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is instantiated.

        :raises URLError: Raised when a network error occurs. Usually when there is no internet.
        :raises XMLEmptyException: Raised when the XML document returned from The Tv Db is empty.
        :raises ShowNotFoundException: Raised when the Show cannot be found on The Tv Db.

        :returns: A show ID.
        :rtype: A string.
        """
        log.debug('Retrieving series id for %s' % self.show)
        url = '%s%s%s' % (url_base, url_series, urllib.quote(self.show))
        log.debug('Series url: %s' % url)

        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            data = req.content
        else:
            raise NoNetworkConnectionException('thetvdb.org')

        log.debug('XML: Attempting to parse')
        tree = fromstring(data)
        log.debug('XML: Parsed')

        if tree is None or len(tree) is 0:
            raise XMLEmptyException(log.name, self.show)
        log.debug('XML retrieved, searching for series')

        for name in tree.findall("Series"):
            show = name.findtext("SeriesName")
            if show.lower() == self.show.lower():
                log.debug('Series chosen: %s' % show)
                return name.findtext('seriesid'), show
            else:
                raise ShowNotFoundException(log.name, self.show)

    def _get_episode_name(self):
        """
        Retrieves the episode title for the given episode from thetvdb.com.

        :raises EpisodeNotFoundException: Raised when the url for an episode
        doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from
        The Tv Db is empty.
        :raises EmptyEpisodeNameException:

        :returns: The episode title.
        :rtype: String
        """
        episode_url = '%s%s/series/%s/default/%s/%s/en.xml' % \
                        (url_base, apikey, self.show_id,
                        str(int(self.season)), str(int(self.episode)))
        log.debug('Episode URL: %s' % episode_url)

        log.debug('Attempting to retrieve episode name')
        req = requests.get(episode_url)
        if req.status_code == requests.codes.ok:
            data = req.content
            log.debug('XML: Retreived')
        else:
            raise EpisodeNotFoundException(log.name, self.show, self.season, self.episode)

        log.debug('XML: Attempting to parse')
        tree = fromstring(data)
        log.debug('XML: Parsed')

        if tree is None:
            raise XMLEmptyException(log.name, self.show)
        log.debug('XML: Episode document retrived for %s - %s%s' % (self.show, self.season, self.episode))

        log.debug('XML: Attempting to finding the episode name')
        episode = tree.find("Episode").findtext("EpisodeName")
        if not episode:
            raise EmptyEpisodeNameException

        return episode

