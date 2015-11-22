import logging
import re

import time

import math
from bs4 import BeautifulSoup

from ..core.decorators import rule, require_admin, command, cron
from ..core.plugin import Plugin
import requests


class Explorer(Plugin):
    name = 'Explorer'

    def __init__(self, core):
        Plugin.__init__(self, core=core)
        self.m = []

    @command('stats')
    def info(self, message):
        servers_number = str(len(self.core.servers))

        members = [member for server in self.core.servers for member in server.members]
        unique_members = set(map(lambda x: x.id, members))

        connected_members = [member.id for member in members if member.status != 'offline']

        connected_members_number = str(len(set(connected_members)))
        unique_members_number = str(len(unique_members))

        response = '``` Connected to {} different servers with {} unique members total \n ({} connected) !\n {} msg received ! ```\n http://nopaj.co'.format(
            servers_number, unique_members_number, connected_members_number,
            str(len(self.m)))
        self.core.send_message(message.channel, response)

    @rule('^(.*)')
    def accept_invites(self, message):
        pattern = 'discord.gg\/([A-Za-z0-9]*)'
        match = re.findall(pattern, message.content)
        for link in match:
            if self.core.accept_invite('http://discord.gg/' + link):
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

    @command('^msg')
    def msg(self, message):
        total = []
        now = time.time()
        for m in self.m:
            if m + 60 >= now:
                total.append(m)
        response = '`Message frequency : {} messages / second !`'.format(str(len(total) / 60.0))
        self.core.send_message(message.channel, response)

    @rule('^(.*)')
    def message_number(self, message):
        self.m.append(time.time())

    @cron(60)
    def snapshot(self):

        servers_number = len(self.core.servers)

        members = [member for server in self.core.servers for member in server.members]
        unique_members = set(map(lambda x: x.id, members))

        connected_members = [member.id for member in members if member.status != 'offline']
        playing_members = [member.game_id for member in members if member.game_id]

        connected_members_number = len(set(connected_members))
        playing_members_number = len(set(playing_members))

        snap = {
            'servers': servers_number,
            'online': connected_members_number,
            'playing': playing_members_number,
            'timestamp': time.time()
        }

        snapshots = self.core.db.snapshots
        snapshots.save(snap)

        logging.info('Snapshot saved !')

    @cron(300)
    def servers(self):

        for server in self.core.servers:
            members_number = len(server.members)
            online_number = len([member.id for member in server.members if member.status != 'offline'])
            data = {
                'id': server.id,
                'name': server.name,
                'region': server.region,
                'owner_name': server.owner.name,
                'icon': server.icon,
                'members': members_number,
                'online': online_number
            }
            dbentry = self.core.db.servers.find_one({'id': server.id})
            if dbentry:
                self.core.db.servers.update({'_id': server.id}, {'$set': data}, upsert=False)
            else:
                self.core.db.servers.insert(data)
