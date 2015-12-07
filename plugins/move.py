import time
from threading import Thread
from core.plugin import Plugin
from core.decorators import command, thread, require_chanmsg, rule, require_privmsg, require_admin
from core.threads import ThreadWrapper
from plugins.rps.structures import Game


class Move(Plugin):
    name = 'Move'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @thread
    @require_admin
    @command('^move <#([0-9]*)>')
    def move(self, message):
        channel = self.core.get_channel(message.options[0])
        if not channel:
            return False
        messages = []
        mentions = []
        for msg in self.core.logs_from(message.channel, limit=15):
            messages.append(msg)
            mentions.append(msg.author.mention())
        for msg in messages:
            formated = "{} said : ```{}```".format(msg.author, msg.content)
            self.core.send_message(channel, formated)
        mentions = " ".join(set(mentions))
        bla = "Continue the discussion here please : <#{}> \n {}".format(channel.id, mentions)
        self.core.send_message(channel, bla)