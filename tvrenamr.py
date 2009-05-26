from tvrenamr_core import TvRenamr
from optparse import OptionParser
import os

parser = OptionParser()
parser.add_option("-w", "--working", dest="working_dir", help="The working DIRECTORY to run tvrenamr in. Required!")
parser.add_option("-r", "--renamed", dest="renamed_dir", help="The DIRECTORY to move renamed files to. Mutually exclusive to -a")
parser.add_option("-a", "--auto", dest="auto_move", help="Automatically move renamed files to the appropriate directory under the DIRECTORY specified. Mutually exclusive to -r")
parser.add_option("-l", "--log", dest="is_logging", help="")
(options, args) = parser.parse_args()

working_dir = options.working_dir
renamed_dir = options.renamed_dir
auto_move = options.auto_move
logging = options.is_logging

tv = TvRenamr(working_dir)
for fn in os.listdir(working_dir):
    if auto_move != None:
        #rename and auto move
        try:
            tv.rename(fn, auto_move=auto_move)
        except Exception, e:
            print e
            continue
    elif renamed_dir != None:
        #rename and move
        try:
            tv.rename(fn, renamed_dir)
        except Exception, e:
            print e
            continue
    elif auto_move == None and renamed_dir == None:
        #rename
        try:
            tv.rename(fn)
        except Exception, e:
            print e
            continue
    else:
        print "incorrect options!"