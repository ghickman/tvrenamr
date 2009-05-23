import logging
import urllib
import xml.etree.ElementTree as ET

class Series:
    apikey = 'C4C424B4E9137AFD'
    url = "http://www.thetvdb.com/api/"
    get_series = "GetSeries.php?seriesname="
    name = ""
    
    def __init__(self, series_name):
        self.name = series_name.lower()
        
    def getSeriesId(self):
        logging.info('Retrieving series ID: %s', self.name)
        f = urllib.urlopen(self.url + self.get_series + self.name)
        try:
            dom = ET.fromstring(f.read())
            for series in dom.findall("Series"):
                s = series.find("SeriesName").text
                if s.lower() == self.name.lower():
                    self.name = s
                    return series.find("seriesid").text
        except Exception:
            logging.warning('Series not found: %s', self.name)
            return None
        
        
    def getEpisodeName(self, series_id, season, episode):
        logging.info('Retrieving episode name for: %s', self.name)
        episode_url = self.url + self.apikey +"/series/"+ series_id +"/default/"+ season +"/"+ episode +"/en.xml"
        f = urllib.urlopen(episode_url)
        try:
            dom = ET.fromstring(f.read())
            return dom.find("Episode").find("EpisodeName").text
        except Exception:
            logging.warning('Episode not found: %s', self.name + " - " + season + episode)
            return None