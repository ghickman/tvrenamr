import os
import re
import urllib
import xml.etree.ElementTree as ET

apikey = 'C4C424B4E9137AFD'
url = "http://www.thetvdb.com/api/"
working_dir = "/Users/madnashua/Projects/TvRenamr/test"

def getInfo(fn):
    m = re.compile("[Ss](\d{2})[Ee](\d{2})").split(fn)
    if m:
        v = m[0].split(".")
        print v
        series = ""
        for s in v:
            series = series + s.replace(s[0:1],s[0:1].upper(),1) + " "
        series = series.strip()
        season = str(int(m[1]))
        episode = m[2]
        info = [series,season,episode]
        return info

def getSeriesInfo(series_name):
    print series_name
    get_series = "GetSeries.php?seriesname="
    f = urllib.urlopen(url+get_series+series_name)
    dom = ET.fromstring(f.read())
    for series in dom.findall("Series"):
        s = series.find("SeriesName").text
        if s == series_name:
            return series.find("seriesid").text

def getEpisodeName(series_id, season, episode):
    episode_url = url+apikey+"/series/"+series_id+"/default/"+season+"/"+episode+"/en.xml"
    f = urllib.urlopen(episode_url)
    dom = ET.fromstring(f.read())
    return dom.find("Episode").find("EpisodeName").text
    

for fn in os.listdir(working_dir):
    extension = fn[-4:]
    if extension == ".avi" or extension == ".mkv":
        file_info = getInfo(fn)
        #print file_info
        series_id = getSeriesInfo(file_info[0])
        #print series_id
        episode = getEpisodeName(series_id, file_info[1], str(int(file_info[2])))
        #print episode
        
        #build filename
        new_fn = file_info[0] + " - " + file_info[1] + file_info[2] + " - " + episode + extension
        print new_fn
        
        #build new directory
        new_dir = file_info[0] + "/Season " + str(int(file_info[1])) + "/"
        try:
            os.listdir(os.path.join(working_dir, new_dir))
        except OSError:
            print "doesn't exist!"
            os.makedirs(os.path.join(working_dir, new_dir), 0755)
            
        print new_dir
        os.rename(os.path.join(working_dir, fn), os.path.join(working_dir + "/" +new_dir, new_fn))
        
        
        
        
        
        
        
        