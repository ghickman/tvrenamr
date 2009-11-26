import logging
import urllib2
import xml.etree.ElementTree as ET

from core.errors import *

log = logging.getLogger('Tv Rage')

url_name = "http://services.tvrage.com/feeds/search.php?show="
url_ep = "http://services.tvrage.com/feeds/full_show_info.php?sid="


class TvRage():
    def __init__(self, show_name):
        """
        :param show_name: The show name of the episode title to be retrieved.
        """
        self.series = show_name
    
    def __get_series_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is instantiated.
        
        :returns: A show ID.
        :rtype: A string.
        """
        url = url_name + self.series.replace(' ', '%20')
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise
        dom = ET.fromstring(data)
        if dom is None: raise XMLEmptyException(log.name, self.series)
        log.debug('XML retrieved, searching for series')
        for name in dom.findall('show'):
            s = name.find('name').text
            if s.lower() == self.series.lower():
                self.series = s
                log.debug('Series chosen %s' % self.series)
                return name.find('showid').text
            else: raise ShowNotFoundException(log.name, self.series)
    
    def get_episode_name(self, season, episode):
        """
        Retrieves the episode title for the given episode from tvrage.com.
        
        :param season: The season number of the episode
        :param episode: The episode number of the episode
        
        :returns: The series name and title. Series name is returned so that it is formatted correctly.
        :rtype: A dictionary whose keys are 'series' and 'title'.
        """
        series_id = self.__get_series_id()
        url = url_ep + series_id
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise EpisodeNotFoundException(log.name, self.series)
        dom = ET.fromstring(data)
        if dom is None: raise XMLEmptyException(log.name, self.series)
        log.debug('XML retrieved, searching for episode')
        
        # In a single digit episode number add a zero
        if len(episode) == 1 and episode[:1] != '0': episode = '0'+episode
        
        title = None
        for s in dom.find('Episodelist'):
            if s.get('no') == season:
                for e in s.findall('episode'):
                    if e.find('seasonnum').text == episode:
                        title = e.find('title').text
                        log.info('Retrieved episode: %s' % title)
        if title is not None: return {'show': self.series, 'title':title}
        else: raise EpisodeNotFoundException(log.name, self.series, season, episode)
    