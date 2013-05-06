import logging
import urllib
from xml.etree.ElementTree import fromstring
try:  # XML Exception class import dance
    from xml.etree.ElementTree import ParseError
except ImportError:  # python 2.6
    from xml.parsers.expat import ExpatError as ParseError

import requests

from .. import errors


log = logging.getLogger('Tv Rage')


url_name = "http://services.tvrage.com/feeds/search.php?show="
url_ep = "http://services.tvrage.com/feeds/full_show_info.php?sid="


class TvRage(object):
    def __init__(self, show, season, episode):
        """
        :param show_name: The show name of the episode name to be retrieved.
        """
        self.show = show
        log.info('Looking up show: {0}'.format(self.show))
        self.season = str(int(season))
        self.episode = str(int(episode))

        self.show_id, self.show = self._get_show_id()
        log.debug('Retrieved show id: {0}'.format(self.show_id))
        log.debug('Retrieved canonical show name: {0}'.format(self.show))
        self.title = self._get_episode_title()
        log.debug('Retrieved episode title: {0}'.format(self.title))

    def _get_show_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is instantiated.

        :raises URLError: Raised when a network error occurs. Usually when there is no internet.
        :raises XMLEmptyException: Raised when the XML document returned from Tv Rage is empty.
        :raises ShowNotFoundException: Raised when the Show cannot be found on Tv Rage.

        :returns: A show ID.
        :rtype: A string.
        """
        log.debug('Retrieving series id for {0}'.format(self.show))
        try:
            quoted_show = urllib.quote(self.show)
        except AttributeError:
            # python 3
            quoted_show = urllib.parse.quote(self.show)
        url = '{0}{1}'.format(url_name, quoted_show)
        log.debug('Series url: {0}'.format(url))

        req = requests.get(url)
        if not req.ok:
            raise errors.NoNetworkConnectionException('tvrage.com')

        log.debug('XML: Attempting to parse')
        try:
            tree = fromstring(req.content)
        except ParseError:
            raise errors.InvalidXMLException(log.name, self.show)
        if tree is None or len(tree) is 0:
            raise errors.InvalidXMLException(log.name, self.show)
        log.debug('XML: Parsed')
        log.debug('XML retrieved, searching for series')

        for name in tree.findall('show'):
            show = name.find('name').text
            if show.lower() == self.show.lower():
                log.debug('Series chosen {0}'.format(self.show))
                return name.find('showid').text, show
            else:
                raise errors.ShowNotFoundException(log.name, self.show)

    def _get_episode_title(self):
        """
        Retrieves the episode title for the given episode from tvrage.com.

        :raises EpisodeNotFoundException: Raised when the url for an episode
        doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from
        Tv Rage is empty.

        :returns: The series name and name. Series name is returned so that it is formatted correctly.
        :rtype: A dictionary whose keys are 'series' and 'name'.
        """
        episode_url = '{0}{1}'.format(url_ep, self.show_id)
        log.debug('Episode URL: {0}'.format(episode_url))

        log.debug('Attempting to retrieve episode title')
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
        log.debug('XML: Episode document retrived for {0} - {1}'.format(*args))

        # In a single digit episode number add a zero
        if len(self.episode) == 1 and self.episode[:1] != '0':
            self.episode = '0' + self.episode

        log.debug('XML: Attempting to finding the episode title')
        episode = None
        for s in tree.find('Episodelist'):
            if s.get('no') == self.season:
                for e in s.findall('episode'):
                    if e.find('seasonnum').text == self.episode:
                        episode = e.find('title').text
        if not episode:
            raise errors.EpisodeNotFoundException(
                log.name,
                self.show,
                self.season,
                self.episode
            )

        return episode
