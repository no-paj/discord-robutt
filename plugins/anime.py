import time

import requests

from ..core.plugin import Plugin
from ..core.decorators import command, thread
from random import randint


class Anime(Plugin):
    name = 'Animelol'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command('anime (.*)')
    def anime(self, message):
        payload = {
            'grant_type': "client_credentials",
            'client_id': "ablk-vteag",
            'client_secret': "vBLS8XVkCqKjk5gOifQdrWYrak",
        }
        r = requests.post('https://anilist.co/api/auth/access_token', params=payload)
        access_token = r.json()['access_token']

        payload = {
            'access_token': access_token
        }
        r = requests.get('https://anilist.co/api/anime/search/{}'.format(message.options[0]), params=payload)
        if r.content == b'\n':
            response = 'Nothing found :-( . Try again !'
            self.core.send_message(message.channel, response)
            return
        anime = r.json()

        response = ''

        r = requests.get('https://anilist.co/api/anime/{}'.format(anime[0]['id']), params=payload)
        anime = r.json()
        if anime:
            for k, v in anime.items():
                if k in ['title_romaji', 'type', 'image_url_lge', 'title_japanese', 'title_english', 'average_score',
                         'total_episodes', 'airing_status', 'start_date', 'end_date', 'classification', 'description', 'duration', ]:
                    response += '**{}** {} \n'.format(k.replace('_', ' '), v)
            if anime['airing']:
                response+='**Next EPISODE IN {}**'.format(str(anime['airing']['countdown']/3600)+'hours')
        else:
            response = 'Nothing found :-( . Try again !'
        self.core.send_message(message.channel, response)

    @command('manga (.*)')
    def manga(self, message):
        payload = {
            'grant_type': "client_credentials",
            'client_id': "ablk-vteag",
            'client_secret': "vBLS8XVkCqKjk5gOifQdrWYrak",
        }
        r = requests.post('https://anilist.co/api/auth/access_token', params=payload)
        access_token = r.json()['access_token']

        payload = {
            'access_token': access_token
        }
        r = requests.get('https://anilist.co/api/manga/search/{}'.format(message.options[0]), params=payload)
        if r.content == b'\n':
            response = 'Nothing found :-( . Try again !'
            self.core.send_message(message.channel, response)
            return
        anime = r.json()

        response = ''

        r = requests.get('https://anilist.co/api/manga/{}'.format(anime[0]['id']), params=payload)
        anime = r.json()
        if anime:
            for k, v in anime.items():
                if k in ['title_romaji', 'type', 'image_url_lge', 'title_japanese', 'title_english', 'average_score',
                         'total_volums', 'total_chapters', 'publishing_status', 'start_date', 'end_date', 'classification', 'description', 'duration', ]:
                    response += '**{}** {} \n'.format(k.replace('_', ' '), v)

        else:
            response = 'Nothing found :-( . Try again !'
        self.core.send_message(message.channel, response)
