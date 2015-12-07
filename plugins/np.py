import os

from core.decorators import cron
from core.plugin import Plugin


class NowPlaying(Plugin):
    def __init__(self, core):
        Plugin.__init__(self, core)
        self.name = 'nopaj'
        self.old_name = 'nopaj'
        self.filepath = 'C:/Users/Utilisateur/Downloads/Snip-v5.1.0/Snip/Snip.txt'

    @cron(5)
    def updateMusic(self):
        new_name = self.name + ' ♪ ' + open(self.filepath, encoding="utf8").read()
        if len(new_name) > 32:
            new_name = new_name[:28] + '...'
        if new_name != self.old_name:
            self.core.edit_profile(password='1218118132', username=new_name)
            self.old_name = new_name

