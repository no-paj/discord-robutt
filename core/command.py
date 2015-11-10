import discord
import re

from shlex import shlex
from core.config import config


class Command:

	def __init__(self, pattern, trigger=config['DEFAULT_TRIGGER'], options=0):

		self.pattern = pattern
		self.trigger = trigger
		self.options = options

	def __call__(self, f):

		def wrapped(core, msg):
			assert isinstance(msg, discord.Message)
			if msg.content[0] == self.trigger:
				options = re.match(self.pattern, msg.content[1:])
				if options:
					options = options.groups()
					msg.options = options
					f(core, msg)

		return wrapped
