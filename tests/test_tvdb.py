# coding=utf-8
from functools import partial

import mock
from pytest import raises
from tvrenamr.errors import EpisodeNotFoundException, ShowNotFoundException
from tvrenamr.main import File

from .mock_requests import mock_get


def test_searching_with_an_ambiguous_name_returns_the_correct_show(tv):
    _file = File('The O.C.', '3', ['04'], 'mp4')
    with mock.patch('requests.get', side_effect=mock_get):
        tv.retrieve_episode_title(_file.episodes[0])
    method = partial(tv.format_show_name, _file.show_name)
    assert method(the=False) == 'The O.C.'
    assert method(the=True) == 'O.C., The'


def test_searching_for_an_incorrect_name_returns_an_exception(tv):
    _file = File('west, wing', '4', ['01'], '.mp4')
    with mock.patch('requests.get', side_effect=mock_get), raises(ShowNotFoundException):
        tv.retrieve_episode_title(_file.episodes[0])


def test_searching_for_an_episode_that_does_not_exist_returns_an_exception(tv):
    _file = File('chuck', '1', ['99'], '.mp4')
    with mock.patch('requests.get', side_effect=mock_get), raises(EpisodeNotFoundException):
        tv.retrieve_episode_title(_file.episodes[0])


def test_searching_for_a_specific_episode_returns_the_correct_episode(tv):
    _file = File('The Big Bang Theory', '3', ['01'], '.mp4')
    with mock.patch('requests.get', side_effect=mock_get):
        title = tv.retrieve_episode_title(episode=_file.episodes[0])
    assert title == 'The Electric Can Opener Fluctuation'


def test_the_return_of_a_formatted_show_name(tv):
    _file = File('The Big Bang Theory', '3', ['01'], '.mp4')
    with mock.patch('requests.get', side_effect=mock_get):
        tv.retrieve_episode_title(_file.episodes[0])
    method = partial(tv.format_show_name, _file.show_name)
    assert method(the=False) == 'The Big Bang Theory'
    assert method(the=True) == 'Big Bang Theory, The'


# def test_unicode_character_in_episode_name():
# #     This is horrible but the libraries are horrendous atm
#     from tvrenamr.errors import EmptyEpisodeTitleException
#     xml = fromstring("""
#     <Data>
#         <Episode>
#             <EpisodeName>¡Viva los Muertos!</EpisodeName>
#         </Episode>
#     </Data>
#     """)
#     episode = xml.find('Episode').findtext('EpisodeName').encode('utf-8')
#     if not episode:
#         raise EmptyEpisodeTitleException
#     episode = TheTvDb().get_episode_title_from_xml(xml)
#     assert episode == u'¡Viva los Muertos!'
