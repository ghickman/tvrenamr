import logging
import os
import re
import urllib
import xml.etree.ElementTree as ET

apikey = 'C4C424B4E9137AFD'
url = "http://www.thetvdb.com/api/"
working_dir = "/Users/madnashua/Projects/TvRenamr/test"
renamed_dir = ""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/Users/madnashua/Projects/TvRenamr/tvrenamr.log',
                    filemode='a')

def getInfo(fn):
    m = re.compile("[Ss](\d{2})[Ee](\d{2})").split(fn)
    if m and len(m) > 1:
        v = m[0].split(".")
        series = ""
        for s in v:
            series = series + s.replace(s[0:1],s[0:1].upper(),1) + " "
        series = series.strip()
        season = str(int(m[1]))
        episode = m[2]
        info = [series,season,episode]
        return info
    else:
        logging.warning('Incorrect format for auto-renaming: %s', fn)
        #print "File not in correct format: " + fn
        return None

def getSeriesInfo(series_name):
    get_series = "GetSeries.php?seriesname="
    f = urllib.urlopen(url+get_series+series_name)
    dom = ET.fromstring(f.read())
    for series in dom.findall("Series"):
        s = series.find("SeriesName").text
        if s == series_name:
            return series.find("seriesid").text

def getEpisodeName(series_id, series_name, season, episode):
    episode_url = url+apikey+"/series/"+series_id+"/default/"+season+"/"+episode+"/en.xml"
    f = urllib.urlopen(episode_url)
    try:
        dom = ET.fromstring(f.read())
        return dom.find("Episode").find("EpisodeName").text
    except Exception:
        logging.warning('Episode not found: %s', series_name + " - " + season + episode)
        #print "Episode not found: " + season + episode
        return None
    

for fn in os.listdir(working_dir):
    extension = fn[-4:]
    if extension == ".avi" or extension == ".mkv":
        file_info = getInfo(fn)
        if file_info == None:
            continue
        series_id = getSeriesInfo(file_info[0])
        episode = getEpisodeName(series_id, file_info[0], file_info[1], str(int(file_info[2])))
        if episode == None:
            continue
        
        #build filename
        new_fn = file_info[0] + " - " + file_info[1] + file_info[2] + " - " + episode + extension
        
        """"
        NOT CURRENTLY REQUIRED
        
        #build new directory
        new_dir = file_info[0] + "/Season " + str(int(file_info[1])) + "/"
        try:
            os.listdir(os.path.join(working_dir + "/named", new_dir))
        except OSError:
            #print "doesn't exist!"
            os.makedirs(os.path.join(working_dir + "/named", new_dir), 0755)
        
        if (os.path.exists(working_dir+"/named"+new_dir+new_fn) == False):
            os.rename(os.path.join(working_dir, fn), os.path.join(working_dir + "/named/" +new_dir, new_fn))
            print "Renamed: " + new_fn
        else:
            print "file exists"
        """
        
        if os.path.exists(working_dir+new_fn) == False:
            os.rename(os.path.join(working_dir, fn), os.path.join(working_dir, new_fn))
            logging.info('Renamed: %s', new_fn)
            #print "Renamed: " + new_fn
        else:
            logging.error('File Exists: %s from %s', new_fn, fn)
            #print "File Exists"
        
        
        
        
        