import discord

from core.command import Command
from core.plugin import Plugin


class Look(Plugin):

	name = 'Look'

	def at_start(self):
		print('Plugin '+self.name+' launched !')

	def __init__(self, core):
		Plugin.__init__(self, core=core)

	def on_message(self, message):
		self.look(message)

	@Command('^look <@([0-9]*)>$')
	def look(self, message):
		assert isinstance(message, discord.Message)
		if message.mentions:
			for mention in message.mentions:
				self.core.send_message(message.channel, mention.avatar_url())
