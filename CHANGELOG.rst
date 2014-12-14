Changelog
=========

v3.6.2
------

- Fix incorrect usage of `config.get` left over from previous fixes


v3.6.1
------

- Fix incorrect usage of `get_config`


v3.6.0
------

- Vendor dependencies
- Harden XML with defusedxml
- Switch to py.test for testing
- Rework frontend code for easier testing


v3.5.0
------

- Remove requirement on config


v3.4.11
-------

- Fix bug when logging episode number that had been overridden


v3.4.10
-------

- Fix bug with organise directory when no config is present


v3.4.9
------

- Fix 1080[p] and [Hh].264 breaking the season & episode searching regular expression


v3.4.8
------

- Fix ignored file list option default


v3.4.7
------

- Enable passing files *and* folders as paths to rename


v3.4.6
------

- Append to main log file instead of overwriting it

- Add some sane defaults for rotating the log file


v3.4.5
------

- Handle unicode in episode names


v3.4.4
------

- Fix specifying an episode on the command line


v3.4.3
------

- Improve the code that checks if tvr has everything needed to rename a file

- Handle seasons & episodes as numbers internally


v3.4.2
------

- Fix renaming shows with 720[p] in the filename


v3.4.1
------

- Fix partial regex support


v3.4.0
------

- Fix python 3 support in the tests

- Show IDs are now cached, cutting web requests by 50% for the majority of renames

- Tentative multiple episode file support. Hope to improve this over time

- Fix custom output format so it can use custom regex syntax


v3.3.3
------

- Add python 3 support!

- Fix python 2.6 support


v3.3.2
------

- Return destination filepath from a rename (useful for libs)


v3.3.1
------

- Tidy up so it can be used as a library too


v3.2.0
------

- Remove lxml and thus it's C building dependencies

- Tidy up the tests

- Clean up the library fallback logic and it's error handling


v3.1.0
------

- Show unhandled exceptions

- Provide a default filenmae format to fall back to

- Use Requests instead of urllib2

- Thanks to sampsyo for his work on this release


v3.0.3
------

- Add documentation and push to Read the Docs

- Fix another silly typo. Regretting the state of the tests now...


v3.0.2
------

- Fix a silly naming bug that broke everything and brown bagged the last
  release.


v3.0.1
------

- Allow the use of apostrophes in the show name regular expression

- Allow the use of hypen as a delimiter in the filename regular expression.

- Clean up the interface to the episode object for use in the front end.

- Use the correct variable name when retrieving the show name from an episode
  object.

- Give more sensible output when the config's defaults are missing.

- Return the correct error code when exiting from an error.


v3.0.0
------

- 720p episodes can now be renamed.

- Fallback to the other library if the first one can't find a tv show or
  episode. This feature also adds better support for new libraries.

- Added a command line option to override the show name when output to the
  filename.

- Can use foward slashes allowed in show names and episode titles.

- Use lxml as the xml library and add an extra check for empty xml files being
  returned from the library.

- Use an episode object to hold an episode's information during the rename
  process.
