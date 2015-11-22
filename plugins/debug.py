import os
import sys
import requests
import time
from math import floor
from core.plugin import Plugin
from core.decorators import command, example, require_privmsg, require_admin, interval, cron


class Debug(Plugin):
    name = 'Debug'

    def __init__(self, core):
        Plugin.__init__(self, core=core)

    @require_admin
    @command('^eval (.*)$')
    @example('{}eval 1+1')
    def evaluate(self, message):
        '''Self-made backdoor!!!'''
        if 'eval' in message.options[0]:
            self.core.send_message(message.channel, '``` EZ man ! ```')
            return True
        if 'exit' in message.content:
            self.core.send_message(message.channel, '``` FUCK OFF <3 ```')
            return True
        try:
            before = time.time()
            e = eval(message.options[0])
            after = time.time()
            timer = (after - before) * 1000
            response = '```python\n {} \n{}\n{} ms```'.format(e, '-' * (len(str(timer)) + 3), str(timer))
            self.core.send_message(message.channel, response)
        except:
            e = "Error : " + sys.exc_info()[0].__name__ + " \n " + str(sys.exc_info()[1])
            response = '```python\n' + e + '```'
            self.core.send_message(message.channel, "```\shell\n{}```".format(__import__('traceback').format_exc()))
            raise

    @command('^uid <@([0-9]*)>')
    @example('{}uid @User')
    def get_uid(self, message):
        '''Get a user id'''
        self.core.send_message(message.channel,
                               "{}'s UID :  `{}`".format("<@{}>".format(message.options[0]), message.options[0]))

    @command('^cid <#([0-9]*)>')
    @example('{}cid @Channel')
    def get_cid(self, message):
        '''Get a channel id'''
        self.core.send_message(message.channel,
                               "{}'s CID :  `{}`".format("<#{}>".format(message.options[0]), message.options[0]))

    @require_admin
    @command('^file (core|plugins) ([A-Za-z0-9]*)')
    def file(self, message):
        directory = message.options[0]
        before = time.time()
        key = requests.post('http://hastebin.com/documents', data=open(
            os.getcwd() + '\Robutt\{}\{}.py'.format(directory, message.options[1])).read()).json()['key']
        after = time.time()
        self.core.send_message(message.channel, 'http://hastebin.com/{} \n `took {} ms`'.format(key, str(
            floor((after - before) * 1000))))

    @require_admin
    @command('^exec (.*)')
    def execute(self, message):
        exec(message.options[0])

    @require_admin
    @command('^save (users)$')
    def save(self, message):
        """Save all users or all channels of the server or both"""
        if message.options[0] == 'users':
            self.core.database.User.insert_many(
                [
                    {
                        'name': user.name,
                        'discord_id': user.id,
                        'discriminator': user.discriminator,
                        'avatar': user.avatar,
                        'avatar_url': user.avatar_url(),
                    } for user in message.channel.server.members
                    ]
            ).on_conflict(action='REPLACE').execute()

