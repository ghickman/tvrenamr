TV Renamr is a utility to rename TV shows based upon filenames or user input.


# Requirements

* Python 2.6+
* PyYaml
* The Interwebs


# Installation

## Python Package Index

Make sure you have the python [setuptools](http://pypi.python.org/pypi/setuptools) package installed for your version of python (check with `python --version`).

To install from the Python Package Index: `easy_install tvrenamr` - You may need to be an administrator to run this.

A nice shiny `tvr` script is now installed in the relevant directory.

### Windows

If you are having trouble installing setup tools on windows make sure you have setup environment variables pointing to your python installation and python scripts folder. This will ensure you can run easy_install and tvr from the command line.


## Source: GitHub

`git clone git://github.com/ghickman/tvrenamr.git`

`cd tvrenamr`

`python setup.py install` - You may need to be an administrator to run this.


# How To Use

Run in your terminal of choice: `tvr [options] file/folder`

## Config File

For ease of use Tv Renamr uses a config file. By default it looks for it in `~/.tvrenamr/config.yml`, an example one is available [here](http://gist.github.com/586062) which shows all the possible default values you can use.

The defaults segment should be self-explanatory but I'll list them just for completeness. The listed values are the assumed defaults if any of the options are not added.

__`format: '%n - %s%e - %t%x'`__
The output format you want your files to be renamed to.

__`library: thetvdb`__
The online database to use for your episode names. Options are: thetvdb or tvrage

__`organise: yes`__
Organise your files within the renamed directory.

__`renamed: /Volumes/Media/TV/`__
The target directory to move your renamed files to.

__`the: true`__
If a show has a leading 'The', such as 'The Big Bang Theory', move it to the end of the show name: 'Big Bang Theory, The'.

Below the defaults are shows that won't get renamed correctly using the default options. Taking CSI as the example you have:

    csi:
        canonical: "CSI: Crime Scene Investigation"
        output: "CSI, Crime Scene Investigation"

`csi` is the torrent name and needs to match whatever name your file is being downloaded with, which for CSI would be `csi.s10e01.blah.blah.avi`.

`canonical` is name that the online database holds for the show.

`output` is what you want the show to be renamed to.

This method is the easiest way to deal with shows with a year in the name too, i.e. Castle (2009).

__Note__: The quotes around the canonical and output names for CSI are needed because of the colon and comma characters as they are reserved by YAML.

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
`-q` or `--quiet` - Don't output logs to the command line.
`-r` or `--recursive` - Recursively lookup files in a given directory.
`--rename-dir` - The directory to move renamed files to, if not specified the working directory is used.
`--no-rename-dir` - Explicitly tell Tv Renamr not to move renamed files. Used to override the config.
`--regex` - The regular expression to use when extracting information from files.
`-s` or `--season` - Set the season number.
`-t` or `--the` - Set the position of 'The' in a show's name to the end of the file.

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


## Custom Output Format

It is possible to set a custom output format for your files using the following syntax:

* `%n` - Show
* `%s` - Season
* `%e` - Episode
* `%t` - Title
* `%x` - Extension

you can specify the format you like, i.e. `%n - %s%e - $t%x` would mirror the default format.

*Note:* Not including the `%x` section on Windows systems can cause problems when trying to run your media files.

On the command line use the `-o` switch or set the `format` option in the defaults section of your config file.


# Caveats | Known Issues

Please report any bugs or feature requests to the [Tv Renamr Lighthouse](http://tvrenamr.lighthouseapp.com/projects/53048-tvrenamr-core/overview) account.

All colons ':' are converted to commas ',' in both the show name and the episode title. This stops issues that can arise with network shares and gives a cleaner format on windows where python replaces the colon character with a backslash '\'.

Shows with a year in the canonical title, like Doctor Who (2005), will fail without specifying the show name which includes the year in brackets. You'll need to put this as the canonical name in the config file.

Multiple episode files are just not coped with at all. The first episode is usually picked up so the file will be renamed using this.
