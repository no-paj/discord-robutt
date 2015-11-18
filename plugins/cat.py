from core.plugin import Plugin
from core.decorators import command, thread
import discord
import requests


class Cats(Plugin):

    name = 'Cats'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @thread
    @command('cats')
    def cats(self, message):
        '''Get some cats !'''
        assert isinstance(message, discord.Message)
        response = self._get_cats()
        self.core.send_message(message.channel, response)

    def _get_cats(self):
        cats = ""
        while cats == "":
            cats = requests.get('http://thecatapi.com/api/images/get?format=html&results_per_page=1')
        return cats.text.split('"')[5]
