from core.plugin import Plugin
from core.decorators import Command
from core.decorators import Example
from random import randint
import discord
import requests


class Boobs(Plugin):
    name = 'Boobs'

    def at_start(self):
        print('Plugin Boobs launched !')

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @Command('boobs')
    def boobs(self, message):
        '''Get some boobies !'''
        assert isinstance(message, discord.Message)
        response = self._get_boobs()
        self.core.send_message(message.author, response)

    def _get_boobs(self):
        boobs = []
        timeOut=0
        while not boobs && timeOut<10:
            boobs = requests.get('http://api.oboobs.ru/boobs/get/' + str(randint(42, 9500))).json()
            timeOut=timeOut+1
        
        if timeOut<10:
            return 'http://media.oboobs.ru/' + boobs[0]['preview']
        else
            return 'boobs not found'
