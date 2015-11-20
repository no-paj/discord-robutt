from core.decorators import command, thread
from core.plugin import Plugin
import requests


class Xkcd(Plugin):
    name = 'Xkcd'

    @thread
    @command('xkcd')
    def xkcd(self, message):
        r = requests.get('http://c.xkcd.com/random/comic/')
        img = r.text.split('http://imgs.xkcd.com/comics/')[1].split('.png')[0]
        response = 'http://imgs.xkcd.com/comics/{}.png'.format(img)
        self.core.send_message(message.channel, response)
