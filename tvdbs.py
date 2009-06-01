import urllib

class TvDbs:
    def get_url(self, url):
        return urllib.urlopen(url).read()
    
    def get_episode_name(self, season, episode):
        return None