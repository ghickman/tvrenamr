import os
from optparse import OptionParser

from tvrenamr_core import TvRenamr

parser = OptionParser()
parser.add_option("-a", "--auto", dest="auto_move", help="Automatically move renamed files to the appropriate directory under the directory specified. Mutually exclusive to -r")
parser.add_option("-n", "--name", dest="name", help="Set the show name for renaming")
parser.add_option("-r", "--renamed", dest="renamed_dir", help="The directory to move renamed files to. Mutually exclusive to -a")
parser.add_option("--regex", dest="regex", help="the regular expression to set the format of files being renamed. Use %n to specify the show name, %s for the season number and %e for the episode number. All spaces are converted to periods before the regex is run")
parser.add_option("-s", "--season", dest="season")
parser.add_option("-w", "--working", dest="working_dir", help="The working directory to run tvrenamr in. Required!")
(options, args) = parser.parse_args()

#options.working_dir = "/Users/madnashua/Projects/tvrenamr/core/testcase/scrubs.s03e05.avi"
def script_rename(working_dir, fn):
    tv = TvRenamr(working_dir)
    try:
        details = tv.extract_episode_details_from_file(fn, user_regex=options.regex)
        name = tv.retrieve_episode_name(details[0],details[1],details[2])
        path = tv.build_path(details, name, renamed_dir=options.renamed_dir, auto_move=options.auto_move)
        tv.rename(fn,path)
    except Exception, e: print e

if os.path.isdir(options.working_dir):
    for each_tuple in os.walk(options.working_dir):
        for fname in each_tuple[2]:
            script_rename(each_tuple[0], fname)
elif os.path.isfile(options.working_dir):
    working = os.path.split(options.working_dir)
    script_rename(working[0], working[1])