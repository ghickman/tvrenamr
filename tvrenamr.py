import logging
import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CREATE
import re
from series import Series

working_dir = "/mnt/media/Sandbox"
renamed_dir = ""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/home/madnashua/projects/tvrenamr/tvrenamr.log',
                    filemode='a')
                    
wm = WatchManager()  # Watch Manager
mask = IN_CREATE  # watched events -> add IN_DONT_FOLLOW to not follow symlinks

class TvRenamr(ProcessEvent):
    def process_IN_CREATE(self, event):
        logging.info('Creating: %s', event.name)
        
        extension = event.name[-4:]
        if extension == ".avi" or extension == ".mkv" or extension == ".mp4":
            file_info = self.extract_file_details(event.name)
            if file_info == None:
                return None
            s = Series(file_info[0])
            
            series_id = s.getSeriesId()
            if file_info == None:
                return None
            
            episode_name = s.getEpisodeName(series_id, file_info[1], str(int(file_info[2])))
            if episode_name == None:
                return None

            #build filename
            new_fn = file_info[0] + " - " + file_info[1] + file_info[2] + " - " + episode_name + extension

            """"
            NOT CURRENTLY USED

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
            
            #replace with exception handling
            if os.path.exists(working_dir+new_fn) == False:
                os.rename(os.path.join(working_dir, event.name), os.path.join(working_dir, new_fn))
                logging.info('Renamed: %s', new_fn)
            else:
                logging.error('File Exists: %s from %s', new_fn, fn)
        
    def extract_file_details(self, fn):
        m = re.compile("[Ss](\d{2})[Ee](\d{2})").split(fn)
        if m and len(m) > 1:
            v = m[0].split(".")
            series = ""
            for s in v:
                series = series + s.replace(s[0:1],s[0:1].upper(),1) + " "
            return [series.strip(),str(int(m[1])),m[2]]
        else:
            logging.warning('Incorrect format for auto-renaming: %s', fn)
            return None

p = TvRenamr()
notifier = Notifier(wm, p)

wdd = wm.add_watch(working_dir, mask, rec=True) #watch this directory, with this mask, recursively
notifier.loop()#daemonize=True, pid_file='/tmp/tvrenamr.pid', force_kill=True, stdout='/tmp/stdout.txt')
        
        
        
        
        