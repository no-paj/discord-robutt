from ..core.plugin import Plugin
from ..core.decorators import command
from random import randint
import discord
import requests


class Boobs(Plugin):

    name = 'Boobs'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command('boobs')
    def boobs(self, message):
        '''Get some boobies !'''
        assert isinstance(message, discord.Message)
        response = self._get_boobs()
        dickbutt = 'http://i.imgur.com/CE4r5vR.jpg'
        if message.author.id == '94203228043874304':
            response = dickbutt
        self.core.send_message(message.channel, response)

    def _get_boobs(self):
        boobs = []
        timeout=0
        while not boobs and timeout<10:
            boobs = requests.get('http://api.oboobs.ru/boobs/get/' + str(randint(42, 9500))).json()
            timeout += 1
        
        if timeout < 10:
            return 'http://media.oboobs.ru/' + boobs[0]['preview']
        else:
            return 'boobs not found'
