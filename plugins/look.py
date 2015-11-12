import discord
from core.decorators import command, example
from core.plugin import Plugin


class Look(Plugin):

    name = 'Look'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command('^look <@([0-9]*)>$')
    @example('{}look @User')
    def look(self, message):
        '''These icons are soooo tinyyyy! Pls fix!'''
        assert isinstance(message, discord.Message)
        if message.mentions:
            for mention in message.mentions:
                self.core.send_message(message.channel, mention.avatar_url())
