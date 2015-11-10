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

	def __init__(self, core):
		Plugin.__init__(self, core=core)

		self.join = Protector(config['ADMINS'])(self.join)

	@Command('^join https://discord\.gg/([A-Za-z0-9]*)$')
	def join(self, message):
		if self.core.accept_invite('https://discord.gg/{}'.join(message.options[0])):
			self.core.send_message(message.channel, 'Server joined !')

	@Command('leave')
	def leave(self, message):
		self.core.leave_server(message.channel.server)
