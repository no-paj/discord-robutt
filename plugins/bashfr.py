from ..core.plugin import Plugin
from ..core.decorators import command
from random import randint
import discord
import requests
import argparse

# TODO REWRITE WITH BS4 AND REQUESTS

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int, help="found quote by ID from dtc")
parser.add_argument("-r", "--random", action='store_true', help="Random quote from dtc")
parser.add_argument("-l", "--last", action='store_true', help="last quote from dtc")
parser.add_argument("-a", "--all", action='store_true', help="all quote from dtc")
args = parser.parse_args()


class Quote(object):
    """Contains a Quote"""

    def __init__(self, number):
        self.number = number
        self.url = "http://danstonchat.com/{}.html".format(self.number)
        self.data = requests.get(self.url)
        if self.data.status_code != 200:
            print(self.data.status_code)
        self.html = self.data.text
        self.parse()

    def parse(self):
        r = fromstring(self.html)
        self.end = 'Quote number %s' % self.number
        for el in r.find_class('decoration'):
            self.end = self.end + "\n" + lxml.html.tostring(el, encoding="unicode").replace('<span class="decoration">',
                                                                                            '').replace('</span>', '')
            self.end = self.end.replace('&lt;', '<').replace('&gt;', '>')

    def display(self):
        print(" ")
        print(self.end)
        print(" ")

    def return_raw(self):
        return self.end.encode("utf-8")

def getlast():
    global last
    lastid = requests.get("http://danstonchat.com/latest.html").text
    r = fromstring(lastid)
    sel = CSSSelector('span')
    a = [e.get('id') for e in sel(r)]
    for x in a:
        if x is not None:
            last = x
            break
    if last:
        return int(last)


class Bashfr(Plugin):

    name = 'Bashfr'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @command('bashfr')
    def bashfr(self, message):
        '''Get some old quote !'''
        assert isinstance(message, discord.Message)
        response = self._get_bashfr()
        self.core.send_message(message.author, response)

    def _get_bashfr(self):
        quote = Quote(randint(1, getlast()))
        return quote.return_raw()
