from core.plugin import Plugin
from core.decorators import command, rule
import discord


class Hello(Plugin):
    name = 'Hello'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command('hi')
    def hi(self, message):
        '''Says hi!'''
        assert isinstance(message, discord.Message)
        response = 'Hi {} !'.format(message.author)
        self.core.send_message(message.author, response)

    @rule('.*(hello|Hello|HELLO).*')
    def hello(self, message):
        '''Respond hello when someone says hello'''
        if message.author != self.core.user:
            response = 'Hello <@{}> !'.format(message.author.id)
            self.core.send_message(message.channel, response)
