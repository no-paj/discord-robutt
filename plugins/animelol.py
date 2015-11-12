from core.plugin import Plugin
from core.decorators import command
from imgurpython import ImgurClient
from random import randint


class Animelol(Plugin):
    name = 'Animelol'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

        client_id = '7d5a48eb8f3b168'
        client_secret = 'f2886ec020ea9c5a46141bf8d6d7e100c2bc1bb1'
        client = ImgurClient(client_id, client_secret)

        self.images = [image for image in client.subreddit_gallery('animenocontext', sort='time', window='day', page=0)]

    @command('animewtf')
    def animewtf(self, message):
        '''Anime shows are wonderful...'''
        self.core.send_message(message.channel, self._get_img())

    def _get_img(self):
        return self.images[randint(0, len(self.images) - 1)].link
