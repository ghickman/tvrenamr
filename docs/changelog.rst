.. _changelog:

Changelog
=========

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
