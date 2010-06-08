import logging
import urllib2
import xml.etree.ElementTree as ET

from errors import *

log = logging.getLogger('The Tv DB')

url_base = 'http://www.thetvdb.com/api/'
url_series = 'GetSeries.php?seriesname='
apikey = 'C4C424B4E9137AFD'

class TheTvDb():
    def __init__(self, show_name):
        """
        :param show_name: The show name of the episode title to be retrieved.
        """
        self.series = show_name
        
    def __get_series_id(self):
        """
        Retrieves the show ID of the show name passed in when the class is instantiated.
        
        :raises URLError: Raised when a network error occurs. Usually when there is no internet.
        :raises XMLEmptyException: Raised when the XML document returned from The Tv Db is empty.
        :raises ShowNotFoundException: Raised when the Show cannot be found on The Tv Db.
        
        :returns: A show ID.
        :rtype: A string.
        """
        url = url_base + url_series + urllib2.quote(self.series)
        log.debug('Series url: '+url)
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise
        dom = ET.fromstring(data)
        if dom is None: raise XMLEmptyException(log.name, self.series)
        log.debug('XML retrieved, searching for series')
        for name in dom.findall("Series"):
            s = name.find("SeriesName").text
            if s.lower() == self.series.lower():
                self.series = s
                log.debug('Series chosen %s' % self.series)
                return name.find('seriesid').text
            else: raise ShowNotFoundException(log.name, self.series)
        
    def get_episode_name(self, season, episode):
        """
        Retrieves the episode title for the given episode from tvrage.com.
        
        :param season: The season number of the episode
        :param episode: The episode number of the episode
        
        :raises EpisodeNotFoundException: Raised when the url for an episode doesn't exist or the network cannot be reached.
        :raises XMLEmptyException: Raised when the XML document returned from The Tv Db is empty.
        
        :returns: The series name and title. Series name is returned so that it is formatted correctly.
        :rtype: A dictionary whose keys are 'series' and 'title'.
        """
        log.debug('Retrieving series id for %s' % self.series)
        series_id = self.__get_series_id()
        log.debug('Building episode url')
        episode_url = url_base + apikey +'/series/'+ series_id +'/default/'+ str(int(season)) +'/'+ str(int(episode)) +'/en.xml'
        log.debug(episode_url)
        log.debug('Attempting to retrieve episode name')
        try: f = urllib2.urlopen(episode_url)
        except urllib2.URLError: raise EpisodeNotFoundException(log.name, self.series, season, episode)
        dom = ET.fromstring(f.read())
        if dom is None: raise XMLEmptyException(log.name, self.series)
        
        log.debug('XML retrived for %s - ' % self.series)
        title = dom.find("Episode").find("EpisodeName").text
        
        log.info('Retrieved episode: %s' % title)
        return {'show': self.series, 'title': title}