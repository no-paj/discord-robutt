import discord
from core.decorators import Command, example
from core.plugin import Plugin


class Look(Plugin):
    name = 'Look'

    def at_start(self):
        print('Plugin ' + self.name + ' launched !')

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @Command('^look <@([0-9]*)>$')
    @example('{}look @User')
    def look(self, message):
        '''These icons are soooo tinyyyy! Pls fix!'''
        assert isinstance(message, discord.Message)
        if message.mentions:
            for mention in message.mentions:
                self.core.send_message(message.channel, mention.avatar_url())
