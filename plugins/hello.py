from core.plugin import Plugin
from core.decorators import Command
import discord


class Hello(Plugin):
    name = 'Hello'

    def at_start(self):
        print('Plugin Hello launched !')

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @Command('hi')
    def hi(self, message):
        '''Says hi!'''
        assert isinstance(message, discord.Message)
        response = 'Hi {} !'.format(message.author)
        self.core.send_message(message.author, response)
