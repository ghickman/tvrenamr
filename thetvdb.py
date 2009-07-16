import logging
import urllib2
import xml.etree.ElementTree as ET

from errors import *

class TheTvDb():
    series = ""
    url = 'http://www.thetvdb.com/api/'
    apikey = 'C4C424B4E9137AFD'
    get_series = 'GetSeries.php?seriesname='
    
    def __init__(self, series_name):
        self.series = series_name
        
    def __get_series_id(self):
        url = self.url + self.get_series + urllib2.quote(self.series)
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise
        dom = ET.fromstring(data)
        if dom == None: raise Exception('Error retriving XML for for: '+ self.series)
        for name in dom.findall("Series"):
            s = name.find("SeriesName").text
            if s.lower() == self.series.lower():
                self.series = s
                return name.find("seriesid").text
            else: raise ShowNotFoundException(self.series)
        
    def get_episode_name(self, season, episode):
        series_id = self.__get_series_id()
        episode_url = self.url + self.apikey +'/series/'+ series_id +'/default/'+ str(int(season)) +'/'+ str(int(episode)) +'/en.xml'
        try: f = urllib2.urlopen(episode_url)
        except urllib2.URLError: raise EpisodeNotFoundException(season+episode)
        dom = ET.fromstring(f.read())
        if dom != None: return dom.find("Episode").find("EpisodeName").text
        else: raise EpisodeNotFoundException(self.series + " - " + season + episode)