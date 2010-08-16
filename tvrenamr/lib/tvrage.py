import logging
import urllib2
import xml.etree.ElementTree as ET

from errors import *

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
        Retrieves the show ID of the show name passed in when the class is instantiated.
        
        :raises URLError: Raised when a network error occurs. Usually when there is no internet.
        :raises XMLEmptyException: Raised when the XML document returned from Tv Rage is empty.
        :raises ShowNotFoundException: Raised when the Show cannot be found on Tv Rage.
        
        :returns: A show ID.
        :rtype: A string.
        """
        url = url_name + self.show.replace(' ', '%20')
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise NoNetworkConnectionException('tvrage.com')
        dom = ET.fromstring(data)
        if dom is None: raise XMLEmptyException(log.name, self.show)
        log.debug('XML retrieved, searching for series')
        for name in dom.findall('show'):
            show = name.find('name').text
            if show.lower() == self.show.lower():
                log.debug('Series chosen %s' % self.show)
                return name.find('showid').text, show
            else: raise ShowNotFoundException(log.name, self.show)
    
    
    def __get_episode_name(self):
        """
        Retrieves the episode title for the given episode from tvrage.com.
        
        :param season: The season number of the episode
        :param episode: The episode number of the episode
        
        :raises EpisodeNotFoundException: Raised when the url for an episode doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from Tv Rage is empty.
        
        :returns: The series name and title. Series name is returned so that it is formatted correctly.
        :rtype: A dictionary whose keys are 'series' and 'title'.
        """
        url = url_ep + self.show_id
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise EpisodeNotFoundException(log.name, self.show)
        dom = ET.fromstring(data)
        if dom is None: raise XMLEmptyException(log.name, self.show)
        log.debug('XML retrieved, searching for episode')
        
        # In a single digit episode number add a zero
        if len(self.episode) == 1 and self.episode[:1] != '0': self.episode = '0' + self.episode
        
        title = None
        for s in dom.find('Episodelist'):
            if s.get('no') == self.season:
                for e in s.findall('episode'):
                    if e.find('seasonnum').text == self.episode:
                        title = e.find('title').text
                        log.info('Retrieved episode: %s' % title)
        if title is not None: return title
        else: raise EpisodeNotFoundException(log.name, self.show, self.season, self.episode)
    