import re
import urllib2

class TvRage():
    series = ""
    url = "http://services.tvrage.com/tools/quickinfo.php?show="
    ep = "&ep="
    
    def __init__(self, series_name):
        self.series = series_name
    
    def get_episode_name(self, season, episode):
        #data = super(TvRage, self).get_url(self.url + self.series + self.ep + str(int(season)) +"x"+ episode)
        url = self.url + self.series.replace(' ','%20') + self.ep + str(int(season)) +"x"+ episode
        try: data = urllib2.urlopen(url).read()
        except URLError: raise
        m = re.compile("Episode\sInfo@[\d]{2}x[\d]{2}\^(?P<name>.+)\^").search(data)
        if m != None: return m.group('name')
        else: raise Exception('Episode could not be found: ' + season + episode)