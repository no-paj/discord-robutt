from time import time

import discord


class Core(discord.Client):
	"""Represents the core of the Bot. Extends from discord.Client
	This class is used to add a plugin layer and a database layer to discord.Client

	:param list plugins: A list of plugins

	"""

	def __init__(self, **kwargs):
		discord.Client.__init__(self, **kwargs)
		self.start_time = time()
		self.plugins = [
			{
				'instance': None,
				'plugin': plugin,
			} for plugin in kwargs.get('plugins')
		]

	def _start_all_plugins(self):
		"""Starts all the plugins"""

		for plug in self.plugins:
			plug['instance'] = plug['plugin'](core=self)

	def _stop_plugin(self, name):
		""""Stops a particular plugin by its name"""

		for index, plug in enumerate(self.plugins):
			if plug['plugin'].name == name:
				if plug['instance'] is not None:
					self.plugins[index]['instance'] = None
					return True
				else:
					print 'Plugin '+name+' not alive.'
					return False
		print 'Plugin '+name+' not found.'
		return False

	def _start_plugin(self, name):
		"""Starts a particular plugin by its name"""

		for index, plug in enumerate(self.plugins):
			if plug['plugin'].name == name:
				if plug['instance'] is None:
					self.plugins[index]['instance'] = plug['plugin'](core=self)
					return True
				else:
					print 'Plugin '+name+' already alive.'
					return False
		print 'Plugin '+name+' not found.'
		return False

	def run_time(self):
		"""Give the run time of the instance

		:return: A :int: in seconds
		"""
		return time() - self.start_time

	def on_ready(self):
		"""Called when the client is running and is ready"""
		self._start_all_plugins()

	def on_message(self, message):
		"""Called whenever a message is posted

		:param message: The message that is posted
		"""

		for plug in self.plugins:
			if plug['instance']:
				plug['instance'].on_message(message)
