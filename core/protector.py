from functools import wraps

import discord


class Protector:

	def __init__(self, user_ids):
		self.user_ids = user_ids

	def __call__(self, f):
		@wraps(f)
		def wrapped(msg):
			assert isinstance(msg, discord.Message)

			if msg.author.id in self.user_ids:
				f(msg)
		return wrapped
