from core.plugin import Plugin
from core.decorators import Command
from core.decorators import Example
from random import randint, random
import discord
import requests
import argparse
import lxml
import sys
import urllib
from lxml.html import fromstring
from lxml.cssselect import CSSSelector

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
        try:
            self.data = urllib.urlopen(self.url)
        except Exception as e:
            raise e
        if self.data.getcode() != 200:
            print(self.data.getcode())
        self.html = self.data.read()
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
    lastid = urllib.urlopen("http://danstonchat.com/latest.html").read()
    r = fromstring(lastid)
    sel = CSSSelector('span')
    a = [e.get('id') for e in sel(r)]
    for x in a:
        if x != None:
            last = x
            break
    if last:
        return int(last)


class Bashfr(Plugin):

    name = 'Bashfr'

    def at_start(self):
        print('Plugin Bashfr launched !')

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @Command('bashfr')
    def bashfr(self, message):
        '''Get some old quote !'''
        assert isinstance(message, discord.Message)
        response = self._get_bashfr()
        self.core.send_message(message.author, response)

    def _get_bashfr(self):
        quote = Quote(random.randint(1, getlast()))
        return quote.return_raw()
