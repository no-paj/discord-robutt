from core.plugin import Plugin
from core.command import Command
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

	def __init__(self, core):
		Plugin.__init__(self, core=core)

		self.join = Protector(config['ADMINS'])(self.join)
		self.leave = Protector(config['ADMINS'])(self.leave)

	@Command('^(join|j) https://discord\.gg/([A-Za-z0-9]*)$')
	def join(self, message):
		if self.core.accept_invite('https://discord.gg/{}'.format(message.options[1])):
			self.core.send_message(message.channel, 'Server joined !')

	@Command('^leave$')
	def leave(self, message):
		self.core.leave_server(message.channel.server)

	@Command('^servers$')
	def server_list(self, message):
		response = ''
		for server in self.core.servers:
			response += '{} | {} connected\n'.format(server.name, len(server.members))
		response = '```\n {}```'.format(response)
		self.core.send_message(message.channel,response)