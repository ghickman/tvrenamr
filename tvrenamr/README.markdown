TV Renamr is a utility to rename TV shows based upon filenames or user input.


# Requirements

* Python 2.6+
* PyYaml
* The Interwebs


# Installation

## Python Package Index

Make sure you have the python [setuptools](http://pypi.python.org/pypi/setuptools) package installed for your version of python (check with `python --version`).

To install from the Python Package Index: `easy_install tvrenamr`

## GitHub

`git clone git://github.com/ghickman/tvrenamr.git`

`cd tvrenamr`

`python setup.py bdist_egg`


# How To Use

Run in your terminal of choice: `tvr [options] file/folder`

## Config File

For ease of use Tv Renamr uses a config file. By default it looks for it in `~/.tvrenamr/config.yml`, an example one is available [here](http://gist.github.com/586062).

## Command Line Options

If you need more control or if theres a pesky file you need to test, then the command line options give you the most power.

`-c` or `--canonical` - Set the show's canonical name to use when performing the online lookup.
`--deluge` - Checks Deluge to make sure the file has been completed before renaming.
`--deluge-ratio` - Checks Deluge for completed and that the file has at least reached X share ratio.
`-d` or `--dry-run` - Dry run your renaming.
`-e` or `--episode` - Set the episode number. Currently this will cause errors when working with more than one file.
`-l` or `--log_file` - Set the log file location.
`--log_level` - Set the log level. Options: debug, info, warning, error and critical.
`--library` - Set the library to use for retrieving episode titles. Options: thetvdb & tvrage.
`-n` or `--name` - Set the show's name. This will be used as the show's when the renaming is completed.
`-o` or `--output` - Set the output format for the episodes being renamed.
`--organise` - Organise renamed files into folders based on their show name and season number.
`--no-organise` - Explicitly tell Tv Renamr not to organise renamed files. Used to override the config.
`-q` or `--quiet` - Don't output logs to the command line
`-r` or `--recursive` - Recursively lookup files in a given directory
`--rename-dir` - The directory to move renamed files to, if not specified the working directory is used.
`--no-rename-dir` - Explicity tell Tv Renamr not to move renamed files. Used to override the config.
`--regex` - The regular expression to use when extracting information from files.
`-s` or `--season` - Set the season number.
`-t` or `--the` - Set the position of 'The' in a show's name to the end of the file

### Examples

* `tvr`
* `tvr /path/to/a/directory/`
* `tvr /path/to/a/file.avi`
* `tvr --organise -r '/path/to/a/directory/' /path/to/a/directory/[a_file.avi]`
* `tvr --season '1' --name 'chuck' /path/to/a/file/the_file.avi`


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




<!-- ## Exceptions File

Specify files that you know have different show names in the their file names to that of the actual show name. Each line should define the expected show 
name from your files and then the actual show name, i.e what The Tv Db and Tv Rage expect the name to be, separated by the string ' => '. Lines 
beginning with # are treated as comments. 

#### Example & Known Shows

    # This is a comment
    american dad => american dad!
    avatar => avatar: the last airbender
    csi => csi: crime scene investigation -->



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