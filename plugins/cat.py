from core.plugin import Plugin
from core.decorators import Command
from core.decorators import Example
from random import randint
import discord
import requests


class Cats(Plugin):
    name = 'Cats'

    def at_start(self):
        print('Plugin Cats launched !')

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @Command('cats')
    def cats(self, message):
        '''Get some cats !'''
        assert isinstance(message, discord.Message)
        response = self._get_cats()
        self.core.send_message(message.author, response)

    def _get_cats(self):
        cats =""
        while cats=="":
            cats = requests.get('http://thecatapi.com/api/images/get?format=src&results_per_page=1')
        return cats
