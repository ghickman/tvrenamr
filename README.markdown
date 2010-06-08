
TV Renamr is a utility to rename TV shows based upon filenames or user input.



# Requirements

* Python 2.5+
* The Interwebs



# How To Use

Run the script with: `python tvrenamr.py [options] file/folder`

## Options

`-e` or `--episode` - Set the episode number for a file. Cannot be used when renaming more than one file.  
`--ignore-recursive` - Only use files from the root of the specified directory and do not enter any sub-directories.  
`-l` or `--log_level` - Set the log level. Valid options are debug, info, warning, error and critical.  
`--library` - Set the library to use for retrieving episode titles. This defaults to tvrage, but thetvdb is also available.  
`-n` or --name - Set the name of the name of the show to rename.  
`-o` or `--output` - Set the output format for the episodes being renamed.  
`--organise` - Automatically move renamed files to the directory specified with -r and organise them based on their show name and season number.  
`-r` or `--renamed` - The directory to move renamed files to, if not specified the working directory is used.  
`--regex` - The regular expression to use when extracting information from files.  
`-s` or `--season` - Set the season number. Cannot be used when renaming more than one file.  
`-t` or `--the` - Set the position of 'The' in a show's name to the end of the show name, i.e. 'The Wire' becomes 'Wire, The'.  
`-x` or `--exceptions` - Specify the location of an exceptions file.  

### Examples

* `python tvrenamr.py --organise -r '/path/to/a/directory/' /path/a/directory/or/file/[the_file.avi]`
* `python tvrenamr.py --season=number --name=name /path/to/a/file/the_file.avi`



## Custom Regular Expressions

By default TV Renamr will match shows in the formats: show.s0e00 and show.0x00 but you can specify custom regular expressions if your files aren't in 
either of these formats. Some custom regular expression syntax has been used to help you specify different parts of the filename:

* Show: `%n` - `(?P<show>[\w\s.,_-]+)`
* Season: `%s` - `(?P<season>[\d]{1,2})`
* Episode: `%e` - `(?P<episode>[\d]{2})`

It is also possible to specify how many digits there are in the season and episode sections of the filename using the syntax:

* Season: `%s{n}`
* Episode: `%e{n}`

where the n in `{n}` specifies how many digits are in each of the sections.

*Note:* All spaces are converted to periods before your regular expression is run.

Python regular expression syntax can be found [here](http://www.python.org/doc/2.6.1/library/re.html#regular-expression-syntax)




## Exceptions File

Specify files that you know have different show names in the their file names to that of the actual show name. Each line should define the expected show 
name from your files and then the actual show name, i.e what The Tv Db and Tv Rage expect the name to be, separated by the string ' => '. Lines 
beginning with # are treated as comments. 

#### Example & Known Shows

    # This is a comment
    american dad => american dad!
    avatar => avatar: the last airbender
    csi => csi: crime scene investigation



## Custom Output Format

It is possible to set a custom output format for your files using the following syntax:

* `%n` - Show
* `%s` - Season
* `%e` - Episode
* `%t` - Title
* `%x` - Extension

you can specify the format you like, i.e. `%n - %s%e - $t%x` would mirror the default format.

*Note:* Not including the `%x` section on Windows systems can cause problems when trying to run your media files.



# Known Issues

All colons ':' are converted to commas ',' in both the show name and the episode title. This stops issues that can arise with network shares and gives a cleaner format on windows where python replaces the colon character with a backslash '\'.

Shows with a year in the canonical title, like Doctor Who (2005), will fail without specifying the show name and including the year in brackets.

Renaming sections of a files output, such as the show name, isn't possible yet.