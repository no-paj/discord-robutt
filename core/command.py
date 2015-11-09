import discord

from shlex import shlex

class Command:

	def __init__(self, name, trigger='>', options=0):
		assert isinstance(name, basestring)

		self.name = name
		self.trigger = trigger
		self.cmd = self.name
		self.options = options

	def __call__(self, f):

		def wrapped(core, msg):
			assert isinstance(msg, discord.Message)
			sh = shlex(msg.content)
			sh.quotes += '`'
			sh.wordchars+='-'
			if sh.get_token() == self.trigger:
				if sh.get_token() == self.name:
					#Good command
					options = []
					#Puting options
					for i in range(self.options):
						options = [sh.get_token()] + options
					#Good number of options
					if sh.get_token() == '':
						msg.options = options
						f(core, msg)

		return wrapped
