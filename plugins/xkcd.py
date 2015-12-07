from ..core.decorators import command, thread
from ..core.plugin import Plugin
import requests


class Xkcd(Plugin):
    name = 'Xkcd'

    @thread
    @command('xkcd')
    def xkcd(self, message):
        r = requests.get('http://c.xkcd.com/random/comic/')
        info = requests.get(r.url+'info.0.json').json()
        response = '{}\n'.format(info['img'])
        self.core.send_message(message.channel, response)
        self.core.send_message(message.channel, '**#{} : {}**\n```\n{}```'.format(info['num'], info['safe_title'].upper(), info['alt']))
