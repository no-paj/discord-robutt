import discord


class Restricter:

	def __init__(self, channel_id):
		self.channel_id = channel_id

	def __call__(self, f):
		def wrapped(msg):
			assert isinstance(msg, discord.Message)

			if msg.channel.id == self.channel_id:
				f(msg)
		return wrapped
