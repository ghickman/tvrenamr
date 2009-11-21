import logging
import urllib2
import xml.etree.ElementTree as ET

from core.errors import *

log = logging.getLogger('The Tv DB')

url_base = 'http://www.thetvdb.com/api/'
url_series = 'GetSeries.php?seriesname='
apikey = 'C4C424B4E9137AFD'

class TheTvDb():
    def __init__(self, series_name):
        self.series = series_name
        
    def __get_series_id(self):
        url = url_base.url + url_series + urllib2.quote(self.series)
        log.debug('Series url: '+url)
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise
        dom = ET.fromstring(data)
        if dom is None: raise SeriesIdNotFoundException(self.series)
        log.debug('XML retrieved, searching for series')
        for name in dom.findall("Series"):
            s = name.find("SeriesName").text
            if s.lower() == self.series.lower():
                self.series = s
                log.debug('Series chosen %s' % self.series)
                return name.find('seriesid').text
            else: raise ShowNotFoundException(self.series)
        
    def get_episode_name(self, season, episode):
        log.debug('Retrieving series id for %s' % self.series)
        series_id = self.__get_series_id()
        log.debug('Building episode url')
        episode_url = url_base + apikey +'/series/'+ series_id +'/default/'+ str(int(season)) +'/'+ str(int(episode)) +'/en.xml'
        log.debug(episode_url)
        log.debug('Attempting to retrieve episode name')
        try: f = urllib2.urlopen(episode_url) # timeout after 15 seconds
        except urllib2.URLError: raise EpisodeNotFoundException(season+episode)
        dom = ET.fromstring(f.read())
        if dom is not None:
            title = dom.find("Episode").find("EpisodeName").text
            log.info('Retrieved episode: %s' % title)
            return {'series': self.series, 'title': title}
        else: raise EpisodeNotFoundException(log.name, self.series, season, episode)