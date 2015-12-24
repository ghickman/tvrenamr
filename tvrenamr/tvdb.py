from __future__ import unicode_literals

import logging
import os
import urllib

import requests
from defusedxml.ElementTree import ParseError, fromstring

from . import errors


class TVDB(object):
    log = logging.getLogger('The Tv DB')
    url_base = 'http://www.thetvdb.com/api/'

    def __init__(self, show, season, episode, cache):
        self.cache = cache
        self.show = show
        self.season = str(season).lstrip('0')
        self.episode = str(episode).lstrip('0')

        self.log.info('Searching: %s', self.show)
        self.set_show_id()

        self.set_episode_title(self.build_episode_url())

    def build_episode_url(self):
        apikey = 'C4C424B4E9137AFD'
        args = (self.url_base, apikey, self.show_id, self.season, self.episode)
        return '{}{}/series/{}/default/{}/{}/en.xml'.format(*args)

    def build_id_url(self, quoted_show):
        url_series = 'GetSeries.php?seriesname='
        return '{}{}{}'.format(self.url_base, url_series, quoted_show)

    def get_cache_dir(self, show):
        show = show.lower().replace(' ', '_')  # sanitise show name
        module = self.__class__.__name__.lower()
        config_dir = os.path.expanduser('~/.tvrenamr')
        cache_dir = os.path.join(config_dir, 'cache', module, show)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        return cache_dir

    def get_episode_title_from_xml(self, xml):
        episode = xml.find('Episode').findtext('EpisodeName')
        if not episode:
            raise errors.EmptyEpisodeTitleException
        return episode

    def get_show_id_from_xml(self, xml):
        for name in xml.findall('Series'):
            show = name.findtext('SeriesName')
            if show.lower() != self.show.lower():
                raise errors.ShowNotFoundException(self.show)

            self.log.debug('Series chosen: %s', show)
            return name.findtext('seriesid'), show

    def request_show_id(self, cache):
        try:
            quoted_show = urllib.parse.quote(self.show)
        except AttributeError:  # python 2
            quoted_show = urllib.quote(self.show)

        url = self.build_id_url(quoted_show)
        self.log.debug('Series url: %s', url)

        req = requests.get(url)
        if not req.ok:
            raise errors.NetworkException()
        if self.cache:
            with open(cache, 'w') as f:
                f.write(req.text)
        return req.text

    def set_episode_title(self, url):
        self.log.debug('Episode URL: %s', url)

        self.log.debug('Attempting to retrieve episode title')
        req = requests.get(url)
        if not req.ok:
            args = (self.show, self.season, self.episode)
            raise errors.EpisodeNotFoundException(*args)
        self.log.debug('XML: Retreived')

        self.log.debug('XML: Attempting to parse')
        try:
            tree = fromstring(req.content)
        except ParseError:
            raise errors.InvalidXMLException(self.show)
        if tree is None:
            raise errors.InvalidXMLException(self.show)
        args = (self.show, self.season, str(self.episode).zfill(2))
        self.log.debug('XML: Episode document retrived for %s - %s%s', *args)

        self.log.debug('XML: Attempting to find the episode title')
        self.title = self.get_episode_title_from_xml(tree)

        self.log.debug('Retrieved episode title: %s', self.title)

    def set_show_id(self):
        self.log.debug('Retrieving series id for %s', self.show)

        cache = os.path.join(self.get_cache_dir(self.show), 'show_id')
        try:
            if not self.cache:
                raise IOError
            with open(cache, 'r') as f:
                xml = f.read()
        except IOError:
            xml = self.request_show_id(cache)

        try:
            xml = xml.encode('utf-8')  # deal with py2 faff
        except UnicodeEncodeError:
            pass

        self.log.debug('XML: Attempting to parse')
        try:
            tree = fromstring(xml)
        except ParseError:
            raise errors.InvalidXMLException(self.show)
        if tree is None or len(tree) is 0:
            raise errors.InvalidXMLException(self.show)
        self.log.debug('XML: Parsed')

        self.show_id, self.show = self.get_show_id_from_xml(tree)
        self.log.debug('Retrieved show id: %s', self.show_id)
        self.log.debug('Retrieved canonical show name: %s', self.show)
