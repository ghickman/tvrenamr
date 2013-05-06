import logging
import urllib
from xml.etree.ElementTree import fromstring
try:  # XML Exception class import dance
    from xml.etree.ElementTree import ParseError
except ImportError:  # python 2.6
    from xml.parsers.expat import ExpatError as ParseError

import requests

from .. import errors


log = logging.getLogger('The Tv DB')


apikey = 'C4C424B4E9137AFD'
url_base = 'http://www.thetvdb.com/api/'
url_series = 'GetSeries.php?seriesname='


class TheTvDb(object):
    def __init__(self, show, season, episode):
        """
        :param show_name: The show name of the episode name to be retrieved.
        """
        self.show = show
        self.season = season
        self.episode = episode

        log.info('Searching: {0}'.format(self.show))
        self.show_id, self.show = self._get_show_id()
        log.debug('Retrieved show id: {0}'.format(self.show_id))
        log.debug('Retrieved canonical show name: {0}'.format(self.show))
        self.name = self._get_episode_name()
        log.debug('Retrieved episode name: {0}'.format(self.name))

    def _get_show_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is
        instantiated.

        :raises URLError: Raised when a network error occurs. Usually when there is no internet.
        :raises XMLEmptyException: Raised when the XML document returned from The Tv Db is empty.
        :raises ShowNotFoundException: Raised when the Show cannot be found on The Tv Db.

        :returns: A show ID.
        :rtype: A string.
        """
        log.debug('Retrieving series id for {0}'.format(self.show))
        try:
            quoted_show = urllib.parse.quote(self.show)
        except AttributeError:
            # python 2
            quoted_show = urllib.quote(self.show)
        url = '{0}{1}{2}'.format(url_base, url_series, quoted_show)
        log.debug('Series url: {0}'.format(url))

        req = requests.get(url)
        if not req.ok:
            raise errors.NoNetworkConnectionException('thetvdb.org')

        log.debug('XML: Attempting to parse')
        try:
            tree = fromstring(req.content)
        except ParseError:
            raise errors.InvalidXMLException(log.name, self.show)
        if tree is None or len(tree) is 0:
            raise errors.InvalidXMLException(log.name, self.show)
        log.debug('XML: Parsed')

        for name in tree.findall('Series'):
            show = name.findtext('SeriesName')
            if show.lower() == self.show.lower():
                log.debug('Series chosen: {0}'.format(show))
                return name.findtext('seriesid'), show
            else:
                raise errors.ShowNotFoundException(log.name, self.show)

    def _get_episode_name(self):
        """
        Retrieves the episode name for the given episode from thetvdb.com.

        :raises EpisodeNotFoundException: Raised when the url for an episode
        doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from
        The Tv Db is empty.
        :raises EmptyEpisodeNameException:

        :returns: The episode name.
        :rtype: String
        """
        args = (url_base, apikey, self.show_id, str(int(self.season)), str(int(self.episode)))
        episode_url = '{0}{1}/series/{2}/default/{3}/{4}/en.xml'.format(*args)
        log.debug('Episode URL: {0}'.format(episode_url))

        log.debug('Attempting to retrieve episode name')
        req = requests.get(episode_url)
        if not req.ok:
            raise errors.EpisodeNotFoundException(
                log.name,
                self.show,
                self.season,
                self.episode
            )
        log.debug('XML: Retreived')

        log.debug('XML: Attempting to parse')
        try:
            tree = fromstring(req.content)
        except ParseError:
            raise errors.InvalidXMLException(log.name, self.show)
        if tree is None:
            raise errors.InvalidXMLException(log.name, self.show)
        log.debug('XML: Parsed')
        args = (self.show, self.season, self.episode)
        log.debug('XML: Episode document retrived for {0} - {1}{2}'.format(*args))

        log.debug('XML: Attempting to find the episode name')
        episode = tree.find('Episode').findtext('EpisodeName')
        if not episode:
            raise errors.EmptyEpisodeNameException

        return episode
