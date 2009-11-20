import logging
import urllib2
import xml.etree.ElementTree as ET

from core.errors import *

log = logging.getLogger('Tv Rage')

url_name = "http://services.tvrage.com/feeds/search.php?show="
url_ep = "http://services.tvrage.com/feeds/full_show_info.php?sid="


class TvRage():
    def __init__(self, series_name):
        self.series = series_name
    
    def __get_series_id(self):
        url = url_name + self.series.replace(' ', '%20')
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise
        dom = ET.fromstring(data)
        if dom is None: raise SeriesIdNotFoundException('Error retriving XML for %s\'s series id' % self.series)
        log.debug('XML retrieved, searching for series')
        for name in dom.findall('show'):
            s = name.find('name').text
            if s.lower() == self.series.lower():
                self.series = s
                log.debug('Series chosen %s' % self.series)
                return name.find('showid').text
            else: raise ShowNotFoundException(self.series)
    
    def get_episode_name(self, season, episode):
        series_id = self.__get_series_id()
        url = url_ep + series_id
        try: data = urllib2.urlopen(url).read()
        except urllib2.URLError: raise
        dom = ET.fromstring(data)
        if dom is None: raise EpisodeNotFoundException('Error retriving XML for %s %s%s' % (self.series, season, episode))
        log.debug('XML retrieved, searching for episode')
        
        for s in dom.find('Episodelist'):
            if s.get('no') == season:
                title = None
                for e in s.findall('episode'):
                    if e.find('epnum').text == str(int(episode)):
                        title = e.find('title').text
                        log.info('Retrieved episode: %s' % title)
                if title: return {'series': self.series, 'title':title}
                else: raise EpisodeNotFoundException(self.series, season, episode)
        
        # for ep in dom.findall('season' % season):
        #     if ep.find('epnum') == episode:
        #         title = ep.find('title')
        # if not title: raise EpisodeNotFoundException('Error finding episode for %s' % self.series)
        # else: return title