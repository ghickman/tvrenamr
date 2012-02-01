import logging
import urllib
import requests

from lxml.etree import fromstring, XMLSyntaxError

try:
    from tvrenamr.errors import EmptyEpisodeNameException, \
                                EpisodeNotFoundException, \
                                NoNetworkConnectionException, \
                                ShowNotFoundException, \
                                XMLEmptyException
except ImportError:
    from . errors import EmptyEpisodeNameException, \
                            EpisodeNotFoundException, \
                            NoNetworkConnectionException, \
                            ShowNotFoundException, \
                            XMLEmptyException

log = logging.getLogger('Tv Rage')

url_name = "http://services.tvrage.com/feeds/search.php?show="
url_ep = "http://services.tvrage.com/feeds/full_show_info.php?sid="

class TvRage():
    def __init__(self, show, season, episode):
        """
        :param show_name: The show name of the episode title to be retrieved.
        """
        self.show = show
        log.info('Looking up show: %s' % self.show)
        self.season = str(int(season))
        self.episode = str(int(episode))

        self.show_id, self.show = self.__get_show_id()
        log.debug('Retrieved show id: %s' % self.show_id)
        log.debug('Retrieved canonical show name: %s' % self.show)
        self.title = self.__get_episode_name()
        log.debug('Retrieved episode name: %s' % self.title)

    def __get_show_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is instantiated.

        :raises URLError: Raised when a network error occurs. Usually when there is no internet.
        :raises XMLEmptyException: Raised when the XML document returned from Tv Rage is empty.
        :raises ShowNotFoundException: Raised when the Show cannot be found on Tv Rage.

        :returns: A show ID.
        :rtype: A string.
        """
        log.debug('Retrieving series id for %s' % self.show)
        url = '%s%s' % (url_name, urllib.quote(self.show))
        log.debug('Series url: %s' % url)

        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            data = req.content
        else:
            raise NoNetworkConnectionException('tvrage.com')

        log.debug('XML: Attempting to parse')
        tree = fromstring(data)
        log.debug('XML: Parsed')

        if tree is None or len(tree) is 0:
            raise XMLEmptyException(log.name, self.show)
        log.debug('XML retrieved, searching for series')

        for name in tree.findall('show'):
            show = name.find('name').text
            if show.lower() == self.show.lower():
                log.debug('Series chosen %s' % self.show)
                return name.find('showid').text, show
            else:
                raise ShowNotFoundException(log.name, self.show)


    def __get_episode_name(self):
        """
        Retrieves the episode title for the given episode from tvrage.com.

        :raises EpisodeNotFoundException: Raised when the url for an episode
        doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from
        Tv Rage is empty.

        :returns: The series name and title. Series name is returned so that it is formatted correctly.
        :rtype: A dictionary whose keys are 'series' and 'title'.
        """
        episode_url = '%s%s' % (url_ep, self.show_id)
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

        # In a single digit episode number add a zero
        if len(self.episode) == 1 and self.episode[:1] != '0':
            self.episode = '0' + self.episode

        log.debug('XML: Attempting to finding the episode name')
        episode = None
        for s in tree.find('Episodelist'):
            if s.get('no') == self.season:
                for e in s.findall('episode'):
                    if e.find('seasonnum').text == self.episode:
                        episode = e.find('title').text
        if not episode:
            raise EpisodeNotFoundException(log.name, self.show, self.season, self.episode)

        return episode

