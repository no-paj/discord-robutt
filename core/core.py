from time import time

import discord


class Core(discord.Client):

	def __init__(self, **kwargs):
		discord.Client.__init__(self, **kwargs)
		self.start_time = time()
		self.plugins = kwargs.get('plugins', [])
		self.running_plugins = []

	def run_time(self):
		"""Give the run time of the instance

		:return: A :int: in seconds
		"""
		return time() - self.start_time

	def on_ready(self):
		"""Called when the client is running and is ready"""
		self._load_plugins()

	def on_message(self, message):
		"""Called whenever a message is posted

		:param
		"""
		for plug in self.running_plugins:
			plug.on_message(message)

	def _load_plugins(self):
		for plug in self.plugins:
			self.running_plugins += [plug(core=self)]
