from core.plugin import Plugin
from core.command import Command
import discord


class Hello(Plugin):

	def at_start(self):
		print 'Plugin Hello launched !'

	def on_message(self, message):
		self.say_hello(message)

	def __init__(self, core):
		Plugin.__init__(self, name='Hello', core=core)

	@Command('hi')
	def say_hello(self, message):
		assert isinstance(message, discord.Message)
		response = 'Hi ' + message.author.name.encode('utf-8') + ' !'
		self.core.send_message(message.author, response)