import discord
import time

from tabulate import tabulate

from core.plugin import Plugin
from core.decorators import Command, example
from core.protector import Protector

from core.config import config


class Manage(Plugin):

	name = 'Manage'

	def at_start(self):
		print('Plugin {} launched !'.format('Manage'))

	def on_message(self, message):
		self.join(message)
		self.leave(message)
		self.server_list(message)
		self.clean(message)

	def __init__(self, core):
		Plugin.__init__(self, core=core)

		self.join = Protector(config['ADMINS'])(self.join)
		self.leave = Protector(config['ADMINS'])(self.leave)
		self.clean = Protector(config['ADMINS'])(self.clean)

	@Command('^(join|j) https://discord\.gg/([A-Za-z0-9]*)$')
	@example('{}join|j invite_url')
	def join(self, message):
		'''Join a server'''
		if self.core.accept_invite('https://discord.gg/{}'.format(message.options[1])):
			self.core.send_message(message.channel, 'Server joined !')

	@Command('^leave$')
	def leave(self, message):
		'''Leave the current server'''
		self.core.leave_server(message.channel.server)

	@Command('^servers$')
	def servers(self, message):
		'''A list of all servers that the bot is connected to'''
		info = {
			'Name': [],
			'Channels': [],
			'Connected': []
		}
		for index, server in enumerate(self.core.servers):
			info['Name'].append(server.name)
			info['Channels'].append(len(server.channels))
			info['Connected'].append(len([member for member in server.members if member.status == 'online']))
		response = tabulate(info, headers="keys", tablefmt="grid")
		self.core.send_message(message.channel, '```\n{} ```'.format(response))

	@Command('^clean ([0-9]*)$')
	@example('{}clean number')
	def clean(self, message):
		'''Clean bot's shit'''
		isinstance(message, discord.Message)
		i = 0
		num = int(message.options[0])
		for msg in self.core.logs_from(channel=message.channel, limit=100):
			if i == num:
				break
			if msg.author == self.core.user:
				i += 1
				self.core.delete_message(msg)
		msg = self.core.send_message(message.channel, "`{} msg deleted ! Channel cleaned.`".format(str(i)))
		time.sleep(5)
		self.core.delete_message(msg)

	@Command('^help$')
	def help(self, message):
		'''You just called it... Faggot -___-'''
		isinstance(message, discord.Message)
		response = ''
		for plugin in self.core.plugins:
			for cmd in plugin['commands']:
				if cmd['example'] != '':
					response += '``` {}\n '.format(cmd['example'].format(self.core.config['DEFAULT_TRIGGER']))
				else:
					response += '``` {}\n'.format('{}{}'.format(self.core.config['DEFAULT_TRIGGER'], cmd['name']))

				response += '\n{}```\n'.format(cmd['description'])
		self.core.send_message(message.channel, response)