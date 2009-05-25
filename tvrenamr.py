from coretvrenamr import TvRenamr
from optparse import OptionParser
import os

parser = OptionParser()
parser.add_option("-w", "--working", dest="working_dir", help="The working DIRECTORY to run tvrenamr in. Required!")
parser.add_option("-r", "--renamed", dest="renamed_dir", help="The DIRECTORY to move renamed files to. Mutually exclusive to -a")
parser.add_option("-a", "--auto", dest="auto_move", help="Automatically move renamed files to the appropriate directory under the DIRECTORY specified. Mutually exclusive to -r")
(options, args) = parser.parse_args()

working_dir = options.working_dir
renamed_dir = options.renamed_dir
auto_move = options.auto_move

tv = TvRenamr(working_dir)
for fn in os.listdir(working_dir):
    if auto_move != None:
        print "rename and auto move"
        tv.rename_and_auto_move(fn, auto_move)
    elif renamed_dir != None:
        print "rename and move"
        tv.rename_and_move(fn, renamed_dir)
    elif auto_move == None and renamed_dir == None:
        try:
            tv.rename(fn)
        except Exception, e:
            print e
            continue
    else:
        print "incorrect options!"