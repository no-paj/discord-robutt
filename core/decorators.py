import discord
import re

from core.config import config
from functools import wraps


class Command:

	def __init__(self, pattern, trigger=config['DEFAULT_TRIGGER']):
		self.pattern = pattern
		self.trigger = trigger

	def __call__(self, f):

		@wraps(f)
		def wrapped(core, msg):
			assert isinstance(msg, discord.Message)
			if msg.content:
				if msg.content[0] == self.trigger:
					options = re.match(self.pattern, msg.content[1:])
					if options:
						options = options.groups()
						msg.options = options
						f(core, msg)
		wrapped.command = True
		return wrapped


def thread(value):
	def wrapper(function):
		function.thread = value
		return function
	return wrapper


def require_privmsg():
	def wrapper(function):
		function.is_privmsg = True
		return function
	return wrapper


def require_chanmsg():
	def wrapper(function):
		function.is_chanmsg = True
		return function
	return wrapper


def require_admin():
	def wrapper(function):
		function.admin = True
		return function
	return wrapper
