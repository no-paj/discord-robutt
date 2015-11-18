import re

import time

import math
from bs4 import BeautifulSoup

from core.decorators import rule, require_admin, command
from core.plugin import Plugin
import requests


class Explorer(Plugin):
    name = 'Explorer'

    @command('info')
    def info(self, message):
        before = time.time()
        servers_number = str(len(self.core.servers))

        members = [member for server in self.core.servers for member in server.members]
        unique_members = set(map(lambda x: x.id, members))

        connected_members = [member.id for member in members if member.status != 'offline']

        connected_members_number = str(len(set(connected_members)))
        unique_members_number = str(len(unique_members))

        response = '``` Connected to {} different servers with {} unique members total \n ({} connected) !\n --- {} ms ```'.format(
            servers_number, unique_members_number, connected_members_number, math.floor((time.time() - before)*1000))
        self.core.send_message(message.channel, response)

    @rule('.*discord.gg/([A-Za-z0-9]*).*')
    def accept_invites(self, message):
        if self.core.accept_invite('http://discord.gg/' + message.options[0]):
            self.core.logger.info('# Joining new server ! ')

    @require_admin
    @command('^vacuum (.*)')
    def vacuum(self, message):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        p = requests.get(message.options[0], headers=headers)
        soup = BeautifulSoup(p.text, 'html.parser')
        links = []
        for link in soup.find_all(href=re.compile('discord.gg')):
            links.append(link['href'])
        i = 0
        for link in links:
            if self.core.accept_invite(link):
                i += 1
        response = '`Joined {} servers !`'.format(str(i))
        self.core.send_message(message.channel, response)
