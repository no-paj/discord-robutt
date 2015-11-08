import discord


class Command:

	def __init__(self, name, startswith=False):
		assert isinstance(name, basestring)

		self.name = name
		self.trigger = "_"
		self.cmd = self.trigger+self.name
		self.startswith = startswith

	def __call__(self, f):
		def wrapped(core, msg):
			assert isinstance(msg, discord.Message)

			if self.startswith:
				if msg.content.startswith(self.cmd) and len(msg.content) > len(self.cmd):
					arg = msg.content.split(' ', 1)[1]
					f(core, msg, [arg])
			else:
				if msg.content == self.cmd:
					f(core, msg)

		return wrapped
