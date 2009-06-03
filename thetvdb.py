import logging
import urllib2
import xml.etree.ElementTree as ET
from tvdbs import TvDbs

class TheTvDb(TvDbs):
    series = ""
    url = 'http://www.thetvdb.com/api/'
    apikey = 'C4C424B4E9137AFD'
    get_series = 'GetSeries.php?seriesname='
    
    def __init__(self, series_name):
        self.series = series_name
        
    def __get_series_id(self):
        logging.debug('Retrieving series ID: %s', self.series)
        #data = super(TheTvDb, self).get_url(self.url + self.get_series + self.series)
        url = self.url + self.get_series + self.series
        try: data = urllib2.urlopen(url).read()
        except URLError: raise
        dom = ET.fromstring(data)
        if dom == None: raise Exception('Error retriving XML for for: '+ self.series)
        for name in dom.findall("Series"):
            s = name.find("SeriesName").text
            if s.lower() == self.series.lower():
                self.series = s
                return name.find("seriesid").text
        
    def get_episode_name(self, season, episode):
        series_id = self.__get_series_id()
        logging.debug('Retrieving episode name for: '+ self.series)
        episode_url = self.url + self.apikey +'/series/'+ series_id +'/default/'+ str(int(season)) +'/'+ str(int(episode)) +'/en.xml'
        try: f = urllib2.urlopen(episode_url)
        except URLError: raise
        dom = ET.fromstring(f.read())
        if dom != None: return dom.find("Episode").find("EpisodeName").text
        else:
            e = 'Episode not found: '+ self.series + " - " + season + episode
            logging.error(e) 
            raise Exception(e)